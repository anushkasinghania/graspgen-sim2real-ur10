cmake_minimum_required(VERSION 3.8)
project(ur10_pick_place)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY config launch urdf worlds scripts
  DESTINATION share/${PROJECT_NAME}
)

install(
  PROGRAMS
    scripts/planning_scene_setup.py
    scripts/test_grasp_pose.py
    scripts/sim_object_pc_publisher.py
    scripts/sam2_segmentation_node.py
    scripts/gripper_joint_state_publisher.py
    scripts/oakd_viewer.py
    scripts/pick.sh
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
