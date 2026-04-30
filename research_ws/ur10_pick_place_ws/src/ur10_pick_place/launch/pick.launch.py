"""
pick.launch.py
--------------
Launches env_cam + SAM2 segmentation node together.
Use this as a single command instead of separate T3 + T4.

SAM2 is delayed 8 seconds to let the camera driver fully initialise
before the node tries to subscribe to camera topics.

Usage:
  ros2 launch ur10_pick_place pick.launch.py
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import TimerAction
from launch_ros.actions import Node


SAM2_CHECKPOINT = os.path.expanduser(
    "~/research_ws/segment-anything-2/checkpoints/sam2.1_hiera_small.pt"
)
SAM2_CFG = "configs/sam2.1/sam2.1_hiera_s.yaml"

# Env cam MX ID — always connect to the tripod camera, not the wrist cam
ENV_CAM_MXID = "14442C1041A6D1D200"


def generate_launch_description():
    pkg_share = get_package_share_directory("ur10_pick_place")

    # Pass MX ID explicitly so the driver always picks the correct device
    # even when both cameras are plugged in.
    env_cam = Node(
        package="depthai_ros_driver",
        executable="camera_node",
        name="env_cam",
        namespace="env_cam",
        output="screen",
        parameters=[
            os.path.join(pkg_share, "config", "oakd_env.yaml"),
            {
                "camera.i_mx_id": ENV_CAM_MXID,
                "camera.i_nn_type": "none",
                "camera.i_pipeline_type": "RGBD",
            },
        ],
    )

    # Pass DISPLAY so the cv2 window can open when launched as a subprocess.
    display = os.environ.get("DISPLAY", ":0")

    sam2 = Node(
        package="ur10_pick_place",
        executable="sam2_segmentation_node.py",
        name="sam2_segmentation_node",
        output="screen",
        additional_env={"DISPLAY": display},
        parameters=[
            {"checkpoint": SAM2_CHECKPOINT},
            {"model_cfg": SAM2_CFG},
        ],
    )

    return LaunchDescription([
        env_cam,
        # Wait 8 s for camera driver to come up before SAM2 subscribes
        TimerAction(period=8.0, actions=[sam2]),
    ])
