"""
camera.launch.py
----------------
Launches OAK-D cameras independently from the main pipeline.
Start this ONLY when ready to do SAM2 segmentation + pick.
Stop it (Ctrl-C) when done picking to free Jetson resources.

Usage:
  # Both cameras (env + wrist)
  ros2 launch ur10_pick_place camera.launch.py

  # Environment camera only (sufficient for SAM2 + GraspGen)
  ros2 launch ur10_pick_place camera.launch.py launch_wrist_cam:=false
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory("ur10_pick_place")

    declared_args = [
        DeclareLaunchArgument(
            "launch_wrist_cam",
            default_value="false",
            description="Also launch the wrist camera (not needed for GraspGen pipeline).",
        ),
    ]

    env_cam = Node(
        package="depthai_ros_driver",
        executable="camera_node",
        name="env_cam",
        namespace="env_cam",
        output="screen",
        parameters=[
            os.path.join(pkg_share, "config", "oakd_env.yaml"),
            {"camera.i_mx_id": "14442C1041A6D1D200"},
        ],
    )

    wrist_cam = Node(
        package="depthai_ros_driver",
        executable="camera_node",
        name="wrist_cam",
        namespace="wrist_cam",
        output="screen",
        parameters=[
            os.path.join(pkg_share, "config", "oakd_wrist.yaml"),
            {"camera.i_mx_id": "14442C10715AD4D200"},
        ],
        condition=IfCondition(LaunchConfiguration("launch_wrist_cam")),
    )

    return LaunchDescription(declared_args + [env_cam, wrist_cam])
