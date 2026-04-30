# WORKFLOW.md — Full Pipeline Documentation

## Project: GraspGen Sim2Real on UR10 + Robotiq 3F + OAK-D

---

## 1. How the System Works (End-to-End)

### 1.1 The Big Picture

The goal is to pick a target object from a cluttered scene and place it on a tray.
The SAME software runs in simulation and on real hardware — only the point cloud source changes.

```
┌──────────────────────────────────────────────────────────────┐
│                     SIMULATION                               │
│                                                              │
│  sim_object_pc_publisher                                     │
│  (Python script, makes a fake cylinder point cloud)          │
│         │                                                    │
│         ▼  /env_cam/points  (PointCloud2, world frame)       │
│  graspgen_bridge_node                                        │
│  (sends PC to GraspGen neural net on GPU)                    │
│         │                                                    │
│         ▼  /graspgen/grasp_pose  (PoseStamped)               │
│  grasp_executor_node                                         │
│  (IK → OMPL → MoveIt2 → UR10 joints → pick → place)         │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                   REAL HARDWARE                              │
│                                                              │
│  env_cam (OAK-D Pro, tripod, looking at workspace)           │
│         │  RGB image + Depth image                           │
│         ▼                                                    │
│  sam2_segmentation_node                                      │
│  (you click the target object in a window)                   │
│  (SAM2 neural net → binary mask over the object)             │
│  (mask × depth → 3D points → transform to world frame)       │
│         │                                                    │
│         ▼  /env_cam/points  ← SAME TOPIC AS SIM              │
│  graspgen_bridge_node  ← SAME NODE AS SIM                    │
│         │                                                    │
│         ▼  /graspgen/grasp_pose                              │
│  grasp_executor_node  ← SAME NODE AS SIM                     │
│  (IK → OMPL → real UR10 arm → Robotiq 3F gripper via TCP)    │
└──────────────────────────────────────────────────────────────┘
```

### 1.2 Camera Naming

| Name | Camera | Mount | MX ID | Namespace | Key Topics |
|------|--------|-------|-------|-----------|-----------|
| `env_cam` | OAK-D Pro | Tripod (workspace view) | `14442C1041A6D1D200` | `/env_cam` | `/env_cam/rgb/image_raw`, `/env_cam/depth/image_raw`, `/env_cam/points` |
| `wrist_cam` | OAK-D Pro Wide | Gripper (eye-in-hand) | `14442C10715AD4D200` | `/wrist_cam` | `/wrist_cam/rgb/image_raw`, `/wrist_cam/depth/image_raw` |

Both cameras are pinned to their MX IDs in YAML configs — they always come up on the correct
topics regardless of USB plug order.

### 1.3 What Each Node Does

| Node | What it does | Sim / Real |
|------|-------------|-----------|
| `sim_object_pc_publisher` | Generates synthetic cylinder point cloud at known object position | Sim only |
| `sam2_segmentation_node` | Shows live env_cam view; user clicks object; SAM2 segments it; depth gives 3D shape | Real only |
| `graspgen_bridge_node` | Receives `/env_cam/points` → GraspGen Generator (proposes grasps) → Discriminator (scores) → best grasp pose | Both |
| `grasp_executor_node` | Receives grasp pose → IK → OMPL motion plan → 8-step pick-and-place via MoveIt2 | Both |
| `planning_scene_setup` | Adds collision objects (trays, all 6 scene objects) to MoveIt scene | Both |

### 1.4 What GraspGen Does

GraspGen is a neural network trained on millions of grasps:
- **Generator**: takes the object point cloud → outputs ~100 candidate grasp poses (position + orientation)
- **Discriminator**: scores each candidate → picks the best one
- Output: a single PoseStamped in world frame = where to position the gripper palm to grasp the object

### 1.5 What MoveIt2 / OMPL Does

MoveIt2 is the motion planning framework:
- You give it a target pose for the end-effector
- **IK (Inverse Kinematics)**: finds joint angles that put the arm at that pose (using KDL solver)
- **OMPL (RRTConnect)**: finds a collision-free path from current joint angles to IK solution
- The arm moves through this path, avoiding all registered collision objects
- Collision objects include: trays, all 6 scene objects, and the floor

### 1.6 8-Step Pick-and-Place Sequence

```
Step 1a: Move arm to HOME position (80,-90,69,-69,-90,-15 degrees)
Step 1b: Move to pre-grasp (directly above object at z=0.41m)
Step 2:  Open gripper (Robotiq 3F fingers spread)
Step 3:  Lower arm straight down to grasp height
Step 4:  Close gripper (fingers curl around object)
         → Object attached to palm in MoveIt collision scene
Step 5:  Lift straight up to z=0.41m (above all distractors)
Step 6:  Move to place position on place tray
         OMPL routes around distractors automatically
Step 7:  Open gripper (object released on tray)
Step 8:  Return arm to HOME position
```

