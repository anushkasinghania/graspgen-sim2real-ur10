# OPERATIONS.md — How to Run the GraspGen Real Hardware Pipeline

**Last updated: 2026-04-21** — wrist_cam only (no env_cam TF calibration), 3-pose multi-view scan

## What This System Does

```
/pick/start → arm moves to scan pose 1 (top view)
→ you click object in wrist_cam window (one click only)
→ arm auto-scans pose 2 (left) and pose 3 (right) — no more clicks needed
→ 3 partial clouds fused into complete point cloud
→ GraspGen finds best grasp → MoveIt plans → UR10 picks → Robotiq 3F places
```

**Why wrist_cam only:** the wrist_cam TF orientation is computed from robot joint encoders (FK) — the arm always knows where it is pointing. The fixed mechanical offset (tool0 → oakd_wide_link) was calibrated once on 2026-04-27 via a near-edge test: **`(x=0.0, y=−0.065, z=−0.04)`** (previously −0.14; centroid was +75 mm too far forward; residual after fix: 4 mm). The env_cam tripod TF required an estimated pitch angle that was never reliable.

---

## Hardware Checklist (before every session)

| Item | Check |
|------|-------|
| UR10 control box power ON | LED on front panel lit |
| Teach pendant screen ON | Shows robot status |
| Robotiq 3F gripper Ethernet | Cable from gripper to switch; gripper IP 192.168.1.105 |
| wrist_cam USB-C cable | Into powered USB hub → Jetson |
| Jetson Ethernet | Jetson → switch |
| UR10 Ethernet | UR10 control box → switch |

> **env_cam is removed from the pipeline.** Do not plug it in — it causes "device not connected" errors and is unused. wrist_cam only.

---

## Scene Layout

```
        Robot base (x=0, y=0)
               |
        forward (x+)
               |
   [Brown pick tray]  [Yellow place tray]
   68×45×12 cm         32×45×12 cm
   centre: (0.55, 0.00) centre: (0.55, 0.45)
```

- **Brown tray** — place objects here to be picked
- **Yellow tray** — robot places objects here after picking

---

## Every Session — Step by Step

### STEP 0 — Maximize Jetson Performance (run once per boot)

```bash
sudo jetson_clocks
sudo systemctl stop packagekit
```

> Locks CPU/GPU/memory to max frequency. Without this the Jetson throttles under load.

---

### STEP 1 — Power On Robot

1. Turn on UR10 control box (power switch on back/side panel)
2. Wait ~30 seconds — teach pendant screen lights up
3. On teach pendant: tap **Power ON** → arm stiffens with a click sound

---

### STEP 2 — Teach Pendant Setup

1. Tap **☰** (top left) → **Program** → **Open** → select `ros2_control`
2. Verify the program is:
   ```
   Robot Program
     External Control (192.168.1.100)
   ```
   **There must be NO loop around External Control** — if there is, remove it.
3. Top-right corner: tap **Remote Control** toggle → confirm switch
4. Teach pendant now shows `Remote Control` — arm waits for Jetson

---

### STEP 3 — Open Terminals on Jetson

Open **3 separate terminals**. Each runs one command and stays open.

---

### Terminal 1 — UR10 Driver

```bash
ros2 launch ur_robot_driver ur_control.launch.py \
  ur_type:=ur10 \
  robot_ip:=192.168.1.102 \
  use_fake_hardware:=false \
  launch_rviz:=false \
  kinematics_params_file:=$HOME/robot_calibration.yaml 2>&1 | tee /tmp/t1.log
```
✅ Wait for: `Robot is ready to receive commands`

> Then press **Play** on the teach pendant to start the External Control program.

---

### Terminal 2 — Main Pipeline (MoveIt + GraspGen)

```bash
cd ~/research_ws/ur10_pick_place_ws && source install/setup.bash
ros2 launch ur10_pick_place grasp_pipeline.launch.py \
  real_hardware:=true \
  launch_graspgen_bridge:=true \
  launch_env_cam:=false \
  launch_wrist_cam:=false \
  use_rviz:=true 2>&1 | tee /tmp/t2.log
```
✅ Wait for: `[GRASPGEN STATUS] READY` and arm moves to home position

> Cameras are NOT launched here — they run in T3.
> Do not proceed until the arm finishes the auto-home move and goes still.

---

### Terminal 3 — wrist_cam + SAM2 (start when ready to pick)

