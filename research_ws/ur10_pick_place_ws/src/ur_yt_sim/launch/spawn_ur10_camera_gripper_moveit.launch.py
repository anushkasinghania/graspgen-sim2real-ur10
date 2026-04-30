from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction, RegisterEventHandler, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessStart
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from moveit_configs_utils import MoveItConfigsBuilder
import os

def generate_launch_description():
    ld = LaunchDescription()

    uryt_share = get_package_share_directory("ur_yt_sim")
    robotiq_share = get_package_share_directory("robotiq_description")
    ur_share = get_package_share_directory("ur_description")
    gazebo_ros_dir = get_package_share_directory("gazebo_ros")

    world_file = os.path.join(uryt_share, 'worlds', 'world2.world')

    # Gazebo env
    ld.add_action(SetEnvironmentVariable(
        name="GAZEBO_RESOURCE_PATH",
        value=":".join(["/usr/share/gazebo-11", uryt_share, robotiq_share, ur_share])
    ))

    joint_controllers_file = os.path.join(uryt_share, "config", "ur10_controllers_gripper.yaml")

    moveit_config = (
        MoveItConfigsBuilder("custom_robot", package_name="ur10_camera_gripper_moveit_config")
        .robot_description(
            file_path=os.path.join(uryt_share, "urdf", "ur10_with_3f_gripper.urdf.xacro"),
            mappings={
                "ur_type": "ur10",
                "sim_gazebo": "true",
                "use_fake_hardware": "false",
                "simulation_controllers": joint_controllers_file,
                "initial_positions_file": os.path.join(uryt_share, "config", "initial_positions.yaml"),
            },
        )
        .robot_description_semantic(file_path="config/ur.srdf")
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .robot_description_kinematics(file_path="config/kinematics.yaml")
        .planning_pipelines(pipelines=["ompl", "chomp", "pilz_industrial_motion_planner"])
        .planning_scene_monitor(
            publish_robot_description=True,
            publish_robot_description_semantic=True,
            publish_planning_scene=True
        )
        .to_moveit_configs()
    )

    # Start gazebo
    gazebo = Node(
        package="gazebo_ros",
        executable="gzserver",
        output="screen",
        arguments=["--verbose", world_file],
    )
    ld.add_action(gazebo)

    # robot_state_publisher
    rsp = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[moveit_config.robot_description, {"use_sim_time": True}],
        output="screen"
    )
    ld.add_action(rsp)

    # spawn entity node (delayed a little so robot_description is published)
    spawn = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=["-entity", "cobot", "-topic", "robot_description", "-x", LaunchConfiguration("x"), "-y", LaunchConfiguration("y"), "-z", LaunchConfiguration("z")],
        output="screen"
    )
    ld.add_action(TimerAction(period=3.0, actions=[spawn]))

    # RViz
    rviz_cfg = os.path.join(get_package_share_directory("ur10_camera_gripper_moveit_config"), "config", "moveit.rviz")
    rviz = Node(
        package="rviz2", executable="rviz2",
        arguments=["-d", rviz_cfg],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.planning_pipelines,
            moveit_config.robot_description_kinematics,
            {"use_sim_time": True},
        ],
        output="screen"
    )
    ld.add_action(rviz)

    # Move group
    mg_params = moveit_config.to_dict()
    mg_params.update({"use_sim_time": True})

    move_group = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[mg_params],
    )
    ld.add_action(move_group)

    return ld

