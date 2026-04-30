#!/usr/bin/env python3
"""
planning_scene_setup.py
-----------------------
Publishes the workspace collision scene to MoveIt2.

SIM mode (real_hardware:=false):
  Publishes floor + trays + 6 known objects (tin_can + 5 distractors).
  Objects are at fixed positions matching the sim scene layout.

REAL mode (real_hardware:=true):
  Publishes floor + trays ONLY.
  No sim objects — real objects are unknown until SAM2 segments them.
  grasp_executor_node adds 'real_target' cylinder dynamically from point cloud.
"""

import time

import rclpy
from geometry_msgs.msg import Pose
from moveit_msgs.msg import CollisionObject, ObjectColor, PlanningScene
from rclpy.node import Node
from shape_msgs.msg import SolidPrimitive
from std_msgs.msg import ColorRGBA


class PlanningSceneSetup(Node):

    FRAME = "world"

    def __init__(self):
        super().__init__("planning_scene_setup")
        self.declare_parameter("real_hardware", False)
        self._real_hardware = self.get_parameter("real_hardware").value
        self._pub = self.create_publisher(PlanningScene, "/planning_scene", 10)
        time.sleep(2.0)
        self._publish_scene()
        if self._real_hardware:
            self.get_logger().info(
                "REAL HARDWARE mode: published floor + trays only (no sim objects).")
        else:
            self.get_logger().info(
                "SIM mode: published floor + trays + 6 scene objects.")

    def _pose(self, x, y, z):
        p = Pose()
        p.position.x = float(x)
        p.position.y = float(y)
        p.position.z = float(z)
        p.orientation.w = 1.0
        return p

    def _box(self, name, x, y, z, lx, ly, lz):
        obj = CollisionObject()
        obj.id = name
        obj.header.frame_id = self.FRAME
        obj.header.stamp = self.get_clock().now().to_msg()
        obj.primitives.append(
            SolidPrimitive(type=SolidPrimitive.BOX,
                           dimensions=[float(lx), float(ly), float(lz)]))
        obj.primitive_poses.append(self._pose(x, y, z))
        obj.operation = CollisionObject.ADD
        return obj

    def _cylinder(self, name, x, y, z, radius, height):
        obj = CollisionObject()
        obj.id = name
        obj.header.frame_id = self.FRAME
        obj.header.stamp = self.get_clock().now().to_msg()
        obj.primitives.append(
            SolidPrimitive(type=SolidPrimitive.CYLINDER,
                           dimensions=[float(height), float(radius)]))
        obj.primitive_poses.append(self._pose(x, y, z))
        obj.operation = CollisionObject.ADD
        return obj

    def _publish_scene(self):
        scene = PlanningScene()
        scene.is_diff = True

        # Always add: floor + trays (real physical objects)
        # REAL HARDWARE coordinate system: world = base_link (identity TF confirmed).
        # Robot is on a 5 cm stand → floor is at Z = -0.05 m in world frame.
        # Tray positions measured from robot base centre (tape measure, Tray_Dim.odt):
        #   Left/right are from robot's POV at home position (facing +Y).
        #   RIGHT = +X,  FORWARD = +Y.
        #
        # Floor surface is at Z=0.00 m in world frame (floor box centre=-0.05, lz=0.10 → top=0.00).
        # Only the robot is on a 5 cm stand — trays sit directly on the floor (Z_bottom=0).
        #
        # pick_tray  (brown cardboard):
        #   X: left edge=-0.23 m, right edge=+0.23 m → centred at X=0.00
        #   Y=99 cm forward.  H=12 cm → centre Z = 0 + 0.06 = 0.06 m
        #   L=67 cm (X axis), W=46 cm (Y axis)
        #
        # place_tray (yellow crate):
        #   X from Right=0 → left edge flush with pick_tray right edge (+0.23 m)
        #   L=49.5 cm in X → centre X = 0.23 + 0.2475 = 0.4775 m
        #   (72.5 cm = 23 + 49.5 = distance from robot centre to place_tray right edge)
        #   Y=66.2 cm forward.  H=15 cm → centre Z = 0 + 0.075 = 0.075 m
        #   L=49.5 cm (X axis), W=32.4 cm (Y axis)
        scene.world.collision_objects = [
            # self._box("floor",
            #           x=0.00, y=0.00, z=-0.05,
            #           lx=4.00, ly=4.00, lz=0.10),
            # self._box("pick_tray",
            #           x=0.655, y=0.00, z=0.06,
            #           lx=0.67, ly=0.46, lz=0.12),
            # self._box("place_tray",
            #           x=0.662, y=0.4775, z=0.075,
            #           lx=0.324, ly=0.495, lz=0.15),
            self._box("floor",
                      x=0.00, y=0.00, z=-0.05,
                      lx=4.00, ly=4.00, lz=0.10),
            self._box("pick_tray",
                      x=0.000, y=0.655, z=0.06,
                      lx=0.46, ly=0.67, lz=0.12),
            self._box("place_tray",
                      x=-0.4775, y=0.662, z=0.075,
                      lx=0.495, ly=0.324, lz=0.15),
        ]

        scene.object_colors = [
            ObjectColor(id="floor",
                        color=ColorRGBA(r=0.1, g=0.1, b=0.1, a=0.6)),
            ObjectColor(id="pick_tray",
                        color=ColorRGBA(r=0.72, g=0.52, b=0.30, a=1.0)),
            ObjectColor(id="place_tray",
                        color=ColorRGBA(r=0.95, g=0.90, b=0.10, a=1.0)),
        ]

        # Sim only: add 6 known objects for collision avoidance
        if not self._real_hardware:
            scene.world.collision_objects += [
                self._cylinder("tin_can",
                               x=0.60, y=0.00, z=0.175,
                               radius=0.037, height=0.110),
                self._cylinder("bottle_large",
                               x=0.60, y=0.15, z=0.240,
                               radius=0.030, height=0.240),
                self._cylinder("boba_tea_cup",
                               x=0.75, y=0.00, z=0.165,
                               radius=0.025, height=0.090),
                self._cylinder("mug",
                               x=0.50, y=-0.10, z=0.168,
                               radius=0.038, height=0.095),
                self._cylinder("spray_bottle",
                               x=0.72, y=0.15, z=0.220,
                               radius=0.022, height=0.200),
                self._cylinder("small_can",
                               x=0.68, y=-0.15, z=0.155,
                               radius=0.032, height=0.070),
            ]
            scene.object_colors += [
                ObjectColor(id="tin_can",
                            color=ColorRGBA(r=0.85, g=0.10, b=0.10, a=1.0)),
                ObjectColor(id="bottle_large",
                            color=ColorRGBA(r=0.10, g=0.40, b=0.85, a=1.0)),
                ObjectColor(id="boba_tea_cup",
                            color=ColorRGBA(r=0.85, g=0.45, b=0.05, a=1.0)),
                ObjectColor(id="mug",
                            color=ColorRGBA(r=0.55, g=0.10, b=0.80, a=1.0)),
                ObjectColor(id="spray_bottle",
                            color=ColorRGBA(r=0.10, g=0.70, b=0.15, a=1.0)),
                ObjectColor(id="small_can",
                            color=ColorRGBA(r=0.10, g=0.65, b=0.65, a=1.0)),
            ]

        for i in range(10):
            self._pub.publish(scene)
            if i < 9:
                time.sleep(0.3)


def main(args=None):
    rclpy.init(args=args)
    node = PlanningSceneSetup()
    rclpy.spin_once(node, timeout_sec=8.0)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
