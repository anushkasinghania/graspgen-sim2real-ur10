#!/usr/bin/env python3
"""
gripper_joint_state_publisher.py
---------------------------------
Publishes zero-valued joint states for all Robotiq 3F finger joints.

In real_hardware mode, ur_robot_driver publishes the 6 arm joints on
/joint_states. MoveIt also needs the 11 gripper finger joints to have
a complete, valid start state. Since the gripper is controlled via TCP
(not a joint controller), no ROS2 driver publishes its joint states.

This node publishes the gripper joints at zero (open position) at 50 Hz
on the same /joint_states topic. robot_state_publisher merges all
joint_states messages it receives, so the combined arm + gripper state
gives MoveIt a valid start state.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

GRIPPER_JOINTS = [
    "robotiq_finger_a_joint_1",
    "robotiq_finger_a_joint_2",
    "robotiq_finger_a_joint_3",
    "robotiq_finger_b_joint_1",
    "robotiq_finger_b_joint_2",
    "robotiq_finger_b_joint_3",
    "robotiq_finger_c_joint_1",
    "robotiq_finger_c_joint_2",
    "robotiq_finger_c_joint_3",
    "robotiq_palm_finger_b_joint",
    "robotiq_palm_finger_c_joint",
]


class GripperJointStatePublisher(Node):

    def __init__(self):
        super().__init__("gripper_joint_state_publisher")
        self._pub = self.create_publisher(JointState, "/joint_states", 10)
        self._timer = self.create_timer(0.10, self._publish)  # 10 Hz
        self.get_logger().info(
            f"Publishing {len(GRIPPER_JOINTS)} gripper joint states at 10 Hz"
        )

    def _publish(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = GRIPPER_JOINTS
        msg.position = [0.0] * len(GRIPPER_JOINTS)
        msg.velocity = [0.0] * len(GRIPPER_JOINTS)
        msg.effort = [0.0] * len(GRIPPER_JOINTS)
        self._pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = GripperJointStatePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
