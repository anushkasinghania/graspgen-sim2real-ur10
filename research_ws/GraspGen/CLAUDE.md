# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Status - Jetson Setup

### Environment
- Hardware: Jetson AGX Orin 64GB, Ubuntu 22.04, JetPack 6.1
- Python 3.10, PyTorch 2.5 (CUDA 12.6, sm_87), pointnet2_ops compiled for aarch64
- `scene_synthesizer` NOT installed; `python-fcl` NOT installable on ARM64
- `LD_LIBRARY_PATH` includes cusparselt path

### Paths
- Code: `~/research_ws/GraspGen/`
- Dataset: `~/GraspDataGen/graspgen_dataset/grasp_data/robotiq_3f/` (webdataset, `shard_000.tar`)
- Objects: `~/GraspDataGen/objects/`
- Splits: `~/GraspDataGen/graspgen_dataset/splits/robotiq_3f/` (8 train objects, 3 valid)
- Gripper meshes: `~/robotiq_clean/meshes/collision/`
- H5 cache: `/tmp/graspgen_cache/robotiq_3f/cache_train_mesh_dis.h5`

### Completed Steps
- Generator trained: `~/GraspDataGen/training_logs/robotiq_3f_gen/epoch_500.pth` (loss 2.2→1.05)
- Discriminator trained (GT data only): `~/GraspDataGen/training_logs/robotiq_3f_disc/epoch_500.pth`
- On-policy data generated: `scripts/generate_onpolicy_data.py` — 300 grasps/object, 1302 pos + 1698 neg written into H5 cache
- Discriminator retrained (on-policy): `~/GraspDataGen/training_logs/robotiq_3f_disc_onpolicy/epoch_500.pth`

### Fixes Applied
- `radius 0.03→0.15` in `grasp_gen/dataset/dataset_utils.py` line 252
- `dataset.py` line 1307: numpy→torch conversion before unsqueeze
- `dataset.py`: tensor unwrap fix for grasps
- `data.discriminator_ratio=[0.25,0.20,0.00,0.05,0.0,0.25,0.25]` for on-policy training (indices 5=pos_onpolicy, 6=neg_onpolicy)
- `neg_hncolliding=0` always — requires FCL which is not installable on ARM64
- `hammer` and `mailbox` denylisted (0 positive grasps) — expected
- Cache rebuild trap: training deletes cache if `denylist_mesh_dis.json` is missing. Workaround: `echo '{}' > /tmp/graspgen_cache/robotiq_3f/denylist_mesh_dis.json` before starting training
- `generate_onpolicy_data.py` uses `trimesh.proximity.closest_point` (no FCL) instead of `trimesh.collision.CollisionManager`

### On-Policy Labelling Method (`scripts/generate_onpolicy_data.py`)
FCL-free — uses TCP (grasp translation) proximity to object mesh surface:
- **Positive**: TCP within `clip(obj_radius * 0.5, 1cm, 5cm)` of surface AND pre-grasp TCP (backed off 5cm along Z) not blocking the object
- **Negative**: everything else
To re-run: `python3 scripts/generate_onpolicy_data.py --num_grasps 300`

### Cache Note
After any training run that rebuilds the cache, re-run `generate_onpolicy_data.py` to restore on-policy grasps (training rebuild wipes them). Always pre-create the denylist stub to prevent rebuilds:
```bash
echo '{}' > /tmp/graspgen_cache/robotiq_3f/denylist_mesh_dis.json
```

### Next Step
Inference / evaluation using the on-policy discriminator (v1 models, 8 objects):
- Generator: `~/GraspDataGen/training_logs/robotiq_3f_gen/epoch_500.pth`
- Discriminator: `~/GraspDataGen/training_logs/robotiq_3f_disc_onpolicy/epoch_500.pth`

---

## v3 Dataset — Full 227-Object Retraining (2026-03-27)

### ✅ ALL STEPS COMPLETE (as of 2026-03-30)

