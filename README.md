# Deep Learning-Based Grasp Pose Detection on Point Clouds and Manipulating the Object using Generated Grasp Pose
### Sim-to-Real Manipulation with UR10 + Robotiq 3F + OAK-D Pro Wide

---

## Overview

This project implements NVIDIA's **GraspGen** on a **UR10 robot arm + Robotiq 3F gripper + OAK-D Pro Wide wrist camera** running on a **Jetson AGX Orin**. The system detects grasp poses on point clouds and executes pick-and-place in both simulation (RViz/MoveIt2) and real hardware.

**Key contribution:** Adapting GraspGen (originally tested on 2-finger grippers and A100 GPUs) to a 3-finger gripper on edge compute, with sim-to-real validation on a cluttered pick scene (FetchBench-style, 6 objects).

---

## Hardware

| Component | Model | Details |
|-----------|-------|---------|
| Robot Arm | UR10 | IP: 192.168.1.102 |
| Gripper | Robotiq 3F | Ethernet Modbus TCP — IP: 192.168.1.105 |
| Wrist Camera | OAK-D Pro Wide | USB-C to Jetson, MX ID: 14442C10715AD4D200 |
| Compute | Jetson AGX Orin 64GB | IP: 192.168.1.10 |

---



## Software Stack

- **ROS2 Humble** + MoveIt2 + OMPL (RRTConnect)
- **GraspGen** (NVIDIA, proprietary research license) — Jetson-adapted fork in `research_ws/GraspGen/`
  - Original: [NVlabs/GraspGen](https://github.com/NVlabs/GraspGen) · Adapted for Robotiq 3F + Jetson AGX Orin
  - © 2025 NVIDIA Corporation. Used for academic research only. See [Acknowledgements](#acknowledgements).
- **GraspDataGen** (NVIDIA, proprietary research license) — Training pipeline in `research_ws/GraspDataGen_src/`
  - Original: [NVlabs/GraspDataGen](https://github.com/NVlabs/GraspDataGen) · Adapted for Robotiq 3F + custom dataset
  - © 2025 NVIDIA Corporation. Used for academic research only. See [Acknowledgements](#acknowledgements).
- **SAM2** (Meta AI, Apache 2.0) — installed as package: `pip install git+https://github.com/facebookresearch/segment-anything-2.git`
  - Original: [facebookresearch/segment-anything-2](https://github.com/facebookresearch/segment-anything-2)
  - Checkpoint: `sam2.1_hiera_small.pt` (176 MB, download separately from Meta)
  - Custom integration: `ur10_pick_place/scripts/sam2_segmentation_node.py`
- **Robotiq 3F** — Pure Python TCP/Modbus controller (no ROS driver needed)

---

## Trained Models (v3, 227 objects)

Models are trained on GraspDataGen data for the Robotiq 3F gripper.
Weights are stored locally (not in this repo — too large for GitHub):

| Model | Path | Epochs |
|-------|------|--------|
| Generator v3 | `~/GraspDataGen/training_logs/robotiq_3f_gen_v3/epoch_500.pth` | 500 |
| Discriminator GT v3 | `~/GraspDataGen/training_logs/robotiq_3f_disc_v3/epoch_500.pth` | 500 |
| Disc On-Policy v3 | `~/GraspDataGen/training_logs/robotiq_3f_disc_onpolicy_v3/epoch_500.pth` | 500 |

---

## Repository Structure

```
graspgen-sim2real-ur10/
├── README.md                            ← You are here
├── .gitignore
│
├── docs/
│   ├── AnushkaSinghania_Thesis_240614.pdf   ← Full thesis
│
├── research_ws/
│   ├── training_plots/                  ← Training loss/accuracy graphs
│   │
│   ├── GraspGen/                        ← GraspGen inference (Jetson-adapted fork)
│   │   ├── grasp_gen/                   ← Core inference library
│   │   ├── config/grippers/             ← Robotiq 3F gripper config (robotiq_3f.yaml)
│   │   ├── scripts/                     ← Training + eval scripts
│   │   └── docker/                      ← Docker build files
│   │
│   ├── GraspDataGen_src/                ← GraspDataGen training pipeline (source only)
│   │   ├── scripts/                     ← Data generation + training scripts
│   │   ├── bots/                        ← Robot USD models (Robotiq 3F, Franka, etc.)
│   │   ├── docker/                      ← Isaac Sim Docker setup
│   │   └── docs/                        ← GraspDataGen API docs
│   │
│   │   (SAM2 is installed as a package — see Installation below)
│   │
│   └── ur10_pick_place_ws/src/
│       ├── ur10_pick_place/             ← Main package: launch files, config, scripts
│       │   ├── launch/grasp_pipeline.launch.py   ← Master launch file
│       │   ├── scripts/
│       │   │   ├── sam2_segmentation_node.py     ← Click→SAM2 mask→point cloud
│       │   │   ├── sim_object_pc_publisher.py    ← Sim point cloud publisher
│       │   │   ├── planning_scene_setup.py       ← MoveIt collision scene
│       │   │   └── pick.sh                       ← Real hardware camera launch
│       │   ├── config/                           ← Controller + camera YAML configs
│       │   └── urdf/                             ← UR10 + gripper + camera URDF
│       │
│       ├── grasp_executor/              ← Core pick-and-place execution
│       │   ├── grasp_executor_node.py   ← 8-step pick-and-place state machine
│       │   ├── graspgen_bridge_node.py  ← GraspGen inference → ROS2 pose
│       │   └── robotiq_3f_gripper.py    ← Robotiq 3F TCP/Modbus controller
│       │
│       ├── ur10_camera_gripper_moveit_config/   ← MoveIt2 config (UR10 + camera + gripper)
│       ├── linkattacher_msgs/           ← Sim object attach/detach messages
│       ├── linkattacher_plugin/         ← Gazebo link attach plugin
│       ├── ros2_robotiq_3f_gripper/     ← Robotiq 3F ROS2 description
│       └── ros2_robotiq_gripper/        ← Robotiq gripper ROS2 interface
│
└── robotiq_clean/                       ← Robotiq 3F URDF + meshes + Isaac Sim USD
    ├── robotiq_3f_isaac.urdf
    ├── robotiq_3f_clean.usd
    └── meshes/
```

---

## Quick Start

### Simulation

```bash
cd ~/research_ws/ur10_pick_place_ws
source /opt/ros/humble/setup.bash && source install/setup.bash

# Launch full pipeline
ros2 launch ur10_pick_place grasp_pipeline.launch.py \
  launch_graspgen_bridge:=true launch_sim_pc:=true sim_pc_object:=tin_can

# Trigger grasp
ros2 topic pub --once /graspgen/trigger std_msgs/msg/Empty "{}"
```

### Real Hardware

```bash
# Terminal 1 — UR10 driver (robot must be in Remote Control mode)
ros2 launch ur_robot_driver ur_control.launch.py \
  ur_type:=ur10 robot_ip:=192.168.1.102 use_fake_hardware:=false \
  kinematics_params_file:=$HOME/robot_calibration.yaml

# Terminal 2 — Main stack
ros2 launch ur10_pick_place grasp_pipeline.launch.py \
  launch_graspgen_bridge:=true launch_sim_pc:=false \
  use_rviz:=true real_hardware:=true \
  launch_env_cam:=false launch_wrist_cam:=false

# Terminal 3 — Cameras + SAM2
~/research_ws/ur10_pick_place_ws/src/ur10_pick_place/scripts/pick.sh

# Per-pick: left-click object in SAM2 window, then trigger scan
ros2 topic pub --once /pick/start std_msgs/msg/Empty "{}"
```

---

## Pipeline

```
Wrist Camera (OAK-D Pro Wide)
        ↓  RGB + Depth
SAM2 Segmentation Node  ←── User left-click on object
        ↓  Masked point cloud (3 views, wrist_2 ±15° tilt)
GraspGen Bridge Node    ←── Generator v3 + Discriminator v3
        ↓  /graspgen/grasp_pose  (PoseStamped, world frame)
Grasp Executor Node
        ↓  IK → MoveIt2/OMPL plan → UR10 joints
Robotiq 3F Gripper      ←── TCP/Modbus to 192.168.1.105
        ↓
Pick → Lift → Place → Home
```

---

## Results

### Dataset & Training
| Metric | Value |
|--------|-------|
| Training objects (Objaverse) | 227 |
| Positive grasp annotations | 9,685 |
| Training epochs (all models) | 500 |
| Generator total loss reduction | ~75% |
| GT Discriminator AP (train / valid) | 0.995 / 0.982 |
| On-Policy Discriminator AP (train / valid) | 0.970 / 0.988 |

### Inference on Jetson AGX Orin (Table 11)
| Metric | GT Discriminator | On-Policy Discriminator |
|--------|-----------------|------------------------|
| Mean warm inference time (s) | 1.83 | 1.87 |
| Grasps sampled per inference | 100 | 100 |
| Mean top discriminator confidence | 0.994 | 0.997 |
| Valid Average Precision | 0.982 | 0.988 |

### Simulation Validation (Table 15)
| Metric | Value |
|--------|-------|
| Sequential pick-and-place attempts | 20 |
| Successes | 20 |
| Success rate | **100%** |
| IK failures | 0 |
| Motion planning failures | 0 |

### Real-Robot Grasp Success — 80 Trials (Table 13)
| Condition | Attempts | Successes | Success Rate |
|-----------|----------|-----------|--------------|
| Isolated objects | 40 | 29 | **72.5%** |
| Cluttered scene | 40 | 24 | **60.0%** |
| **Overall** | **80** | **53** | **66.3%** |

**Failure mode breakdown:** IK failure 5.0% · Motion planning failure 3.75% · Drop during lift 16.25% · Drop during transport 8.75%

### Comparison with Existing Methods (Table 16)
| System | Gripper | Grasp Success |
|--------|---------|---------------|
| GraspGen best reported | Robotiq 2F-140 | 81.3% |
| GraspGen (FetchBench task) | Robotiq 2F-140 | 65.3% |
| AnyGrasp | Two-Finger | 63.7% |
| M2T2 | Two-Finger | 52.6% |
| DexDiffuser (real robot) | Allegro Hand | 68.9% |
| **Proposed — isolated (N=40)** | **Robotiq 3F** | **72.5%** |
| **Proposed — cluttered (N=40)** | **Robotiq 3F** | **60.0%** |
| **Proposed — overall (N=80)** | **Robotiq 3F** | **66.3%** |

The proposed system (72.5% isolated) exceeds the GraspGen FetchBench task result (65.3%) and outperforms AnyGrasp (63.7%) and M2T2 (52.6%), despite using a smaller training set (227 vs 8,515 objects), FCL-free labelling, and an edge GPU platform.

---

## Publication

A research paper based on this work was presented at the **1st International Conference on Systems Approach in Control Architecture and Design (SACAD-2025)**, IIT Hyderabad, December 21–23, 2025.

> *"Generative Deep Learning Models for Grasp Pose Detection under Occluded and Partial Point Clouds: A Comprehensive Review"*  
> Anushka Singhania — SACAD-2025, IIT Hyderabad

---

## Citation / Thesis

```
Singhania, A. (2026). Deep Learning-Based Grasp Pose Detection on Point Clouds
and Manipulating the Object using Generated Grasp Pose. M.Tech Thesis,
DIAT (DU), Pune.
```

Full thesis: [`docs/AnushkaSinghania_Thesis_240614.pdf`](docs/AnushkaSinghania_Thesis_240614.pdf)

---

## Acknowledgements

This project builds upon the following repositories. All credit for the original implementations belongs entirely to their respective authors. This repository exists solely for academic research and thesis documentation purposes.

---

### 1. GraspGen — NVIDIA Research

| | |
|---|---|
| **Repository** | [NVlabs/GraspGen](https://github.com/NVlabs/GraspGen) |
| **Authors** | Murali, A., Sundaralingam, B., Chao, Y.-W., Yamada, J., Yuan, W., Carlson, M., Ramos, F., Birchfield, S., Fox, D., & Eppner, C. |
| **Paper** | *GraspGen: A Diffusion-based Framework for 6-DOF Grasping with On-Generator Training* — [arXiv:2507.13097](https://arxiv.org/abs/2507.13097) |
| **License** | Copyright © 2025, NVIDIA Corporation & affiliates. **All rights reserved.** Proprietary research license. For commercial use: [NVIDIA Research Licensing](https://www.nvidia.com/en-us/research/inquiries/). |
| **Usage here** | Academic/research only. All original NVIDIA copyright notices and headers are retained in `research_ws/GraspGen/`. |

**Modifications made in this fork:**
- Added Robotiq 3F gripper YAML configuration (`config/grippers/robotiq_3f.yaml`)
- Adapted inference pipeline for Jetson AGX Orin (ARM64, JetPack 6, CUDA 12.2)
- Integrated ROS2 Humble bridge node (`grasp_executor/graspgen_bridge_node.py`) for real-time grasp pose publishing via `/graspgen/grasp_pose`

---

### 2. GraspDataGen — NVIDIA Research

| | |
|---|---|
| **Repository** | [NVlabs/GraspDataGen](https://github.com/NVlabs/GraspDataGen) |
| **Authors** | NVIDIA Research (companion pipeline to GraspGen — cite the GraspGen paper above) |
| **License** | Copyright © 2025, NVIDIA Corporation & affiliates. **All rights reserved.** Proprietary research license. Contributions to the original repository are not accepted per NVIDIA policy. |
| **Usage here** | Academic/research only. All original NVIDIA copyright notices and headers are retained in `research_ws/GraspDataGen_src/`. |

**Modifications made in this fork:**
- Added Robotiq 3F gripper USD model and robot configuration (`bots/robotiq_3f/`)
- Adapted training scripts for a custom 227-object Objaverse subset
- Modified grasp labelling pipeline to operate without FCL collision checking (replaced with Trimesh due to ARM64 compatibility issues on Jetson)

---

### 3. Segment Anything Model 2 (SAM2) — Meta AI Research

| | |
|---|---|
| **Repository** | [facebookresearch/segment-anything-2](https://github.com/facebookresearch/segment-anything-2) |
| **Authors** | Ravi, N., Gabeur, V., Hu, Y.-T., et al. — Meta AI Research |
| **Paper** | *SAM 2: Segment Anything in Images and Videos* — [arXiv:2408.00714](https://arxiv.org/abs/2408.00714) |
| **License** | **Apache 2.0** — free to use, modify, and redistribute with attribution. |
| **Usage here** | Installed as a package (`pip install git+https://github.com/facebookresearch/segment-anything-2.git`). The `research_ws/sam2_source/` folder contains unmodified source files kept for local reference. No changes were made to the core SAM2 library. |

**Integration in this project:**
- Custom ROS2 node (`ur10_pick_place/scripts/sam2_segmentation_node.py`) wraps SAM2's image predictor for single-click object segmentation → masked point cloud generation
- Model checkpoint used: `sam2.1_hiera_small.pt` (download separately from [Meta's model card](https://github.com/facebookresearch/segment-anything-2#model-description))