```bash
~/research_ws/ur10_pick_place_ws/src/ur10_pick_place/scripts/pick.sh 2>&1 | tee /tmp/t3.log
```
✅ Wait for: SAM2 window opens showing live wrist_cam RGB view (~10 seconds)

> The SAM2 window shows the **live wrist_cam view immediately** (from home position).
> The top bar shows **"Send /pick/start first — arm must move to scan pose before clicking"** in grey.
> **Do not click yet** — clicks are ignored until the arm reaches scan pose.

If wrist_cam fails to start:
```bash
pkill -9 -f "camera_node.*wrist_cam"
# Then restart T3
```

---

## STEP 4 — Picking an Object

**Rule: trigger FIRST, click SECOND. Clicks are blocked until the arm is at scan pose.**

### 4a. Place object on the brown pick tray

### 4b. Send the trigger (from any terminal-> Terminal 4):

```bash
ros2 topic pub --once /pick/start std_msgs/msg/Empty "{}" 2>&1 | tee /tmp/t4.log
```

The arm moves to **scan pose 1** (physically measured: pan=-85.5°, lift=-102.3°, elbow=80.1°).
Watch the SAM2 window top bar — it changes from grey to **green "ARM AT SCAN POSE — LEFT-CLICK the target object"**.

### 4c. Click the target object in the SAM2 window

- Top bar is **green** = arm is ready, clicks are active
- **Left-click** on the object → green mask appears
- If mask is wrong: **right-click** to add a negative point, or press **R** to re-click
- You have **60 seconds** — the arm waits at scan pose

### 4d. Done — arm completes the scan automatically

After your click the arm moves on its own:
1. **Pose 2** (pan −15°) → wrist_cam captures left-side view
2. **Pose 3** (pan +15°) → wrist_cam captures right-side view
3. Returns to **home**
4. GraspGen infers on the 3-view fused cloud
5. Arm executes pick and places object on yellow tray

### 4e. Watch Terminal 2 for step-by-step progress

```
[SCANNING] → WAITING FOR CLICK → click → SCANNING L → SCANNING R →
[GRASPGEN STATUS] INFERRING → DONE →
step1b pre-grasp → step2 open → step3 descend →
step4 close → step5 lift → step6 place → step7 release → step8 home
```

### Between Picks

- Press **R** in SAM2 window to clear the old mask
- Place next object → send `/pick/start` → wait for green bar → click
- No need to restart T3

---

## What You See in RViz

| Object | What it is |
|--------|-----------|
| Grey robot arm | UR10 — moves in sync with real arm |
| Brown box | Pick tray — centre (0.55, 0.00) |
| Yellow box | Place tray — centre (0.55, 0.45) |
| Grey floor | Floor collision boundary |
| Green cylinder (appears at start of pick) | `real_target` — estimated object shape from point cloud — **correct and expected** |

---

## How 3-View Point Cloud Fusion Works

The wrist_cam scans the object from 3 angles before GraspGen runs:

| Pose | Shoulder pan | What it captures |
|------|-------------|-----------------|
| Pose 1 — top | −85.5° (measured) | Top face — SAM2 mask applied (your click) |
| Pose 2 — left | −70.5° (+15°) | Left side face — spatial filter auto-applied |
| Pose 3 — right | −100.5° (−15°) | Right side face — spatial filter auto-applied |

**You click once at pose 1.** The centroid from that click is used as a spatial anchor at poses 2 and 3 — any wrist_cam depth point within **0.25 m** of that centroid is kept automatically.

**Noise filtering applied at every pose:**
- World-frame height clamp `[0.13 m, 0.55 m]` — removes tray surface and ceiling
- Statistical outlier removal (k=20 neighbours, 1.5σ threshold) — removes depth spikes

All 3 partial clouds are transformed to world frame using the robot's own FK (joint encoders → URDF → exact camera position) and concatenated before GraspGen inference.

---

## Quick Connection Check (run any time)