| Step | Model | Checkpoint | Status |
|------|-------|-----------|--------|
| Generator | `robotiq_3f_gen_v3` | `epoch_500.pth` | ✅ Done |
| Disc GT | `robotiq_3f_disc_v3` | `epoch_500.pth` | ✅ Done |
| On-policy data | `generate_onpolicy_data.py` | — | ✅ Done |
| Disc On-Policy | `robotiq_3f_disc_onpolicy_v3` | `epoch_500.pth` | ✅ Done |

**Active models for all future inference:**
- Generator: `~/GraspDataGen/training_logs/robotiq_3f_gen_v3/epoch_500.pth`
- Discriminator: `~/GraspDataGen/training_logs/robotiq_3f_disc_onpolicy_v3/epoch_500.pth`

TensorBoard (per run):
```bash
tensorboard --logdir ~/GraspDataGen/training_logs/robotiq_3f_gen_v3/        --port 6006
tensorboard --logdir ~/GraspDataGen/training_logs/robotiq_3f_disc_v3/       --port 6007
tensorboard --logdir ~/GraspDataGen/training_logs/robotiq_3f_disc_onpolicy_v3/ --port 6008
```

---

## ⚡ Immediate Priorities (Post-Training)

- [x] Generate combined training graphs (all 3 v3 runs)
- [x] Create training documentation file
- [ ] Generate individual TensorBoard graphs for on-policy discriminator v3 (port 6008)
- [x] Run offline inference on real OAK-D point cloud (see Phase 1 below)
- [ ] Phase 1.5: Add table plane removal + object isolation (see below)

---



### New Dataset
- Transferred from x86: `~/GraspDataGen/graspgen_dataset_v3/` (227 objects, 9685 positive grasps)
- Meshes: `~/GraspDataGen/objects_v3/` (flat `.obj`/`.usd` files)
- Splits: `graspgen_dataset_v3/splits/robotiq_3f/` — 180 train, 45 valid
- Grasp data: `graspgen_dataset_v3/grasp_data/robotiq_3f/` (228 JSON files + `uuid_index.json`)

### Fix: map_uuid_to_path.json
`objects_v3` has flat files (no subdirs) but the code expects `map_uuid_to_path.json`.
Generated it with: `python3 -c "import os,json; d='/home/ubuntu/GraspDataGen/objects_v3'; m={f[:-4]:f for f in os.listdir(d) if f.endswith('.obj')}; json.dump(m,open(d+'/map_uuid_to_path.json','w'),indent=2)"`

### v3 Generator Training
- Log dir: `~/GraspDataGen/training_logs/robotiq_3f_gen_v3/`
- Cache: `/tmp/graspgen_cache_v3/robotiq_3f/` (denylist uses `denylist_meshandpc_gen.json`, NOT `denylist_mesh_dis.json`)
- 92/180 train objects in cache (rest denylisted — `scene_synthesizer` absent, as expected)
- **Fix**: must pass `discriminator.gripper_name=robotiq_3f` explicitly — default is `franka_panda` and an assertion fires otherwise
- Training command (nohup, background):
```bash
cd ~/research_ws/GraspGen/scripts && nohup python3 train_graspgen.py \
  train.model_name=diffusion \
  data.root_dir=/home/ubuntu/GraspDataGen/graspgen_dataset_v3/splits/robotiq_3f \
  data.object_root_dir=/home/ubuntu/GraspDataGen/objects_v3/ \
  data.grasp_root_dir=/home/ubuntu/GraspDataGen/graspgen_dataset_v3/grasp_data/robotiq_3f/ \
  data.gripper_name=robotiq_3f \
  data.dataset_version=v2 \
  data.dataset_cls=ObjectPickDataset \
  data.cache_dir=/tmp/graspgen_cache_v3/ \
  data.num_grasps_per_object=100 \
  data.prob_point_cloud=0.5 \
  diffusion.gripper_name=robotiq_3f \
  train.log_dir=/home/ubuntu/GraspDataGen/training_logs/robotiq_3f_gen_v3/ \
  train.num_epochs=500 \
  "data.discriminator_ratio=[0.50,0.45,0.00,0.05,0.0,0.0,0.0]" \
  > ~/GraspDataGen/training_logs/robotiq_3f_gen_v3/train.log 2>&1 &
```
- Progress bar uses `\r`, no loss in `train.log`. Monitor via TensorBoard:
  `tensorboard --logdir ~/GraspDataGen/training_logs/robotiq_3f_gen_v3/`
