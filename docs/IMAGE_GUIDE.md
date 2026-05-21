# Image Guide — Where to Add What

All images are referenced in the thesis `docs/AnushkaSinghania_Thesis_240614.pdf`.
Most figures are already in the thesis; this guide tells you which extra images to
add directly to the repo and where to put them.

Upload images to: `docs/images/<category>/`

---

## Folder Structure to Create

```
docs/images/
├── hardware/          ← Real robot setup photos
├── simulation/        ← RViz and Gazebo screenshots
├── pipeline/          ← Architecture and system diagrams
├── results/           ← Quantitative plots, grasp success graphs
└── graspgen/          ← GraspGen output visualizations
```

---

## What Goes Where

### `docs/images/hardware/`
Photos of your actual physical setup. Add these from Google Drive:

| Image | Description | Source |
|-------|-------------|--------|
| `robot_full_setup.jpg` | UR10 arm + Robotiq 3F + tray on table | Google Drive |
| `wrist_cam_mount.jpg` | OAK-D Pro Wide mounted on gripper | Google Drive |
| `gripper_close.jpg` | Robotiq 3F gripper close-up | Google Drive |
| `jetson_setup.jpg` | Jetson AGX Orin compute unit | Google Drive |
| `pick_tray_overhead.jpg` | Pick tray with objects from above | Google Drive |
| `grasp_executing.jpg` | Arm mid-grasp on real hardware | Google Drive |

---

### `docs/images/simulation/`
RViz and Gazebo screenshots. Most are in the thesis already.

| Image | Description | Source |
|-------|-------------|--------|
| `rviz_planning_scene.png` | MoveIt planning scene with trays | Thesis Fig / Drive |
| `rviz_grasp_pose.png` | GraspGen grasp pose arrow on point cloud | Thesis Fig / Drive |
| `sim_pick_sequence.png` | Step-by-step sim pick (approach→grasp→lift→place) | Thesis Fig / Drive |
| `sam2_mask.png` | SAM2 segmentation window with green mask | Drive |
| `pointcloud_fused.png` | Fused 3-view point cloud from wrist cam | Drive |

---

### `docs/images/pipeline/`
System architecture diagrams.

| Image | Description | Source |
|-------|-------------|--------|
| `system_architecture.png` | Full pipeline block diagram (sim + real) | Thesis Fig |
| `hardware_connections.png` | Network topology: UR10 / Gripper / Jetson / Cameras | Thesis Fig |
| `ros2_node_graph.png` | ROS2 node graph (rosgraph.png already in repo root) | `~/rosgraph.png` |
| `graspgen_pipeline.svg` | GraspGen inference pipeline overview | `~/Downloads/graspgen_pipeline_overview.svg` |

---

### `docs/images/results/`
Quantitative evaluation graphs and sim2real comparison.

| Image | Description | Source |
|-------|-------------|--------|
| `training_loss_generator.png` | GraspGen Generator v3 training loss curve | `research_ws/training_plots/` |
| `training_loss_discriminator.png` | Discriminator v3 loss curve | `research_ws/training_plots/` |
| `sim_success_rate.png` | N=20 sim trial success rate bar chart | Drive / thesis results |
| `real_success_rate.png` | N=20 real trial success rate bar chart | Drive / thesis results |
| `sim2real_comparison.png` | Sim vs Real grasp quality comparison | Thesis Fig |

---

### `docs/images/graspgen/`
GraspGen output visualizations.

| Image | Description | Source |
|-------|-------------|--------|
| `graspgen_output_sim.png` | GraspGen grasp candidates on sim point cloud | Drive |
| `graspgen_output_real.png` | GraspGen grasp candidates on real point cloud | Drive |
| `robotiq3f_grasp_config.png` | Robotiq 3F grasp configuration used | Thesis Fig |

---

## How to Upload Images

```bash
# Create folders
mkdir -p ~/docs/images/hardware ~/docs/images/simulation \
         ~/docs/images/pipeline ~/docs/images/results ~/docs/images/graspgen

# Copy images (example)
cp ~/Downloads/robot_photo.jpg ~/docs/images/hardware/robot_full_setup.jpg

# Copy training plots (already on disk)
cp ~/research_ws/training_plots/*.png ~/docs/images/results/

# Copy rosgraph
cp ~/rosgraph.png ~/docs/images/pipeline/ros2_node_graph.png

# Stage and push
git add docs/images/
git commit -m "Add hardware, simulation and result images"
git push origin master
```

---

## Already in Repo (no action needed)

| File | Location |
|------|----------|
| Thesis PDF | `docs/AnushkaSinghania_Thesis_240614.pdf` |
| Training plots | `research_ws/training_plots/` |
| GraspDataGen docs/images | `research_ws/GraspDataGen_src/docs/images/` |
