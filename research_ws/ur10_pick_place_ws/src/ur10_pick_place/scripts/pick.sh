#!/bin/bash
# pick.sh — Start wrist_cam + SAM2 in one command.
#
# Uses wrist_cam only — TF is derived from robot FK (joint states → URDF),
# so no external camera calibration is needed.
# SAM2 runs in foreground so it inherits X11 display auth.
# Ctrl-C stops everything.
#
# Usage: ./pick.sh

WS="$HOME/research_ws/ur10_pick_place_ws"
CHECKPOINT="$HOME/research_ws/segment-anything-2/checkpoints/sam2.1_hiera_small.pt"
MODEL_CFG="configs/sam2.1/sam2.1_hiera_s.yaml"
WRIST_CAM_MXID="14442C10715AD4D200"

source /opt/ros/humble/setup.bash
source "$WS/install/setup.bash"

echo "[pick.sh] Starting wrist_cam (MXID: $WRIST_CAM_MXID)..."
ros2 run depthai_ros_driver camera_node \
  --ros-args \
  --remap __ns:=/ \
  --remap __node:=wrist_cam \
  -p camera.i_mx_id:="$WRIST_CAM_MXID" \
  -p camera.i_nn_type:="none" \
  -p camera.i_pipeline_type:="RGBD" \
  -p camera.i_enable_imu:=false \
  -p camera.i_enable_ir:=false \
  -p rgb.i_fps:=10.0 \
  -p stereo.i_fps:=10.0 \
  -p stereo.i_resolution:="400" \
  -p stereo.i_align_depth:=true \
  -p stereo.i_subpixel:=false &
WRIST_CAM_PID=$!

echo "[pick.sh] Publishing wrist_cam TFs..."
# Step 1: tool0 → oakd_wide_link (fixed mechanical offset of camera mount)
#
# Camera is mounted on the FRONT face of the gripper bracket (facing the arm reach
# direction).  At scan pose (pan≈90°): tool0+Y = world −Y, so the front of the
# gripper = tool0 −Y direction → TF Y must be NEGATIVE to move camera toward tray.
#
# Physical measurement: camera ≈14 cm from gripper centre, mounted on front face.
# TF = (x=0, y=−0.065, z=−0.04):
#   x=0       → no lateral offset
#   y=−0.065  → 6.5 cm in tool0 −Y = world +Y (toward tray) at scan pose
#               CALIBRATED 2026-04-27: was −0.14; centroid Y read +75 mm too far forward
#               with object (17 cm length in Y) against near tray edge (Y=0.320 m):
#               measured centroid Y=0.480, expected=0.405 → corrected by +0.075
#   z=−0.04   → 4 cm in tool0 −Z (Z error ≈23 mm = within stereo depth noise, no fix)
ros2 run tf2_ros static_transform_publisher \
  0.0 -0.065 -0.04 0 0 0 tool0 oakd_wide_link &
TF_TOOL0_PID=$!

# Step 2: oakd_wide_link → optical frame
# Camera is mounted upside-down (180° rotation about optical axis).
# ROS2 static_transform_publisher positional order: x y z yaw pitch roll parent child
# yaw=π flips cam +X and +Y; cam +Z (depth) is unchanged → still points world −Z (down ✓).
# At scan pose after fix: cam+Z=world−Z ✓, cam+X=world−X, cam+Y=world+Y.
ros2 run tf2_ros static_transform_publisher \
  0 0 0 3.14159 0 0 oakd_wide_link wrist_cam_rgb_camera_optical_frame &
TF_WRIST_PID=$!

trap "echo '[pick.sh] Stopping...'; kill $WRIST_CAM_PID $TF_TOOL0_PID $TF_WRIST_PID 2>/dev/null; wait $WRIST_CAM_PID $TF_TOOL0_PID $TF_WRIST_PID 2>/dev/null" EXIT

echo "[pick.sh] Waiting 10 s for wrist_cam to initialise..."
sleep 10

echo "[pick.sh] Checking wrist_cam topics..."
ros2 topic list --no-daemon 2>/dev/null | grep wrist_cam || echo "[pick.sh] WARNING: no wrist_cam topics yet"

echo "[pick.sh] Starting SAM2."
echo "[pick.sh]   Send /pick/start FIRST — arm moves to scan pose, THEN click object."
export QT_QPA_PLATFORM=xcb
ros2 run ur10_pick_place sam2_segmentation_node.py \
  --ros-args \
  -p checkpoint:="$CHECKPOINT" \
  -p model_cfg:="$MODEL_CFG"