- Checkpoints every 10 epochs; ~2.5 min/10 epochs on Jetson AGX Orin

### v3 On-Policy Pipeline
Automated 3-step pipeline script: `~/GraspDataGen/run_onpolicy_v3.sh`
Log: `~/GraspDataGen/training_logs/onpolicy_pipeline_v3.log`

Steps:
1. **Disc GT training** → `robotiq_3f_disc_v3/` (discriminator_ratio=[0.50,0.45,0.00,0.05,0,0,0])
2. **generate_onpolicy_data.py** → writes on-policy grasps into `cache_train_mesh_dis.h5` using v3 gen checkpoint
3. **Disc on-policy training** → `robotiq_3f_disc_onpolicy_v3/` (discriminator_ratio=[0.25,0.20,0.00,0.05,0,0.25,0.25])

Critical: recreate `denylist_mesh_dis.json` stub before step 3 — otherwise training rebuilds cache and wipes on-policy grasps.

### Resuming After Interruption

**Cache warning**: `/tmp/graspgen_cache_v3/` is wiped on reboot. Always recreate stub first:
```bash
mkdir -p /tmp/graspgen_cache_v3/robotiq_3f
echo '{}' > /tmp/graspgen_cache_v3/robotiq_3f/denylist_mesh_dis.json
```
If `/tmp` is fully gone, disc cache rebuilds automatically (~2 min) but **on-policy grasps are lost** — must rerun Step 2 before Step 3.

**Resume Step 1 (Disc GT)** — add `train.checkpoint=.../robotiq_3f_disc_v3/last.pth` to the training command. Epoch count is stored in the checkpoint, training resumes from where it left off.

**Resume Step 3 (Disc on-policy)** — same, point to `robotiq_3f_disc_onpolicy_v3/last.pth`.

**Step 2 (generate_onpolicy_data.py)** — reruns from scratch, safe to rerun if cache is intact.

**Full resume script** (run after reboot if pipeline was interrupted):
```bash
# 1. Restore cache stub
mkdir -p /tmp/graspgen_cache_v3/robotiq_3f
echo '{}' > /tmp/graspgen_cache_v3/robotiq_3f/denylist_mesh_dis.json

# 2. Check which step was interrupted, then resume:
#    Step 1 incomplete → add train.checkpoint to disc GT command in run_onpolicy_v3.sh
#    Step 2 incomplete → rerun generate_onpolicy_data.py directly
#    Step 3 incomplete → add train.checkpoint to disc on-policy command in run_onpolicy_v3.sh
```

### Training Speed (Disc, Jetson AGX Orin)
- ~4 min per 10 epochs
- 500 epochs total ≈ ~3.3 hrs per disc training run

---

## Real Robot Integration Roadmap

> **NOTE**: The previous `ur10_pick_place_ws` was patched together and is NOT usable.
> Problems: UR10 URDF broken (arm body missing), Robotiq 3F floating disconnected from arm,
> robot never spawned in Gazebo, wrong cameras (RealSense instead of OAK-D Wide/Pro).
> **Do NOT reuse it.** Follow the phases below from scratch.

### Actual Hardware
- **Robot arm**: UR10 (Universal Robots)
- **Gripper**: Robotiq 3F (3-finger adaptive)
- **Camera 1**: OAK-D Pro — on a tripod, sees the whole workspace from above/side
- **Camera 2**: OAK-D Wide — mounted on the gripper on a 3D-printed slab (wrist camera)
- **Compute**: Jetson AGX Orin 64GB (runs everything: GraspGen inference + ROS2)

---

### Phase 1 — Offline Inference on Real OAK-D Point Cloud
**Status: ✅ PARTIAL (2026-03-31)** — see `docs/phase1_inference_results.md` for full details.

