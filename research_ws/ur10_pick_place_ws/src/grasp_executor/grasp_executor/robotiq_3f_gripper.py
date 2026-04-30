#!/usr/bin/env python3
"""
robotiq_3f_gripper.py
----------------------
Python TCP (Modbus TCP) controller for the Robotiq 3-Finger Adaptive Gripper.

Connects to the gripper's Ethernet adapter at a fixed IP/port.
Activates the gripper on startup and deactivates on shutdown —
the gripper is only powered/active while this script is running.

Usage (from grasp_executor_node in real_hardware mode):
    gripper = RobotiqGripper3F(ip="192.168.1.105", port=502)
    gripper.activate()      # called once at startup
    gripper.open()          # fully open fingers
    gripper.close(force=50) # close with medium force
    gripper.shutdown()      # deactivate on node exit

Modbus TCP register map (Robotiq 3F S-model):
  Output (master writes, address 0x03E8):
    Reg 0 byte0: rACT(b0) rMOD(b1-2) rGTO(b3) rATR(b4) rGLV(b5)
    Reg 1 byte0: rPRA  — position request finger A (0=open, 255=closed)
    Reg 1 byte1: rSPA  — speed (0=min, 255=max)
    Reg 2 byte0: rFRA  — force (0=min, 255=max)

  Input (gripper writes, address 0x07D0):
    Reg 0 byte0: gACT(b0) gMOD(b1-2) gGTO(b3) gIMC(b4-5) gSTA(b6-7)
    gIMC == 3 means gripper fully initialised (activation complete)
"""

import socket
import struct
import time


# ---------------------------------------------------------------------------
# Modbus TCP helpers
# ---------------------------------------------------------------------------

_TRANSACTION_ID = 0x0001
_PROTOCOL_ID    = 0x0000
_UNIT_ID        = 0x09          # Robotiq unit ID (also try 0x02 if 0x09 fails)

_REG_OUTPUT     = 0x0000        # First output register (master → gripper)
_REG_INPUT      = 0x0000        # First input  register (gripper → master)

_TIMEOUT_SEC    = 3.0           # Socket timeout
_ACT_TIMEOUT    = 25.0          # Max wait for activation (fingers need ~15s to home)


def _build_write_frame(start_addr: int, register_values: list[int]) -> bytes:
    """Build a Modbus TCP 'Write Multiple Registers' (FC 0x10) request frame."""
    n        = len(register_values)
    byte_cnt = n * 2
    # PDU: func(1) + addr(2) + count(2) + byte_count(1) + data(n*2)
    pdu = struct.pack(">BHHB", 0x10, start_addr, n, byte_cnt)
    for v in register_values:
        pdu += struct.pack(">H", v & 0xFFFF)
    # MBAP header: tx_id(2) + proto_id(2) + length(2) + unit_id(1)
    length = 1 + len(pdu)
    header = struct.pack(">HHHB", _TRANSACTION_ID, _PROTOCOL_ID, length, _UNIT_ID)
    return header + pdu


def _build_read_frame(start_addr: int, n_registers: int) -> bytes:
    """Build a Modbus TCP 'Read Input Registers' (FC 0x04) request frame."""
    pdu    = struct.pack(">BHH", 0x04, start_addr, n_registers)
    length = 1 + len(pdu)
    header = struct.pack(">HHHB", _TRANSACTION_ID, _PROTOCOL_ID, length, _UNIT_ID)
    return header + pdu


# ---------------------------------------------------------------------------
# Gripper class
# ---------------------------------------------------------------------------

