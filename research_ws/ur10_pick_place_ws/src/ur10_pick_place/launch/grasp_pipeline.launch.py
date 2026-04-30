"""
grasp_pipeline.launch.py
------------------------
Launches the full GraspGen pick-and-place pipeline (RViz only — no Gazebo):
  - UR10 + Robotiq 3F gripper — all joints use mock_components/GenericSystem
  - Standalone ros2_control_node (controller_manager)
  - ros2_control controllers (arm JTC + gripper JTC)
  - MoveIt 2 move_group
  - RViz2 — primary visualization (robot + planning scene)
  - grasp_executor_node (subscribes /graspgen/grasp_pose)
  - planning_scene_setup: table + objects published to MoveIt at t+8s

All nodes run on WALL TIME (no use_sim_time).
Hardware: Jetson AGX Orin 64GB, Ubuntu 22.04, JetPack 6.1, ROS2 Humble.
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    TimerAction,
)
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import (
    Command,
    FindExecutable,
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare
from moveit_configs_utils import MoveItConfigsBuilder


# ---------------------------------------------------------------------------
# generate_launch_description
# ---------------------------------------------------------------------------

def generate_launch_description():
    pkg_share = get_package_share_directory("ur10_pick_place")

    # ------------------------------------------------------------------
    # Declared arguments
    # ------------------------------------------------------------------
    declared_args = [
        DeclareLaunchArgument(
            "use_rviz",
            default_value="true",
            description="Launch RViz2.",
        ),
        DeclareLaunchArgument(
            "launch_grasp_executor",
            default_value="true",
            description="Launch the grasp_executor_node (subscribes /graspgen/grasp_pose).",
        ),
        DeclareLaunchArgument(
            "launch_graspgen_bridge",
            default_value="false",
            description="Launch graspgen_bridge_node (requires GraspGen models).",
        ),
        DeclareLaunchArgument(
            "launch_sim_pc",
            default_value="false",
            description="Launch sim_object_pc_publisher (synthetic point cloud for GraspGen in sim).",
        ),
        DeclareLaunchArgument(
            "sim_pc_object",
            default_value="tin_can",
            description="Object to publish synthetic PC for: tin_can, bottle_large, boba_tea_cup, all.",
        ),
        DeclareLaunchArgument(
            "real_hardware",
            default_value="false",
            description="Real hardware mode: estimate object geometry from /env_cam/points cloud. "
                        "Disables position snap and SCENE_PICK_OBJECTS lookup. "
                        "Activates Robotiq 3F gripper via TCP (192.168.1.105).",
        ),
        DeclareLaunchArgument(
            "launch_env_cam",
            default_value="false",
            description="Launch environment camera (OAK-D Pro tripod, MX ID: 14442C1041A6D1D200).",
        ),
        DeclareLaunchArgument(
            "launch_wrist_cam",
            default_value="false",
            description="Launch wrist camera (OAK-D Pro Wide on gripper, MX ID: 14442C10715AD4D200).",
        ),
    ]

    # ------------------------------------------------------------------
    # Robot description (URDF via xacro)
    # All joints use mock_components/GenericSystem — no ign_ros2_control.
    # ------------------------------------------------------------------
    controllers_yaml = os.path.join(pkg_share, "config", "ur10_3f_controllers.yaml")
    urdf_xacro = os.path.join(pkg_share, "urdf", "ur10_3f_ignition.urdf.xacro")
    robot_description_content = ParameterValue(
        Command(
            [
                PathJoinSubstitution([FindExecutable(name="xacro")]),
                " ",
                urdf_xacro,
            ]
        ),
        value_type=str,
    )
    robot_description = {"robot_description": robot_description_content}

    # ------------------------------------------------------------------
    # MoveIt 2 config
    # ------------------------------------------------------------------
    moveit_config = (
        MoveItConfigsBuilder("custom_robot", package_name="ur10_camera_gripper_moveit_config")
        .robot_description(file_path=urdf_xacro)
        .robot_description_semantic(file_path="config/ur.srdf")
        .trajectory_execution(
            file_path=os.path.join(pkg_share, "config", "moveit_controllers.yaml")
        )
        .robot_description_kinematics(file_path="config/kinematics.yaml")
        .planning_pipelines(pipelines=["ompl"])
        .planning_scene_monitor(
            publish_robot_description=True,
            publish_robot_description_semantic=True,
            publish_planning_scene=True,
        )
        .to_moveit_configs()
    )

    # ------------------------------------------------------------------
    # robot_state_publisher — SIM only.
    # In real_hardware mode, ur_robot_driver launches its own RSP from
    # real joint states. We skip ours to avoid TF conflicts on arm links.
    # ------------------------------------------------------------------
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[robot_description],
        condition=UnlessCondition(LaunchConfiguration("real_hardware")),
    )


    # ------------------------------------------------------------------
    # Standalone ros2_control_node — SIM only (mock hardware).
    # In real_hardware mode this is skipped — ur_robot_driver owns ros2_control.
    # ------------------------------------------------------------------
    ros2_control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        output="screen",
        parameters=[
            robot_description,
            controllers_yaml,
        ],
        condition=UnlessCondition(LaunchConfiguration("real_hardware")),
    )

    # ------------------------------------------------------------------
    # Gripper joint state publisher — REAL HARDWARE only.
    # ur_robot_driver publishes arm joints but not gripper finger joints.
    # MoveIt needs all URDF joints. This node merges arm states (from
    # ur_robot_driver /joint_states) with zero-valued gripper joints so
    # MoveIt has a complete, valid start state.
    # ------------------------------------------------------------------
    gripper_joint_state_pub = Node(
        package="ur10_pick_place",
        executable="gripper_joint_state_publisher.py",
        name="gripper_joint_state_publisher",
        output="screen",
        condition=IfCondition(LaunchConfiguration("real_hardware")),
    )

    # ------------------------------------------------------------------
    # Controller spawners — wall time
    # ------------------------------------------------------------------
    # Controller spawners — SIM only (real_hardware uses ur_robot_driver's controllers)
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        name="jsb_spawner",
        output="screen",
        arguments=[
            "joint_state_broadcaster",
            "-t", "joint_state_broadcaster/JointStateBroadcaster",
            "-c", "/controller_manager",
        ],
        condition=UnlessCondition(LaunchConfiguration("real_hardware")),
    )

    arm_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        name="arm_ctrl_spawner",
        output="screen",
        arguments=[
            "joint_trajectory_controller",
            "-t", "joint_trajectory_controller/JointTrajectoryController",
            "-c", "/controller_manager",
        ],
        condition=UnlessCondition(LaunchConfiguration("real_hardware")),
    )

    gripper_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        name="gripper_ctrl_spawner",
        output="screen",
        arguments=[
            "gripper_trajectory_controller",
            "-t", "joint_trajectory_controller/JointTrajectoryController",
            "-c", "/controller_manager",
        ],
        condition=UnlessCondition(LaunchConfiguration("real_hardware")),
    )

    # Arm/gripper controllers start independently — using separate timers
    # avoids the OnProcessExit race where arm/gripper launch even when JSB fails.

    # ------------------------------------------------------------------
    # MoveIt 2 move_group node — wall time
    # ------------------------------------------------------------------
    move_group_params = moveit_config.to_dict()
    move_group_params.pop("use_sim_time", None)

    move_group = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[move_group_params],
    )

    # ------------------------------------------------------------------
    # RViz 2 — wall time (primary robot visualization)
    # ------------------------------------------------------------------
    rviz_config = os.path.join(
        get_package_share_directory("ur10_camera_gripper_moveit_config"),
        "config",
        "moveit.rviz",
    )
    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.planning_pipelines,
            moveit_config.robot_description_kinematics,
        ],
        condition=IfCondition(LaunchConfiguration("use_rviz")),
    )

    # ------------------------------------------------------------------
    # grasp_executor_node — wall time
    # ------------------------------------------------------------------
    grasp_executor = Node(
        package="grasp_executor",
        executable="grasp_executor_node",
        name="grasp_executor_node",
        output="screen",
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            {"real_hardware": LaunchConfiguration("real_hardware")},
        ],
        condition=IfCondition(LaunchConfiguration("launch_grasp_executor")),
    )

    # ------------------------------------------------------------------
    # Planning scene setup — publishes table + pick objects to MoveIt
    # Delayed so move_group is fully initialised before publishing.
    # ------------------------------------------------------------------
    planning_scene_setup = Node(
        package="ur10_pick_place",
        executable="planning_scene_setup.py",
        name="planning_scene_setup",
        output="screen",
        parameters=[{
            "real_hardware": LaunchConfiguration("real_hardware"),
        }],
    )

    # ------------------------------------------------------------------
    # GraspGen bridge node (optional — requires GraspGen + checkpoints)
    # ------------------------------------------------------------------
    graspgen_bridge = Node(
        package="grasp_executor",
        executable="graspgen_bridge_node",
        name="graspgen_bridge_node",
        output="screen",
        condition=IfCondition(LaunchConfiguration("launch_graspgen_bridge")),
    )

    # ------------------------------------------------------------------
    # Simulation point cloud publisher
    # Generates synthetic PointCloud2 of a scene object in world frame
    # so GraspGen bridge can run without a real camera.
    # Enable with: launch_sim_pc:=true  (and launch_graspgen_bridge:=true)
    # ------------------------------------------------------------------
    sim_pc_publisher = Node(
        package="ur10_pick_place",
        executable="sim_object_pc_publisher.py",
        name="sim_object_pc_publisher",
        output="screen",
        parameters=[{
            "object_id": LaunchConfiguration("sim_pc_object"),
            "n_points":  2000,
            "pub_rate":  2.0,
        }],
        condition=IfCondition(LaunchConfiguration("launch_sim_pc")),
    )

    # ------------------------------------------------------------------
    # Environment camera — OAK-D Pro tripod (env_cam)
    # ⚠️  env_cam is NOT in the current hardware setup — only wrist_cam is used.
    # This node definition is kept for sim compatibility but is never launched
    # (launch_env_cam defaults to false and is not set in real hardware launch).
    # The /env_cam/points topic is published by sam2_segmentation_node (wrist_cam data).
    # ------------------------------------------------------------------
    env_cam = Node(
        package="depthai_ros_driver",
        executable="camera_node",
        name="env_cam",
        namespace="env_cam",
        output="screen",
        parameters=[
            os.path.join(pkg_share, "config", "oakd_env.yaml"),
        ],
        condition=IfCondition(LaunchConfiguration("launch_env_cam")),
    )

    # ------------------------------------------------------------------
    # Wrist camera — OAK-D Pro Wide on gripper (wrist_cam)
    # Fixed MX ID in config: 14442C10715AD4D200
    # Topics: /wrist_cam/rgb/image_raw  /wrist_cam/depth/image_raw
    # ------------------------------------------------------------------
    wrist_cam = Node(
        package="depthai_ros_driver",
        executable="camera_node",
        name="wrist_cam",
        namespace="wrist_cam",
        output="screen",
        parameters=[
            os.path.join(pkg_share, "config", "oakd_wrist.yaml"),
        ],
        condition=IfCondition(LaunchConfiguration("launch_wrist_cam")),
    )

    # env_cam static TF removed — env_cam is not in the hardware setup.
    # wrist_cam TF is derived automatically from robot FK via ur_robot_driver.

    return LaunchDescription(
        declared_args
        + [
            # Gripper joint state publisher (real_hardware only — fills missing finger joints)
            gripper_joint_state_pub,
            # robot_state_publisher (sim only — real uses ur_robot_driver RSP)
            robot_state_publisher,
            # Standalone ros2_control_node (wall time, mock hardware)
            ros2_control_node,
            # Controller spawners — staggered timers: JSB first, then arm/gripper.
            # Stagger (4s / 6s / 7s) gives the CM time to finish hardware init
            # and avoids OnProcessExit race condition (arm launched on JSB failure).
            TimerAction(period=4.0, actions=[joint_state_broadcaster_spawner]),
            TimerAction(period=6.0, actions=[arm_controller_spawner]),
            TimerAction(period=7.0, actions=[gripper_controller_spawner]),
            # MoveIt move_group (wall time)
            move_group,
            # RViz — primary robot visualization
            rviz,
            # Grasp executor node
            grasp_executor,
            # GraspGen bridge (optional — set launch_graspgen_bridge:=true)
            graspgen_bridge,
            # Sim point cloud publisher (optional — set launch_sim_pc:=true)
            sim_pc_publisher,
            # Camera drivers (optional — set launch_env_cam:=true / launch_wrist_cam:=true)
            env_cam,
            wrist_cam,
            # Planning scene: floor + trays + objects (delayed so move_group is ready)
            TimerAction(period=8.0, actions=[planning_scene_setup]),
        ]
    )