- 87–108 grasps, scores up to 0.997, inference **1.85 sec warm** on Jetson ✓
- Camera: OAK-D Pro → Honeywell USB 3.1 hub → Jetson USB-A
- Scripts: `capture_oakd_pc.py`, `camera_stream.py`, `config/grippers/robotiq_3f_infer.yaml`
- **Done with**: complete point cloud (synthetic/full mesh view) only
- **Not done yet**: partial point cloud (single camera viewpoint — one of the project objectives)
- **Known issue**: grasps on table + empty space → needs Phase 1.5 preprocessing first

**Full testing plan** (see `docs/phase1_inference_results.md`):

| Test | Point Cloud | Environment | Status |
|------|------------|-------------|--------|
| 1a | Complete (mesh) | Single object | ✅ done |
| 1b | Complete (mesh) | Cluttered scene, pick one | ⬜ needs Phase 1.5 first |
| 1c | Partial (OAK-D real view) | Single + Cluttered | ⬜ requires retraining first |

**Note:** v3 model trained on complete point clouds only — partial PC rendering gave errors
during training (`scene_synthesizer` not installable on ARM64) so it was disabled.
Partial PC testing (1c) requires retraining with partial views before it is meaningful.

---

### Phase 1.5 — Table Removal + Object Isolation (prerequisite for 1b and 1c)
**Status: [ ] TODO** — see `docs/phase1_inference_results.md` for full implementation details.

- Add RANSAC table plane removal to `capture_oakd_pc.py`
- Add DBSCAN Euclidean clustering to isolate single object
- `pip install scikit-learn` (only new dependency)
- Expected result: clean partial point cloud of one object → grasps only on that object

---

### Phase 2 — UR10 Arm Bringup (arm only, no gripper)
**Goal**: get the real UR10 arm moving with ROS2 + MoveIt2. No gripper yet.

**What you need to install** (on Jetson):
```bash
sudo apt install ros-humble-ur          # official UR ROS2 driver + description
sudo apt install ros-humble-moveit      # MoveIt2
```

**What to do:**
1. Connect UR10 teach pendant → go to **Setup → URCaps** → enable **External Control** URCap
   - Set "Host IP" to your Jetson's IP address (e.g. 192.168.1.x)
   - Set port 50002
2. On Jetson, launch the driver:
   ```bash
   ros2 launch ur_robot_driver ur_control.launch.py \
     ur_type:=ur10 \
     robot_ip:=<UR10_IP_ADDRESS> \
     launch_rviz:=false
   ```
3. Press "Play" on the teach pendant (starts the external control program)
4. Verify arm connects — you should see joint states:
   ```bash
   ros2 topic echo /joint_states
   ```
5. Launch MoveIt2:
   ```bash
   ros2 launch ur_moveit_config ur_moveit.launch.py ur_type:=ur10
   ```
6. In RViz MotionPlanning panel → drag the end-effector → Plan & Execute
7. Arm should move smoothly. If it does, Phase 2 is done ✅

**Key concept**: `ur_robot_driver` is the official Universal Robots driver. It talks directly
to the robot controller over Ethernet. No simulation involved.

---

### Phase 3 — Add Robotiq 3F Gripper
**Goal**: attach the real Robotiq 3F and control it from ROS2.

**Physical setup**: gripper plugged into UR10 tool flange (power + RS485 via tool connector)

**What you need**:
```bash
# Robotiq ROS2 driver (community package):
sudo apt install ros-humble-robotiq-description  # or clone from github
# Also need: robotiq_3f_driver (ROS2 Humble compatible)
```

**What to do:**
1. Verify the gripper is recognized:
   ```bash
   # The UR10 tool port exposes the gripper on /dev/ttyUSB0 or via URCap
   # Check: ls /dev/ttyUSB*
   ```
2. Launch gripper driver and test open/close manually
3. Add Robotiq 3F URDF as a `xacro:include` attached to `tool0` link of the UR10 URDF
4. Rebuild MoveIt2 config to include the gripper group
5. Test: plan arm motion to pre-grasp pose, then command gripper close

---

### Phase 4 — OAK-D Cameras in ROS2
**Goal**: get point cloud topics flowing from both cameras.

