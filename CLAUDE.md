# CLAUDE.md — Project Overview

## Project Title
Deep Learning based Grasp Pose Detection on Point Clouds with Sim2Real Manipulation

## Goal
Implement NVIDIA's GraspGen on a UR10 + Robotiq 3F + OAK-D cameras in a cluttered pick scene.
Validate sim-to-real transfer: same GraspGen model trained on GraspDataGen data deployed first in
RViz simulation (synthetic PC), then on real hardware (real camera PC).

## Research Gap
- GraspGen originally tested on 2F grippers and A100 clusters — adapt to Robotiq 3F + Jetson AGX Orin
- Real-world cluttered pick scene evaluation (FetchBench-style, 6 objects)
- Sim2Real gap analysis: compare GraspGen grasp quality and success rate in sim vs real

## Hardware
- Robot Arm: UR10 — IP: 192.168.1.102
- Gripper: Robotiq 3F — IP: 192.168.1.105 (Ethernet/Modbus TCP, controlled via Python script)
- Environment Camera: OAK-D Pro — **NOT in current setup** — MX ID: 14442C1041A6D1D200 (reserved, not connected)
- Wrist Camera: OAK-D Pro Wide — mounted on gripper — MX ID: 14442C10715AD4D200 → topic ns: wrist_cam
- Compute: Jetson AGX Orin 64GB — PC IP: 192.168.1.100 (user's PC / SSH host)
- Robot stand height: **5 cm** → floor at Z = −0.05 m in world/base_link frame

## Network
| Device | IP | Notes |
|--------|----|-------|
| UR10 arm | 192.168.1.102 | Ethernet to Jetson |
| Robotiq 3F gripper | 192.168.1.105 | Ethernet, Modbus TCP port 502 |
| User PC | 192.168.1.100 | SSH to Jetson; also UR10 External Control Host IP if driver runs on PC |
| Jetson AGX Orin | 192.168.1.10 (set manually) | Runs all ROS2 nodes |

## Software Stack
- ROS2 Humble + MoveIt2 + OMPL (RRTConnect)
- Python, C++
- GraspGen (NVIDIA) — ~/research_ws/GraspGen/ (Jetson-adapted fork)
- GraspDataGen (NVIDIA) — ~/GraspDataGen/ (18GB dataset, not pushed to GitHub)
- SAM2 (Meta) — INSTALLED ✅ at ~/.local/lib/python3.10/site-packages/sam2/
  - Checkpoint: ~/research_ws/segment-anything-2/checkpoints/sam2.1_hiera_small.pt (176MB)
  - Config: configs/sam2.1/sam2.1_hiera_s.yaml
  - Dependencies: iopath==0.1.10, portalocker==3.2.0 (installed --no-deps)
  - torchvision 0.20.1 patched: _meta_registrations.py nms try/except for Jetson compat
- Robotiq 3F TCP controller: src/grasp_executor/grasp_executor/robotiq_3f_gripper.py
  - Modbus TCP to 192.168.1.105:502 — activates on node start, deactivates on shutdown
- depthai_ros_driver — OAK-D camera driver (built in ~/ur_camera_ws/)
- ur_robot_driver — UR10 ROS2 driver

## Camera Topics
| Camera | MX ID | ROS2 Namespace | Key Topics | Status |
|--------|-------|----------------|-----------|--------|
| OAK-D Pro (tripod) | 14442C1041A6D1D200 | env_cam | /env_cam/rgb/image_raw, /env_cam/depth/image_raw | **NOT USED** |
| OAK-D Pro Wide (wrist) | 14442C10715AD4D200 | wrist_cam | /wrist_cam/rgb/image_raw, /wrist_cam/stereo/image_raw | **ACTIVE** |

**Only wrist_cam is in the current hardware setup.**
- `/env_cam/points` topic is still used as the pipeline point cloud topic name (published by sam2_segmentation_node from wrist_cam data — kept for compatibility with GraspGen bridge).
- `config/oakd_wrist.yaml` → wrist_cam (fixed MX ID)
- `config/oakd_env.yaml` → kept but env_cam hardware not connected

## Home Position
```
shoulder_pan  =  80° =  1.3963 rad
shoulder_lift = -90° = -1.5708 rad
elbow         =  69° =  1.2043 rad
wrist_1       = -69° = -1.2043 rad
wrist_2       = -90° = -1.5708 rad
wrist_3       = -15° = -0.2618 rad
```
Defined as `HOME_JOINTS` constant in grasp_executor_node.py — used for auto-home and steps 1a/8.

**At HOME: wrist_cam faces straight down toward the centre of the pick tray.**
FK-verified: tool0 at world (-0.061, 0.663, 0.859) → pick_tray XY ≈ (-0.06, 0.66).

## Scan Poses (Real Hardware — wrist_2 tilt only, base stays still)
```
SCAN_JOINTS   (centre above tray):  pan=90.52°, lift=-94.38°, elbow=67.46°, w1=-63.07°, w2=-89.97°, w3=0.96°
SCAN_JOINTS_L (wrist_2 tilt +15°): same pan/lift/elbow/w1/w3; wrist_2=-74.97° (-1.3088 rad)
SCAN_JOINTS_R (wrist_2 tilt -15°): same pan/lift/elbow/w1/w3; wrist_2=-104.97° (-1.8318 rad)
```
Measured on teach pendant 2026-04-24 — arm physically above pick tray centre.
- Only wrist_2 moves between centre/L/R poses — arm base does NOT swing
- Duration: 5 s per L/R move (reduced from 10 s because only wrist moves)
- FK at SCAN_JOINTS (tf2_echo world tool0, 2026-04-24): tool0=(-0.174, 0.583, 0.917), RPY≈(-175°,0,0)
  → tool0+Y=world−Y, tool0+Z=world−Z (≈5° forward tilt toward +Y)
  → wrist_cam (with TF y=−0.065, calibrated 2026-04-27) at world (-0.174, 0.644, 0.957)
  → depth axis hits tray surface at world Y≈0.718 (inside tray near edge) ✓
  → [OLD: TF y=−0.14 gave world Y=0.719 — centroid was +75 mm too far forward; calibrated by near-edge test]

---

## Critical Real-Hardware Coordinate System Facts

**world = base_link (IDENTITY TF — confirmed via `ros2 run tf2_ros tf2_echo world base_link`)**

In simulation, world→base_link had a 90° yaw rotation. In real hardware it is IDENTITY.
All world-frame coordinates are the same as base_link-frame coordinates.

**UR10 base_link axes (real hardware):**
- +X: direction arm faces when shoulder_pan = 0°
- +Y: direction arm faces when shoulder_pan = 90° — approximately the arm's home reach direction
- At home (pan=80°), arm points ≈ (+0.17, +0.98) — mostly +Y, slight +X
- When standing at base facing +Y: LEFT = −X, RIGHT = +X

**IK formulas (use these — NOT the sim versions):**
```python
expected_pan = math.atan2(gy, gx)          # world=base_link identity
expected_pan = clamp(expected_pan, 60°, 160°)
seed_wrist_2 = -1.5708                      # -90° matches real arm at home/scan
```

---

## GraspGen Pipeline (Our Implementation)

### Simulation Pipeline
```
sim_object_pc_publisher → /env_cam/points (synthetic PC, world frame)
         ↓
graspgen_bridge_node → GraspGen inference (Generator v3 + Discriminator v3)
         ↓ /graspgen/grasp_pose (PoseStamped, world frame)
grasp_executor_node → IK → OMPL plan → UR10 joints → pick → place
```

### Real Hardware Pipeline
```
OAK-D Pro Wide (wrist_cam at HOME, looking straight down at pick tray)
         ↓ /wrist_cam/rgb/image_raw  /wrist_cam/stereo/image_raw
sam2_segmentation_node:
  User left-clicks target in live wrist_cam RGB window → SAM2 (CUDA) → binary mask
  mask × wrist_cam depth → back-project via FK TF → partial point cloud
         ↓ /pick/start trigger
grasp_executor_node: moves arm to SCAN_JOINTS (wrist_cam above pick tray, different pose)
         ↓
sam2_segmentation_node: fuses wrist_cam depth at SCAN_JOINTS_L / SCAN_JOINTS_R
  (spatial filter ±0.25 m of pose-1 centroid) → complete point cloud (3 views)
         ↓
grasp_executor_node: returns home, publishes /graspgen/trigger
         ↓
graspgen_bridge_node → GraspGen inference (complete PC → better grasps)
         ↓ /graspgen/grasp_pose
grasp_executor_node (real_hardware:=true):
  Robotiq 3F TCP → open gripper → descend → close → lift → place → home
```

---

## Software Status — Updated 2026-04-24

### Done ✅
| Component | Status |
|-----------|--------|
| Simulation pipeline | VERIFIED 2× SUCCESS (2026-04-09) |
| SAM2 installation + CUDA inference | DONE (2026-04-13) |
| sam2_segmentation_node.py | BUILT |
| real_hardware mode in grasp_executor | DONE — geometry from cloud, TCP gripper |
| Robotiq 3F TCP controller | DONE (robotiq_3f_gripper.py) |
| Home position updated (80,-90,69,-69,-90,-15°) | DONE |
| Camera topics renamed: env_cam / wrist_cam | DONE |
| Camera MX IDs fixed in YAML | DONE |
| Camera nodes in launch file | DONE (pick.sh launches both cameras) |
| All /oakd_pro/points → /env_cam/points | DONE |
| Dual-cam PC fusion (env_cam + wrist_cam) | DONE (2026-04-16) |
| SCAN_JOINTS pose (wrist_cam above pick tray) | DONE (2026-04-16) |
| /pick/start topic → scan then GraspGen | DONE (2026-04-16) |
| grasp_executor _pc_callback dtype fix | DONE (2026-04-16) |
| world=base_link identity TF confirmed | DONE (2026-04-20) |
| Scan changed to wrist_2 ±15° (not shoulder_pan) | DONE (2026-04-23) |
| expected_pan formula corrected for identity TF | DONE (2026-04-23) |
| Workspace bounds: arm-reach sphere not +X bias | DONE (2026-04-23) |
| IK seed wrist_2=-1.5708 (-90°) | DONE (2026-04-23) |
| PLACE_SLOTS updated to real-hardware coords | DONE (2026-04-23) |
| SAM2 "PROCESSING..." indicator during inference | DONE (2026-04-23) |
| Tray positions from tape measure (Tray_Dim.odt) | DONE (2026-04-23) |
| env_cam removed — wrist_cam only pipeline | DONE (2026-04-23) |
| TABLE_TOP_Z corrected for 5 cm robot stand | DONE (2026-04-23) |
| wrist_cam TF Y sign fixed (−0.14 toward tray) | DONE (2026-04-24) |
| FK at SCAN_JOINTS verified: tool0=(−0.174,0.583,0.917) | DONE (2026-04-24) |
| wrist_cam TF Y calibrated: −0.14 → −0.065 (near-edge test, residual 4 mm) | DONE (2026-04-27) |
| Robot velocity scaling reduced: 0.3 → 0.15 (accel 0.2 → 0.1) in grasp_executor | DONE (2026-04-27) |
| FTS (3 cm) added to URDF mount: ur_to_robotiq_mount z 0.02 → 0.05 (ur.urdf + xacro) | DONE (2026-04-29) |
| GRASP_Z_MIN = 0.190 m clamp added in grasp_executor — palm ≥ 2 cm above tray | DONE (2026-04-29) |
| TOOL0_TO_PALM_Z = 0.050 constant; palm offset in _attach_pick_object corrected | DONE (2026-04-29) |
| gz_obj_min = obj_cz + TOOL0_TO_FINGER_BASE_Z floor — finger base at object centre (real hw only) | DONE (2026-04-29) |
| GRIPPER_PALM_HEIGHT = 0.160 m added; TOOL0_TO_FINGER_BASE_Z = 0.210 m; GRASP_Z_MIN = 0.350 m | DONE (2026-04-29) |

### Pending
| Item | What's needed |
|------|--------------|
| Full pick-and-place test | All geometry now from tape measure — need clean end-to-end run |
| Gripper connectivity | Robotiq 3F at 192.168.1.105 activation timing out |
| N=20 sim + N=20 real trials | Final sim2real evaluation |

---

## Launch Commands

### Simulation (unchanged — no hardware needed)
```bash
pkill -f rviz2; pkill -f ros2; sleep 2
cd ~/research_ws/ur10_pick_place_ws
source /opt/ros/humble/setup.bash && source install/setup.bash
ros2 launch ur10_pick_place grasp_pipeline.launch.py \
  launch_graspgen_bridge:=true launch_sim_pc:=true sim_pc_object:=tin_can
ros2 topic pub --once /graspgen/trigger std_msgs/msg/Empty "{}"
```

### Real Hardware
```bash
# T1 — UR10 driver (robot must be in Remote Control mode on teach pendant)
ros2 launch ur_robot_driver ur_control.launch.py \
  ur_type:=ur10 robot_ip:=192.168.1.102 use_fake_hardware:=false \
  kinematics_params_file:=$HOME/robot_calibration.yaml

# T2 — Main stack (no cameras — cameras are in T3)
ros2 launch ur10_pick_place grasp_pipeline.launch.py \
  launch_graspgen_bridge:=true launch_sim_pc:=false \
  use_rviz:=true real_hardware:=true \
  launch_env_cam:=false launch_wrist_cam:=false

# T3 — Both cameras + SAM2 (run only when picking)
~/research_ws/ur10_pick_place_ws/src/ur10_pick_place/scripts/pick.sh

# Per-pick workflow (after T3 is running and arm is at home):
#   1. Left-click target object in SAM2 window → green mask appears
#      (yellow "SAM2 PROCESSING..." shown during 2-5 s inference — do not click again)
#   2. Trigger scan + GraspGen:
ros2 topic pub --once /pick/start std_msgs/msg/Empty "{}"
#      → arm moves to scan pose (wrist_cam above object, wrist_2 ±15° L/R tilt, 5 s each)
#      → arm returns home
#      → GraspGen infers on complete fused cloud
#      → grasp_executor picks and places
```

---

## Hardware Connections
```
UR10 control box ──Ethernet──────────────► Jetson eth0  (Jetson IP: 192.168.1.10)
Robotiq 3F       ──Ethernet──────────────► Switch/hub   (Gripper IP: 192.168.1.105)
OAK-D Pro tripod ──(NOT CONNECTED)────────────────────────────── env_cam not in current setup
OAK-D Pro Wide   ──USB-C─────────────────► powered USB3 hub → Jetson  (wrist_cam)
```

## UR10 Teach Pendant Setup (before every real run)
1. Installation → URCaps → External Control → Host IP = 192.168.1.100 (PC) or Jetson IP
2. Load External Control program
3. Mode → **Remote Control**

## Gripper Activation
- Gripper activates automatically when `grasp_executor_node` starts with `real_hardware:=true`
- Deactivates automatically on Ctrl+C / node shutdown
- No separate gripper driver needed — pure Python TCP (Modbus) to 192.168.1.105:502

---

## Scene — Real Hardware Coordinates (world = base_link)

**Trays sit directly on the floor (only the robot is on a 5 cm stand).**
Floor surface is at Z = 0.00 m in world frame (floor collision box centre=−0.05, lz=0.10 → top=0.00).
Left/right are from robot's POV at home (facing +Y): RIGHT = +X, LEFT = −X.
Source: `~/research_ws/Tray_Dim.odt` (tape-measured).

```
pick_tray  (brown cardboard): centre (0.00, 0.655, 0.06)  lx=0.46 ly=0.67 lz=0.12
  ↳ CENTRED on robot: left edge X=-0.23 m (23 cm LEFT), right edge X=+0.23 m (23 cm RIGHT)
  ↳ Centre Y=65.5 cm FORWARD from robot base centre
  ↳ Near edge Y=0.32 m, far edge Y=0.99 m  (0.99 = 0.32 + 0.67 — far edge, NOT centre)
  ↳ H=12 cm; floor at Z=0.00 m → tray top at 0.12 m, centre Z=0.06 m
  ↳ W=46 cm along X axis, L=67 cm along Y axis

place_tray (yellow crate):    centre (-0.4775, 0.662, 0.075)  lx=0.495 ly=0.324 lz=0.15
  ↳ On the LEFT side of the robot (−X direction)
  ↳ L=49.5 cm (X axis, lx) → centre X = −0.4775 m
  ↳ Y=66.2 cm FORWARD from robot base centre
  ↳ H=15 cm; floor at Z=0.00 m → tray top at 0.15 m, centre Z=0.075 m
  ↳ L=49.5 cm along X axis, W=32.4 cm along Y axis

TABLE_TOP_Z = 0.12 m  (pick tray top surface — floor at Z=0, tray H=12 cm)
PLACE_SLOTS (Y-spread inside place_tray):
  slot 0: (-0.4775, 0.512)   slot 1: (-0.4775, 0.662)   slot 2: (-0.4775, 0.812)
```

---

## Architecture Decisions
- **No cuRobo. No NVBlox.** MoveIt2+OMPL handles all collision avoidance.
- **real_hardware=true**: geometry estimated from /env_cam/points cloud; Robotiq TCP; GraspGen pose used directly.
- **real_hardware=false (sim)**: position snap to SCENE_PICK_OBJECTS; sim JTC gripper; auto-trigger.
- **Camera MX IDs fixed**: both cameras always come up on correct topics regardless of plug order.
- **Gripper lifecycle**: activate on node start, deactivate on node stop — safe, no runaway state.
- **Scan motion**: only wrist_2 tilts ±15° for L/R views — arm base does not move, avoiding re-planning.
- **Workspace bounds**: arm-reach sphere (1.5 m radius) with gz ∈ (0, 0.8) — no directional bias.

---

## Key Files
| File | Purpose |
|------|---------|
| `src/ur10_pick_place/launch/grasp_pipeline.launch.py` | Main launch file (all flags) |
| `src/ur10_pick_place/config/oakd_env.yaml` | env_cam config (MX ID fixed) |
| `src/ur10_pick_place/config/oakd_wrist.yaml` | wrist_cam config (MX ID fixed) |
| `/tmp/oakd_viewer.py` | depthai v3 live viewer — RGB+Depth for both cameras (run: `python3 /tmp/oakd_viewer.py`) |
| `src/ur10_pick_place/scripts/planning_scene_setup.py` | Tray + object collision scene |
| `src/ur10_pick_place/scripts/sim_object_pc_publisher.py` | Sim PC → /env_cam/points |
| `src/ur10_pick_place/scripts/sam2_segmentation_node.py` | SAM2 click→mask→/env_cam/points |
| `src/grasp_executor/grasp_executor/grasp_executor_node.py` | 8-step pick-and-place |
| `src/grasp_executor/grasp_executor/robotiq_3f_gripper.py` | Robotiq TCP controller |
| `src/grasp_executor/grasp_executor/graspgen_bridge_node.py` | GraspGen inference bridge |
| `~/research_ws/segment-anything-2/checkpoints/sam2.1_hiera_small.pt` | SAM2 checkpoint (176MB) |

---

## Training Status (v3, 227 objects)
- ✅ Generator v3: ~/GraspDataGen/training_logs/robotiq_3f_gen_v3/epoch_500.pth
- ✅ Disc GT v3: ~/GraspDataGen/training_logs/robotiq_3f_disc_v3/epoch_500.pth
- ✅ Disc On-Policy v3: ~/GraspDataGen/training_logs/robotiq_3f_disc_onpolicy_v3/epoch_500.pth

---

## Bug Fixes Log
| Bug | Root Cause | Fix | Date |
|-----|-----------|-----|------|
| Lift failed error 99999 | wrist_2_link missing from GRIPPER_TOUCH_LINKS + palm_frame_z clamped | Added wrist_2_link; removed max(0,…) clamp | 2026-04-09 |
| Lift failed cycle 2 | tin_can left at place; SCENE_PICK_OBJECTS missing from global ACM | _reset_world_scene() + ACM fix | 2026-04-09 |
| Arm through blue object during place | Distractors in place_allow → OMPL ignored them | Restore distractor ACM=False before step 6 | 2026-04-09 |
| SAM2 torchvision nms crash | torchvision 0.20.1 binary-incompatible with Jetson torch nv24.08 | try/except around register_fake("torchvision::nms") | 2026-04-13 |
| SAM2 from_pretrained with local ckpt | model_id=None not supported | Use build_sam2(cfg, ckpt) + SAM2ImagePredictor(model) | 2026-04-13 |
| SAM2 iopath/portalocker missing | Not installed | pip3 install --no-deps iopath portalocker | 2026-04-13 |
| grasp_executor hardcoded to tin_can | SCENE_PICK_OBJECTS/snap/DISTRACTOR was sim-only | real_hardware param: geometry from /env_cam/points cloud | 2026-04-13 |
| depthai v3 Camera has no setBoardSocket | v3 API changed — use build(socket) instead | cam.build(dai.CameraBoardSocket.CAM_A) | 2026-04-13 |
| depthai v3 no XLinkOut node | v3 removed XLinkOut — use createOutputQueue() on output directly | output.createOutputQueue() | 2026-04-13 |
| StereoDepth crash: width not multiple of 16 | ISP outputs 1352px wide, StereoDepth requires multiple of 16 | stereo.setOutputSize(1280, 720) | 2026-04-13 |
| Arm collision during pre-grasp approach | ACM=True for pick_tray set globally before step 1b — OMPL routed arm through tray | ACM for trays now set only just before step 3 (grasp descent); trays kept as obstacles during approach | 2026-04-16 |
| IK fails / arm goes to extreme position | (1) expected_pan used wrong formula assuming 90° world→base rotation that does NOT exist in real hardware; (2) seed wrist_2=0.0 caused KDL to find wrong arm branch; (3) no lift validity check allowed backward-arm solutions | (1) expected_pan=atan2(gy,gx) for identity TF; (2) seed wrist_2=-1.5708; (3) lift<-0.3 check; (4) 4th IK attempt with SCAN_JOINTS seed | 2026-04-23 |
| GraspGen pose rejected as "out of workspace" | Workspace check used +X-only bounds (0.20<gx<1.00) — rejected valid poses at negative X (real tray at x≈-0.06) | Replaced with arm-reach sphere: reach²<1.5² and gz∈(0,0.8) | 2026-04-23 |
| Arm base moved during scan L/R | SCAN_JOINTS_L/R varied shoulder_pan ±15°, moving entire arm base | Changed to wrist_2 ±15° — only wrist moves, base stays still | 2026-04-23 |
| SAM2 window appeared frozen during inference | No visual feedback during 2-5 s CUDA inference; user clicked multiple times | Added yellow "SAM2 PROCESSING..." overlay; cv2.waitKey(1) at 30 Hz in background thread | 2026-04-23 |
| Pre-grasp motion timeout at 10s | allowed_execution_duration_scaling=2.0 too small at low UR speed slider | Increased to scaling=10.0, margin=30.0 | 2026-04-16 |
| Green cylinder in RViz (real_target) | Correct behavior — object geometry estimated from fused point cloud and added to MoveIt scene | Not a bug | 2026-04-16 |
| Object spawning in front of robot (Y≈0.57) not on tray | Camera TF Y sign wrong: (0,+0.10,−0.04) moved camera 10 cm TOWARD robot (world −Y) instead of toward tray; same click now back-projects to Y≈0.90 (on tray) | Changed pick.sh TF to (0,−0.14,−0.04) — 14 cm in tool0 −Y = world +Y (toward tray) | 2026-04-24 |
| Object centroid Y systematically +75 mm too far forward | TF y=−0.14 over-estimated camera forward offset; calibrated via near-edge test: object (D=17 cm) against near tray edge (Y=0.320 m), expected centroid Y=0.405 m, measured=0.480 m → error=+75 mm | Changed pick.sh TF to (0,−0.065,−0.04) — residual after fix: 4 mm ✓ | 2026-04-27 |
| IK failed all 4 attempts (pan=192.6° vs expected 118.7°) | Direct consequence of wrong object Y=0.568 → GraspGen pose at wrong location; resolved by TF fix above | Fixed by camera TF fix | 2026-04-24 |
| Gripper colliding with pick tray during grasp | FTS (3 cm) between UR10 flange and Robotiq 3F mount was NOT in URDF. `ur_to_robotiq_mount` joint had z=0.02 m (adapter only); gripper descended 3 cm too low into tray. Also no minimum Z floor on GraspGen output | (1) Fixed ur.urdf + xacro: mount z 0.02 → 0.05 m; (2) Added GRASP_Z_MIN=0.190 m clamp on GraspGen pose Z in grasp_executor; (3) Updated TOOL0_TO_PALM_Z=0.050 in _attach_pick_object | 2026-04-29 |
| Fingers reaching below tray — GRASP_Z_MIN=0.190 insufficient | robotiq_palm URDF link is the TOP of the gripper body. Palm body is 16 cm tall. Finger base is 5+16=21 cm below tool0. Old code only added 5 cm (tool0→palm link), leaving fingers 16 cm below object centre → into tray. Fix: use TOOL0_TO_FINGER_BASE_Z=0.210 m in all Z clamps. GRASP_Z_MIN raised from 0.190 → 0.350 m. gz_obj_min = obj_cz + 0.210 m. ROLLBACK: revert GRIPPER_PALM_HEIGHT=0.160, TOOL0_TO_FINGER_BASE_Z=0.210, GRASP_Z_MIN=0.350 back to original values and remove the gz_obj_min block | 2026-04-29 |
| Place motion failed — floor collision with attached object | place_z = TABLE_TOP_Z + obj_height was wrong. palm_frame_z (grasp offset) was ignored → at place, object bottom landed at -0.10 m inside floor. Also SAM2 over-segmented whole tray (h=0.360). Fix: place_z = gz - obj_cz + PLACE_TRAY_TOP_Z + obj_height/2 preserves palm_frame_z; added PLACE_TRAY_TOP_Z=0.150 constant. Same formula used for sim. | 2026-04-30 |
| SCAN_JOINTS outdated | Previous values (pan=90.52°) from 2026-04-24 teach pendant; new physically measured session (2026-04-30) gave pan=75.19°, shoulder=-101.06°, elbow=82.69°, w1=-73.32°, w2=-89.58°, w3=-14.12°. L/R tilt joints updated accordingly | 2026-04-30 |

---

## Next Steps
1. ✅ Tray positions measured (Tray_Dim.odt) — planning_scene_setup.py + PLACE_SLOTS updated
2. ✅ env_cam removed from pipeline — wrist_cam only; env_cam_tf removed from launch file
3. ✅ TABLE_TOP_Z = 0.12 m (floor at Z=0, pick tray H=12 cm; trays on floor, only robot on 5 cm stand)
4. ✅ world_z_min_m = 0.12 m in sam2_segmentation_node (filters below pick tray top surface)
5. ✅ wrist_cam TF fixed sign: (0,−0.14,−0.04) — camera back-projects to tray (2026-04-24)
6. ✅ wrist_cam TF Y calibrated: (0,−0.065,−0.04) — near-edge test residual 4 mm (2026-04-27)
7. ⏳ Full real pick-and-place test end-to-end — TF calibrated, ready to run
8. ⏳ N=20 sim + N=20 real trials → sim2real evaluation