### 1.7 Why Sim Arm Clips Through Distractors During Pick (Steps 1b→3)

During steps 1b and 3 (pre-grasp descent), MoveIt2's **global ACM** (Allowed Collision Matrix)
has distractors set to `allow=True`. This is intentional: the arm descends vertically through
the space above the target, and the thin links (forearm, wrist) pass very close to or through
distractor bounding cylinders. Since real objects are not infinite cylinders, and the arm
doesn't actually contact them, this is physically correct. During **place (step 6)**, distractors
are restored to `allow=False` so OMPL routes the arm around them properly.

---

## 2. Network & Hardware Reference

| Device | IP | Connection | Notes |
|--------|-----|-----------|-------|
| Jetson AGX Orin | 192.168.1.10 | Ethernet to switch | Set static IP on eth0 |
| UR10 arm | 192.168.1.102 | Ethernet to switch | ur_robot_driver |
| Robotiq 3F gripper | 192.168.1.105 | Ethernet (Modbus TCP, port 502) | Controlled via Python TCP — NO RS-485 |
| OAK-D Pro (env_cam) | — | USB-C → powered USB3 hub | MX ID: 14442C1041A6D1D200 |
| OAK-D Pro Wide (wrist_cam) | — | USB-C → powered USB3 hub | MX ID: 14442C10715AD4D200 |
| Developer PC | 192.168.1.100 | Ethernet to switch | RViz / SSH access |

**Gripper note**: The Robotiq 3F connects via Ethernet (not RS-485). The `grasp_executor_node`
activates the gripper on startup and deactivates it on shutdown using raw Modbus TCP frames.
No separate ROS2 gripper driver is needed.

---

## 3. Software Status (2026-04-13)

### Installed and Verified ✅
| Component | Location | Status |
|-----------|---------|--------|
| ROS2 Humble + MoveIt2 + OMPL | system | ✅ |
| ur10_pick_place package | ~/research_ws/ur10_pick_place_ws/ | ✅ built |
| GraspGen v3 (Generator + Discriminator) | ~/research_ws/GraspGen/ | ✅ |
| Torch nv24.08 (CUDA) | ~/.local/lib/python3.10/site-packages/ | ✅ CUDA=True |
| SAM2 (Meta) | ~/.local/lib/python3.10/site-packages/sam2/ | ✅ inference OK |
| SAM2 checkpoint | ~/research_ws/segment-anything-2/checkpoints/sam2.1_hiera_small.pt | ✅ 176MB |
| sam2_segmentation_node.py | src/ur10_pick_place/scripts/ | ✅ built |
| robotiq_3f_gripper.py | src/grasp_executor/grasp_executor/ | ✅ Modbus TCP |
| Simulation pipeline | — | ✅ 2× SUCCESS verified (2026-04-09) |

### Not Needed (confirmed)
- ~~cuRobo~~ — MoveIt2+OMPL handles all collision avoidance
- ~~NVBlox~~ — distractors added as cylinders to MoveIt scene
- ~~RS-485 gripper driver~~ — Robotiq 3F uses Ethernet Modbus TCP

### Pending (hardware required)
- env_cam TF calibration (tape-measure x,y,z,pitch from robot base)
- Tray position measurements (pick tray + place tray actual x,y,z)
- UR10, OAK-D bringup and verification

---

## 4. Phase 0 — Simulation (VERIFIED ✅ 2026-04-09)

```bash
pkill -f rviz2; pkill -f ros2; sleep 2
cd ~/research_ws/ur10_pick_place_ws
source /opt/ros/humble/setup.bash && source install/setup.bash
ros2 launch ur10_pick_place grasp_pipeline.launch.py \
  launch_graspgen_bridge:=true launch_sim_pc:=true sim_pc_object:=tin_can
```

After `[GRASPGEN STATUS] READY` appears:
```bash
ros2 topic pub --once /graspgen/trigger std_msgs/msg/Empty "{}"
ros2 topic echo /grasp_executor/status
```

Expected: `EXECUTING` → step 1a → 1b → 2 → 3 → 4 → 5 → 6 → 7 → 8 → `SUCCESS`

---

## 5. Phase 1 — Hardware Bringup (Step-by-Step)

Do these in order. Each step has a verification before moving on.

---

### STEP 1 — Physical Connections