```bash
# Network
ping -c 1 192.168.1.102 && echo "UR10 OK"     || echo "UR10 OFFLINE"
ping -c 1 192.168.1.105 && echo "Robotiq OK"  || echo "Robotiq OFFLINE"
ping -c 1 192.168.1.10  && echo "Jetson OK"   || echo "Jetson OFFLINE"

# Gripper Modbus TCP
python3 -c "
import socket
try:
    s = socket.create_connection(('192.168.1.105', 502), timeout=3)
    s.close(); print('Robotiq port 502 OPEN — gripper reachable')
except Exception as e:
    print(f'Robotiq UNREACHABLE: {e}')
"

# wrist_cam only
python3 -c "
import depthai as dai
devs = dai.Device.getAllAvailableDevices()
for d in devs:
    if d.deviceId == '14442C10715AD4D200':
        print('wrist_cam OK')
    else:
        print(f'Unknown device: {d.deviceId} (env_cam? leave unplugged)')
if not devs:
    print('No cameras found — check USB-C cable and powered hub')
"
```

---

## If Something Goes Wrong

| Symptom | What to do |
|---------|-----------|
| Top bar stays grey after /pick/start | Arm still moving to scan pose — wait 5–15 s; check T2 for motion errors |
| Top bar never turns green | Arm failed to reach scan pose — check T2 for planning error; retry /pick/start |
| Click has no effect (mask doesn't appear) | Top bar must be green before clicking — send /pick/start first |
| 60-second timeout — "No user click received" | Top bar was green but no click in time; send /pick/start again |
| Green mask wrong shape | Right-click negative points or press R and re-click |
| Arm skips pose 2 or 3 — "motion failed" | Planning collision or IK issue; pick still proceeds on partial cloud |
| `GRASPGEN STATUS` never READY | Model loading takes ~30 s — wait longer; check T2 for import errors |
| Arm doesn't move after GraspGen DONE | IK failure — publish `/pick/start` again to retry from scratch |
| `planning failed` in logs | Bad GraspGen pose — publish `/pick/start` again |
| Gripper doesn't close | `ping 192.168.1.105` — check Ethernet cable to gripper; check port 502 with socket test above |
| Robot position wrong in RViz | T1 must be running before T2; teach pendant must be in Remote Control with External Control program running |
| Arm through tray / collision | Object centroid z too low — check wrist_cam depth at scan pose in T3 logs; height filter may be removing all points |
| Cursor lags / system hangs | Run `sudo jetson_clocks`; stop T3 when not actively picking |

---

## Emergency Stop

**If the arm moves unexpectedly:**
1. Press the big **red STOP button** on the teach pendant immediately
2. Arm halts. Power stays on.
3. To resume: clear Protective Stop on pendant → tap **Resume** → check all terminals

> After an emergency stop: close T1 → restart T1 → wait for `Robot is ready` → press Play on pendant.

---

## Shutdown Sequence

1. Ctrl-C in **T3** (wrist_cam + SAM2 stop together)
2. Ctrl-C in **T2** (pipeline) — grasp_executor deactivates gripper automatically
3. Ctrl-C in **T1** (UR10 driver)
4. On teach pendant: switch back to **Local** mode
5. Tap **Power OFF** on pendant → arm relaxes
6. Turn off UR10 control box power switch

---

## Camera Viewer (checking wrist_cam view without pipeline)

```bash
python3 ~/research_ws/ur10_pick_place_ws/src/ur10_pick_place/scripts/oakd_viewer.py
```

Move arm to scan pose manually first to verify wrist_cam sees the tray:
```bash
# In any sourced terminal — move arm to scan pose 1 (top view)
ros2 topic pub --once /pick/start std_msgs/msg/Empty "{}"
# Then check the wrist_cam window shows the tray clearly
```

---

## File Locations

| File | Purpose |
|------|---------|
| `~/research_ws/OPERATIONS.md` | This file |
| `~/CLAUDE.md` | Project overview and full status |
| `~/robot_calibration.yaml` | UR10 kinematic calibration |
| `src/ur10_pick_place/launch/grasp_pipeline.launch.py` | Main pipeline launch |
| `src/ur10_pick_place/scripts/pick.sh` | wrist_cam + SAM2 launch (T3) |
| `src/ur10_pick_place/scripts/sam2_segmentation_node.py` | SAM2 click → 3-view fusion → /env_cam/points |
| `src/grasp_executor/grasp_executor/grasp_executor_node.py` | 8-step pick + multi-view scan sequence |
| `src/grasp_executor/grasp_executor/robotiq_3f_gripper.py` | Gripper Modbus TCP controller |
| `src/grasp_executor/grasp_executor/graspgen_bridge_node.py` | GraspGen inference bridge |
