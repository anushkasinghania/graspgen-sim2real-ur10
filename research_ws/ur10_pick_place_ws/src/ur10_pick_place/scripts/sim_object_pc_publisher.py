#!/usr/bin/env python3
"""
sim_object_pc_publisher.py
--------------------------
Generates synthetic PointCloud2 messages for the cluttered pick scene and
publishes them on /oakd_pro/points (world frame) so the GraspGen bridge node
can run inference without a real camera.

Cluttered scene — 6 real GraspDataGen objects on pick tray:
  tin_can      r=0.037 h=0.110  (0.60,  0.00, 0.175)  ← PICK TARGET
  bottle_large r=0.030 h=0.240  (0.60,  0.15, 0.240)  15cm left,   tall
  boba_tea_cup r=0.025 h=0.090  (0.75,  0.00, 0.165)  15cm behind, short
  mug          r=0.038 h=0.095  (0.50, -0.10, 0.168)  front-left,  wide
  spray_bottle r=0.022 h=0.200  (0.72,  0.15, 0.220)  back-left,   tall
  small_can    r=0.032 h=0.070  (0.68, -0.15, 0.155)  right,       short

Default: object_id="tin_can" — mirrors SAM2 segmentation in real hardware.
  Real: SAM2 click on tin_can → segment → extract PC → send to GraspGen
  Sim:  publish only tin_can PC → same GraspGen inference path

object_id="all" sends combined PC of all 6 objects (future cluttered-inference mode).

Parameters (ROS2):
  object_id  (str, default "tin_can")  — any object id or "all"
  n_points   (int, default 2000)       — surface sample count per object
  pub_rate   (float, default 2.0)      — Hz
"""

import math
import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import ParameterDescriptor
import numpy as np
from sensor_msgs.msg import PointCloud2, PointField
from std_msgs.msg import String
import struct


# ---------------------------------------------------------------------------
# Scene objects: {id: (cx, cy, cz, radius, height)}
# All on pick tray (bottom at z=0.12 m). Positions match planning_scene_setup.py.
# ---------------------------------------------------------------------------

SCENE_OBJECTS = {
    "tin_can":      (0.60,  0.00, 0.175, 0.037, 0.110),  # PICK TARGET
    "bottle_large": (0.60,  0.15, 0.240, 0.030, 0.240),  # 15cm left,   tall
    "boba_tea_cup": (0.75,  0.00, 0.165, 0.025, 0.090),  # 15cm behind, short
    "mug":          (0.50, -0.10, 0.168, 0.038, 0.095),  # front-left,  wide
    "spray_bottle": (0.72,  0.15, 0.220, 0.022, 0.200),  # back-left,   tall
    "small_can":    (0.68, -0.15, 0.155, 0.032, 0.070),  # right,       short
}

# Only pick targets get excluded from the cloud after being picked.
# All 5 distractors remain in the cloud permanently (never picked in sim).
PICK_TARGETS = {"tin_can"}


def _cylinder_surface_pts(cx, cy, cz, radius, height, n_pts, noise_m=0.001):
    """
    Sample n_pts 3-D points uniformly from the visible surface of a cylinder.

    The camera is above and to the side, so we sample the top cap and the
    upper half of the lateral surface.  Gaussian noise (noise_m std) simulates
    real depth-sensor noise.
    """
    rng = np.random.default_rng()

    # --- Top cap (40 % of points) ---
    n_top = int(n_pts * 0.40)
    r_top  = radius * np.sqrt(rng.uniform(0, 1, n_top))
    th_top = rng.uniform(0, 2 * math.pi, n_top)
    top_x  = cx + r_top * np.cos(th_top)
    top_y  = cy + r_top * np.sin(th_top)
    top_z  = np.full(n_top, cz + height / 2.0)

    # --- Lateral surface — full height (60 % of points) ---
    n_lat  = n_pts - n_top
    th_lat = rng.uniform(0, 2 * math.pi, n_lat)
    h_lat  = rng.uniform(-height / 2.0, height / 2.0, n_lat)
    lat_x  = cx + radius * np.cos(th_lat)
    lat_y  = cy + radius * np.sin(th_lat)
    lat_z  = cz + h_lat

    x = np.concatenate([top_x, lat_x]).astype(np.float32)
    y = np.concatenate([top_y, lat_y]).astype(np.float32)
    z = np.concatenate([top_z, lat_z]).astype(np.float32)

    # Add sensor noise
    x += rng.normal(0, noise_m, len(x)).astype(np.float32)
    y += rng.normal(0, noise_m, len(y)).astype(np.float32)
    z += rng.normal(0, noise_m, len(z)).astype(np.float32)

    return np.column_stack([x, y, z])