class RobotiqGripper3F:
    """
    Robotiq 3-Finger Adaptive Gripper — Ethernet (Modbus TCP) controller.

    The gripper is activated on `activate()` and deactivated on `shutdown()`.
    Between those calls it is ready to receive open/close commands.
    """

    # Position byte: 0 = fully open, 255 = fully closed
    POS_OPEN   = 0
    POS_CLOSE  = 220    # ~85 % closed — firm enough without crushing
    SPEED_MAX  = 255
    FORCE_SOFT = 50     # for open (gentle)
    FORCE_FIRM = 150    # for close — 100 insufficient, 180 caused protective stops at wrong height

    def __init__(self, ip: str = "192.168.1.105", port: int = 502):
        self._ip   = ip
        self._port = port
        self._sock: socket.socket | None = None
        self._active = False

    # ------------------------------------------------------------------
    # Connection management
    # ------------------------------------------------------------------

    def _connect(self):
        if self._sock is not None:
            return
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self._sock.settimeout(_TIMEOUT_SEC)
        self._sock.connect((self._ip, self._port))

    def _disconnect(self):
        if self._sock is not None:
            try:
                self._sock.close()
            except Exception:
                pass
            self._sock = None

    def _send(self, frame: bytes) -> bytes:
        """Send a Modbus frame and return the response bytes.
        If the socket is stale (dropped after E-stop etc.), reconnect once and retry."""
        self._connect()
        try:
            self._sock.sendall(frame)
            return self._sock.recv(256)
        except (OSError, BrokenPipeError, ConnectionResetError):
            # Socket went dead — drop it and reconnect once.
            # NOTE: do NOT clear _active here. The gripper hardware stays activated
            # even when the TCP connection drops; clearing _active would trigger a
            # full re-activation homing sweep on the next command.
            self._disconnect()
            self._connect()
            self._sock.sendall(frame)
            return self._sock.recv(256)

    def _write_registers(self, start: int, values: list[int]):
        frame = _build_write_frame(start, values)
        self._send(frame)

    def _read_input_registers(self, start: int, count: int) -> list[int]:
        """Read input registers; return list of 16-bit values."""
        frame = _build_read_frame(start, count)
        resp  = self._send(frame)
        # Response: MBAP(7) + func(1) + byte_count(1) + data
        if len(resp) < 9:
            return []
        byte_count = resp[8]
        data       = resp[9: 9 + byte_count]
        values     = []
        for i in range(0, len(data), 2):
            values.append(struct.unpack(">H", data[i:i+2])[0])
        return values

    # ------------------------------------------------------------------
    # Gripper lifecycle
    # ------------------------------------------------------------------

    def activate(self) -> bool:
        """
        Activate the gripper (must be called once after connecting).

        Sequence:
          1. Reset (clear rACT)
          2. Set rACT = 1
          3. Poll until gIMC == 3 (initialisation complete)

        Returns True on success, False on timeout.
        """
        try:
            self._connect()

            # 1. Reset
            self._write_registers(_REG_OUTPUT, [0x0000, 0x0000, 0x0000])
            time.sleep(0.5)

            # 2. Activate: rACT=1 → byte0 of reg0 = 0x01
            self._write_registers(_REG_OUTPUT, [0x0100, 0x0000, 0x0000])

            # 3. Poll for activation complete (gIMC bits 4-5 of input reg 0 == 3)
            deadline = time.monotonic() + _ACT_TIMEOUT
            while time.monotonic() < deadline:
                vals = self._read_input_registers(_REG_INPUT, 3)
                if vals:
                    reg0_hi = (vals[0] >> 8) & 0xFF   # high byte = status bits
                    gimc    = (reg0_hi >> 4) & 0x03    # bits 4-5
                    if gimc == 3:
                        self._active = True
                        return True
                time.sleep(0.1)

            print(f"[RobotiqGripper3F] Activation timed out after {_ACT_TIMEOUT}s")
            return False

        except Exception as e:
            print(f"[RobotiqGripper3F] Activation failed: {e}")
            return False

    def shutdown(self):
        """
        Deactivate the gripper and close the TCP connection.
        Leaves the gripper in a safe, unpowered state.
        """
        try:
            if self._sock is not None:
                # Clear rACT → gripper returns to standby (fingers hold position)
                self._write_registers(_REG_OUTPUT, [0x0000, 0x0000, 0x0000])
        except Exception:
            pass
        self._active = False
        self._disconnect()

    def _wake(self) -> bool:
        """
        Re-assert rACT=1 without touching position/speed/force registers.

        Writes ONLY register 0 (count=1, FC 0x10) so the position register
        is not overwritten.  rGTO=0 means no motion is commanded — fingers
        hold their current position.  Polls until gIMC==3 (gripper ready).

        Safe to call at any time: if already active, gIMC==3 returns in <100 ms.
        Needed after a TCP reconnect — Robotiq firmware may ignore motion
        commands until it sees rACT=1 on the new connection.
        """
        try:
            self._connect()
            # Write ONLY reg0: rACT=1 (b0), rGTO=0, all other bits 0.
            # count=1 → FC 0x10 writes a single 16-bit register, leaving
            # reg1 (position/speed) and reg2 (force) completely unchanged.
            self._write_registers(_REG_OUTPUT, [0x0100])
            deadline = time.monotonic() + 5.0
            while time.monotonic() < deadline:
                vals = self._read_input_registers(_REG_INPUT, 3)
                if vals:
                    reg0_hi = (vals[0] >> 8) & 0xFF
                    gimc    = (reg0_hi >> 4) & 0x03
                    if gimc == 3:
                        self._active = True
                        return True
                time.sleep(0.1)
            return False
        except Exception as e:
            print(f"[RobotiqGripper3F] Wake failed: {e}")
            return False

    # ------------------------------------------------------------------
    # Motion commands
    # ------------------------------------------------------------------

    def _go_to(self, position: int, speed: int, force: int):
        """
        Send a go-to command in basic mode (all 3 fingers move together).

        position : 0 (open) … 255 (closed)
        speed    : 0 (slow) … 255 (fast)
        force    : 0 (light) … 255 (max)
        """
        position = max(0, min(255, position))
        speed    = max(0, min(255, speed))
        force    = max(0, min(255, force))

        # Reg 0: rACT=1, rGTO=1 → 0x09 in high byte → register value 0x0900
        # Reg 1: rPRA (pos) in high byte, rSPA (speed) in low byte
        # Reg 2: rFRA (force) in high byte
        reg0 = 0x0900
        reg1 = (position << 8) | speed
        reg2 = (force << 8)

        self._write_registers(_REG_OUTPUT, [reg0, reg1, reg2])

    def open(self, speed: int = 200) -> bool:
        """Open gripper fully."""
        try:
            self._wake()   # ensure rACT=1 after any TCP reconnect
            self._go_to(self.POS_OPEN, speed, self.FORCE_SOFT)
            time.sleep(2.5)
            return True
        except Exception as e:
            print(f"[RobotiqGripper3F] Open failed: {e}")
            return False

    def close(self, force: int = None, speed: int = 200) -> bool:
        """Close gripper to grasp position."""
        if force is None:
            force = self.FORCE_FIRM
        try:
            self._wake()   # ensure rACT=1 after any TCP reconnect
            self._go_to(self.POS_CLOSE, speed, force)
            time.sleep(2.0)
            return True
        except Exception as e:
            print(f"[RobotiqGripper3F] Close failed: {e}")
            return False

    def is_active(self) -> bool:
        return self._active

    # Context manager support
    def __enter__(self):
        self.activate()
        return self

    def __exit__(self, *_):
        self.shutdown()
