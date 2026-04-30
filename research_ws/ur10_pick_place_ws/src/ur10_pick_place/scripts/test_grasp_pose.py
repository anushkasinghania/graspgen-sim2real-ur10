#!/usr/bin/env python3
"""
test_grasp_pose.py
------------------
Publishes a hardcoded PoseStamped to /graspgen/grasp_pose to trigger the
grasp_executor_node without needing real GraspGen inference.

The default pose targets the tin_can top at (0.60, -0.15, 0.760) with a
top-down approach (gripper Z pointing down — quaternion (1, 0, 0, 0)).

Usage:
    # Publish default pose (tin_can top-down):
    ros2 run ur10_pick_place test_grasp_pose.py

    # Publish to a custom position:
    ros2 run ur10_pick_place test_grasp_pose.py --ros-args \
        -p x:=0.80 -p y:=0.10 -p z:=1.17

Watch status:
    ros2 topic echo /grasp_executor/status
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from rcl_interfaces.msg import ParameterDescriptor


class TestGraspPosePublisher(Node):

    def __init__(self):
        super().__init__("test_grasp_pose")

        # Declare parameters so the user can override via --ros-args -p
        self.declare_parameter("x", 0.60,
            ParameterDescriptor(description="Grasp X in world frame (m)"))
        self.declare_parameter("y", -0.15,
            ParameterDescriptor(description="Grasp Y in world frame (m)"))
        self.declare_parameter("z", 0.760,
            ParameterDescriptor(description="Grasp Z in world frame (m) — tin_can top surface (bottom=0.650, top=0.760, h=110mm)"))
        self.declare_parameter("frame_id", "world",
            ParameterDescriptor(description="Reference frame for the pose"))

        x = self.get_parameter("x").value
        y = self.get_parameter("y").value
        z = self.get_parameter("z").value
        frame_id = self.get_parameter("frame_id").value

        pub = self.create_publisher(PoseStamped, "/graspgen/grasp_pose", 10)

        # Give subscribers (grasp_executor_node) 3 seconds to connect
        import time
        time.sleep(3.0)

        msg = PoseStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = frame_id

        # Position: object centre
        msg.pose.position.x = float(x)
        msg.pose.position.y = float(y)
        msg.pose.position.z = float(z)

        # Orientation: top-down approach — gripper Z axis pointing straight down.
        # Quaternion for 180° rotation around X:  (x=1, y=0, z=0, w=0)
        msg.pose.orientation.x = 1.0
        msg.pose.orientation.y = 0.0
        msg.pose.orientation.z = 0.0
        msg.pose.orientation.w = 0.0

        pub.publish(msg)
        self.get_logger().info(
            f"Published grasp pose → frame={frame_id}, "
            f"x={x:.3f}, y={y:.3f}, z={z:.3f}"
        )
        self.get_logger().info("Watch: ros2 topic echo /grasp_executor/status")


def main(args=None):
    rclpy.init(args=args)
    node = TestGraspPosePublisher()
    # Spin briefly to flush the publish, then exit
    rclpy.spin_once(node, timeout_sec=1.0)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