#### What you need before starting:
- Powered USB3 hub (min 60W rated, e.g. Anker 10-port powered hub)
- Ethernet switch or cables: Jetson ↔ UR10 ↔ Robotiq 3F ↔ developer PC (all on 192.168.1.x)
- USB-C cables for both OAK-D cameras

#### Connect everything:

```
[UR10 control box] ──Ethernet──► [switch] ──Ethernet──► [Jetson eth0]  (192.168.1.10)
[Robotiq 3F base]  ──Ethernet──► [switch]               (gripper at 192.168.1.105)
[Developer PC]     ──Ethernet──► [switch]                (PC at 192.168.1.100)

[env_cam OAK-D Pro]       ──USB-C──► [powered USB3 hub] ──USB3──► [Jetson]
[wrist_cam OAK-D Pro Wide] ──USB-C──► [powered USB3 hub] ──USB3──► [Jetson]
```

**Power on order**: Jetson → powered USB hub → UR10 control box (its own PSU) → Robotiq 3F (powered from UR10 tool I/O).

---

### STEP 2 — Jetson Network Configuration

Set Jetson's Ethernet interface on the 192.168.1.x subnet:

```bash
# Find Ethernet interface name
ip link show
# Typically: eth0 or enp3s0 or enx...

# Set static IP (replace eth0 with your interface name)
sudo ip addr add 192.168.1.10/24 dev eth0
sudo ip link set eth0 up

# Verify connectivity
ping 192.168.1.102    # should reply from UR10
ping 192.168.1.105    # should reply from Robotiq 3F gripper
```

To make permanent (survives reboot):
```bash
nmcli con add type ethernet ifname eth0 con-name ur10-net \
  ip4 192.168.1.10/24
nmcli con up ur10-net
```

---

### STEP 3 — UR10 Teach Pendant Setup

On the UR10 teach pendant (touchscreen on the robot):

1. **Install URCap** (one-time, if not already done):
   - Go to: `Settings` → `System` → `URCaps`
   - Install `ExternalControl-x.x.x.urcap`
   - Reboot robot

2. **Set External Control Host IP**:
   - `Installation` → `URCaps` → `External Control`
   - Set `Host IP` = `192.168.1.10` (Jetson IP)
   - Set `Custom port` = `50002`

3. **Load the External Control program**:
   - `Program` tab → `URCaps` → `External Control`

4. **Switch to Remote Control mode**:
   - Top-right of teach pendant → toggle `Local` → `Remote Control`

5. **Move arm to HOME position** manually first (if not already near it):
   - Joint angles: shoulder_pan=80°, lift=-90°, elbow=69°, wrist1=-69°, wrist2=-90°, wrist3=-15°
   - Then enable Remote Control — arm holds position until ROS2 sends a command

---

### STEP 4 — Launch UR10 Driver

```bash
# Terminal 1
source /opt/ros/humble/setup.bash
ros2 launch ur_robot_driver ur_control.launch.py \
  ur_type:=ur10 \
  robot_ip:=192.168.1.102 \
  use_fake_hardware:=false \
  launch_rviz:=false \
  kinematics_params_file:=$HOME/robot_calibration.yaml
```

**Expected output** (within 5 seconds):
```
[ur_robot_driver]: Robot is ready to receive commands
```

**Verify joint states are publishing**:
```bash
ros2 topic echo /joint_states --once
# Expected: 6 joints matching actual arm position
```

**If it fails**:
- Check `ping 192.168.1.102`
- Check teach pendant is in Remote Control mode
- Check External Control URCap Host IP = 192.168.1.10

---

### STEP 5 — Verify Robotiq 3F Gripper Connection

The gripper connects via Ethernet (Modbus TCP). The `grasp_executor_node` controls it directly —
no separate ROS2 driver is needed. Just verify connectivity:

```bash
# Check gripper is reachable
ping 192.168.1.105

# Quick Python test (optional — gripper will activate when executor starts):
python3 -c "
import socket
s = socket.socket()
s.settimeout(2.0)
s.connect(('192.168.1.105', 502))
print('Gripper TCP OK')
s.close()
"
```

If the ping fails:
- Check Ethernet cable from Robotiq 3F base to switch
- Verify gripper IP is set to 192.168.1.105 (use Robotiq config tool if needed)

---

### STEP 6 — Launch Cameras (env_cam + wrist_cam)

Both cameras are launched via the main launch file using their MX IDs — no separate terminals needed.
Add these flags to the main launch command:

```bash
launch_env_cam:=true launch_wrist_cam:=true
```

