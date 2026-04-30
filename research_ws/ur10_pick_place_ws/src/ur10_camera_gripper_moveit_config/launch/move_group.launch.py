import os
import yaml

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue

from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():

    # ------------------------------------------------
    # Robot description (URDF)
    # ------------------------------------------------
    urdf_path = PathJoinSubstitution([
        FindPackageShare("ur10_camera_gripper_moveit_config"),
        "config",
        "ur.urdf"
    ])

    robot_description = {
        "robot_description": ParameterValue(
            Command(["cat ", urdf_path]),
            value_type=str,
        )
    }

    # ------------------------------------------------
    # Robot semantic description (SRDF)
    # ------------------------------------------------
    srdf_path = PathJoinSubstitution([
        FindPackageShare("ur10_camera_gripper_moveit_config"),
        "config",
        "ur.srdf"
    ])

    robot_description_semantic = {
        "robot_description_semantic": ParameterValue(
            Command(["cat ", srdf_path]),
            value_type=str,
        )
    }

    # ------------------------------------------------
    # MoveIt config builder
    # ------------------------------------------------
    moveit_config = (
        MoveItConfigsBuilder(
            robot_name="ur",
            package_name="ur10_camera_gripper_moveit_config",
        )
        .to_moveit_configs()
    )

    moveit_config.robot_description = robot_description
    moveit_config.robot_description_semantic = robot_description_semantic

    # ------------------------------------------------
    # Load MoveIt controllers YAML (FAKE controllers)
    # ------------------------------------------------
    controllers_yaml_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "config",
        "moveit_controllers.yaml",
    )

    with open(controllers_yaml_path, "r") as f:
        moveit_controllers = yaml.safe_load(f)

    # ------------------------------------------------
    # move_group node
    # ------------------------------------------------
    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            robot_description,
            robot_description_semantic,
            moveit_config.planning_pipelines,
            moveit_config.robot_description_kinematics,
            moveit_config.joint_limits,
            moveit_controllers,          # ✅ controllers FIX
            {"use_sim_time": True},
        ],
    )

    return LaunchDescription([
        move_group_node
    ])

