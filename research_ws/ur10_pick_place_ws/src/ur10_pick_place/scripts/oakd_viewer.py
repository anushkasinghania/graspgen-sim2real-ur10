#!/usr/bin/env python3
"""
oakd_viewer.py — Live RGB + Depth viewer for env_cam and wrist_cam.
depthai v3 API. Run modes:
  python3 oakd_viewer.py        — RGB only (fast, no lag)
  python3 oakd_viewer.py depth  — RGB + Depth (heavier)

Press Q to quit.
"""

import queue
import sys
import threading
import time

import cv2
import depthai as dai
import numpy as np

MX_NAMES = {
    "14442C1041A6D1D200": "env_cam",
    "14442C10715AD4D200": "wrist_cam",
}

SHOW_DEPTH = "depth" in sys.argv
QUEUES: dict = {}
stop_event = threading.Event()


def build_pipeline_rgb():
    """RGB only — lightweight, no lag."""
    p = dai.Pipeline()
    cam = p.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_A)
    q = cam.requestOutput((1280, 720), dai.ImgFrame.Type.BGR888p
                          ).createOutputQueue(maxSize=2, blocking=False)
    return p, q, None, None


def build_pipeline_depth():
    """RGB + stereo depth. Mono at 400p keeps disparity within median filter limit."""
    p = dai.Pipeline()

    # RGB
    cam_rgb = p.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_A)
    q_rgb = cam_rgb.requestOutput(
        (1280, 720), dai.ImgFrame.Type.BGR888p
    ).createOutputQueue(maxSize=2, blocking=False)

    # Mono 400p — max disparity stays well under 1024 limit
    cam_left  = p.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_B)
    cam_right = p.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_C)
    left_out  = cam_left.requestOutput((640, 400), dai.ImgFrame.Type.GRAY8)
    right_out = cam_right.requestOutput((640, 400), dai.ImgFrame.Type.GRAY8)

    stereo = p.create(dai.node.StereoDepth)
    stereo.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.DENSITY)
    stereo.setLeftRightCheck(True)
    stereo.setDepthAlign(dai.CameraBoardSocket.CAM_A)
    stereo.setOutputSize(1280, 720)

    left_out.link(stereo.left)
    right_out.link(stereo.right)

    max_disp = stereo.initialConfig.getMaxDisparity()
    q_disp = stereo.disparity.createOutputQueue(maxSize=2, blocking=False)

    return p, q_rgb, q_disp, max_disp


def capture_thread(label: str):
    q_rgb_out  = QUEUES[label]["rgb"]
    q_disp_out = QUEUES[label]["depth"]

    try:
        if SHOW_DEPTH:
            p, q_rgb, q_disp, max_disp = build_pipeline_depth()
        else:
            p, q_rgb, q_disp, max_disp = build_pipeline_rgb()

        p.start()
        dev_id = p.getDefaultDevice().getDeviceId()
        print(f"[{MX_NAMES.get(dev_id, dev_id)}] streaming  (MX: {dev_id})")

        while not stop_event.is_set():
            f = q_rgb.tryGet()
            if f is not None:
                try:
                    q_rgb_out.put_nowait(f.getCvFrame())
                except queue.Full:
                    pass

            if SHOW_DEPTH and q_disp is not None:
                f = q_disp.tryGet()
                if f is not None:
                    frame = f.getFrame()
                    frame = (frame * (255.0 / max_disp)).astype(np.uint8)
                    frame = cv2.applyColorMap(frame, cv2.COLORMAP_JET)
                    try:
                        q_disp_out.put_nowait(frame)
                    except queue.Full:
                        pass

            time.sleep(0.005)

        p.stop()

    except Exception as exc:
        print(f"[{label}] ERROR: {exc}")


def main():
    devices = dai.Device.getAllAvailableDevices()
    if not devices:
        print("No OAK-D cameras found. Check USB cables and powered hub.")
        sys.exit(1)

    mode = "RGB + Depth" if SHOW_DEPTH else "RGB only (fast)"
    print(f"\nMode: {mode}  |  tip: add 'depth' arg for depth windows")
    print(f"Found {len(devices)} OAK-D camera(s):")
    labels = []
    for d in devices:
        label = MX_NAMES.get(d.deviceId, d.deviceId[:12])
        print(f"  [{label}]  MX ID: {d.deviceId}")
        labels.append(label)
        QUEUES[label] = {"rgb":   queue.Queue(maxsize=2),
                         "depth": queue.Queue(maxsize=2)}

    missing = [n for mx, n in MX_NAMES.items()
               if not any(d.deviceId == mx for d in devices)]
    if missing:
        print(f"  NOT DETECTED: {', '.join(missing)} — check USB / powered hub")

    print()
    for label in labels:
        cv2.namedWindow(f"{label} | RGB", cv2.WINDOW_NORMAL)
        cv2.resizeWindow(f"{label} | RGB", 960, 540)
        if SHOW_DEPTH:
            cv2.namedWindow(f"{label} | Depth", cv2.WINDOW_NORMAL)
            cv2.resizeWindow(f"{label} | Depth", 960, 540)

    threads = []
    for label in labels:
        t = threading.Thread(target=capture_thread, args=(label,), daemon=True)
        t.start()
        threads.append(t)
        time.sleep(1.5)

    print("Streaming — press Q to quit.\n")

    while not stop_event.is_set():
        for label in labels:
            try:
                img = QUEUES[label]["rgb"].get_nowait()
                cv2.putText(img, label, (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
                cv2.imshow(f"{label} | RGB", img)
            except queue.Empty:
                pass

            if SHOW_DEPTH:
                try:
                    dep = QUEUES[label]["depth"].get_nowait()
                    cv2.putText(dep, f"{label} | depth", (10, 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
                    cv2.imshow(f"{label} | Depth", dep)
                except queue.Empty:
                    pass

        key = cv2.waitKey(1) & 0xFF
        if key in (ord('q'), ord('Q'), 27):
            stop_event.set()

    cv2.destroyAllWindows()
    for t in threads:
        t.join(timeout=4.0)
    print("Viewer closed.")


if __name__ == "__main__":
    main()