def _make_pc2(pts: np.ndarray, frame_id: str, stamp) -> PointCloud2:
    """Pack an Nx3 float32 array into a PointCloud2 message."""
    msg = PointCloud2()
    msg.header.frame_id = frame_id
    msg.header.stamp = stamp
    msg.height = 1
    msg.width  = len(pts)
    msg.is_dense = True
    msg.is_bigendian = False
    msg.point_step = 12   # 3 × float32
    msg.row_step   = msg.point_step * msg.width
    msg.fields = [
        PointField(name="x", offset=0,  datatype=PointField.FLOAT32, count=1),
        PointField(name="y", offset=4,  datatype=PointField.FLOAT32, count=1),
        PointField(name="z", offset=8,  datatype=PointField.FLOAT32, count=1),
    ]
    msg.data = pts.tobytes()
    return msg


class SimObjectPCPublisher(Node):

    def __init__(self):
        super().__init__("sim_object_pc_publisher")

        self.declare_parameter("object_id", "tin_can",
            ParameterDescriptor(description="Scene object to publish ('tin_can', 'bottle_large', 'boba_tea_cup', or 'all')"))
        self.declare_parameter("n_points", 2000,
            ParameterDescriptor(description="Number of surface points per object"))
        self.declare_parameter("pub_rate", 2.0,
            ParameterDescriptor(description="Publication rate in Hz"))

        obj_id   = self.get_parameter("object_id").value
        n_points = int(self.get_parameter("n_points").value)
        rate     = float(self.get_parameter("pub_rate").value)

        self._pub = self.create_publisher(PointCloud2, "/env_cam/points", 10)
        self._obj_id   = obj_id
        self._n_points = n_points
        self._excluded: set = set()   # objects already placed — excluded from PC

        # When executor places an object, it publishes its ID here so we stop
        # including it in the synthetic point cloud (GraspGen sees remaining objects).
        self.create_subscription(
            String, "/grasp_executor/picked_object", self._picked_cb, 10
        )

        self.create_timer(1.0 / rate, self._publish)
        self.get_logger().info(
            f"SimObjectPCPublisher: publishing '{obj_id}' on /env_cam/points "
            f"at {rate} Hz ({n_points} pts). "
            f"Trigger GraspGen: ros2 topic pub --once /graspgen/trigger std_msgs/msg/Empty '{{}}'"
        )

    def _picked_cb(self, msg: String):
        obj_id = msg.data.strip()
        if obj_id in PICK_TARGETS:
            self._excluded.add(obj_id)
            remaining_targets = [k for k in PICK_TARGETS if k not in self._excluded]
            if not remaining_targets:
                self.get_logger().info(
                    "All pick targets placed — resetting PC for next demo cycle.")
                self._excluded.clear()
            else:
                self.get_logger().info(
                    f"Excluded '{obj_id}' from PC. Remaining targets: {remaining_targets}"
                )

    def _publish(self):
        stamp = self.get_clock().now().to_msg()

        obj_id = self._obj_id
        if obj_id == "all":
            active = {k: v for k, v in SCENE_OBJECTS.items() if k not in self._excluded}
            if not active:
                return   # all placed — wait for reset
            pts_list = []
            for oid, (cx, cy, cz, r, h) in active.items():
                pts_list.append(
                    _cylinder_surface_pts(cx, cy, cz, r, h,
                                          self._n_points // len(active)))
            pts = np.concatenate(pts_list, axis=0)
        else:
            if obj_id not in SCENE_OBJECTS:
                self.get_logger().warn(
                    f"Unknown object_id '{obj_id}'. "
                    f"Valid: {list(SCENE_OBJECTS.keys())} or 'all'")
                return
            if obj_id in self._excluded:
                return   # this object was placed; wait for reset
            cx, cy, cz, r, h = SCENE_OBJECTS[obj_id]
            pts = _cylinder_surface_pts(cx, cy, cz, r, h, self._n_points)

        msg = _make_pc2(pts, frame_id="world", stamp=stamp)
        self._pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = SimObjectPCPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