**Install DepthAI ROS2 driver:**
```bash
sudo apt install ros-humble-depthai-ros
# or: git clone https://github.com/luxonis/depthai-ros && colcon build
```

**Camera 1 — OAK-D Pro (tripod, workspace view):**
```bash
ros2 launch depthai_ros_driver camera.launch.py \
  camera_model:=OAK-D-PRO \
  camera_name:=oak_pro
# Point cloud topic: /oak_pro/stereo/points
```

**Camera 2 — OAK-D Wide (on gripper):**
```bash
ros2 launch depthai_ros_driver camera.launch.py \
  camera_model:=OAK-D-W \
  camera_name:=oak_wide
# Point cloud topic: /oak_wide/stereo/points
```

**Add to URDF**: add static transform for OAK-D Pro tripod pose (measure with tape measure),
and add OAK-D Wide as a link attached to the gripper mount in the URDF.

**Verify:**
```bash
ros2 topic hz /oak_pro/stereo/points   # should be ~10-30 Hz
rviz2  # add PointCloud2 display, select topic
```

---

### Phase 5 — Full GraspGen Pipeline on Real Robot
**Goal**: OAK-D Pro sees object → GraspGen gives grasp pose → UR10 picks it up.

**Architecture (all on Jetson):**
```
OAK-D Pro → /oak_pro/stereo/points
                    ↓
         GraspGen bridge node
         (gen_v3 + disc_onpolicy_v3)
                    ↓
         /graspgen/grasp_pose  (PoseStamped)
                    ↓
         Grasp executor node
                    ↓
         MoveIt2 → ur_robot_driver → UR10 arm
                    ↓
         Robotiq 3F driver → gripper close
```

**Update GraspGen bridge to v3 models** (in `graspgen_bridge_node.py`):
```python
# Change these two paths:
GEN_CHECKPOINT  = "~/GraspDataGen/training_logs/robotiq_3f_gen_v3/epoch_500.pth"
DISC_CHECKPOINT = "~/GraspDataGen/training_logs/robotiq_3f_disc_onpolicy_v3/epoch_500.pth"
# Change camera topic:
POINTCLOUD_TOPIC = "/oak_pro/stereo/points"
```

**Steps:**
1. Start all drivers (UR10, Robotiq 3F, OAK-D Pro)
2. Launch MoveIt2
3. Launch GraspGen bridge node
4. Place an object in the workspace
5. Trigger inference: `ros2 topic pub /graspgen/trigger std_msgs/Empty "{}"`
6. Watch the arm move to the grasp pose and close the gripper

---

### Phase 6 — Evaluate & Document
- Test grasp success rate on 5-10 objects (from your dataset)
- Test on unseen objects (generalization)
- Record success rate: # successful picks / # attempts
- Note Jetson inference time (target: <2 sec per grasp)
- Document: Robotiq 3F performance vs original GraspGen (Robotiq 2F on A100)
- This becomes your research contribution

## Installation

```bash
# Install main package
pip install -e .

# Install PointNet++ ops (required for training/inference)
cd pointnet2_ops && pip install --no-build-isolation .

# Additional dependencies
pip install pyrender PyOpenGL transformers tensordict "diffusers==0.11.1" timm "huggingface-hub==0.25.2" scene-synthesizer[recommend]
```

Docker (recommended for GPU environments):
```bash
bash docker/build.sh   # builds CUDA 12.1/12.8 container
bash docker/run.sh     # launches container
```

## Training

