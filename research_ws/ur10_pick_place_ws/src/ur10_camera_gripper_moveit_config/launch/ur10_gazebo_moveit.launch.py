from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution, Command
from launch_ros.parameter_descriptions import ParameterValue
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():

    # ---------------------------
    # Gazebo
    # ---------------------------
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare("gazebo_ros"),
                "launch",
                "gazebo.launch.py"
            ])
        )
    )

    # ---------------------------
    # Robot Description (XACRO)
    # ---------------------------
    xacro_file = PathJoinSubstitution([
        FindPackageShare("ur10_camera_gripper_moveit_config"),
        "urdf",
        "ur10_with_3f_gripper.urdf.xacro"
    ])

    robot_description = {
        "robot_description": ParameterValue(
            Command(["xacro ", xacro_file]),
            value_type=str
        )
    }

    # ---------------------------
    # Robot State Publisher
    # ---------------------------
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[robot_description, {"use_sim_time": True}],
        output="screen"
    )

    # ---------------------------
    # Spawn in Gazebo
    # ---------------------------
    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-topic", "robot_description",
            "-entity", "ur10"
        ],
        output="screen"
    )

    # ---------------------------
    # MoveIt
    # ---------------------------
    moveit_config = (
        MoveItConfigsBuilder(
            robot_name="ur",
            package_name="ur10_camera_gripper_moveit_config"
        )
        .to_moveit_configs()
    )

    move_group = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.planning_pipelines,
            moveit_config.robot_description_kinematics,
            moveit_config.joint_limits,
            {"use_sim_time": True},
        ],
    )

    # ---------------------------
    # RViz (EXPLICIT — YOU WERE MISSING THIS)
    # ---------------------------
    rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments=[
            "-d",
            PathJoinSubstitution([
                FindPackageShare("ur10_camera_gripper_moveit_config"),
                "config",
                "moveit.rviz"
            ])
        ],
        parameters=[robot_description],
        output="screen"
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_entity,
        move_group,
        rviz
    ])

