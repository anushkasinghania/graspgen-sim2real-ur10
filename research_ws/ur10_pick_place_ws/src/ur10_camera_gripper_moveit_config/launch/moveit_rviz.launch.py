from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue
from moveit_configs_utils import MoveItConfigsBuilder

def generate_launch_description():

    urdf_path = PathJoinSubstitution([
        FindPackageShare("ur10_camera_gripper_moveit_config"),
        "config",
        "ur.urdf"
    ])

    robot_description = {
        "robot_description": ParameterValue(
            Command(["cat ", urdf_path]),   # ← SPACE IS CRITICAL
            value_type=str
        )
    }

    srdf_path = PathJoinSubstitution([
        FindPackageShare("ur10_camera_gripper_moveit_config"),
        "config",
        "ur.srdf"
    ])

    robot_description_semantic = {
        "robot_description_semantic": ParameterValue(
            Command(["cat ", srdf_path]),   # ← SPACE IS CRITICAL
            value_type=str
        )
    }

    moveit_config = (
        MoveItConfigsBuilder(
            robot_name="ur",
            package_name="ur10_camera_gripper_moveit_config"
        )
        .to_moveit_configs()
    )

    moveit_config.robot_description = robot_description
    moveit_config.robot_description_semantic = robot_description_semantic

    rviz_config = PathJoinSubstitution([
        FindPackageShare("ur10_camera_gripper_moveit_config"),
        "config",
        "moveit.rviz"
    ])

    return LaunchDescription([
        Node(
            package="rviz2",
            executable="rviz2",
            arguments=["-d", rviz_config],
            parameters=[
                moveit_config.robot_description,
                moveit_config.robot_description_semantic,
                moveit_config.planning_pipelines,
                moveit_config.robot_description_kinematics,
            ],
            output="screen",
        )
    ])