All training is done via `scripts/train_graspgen.py` using [Hydra](https://hydra.cc/) config overrides. There is no Makefile or pytest setup.

**Generator training:**
```bash
cd scripts && python3 train_graspgen.py \
  train.model_name=generator \
  data.root_dir=<splits_dir> \
  data.object_root_dir=<objects_dir> \
  data.grasp_root_dir=<grasp_data_dir> \
  data.gripper_name=robotiq_3f \
  train.log_dir=<output_dir> \
  train.num_epochs=500
```

**Discriminator training** (run after generator, uses on-generator training):
```bash
cd scripts && python3 train_graspgen.py \
  train.model_name=discriminator \
  data.load_discriminator_dataset=True \
  train.checkpoint=<path/to/last.pth> \
  train.num_epochs=500
```

Pre-built shell scripts exist in `runs/` for Franka Panda and Robotiq grippers.

**Resuming from checkpoint:** pass `train.checkpoint=<path/to/last.pth>` — the script resumes from the saved epoch.

**Key config parameters** (see `scripts/config.yaml` for full reference):
- `data.cache_dir` — HDF5 dataset cache (speeds up repeated training runs)
- `data.discriminator_ratio` — class balance list for discriminator sampling
- `train.num_gpus` — enables DDP multi-GPU training
- `discriminator.gripper_name` — must match `data.gripper_name`

## Inference / Demo

```bash
# Grasp from segmented object point cloud
python3 scripts/demo_object_pc.py

# Grasp from mesh
python3 scripts/demo_object_mesh.py

# Grasp in cluttered scene
python3 scripts/demo_scene_pc.py

# Full inference pipeline with MeshCat visualization
python3 scripts/inference_graspgen.py
```

**Programmatic API:**
```python
from grasp_gen.grasp_server import GraspGenSampler, load_grasp_cfg

cfg = load_grasp_cfg("path/to/gripper.yml")
sampler = GraspGenSampler(cfg)
grasps, confidences = GraspGenSampler.run_inference(object_pc, sampler, topk_num_grasps=100)
```

## Architecture Overview

GraspGen is a **diffusion-based 6-DOF grasp generation** framework with two sequentially-trained components:

### Generator (`grasp_gen/models/generator.py`)
- `GraspGenGenerator` — diffusion model that generates candidate grasp poses from a point cloud
- Backbone: PointNet++ (`grasp_gen/pointnet/pointnet2.py`) or ViT (`grasp_gen/models/vit.py`) encodes the object point cloud into a latent feature
- Diffusion head uses DDPMScheduler from `diffusers`; optionally uses **compositional schedulers** (separate schedules for position vs. rotation)
- Grasp representations: `r3_6d` (9-dim), `r3_so3` (6-dim), `r3_euler` (6-dim)

### Discriminator (`grasp_gen/models/discriminator.py`)
- `GraspGenDiscriminator` — quality scoring network trained via **on-generator training** (trained on the generator's own outputs, not ground-truth grasps)
- Takes point cloud + candidate grasp as input; outputs a success probability
- Used post-generation to rank and filter grasps (top-k selection)

### Combined inference (`grasp_gen/models/grasp_gen.py`)
- `GraspGen` top-level class orchestrates: encode → diffuse → score → filter

### Data pipeline (`grasp_gen/dataset/`)
- `ObjectPickDataset` — primary dataset class; supports HDF5 caching (`data.cache_dir`)
- `dataset_utils.py` — cache builders; point cloud loading from mesh + partial views
- `renderer.py` — renders partial point clouds from meshes at training time
- Dataset: 57M+ grasps across ~8,500 objects (Objaverse-based)

### Gripper abstraction (`grasp_gen/robot.py`)
- `get_gripper_info()` / `GripperInfo` — loads URDF and YAML config for a gripper
- Gripper configs live in `config/grippers/` (one YAML per gripper)
- Supported grippers: `franka_panda`, `robotiq_2f_140`, `robotiq_3f`, `suction_30mm`

### Utilities
- `grasp_gen/utils/train_utils.py` — optimizer construction, gradient clipping, DDP helpers
- `grasp_gen/utils/math_utils.py` — RT matrix conversions
- `grasp_gen/utils/rotation_conversions.py` / `so3.py` — rotation representation math
- `grasp_gen/dataset/eval_utils.py` — collision checking, evaluation metrics
- `grasp_gen/utils/meshcat_utils.py` — real-time 3D visualization

## Checkpoints

Training saves `last.pth` and `best.pth` to `train.log_dir`. TensorBoard logs go to the same directory. When resuming, only `last.pth` is needed — epoch count is stored inside the checkpoint.