**Verify env_cam topics are live**:
```bash
ros2 topic list | grep env_cam
# Expected:
# /env_cam/rgb/image_raw
# /env_cam/depth/image_raw
# /env_cam/rgb/camera_info
# /env_cam/points  (after sam2_segmentation_node or sim_pc_publisher)

ros2 topic hz /env_cam/rgb/image_raw
# Expected: ~30 Hz

ros2 run rqt_image_view rqt_image_view /env_cam/rgb/image_raw
# View live workspace
```

**Verify wrist_cam topics**:
```bash
ros2 topic hz /wrist_cam/rgb/image_raw
# Expected: ~30 Hz
```

**If a camera fails to start**:
- Check `lsusb | grep MyriadX` (OAK-D appears as Myriad device)
- Check USB hub is powered
- The MX ID in the YAML must match the physical device — confirm with `depthai_device_finder`

---

### STEP 7 — Calibrate env_cam Tripod Position (TF)

This is critical. GraspGen needs 3D points in the **world frame** (robot base frame).
The camera outputs points in its own **camera frame**. We need the TF between them.

#### Measure physically:
1. From the robot base centre (floor-level mounting hole) measure with tape:
   - `x`: distance forward (+ = toward workspace)
   - `y`: distance left/right (+ = left when facing robot)
   - `z`: height of camera lens above floor
2. Estimate camera tilt with phone inclinometer app:
   - `pitch`: angle tilting down toward workspace (positive = down)

#### Update static TF in `grasp_pipeline.launch.py`:
```python
Node(
    package='tf2_ros',
    executable='static_transform_publisher',
    arguments=['X', 'Y', 'Z', 'YAW', 'PITCH', 'ROLL',
               'world', 'env_cam_link'],
)
```
Replace X, Y, Z, YAW, PITCH, ROLL with your measured values (metres and radians).

#### Verify calibration:
```bash
# Place tin_can at a known position, e.g. (0.60, 0.00)
# Check point cloud appears at correct position in RViz
ros2 run rviz2 rviz2  # add PointCloud2 display, topic=/env_cam/points
```

---

### STEP 8 — Measure and Update Tray Positions

Measure actual tray x, y, z positions from robot base centre and update `planning_scene_setup.py`.

Current sim values (update these with real measurements):
```
pick_tray:  centre (0.55, 0.00), lx=0.68, ly=0.45, top_z=0.12
place_tray: centre (0.55, 0.60), lx=0.32, ly=0.45, top_z=0.12
```

Once measured, provide the values and planning_scene_setup.py will be updated.

---

## 6. Phase 2 — SAM2 + Full Real Pipeline

### 6.1 Full Real Hardware Launch Command

```bash
# Kill any previous ROS2 nodes
pkill -f rviz2; pkill -f ros2; sleep 2

cd ~/research_ws/ur10_pick_place_ws
source /opt/ros/humble/setup.bash && source install/setup.bash

ros2 launch ur10_pick_place grasp_pipeline.launch.py \
  real_hardware:=true \
  launch_graspgen_bridge:=true \
  launch_env_cam:=true \
  launch_wrist_cam:=true
```

### 6.2 Launch SAM2 Node (separate terminal)

```bash
source /opt/ros/humble/setup.bash && source install/setup.bash
ros2 run ur10_pick_place sam2_segmentation_node \
  --ros-args \
  -p checkpoint:=$HOME/research_ws/segment-anything-2/checkpoints/sam2.1_hiera_small.pt \
  -p model_cfg:=configs/sam2.1/sam2.1_hiera_s.yaml
```

A window opens showing the live env_cam RGB stream.

### 6.3 Per-Pick Procedure

1. Arrange scene: target object front-centre on pick tray, distractors around it
2. Wait for `[GRASPGEN STATUS] READY` in main launch terminal
3. In SAM2 window: **left-click on the target object**
   - Green mask appears over the object
   - If mask is wrong: right-click to add negative prompt, or press R to reset
4. Trigger GraspGen:
   ```bash
   ros2 topic pub --once /graspgen/trigger std_msgs/msg/Empty "{}"
   ```
5. Watch arm execute pick-and-place
6. Monitor: `ros2 topic echo /grasp_executor/status`

### 6.4 Real Hardware vs Simulation Differences

| Aspect | Simulation | Real Hardware |
|--------|-----------|--------------|
| PC source | sim_object_pc_publisher (synthetic cylinder) | env_cam → SAM2 (real depth, real shape) |
| PC topic | `/env_cam/points` | `/env_cam/points` (same) |
| Object identity | Hardcoded SCENE_PICK_OBJECTS (tin_can etc.) | Any unknown object — geometry estimated from cloud |
| Object geometry | Known radius/height from dict | Estimated: z5/z95 → height, 90th-pct XY dist → radius |
| Grasp position | Snapped to SCENE_PICK_OBJECTS centre | Used directly from GraspGen SE(3) output |
| Distractors in MoveIt | 5 known cylinders from planning_scene_setup.py | None registered (no prior scene knowledge) |
| Gripper | Simulated joint controller | Real Robotiq 3F via Modbus TCP (192.168.1.105) |
| Gripper lifecycle | N/A | Activates on executor start, deactivates on shutdown |
| IK / OMPL | Identical | Identical |
| Home position | 80,-90,69,-69,-90,-15° | 80,-90,69,-69,-90,-15° (same) |

**What happens in real hardware mode (`real_hardware:=true`)**:
1. Executor subscribes to `/env_cam/points` (SAM2 node output)
2. Connects to Robotiq 3F at 192.168.1.105 via Modbus TCP; activates gripper
3. On trigger, reads latest cloud → estimates object geometry from point statistics
4. Adds `"real_target"` cylinder to MoveIt scene with estimated dimensions
5. Uses GraspGen's pose directly (no snap to known position)
6. Places object at place tray position
7. No auto-trigger — user clicks SAM2 window to segment each object

---

## 7. Phase 3 — Sim2Real Evaluation

### 7.1 Experiment Design

N = 20 trials per condition.

| Condition | PC Source | Robot |
|-----------|----------|-------|
| Simulation | sim_object_pc_publisher (synthetic cylinder) | RViz (virtual execution) |
| Real | env_cam → SAM2 (real texture + shape) | Physical UR10 + Robotiq 3F |

Same scene layout for all trials. Reset scene between trials.

### 7.2 Log Per Trial
```
trial_id, condition, grasp_success (0/1),
discriminator_confidence (float),
ik_success (0/1), ompl_success (0/1),
execution_time_sec, failure_mode
```

### 7.3 Metrics
| Metric | Formula |
|--------|---------|
| Grasp success rate | successes / N × 100% |
| Mean GraspGen confidence | avg discriminator score |
| Planning success rate | (IK ∩ OMPL success) / N |
| Mean execution time | avg sec per successful trial |

### 7.4 Plots to Generate
1. Success rate bar — Sim vs Real
2. Confidence histogram — Sim vs Real overlaid (domain gap visualization)
3. Planning time CDF — Sim vs Real
4. Failure mode breakdown — pie per condition
5. Qualitative figure — RViz screenshot (sim) + photo (real) side by side

---

## 8. Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Lift failed error 99999 | wrist_2_link clips attached object | wrist_2_link in GRIPPER_TOUCH_LINKS; palm_frame_z signed |
| Arm through distractor during place | Distractors in place_allow list | Restore distractor ACM=False before step 6 |
| Pre-grasp IK failed | Backward arm solution | 3-attempt fallback with forward-reach seed |
| GraspGen returns no grasps | Empty PC or wrong frame | Check `/env_cam/points`; verify frame_id=world |
| SAM2 mask on wrong object | Click landed on background | Press R, re-click; right-click adds negative prompt |
| UR10 joint states stale | Driver not connected | Check ping 192.168.1.102; robot in Remote Control |
| Gripper not responding | Ethernet not connected | ping 192.168.1.105; check switch connections |
| Gripper fails to activate | Wrong Modbus register or unit ID | Check RobotiqGripper3F logs; verify gIMC bits |
| env_cam not detected | USB hub not powered or wrong MX ID | `lsusb | grep Myriad`; verify MX ID in oakd_env.yaml |
| wrist_cam not detected | Same as above | Verify MX ID in oakd_wrist.yaml |
| PC in wrong world position | env_cam TF not calibrated | Re-measure; update static_transform_publisher args |
| torch CUDA False | Wrong torch installed | Use Jetson nv24.08 torch, not PyPI torch |

---

## 9. GitHub Setup

```bash
cd ~/research_ws
git init
echo -e "GraspDataGen/training_data/\n**/build/\n**/install/\n**/log/\n**/__pycache__/\n*.pth\ncheckpoints/*.pt" > .gitignore
git add .
git commit -m "Initial commit: GraspGen sim2real pipeline, SAM2 node"
git remote add origin git@github.com:YOUR_USERNAME/graspgen-sim2real.git
git push -u origin main

# Daily auto-commit at 11PM
crontab -e
# Add:
# 0 23 * * * cd ~/research_ws && git add -A && git commit -m "auto: $(date +\%Y-\%m-\%d)" && git push
```
