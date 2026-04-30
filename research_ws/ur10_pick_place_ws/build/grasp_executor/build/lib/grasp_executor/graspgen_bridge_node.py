#!/usr/bin/env python3
"""
graspgen_bridge_node.py
-----------------------
Subscribes to /realsense_d435/points (sensor_msgs/PointCloud2), runs GraspGen
inference (generator + on-policy discriminator), and publishes the top-scoring
grasp as geometry_msgs/PoseStamped to /graspgen/grasp_pose.

Workflow:
  1. Send std_msgs/Empty to /graspgen/trigger to start inference.
  2. Bridge grabs the latest point cloud from /realsense_d435/points.
  3. Runs GraspGen inference (subsamples to 1024 pts, topk=5 grasps).
  4. Publishes best grasp to /graspgen/grasp_pose → picked up by grasp_executor_node.

Alternatively subscribe to /oakd_pro/points by remapping:
  ros2 run grasp_executor graspgen_bridge_node \
    --ros-args -r /realsense_d435/points:=/oakd_pro/points

GraspGen checkpoints:
  Generator:      ~/GraspDataGen/training_logs/robotiq_3f_gen/epoch_500.pth
  Discriminator:  ~/GraspDataGen/training_logs/robotiq_3f_disc_onpolicy/epoch_500.pth
  Gripper config: ~/research_ws/GraspGen/config/grippers/robotiq_3f.yaml

Status published to /graspgen/status (std_msgs/String):
  LOADING → READY → INFERRING → PUBLISHED / FAILED
"""

import os
import sys
import threading
import numpy as np

import rclpy
from rclpy.node import Node
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import Empty, String
import sensor_msgs_py.point_cloud2 as pc2


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

GRASPGEN_PATH = os.path.expanduser("~/research_ws/GraspGen")
GEN_CKPT = os.path.expanduser(
    "~/GraspDataGen/training_logs/robotiq_3f_gen_v3/epoch_500.pth"
)
DISC_CKPT = os.path.expanduser(
    "~/GraspDataGen/training_logs/robotiq_3f_disc_onpolicy_v3/epoch_500.pth"
)
GRIPPER_CFG = os.path.join(GRASPGEN_PATH, "config/grippers/robotiq_3f_infer.yaml")


# ---------------------------------------------------------------------------
# Rotation math
# ---------------------------------------------------------------------------

def _rot_to_quat(R: np.ndarray):
    """Convert 3×3 rotation matrix → (x, y, z, w) quaternion."""
    trace = R[0, 0] + R[1, 1] + R[2, 2]
    if trace > 0:
        s = 0.5 / np.sqrt(trace + 1.0)
        w = 0.25 / s
        x = (R[2, 1] - R[1, 2]) * s
        y = (R[0, 2] - R[2, 0]) * s
        z = (R[1, 0] - R[0, 1]) * s
    elif R[0, 0] > R[1, 1] and R[0, 0] > R[2, 2]:
        s = 2.0 * np.sqrt(1.0 + R[0, 0] - R[1, 1] - R[2, 2])
        w = (R[2, 1] - R[1, 2]) / s
        x = 0.25 * s
        y = (R[0, 1] + R[1, 0]) / s
        z = (R[0, 2] + R[2, 0]) / s
    elif R[1, 1] > R[2, 2]:
        s = 2.0 * np.sqrt(1.0 + R[1, 1] - R[0, 0] - R[2, 2])
        w = (R[0, 2] - R[2, 0]) / s
        x = (R[0, 1] + R[1, 0]) / s
        y = 0.25 * s
        z = (R[1, 2] + R[2, 1]) / s
    else:
        s = 2.0 * np.sqrt(1.0 + R[2, 2] - R[0, 0] - R[1, 1])
        w = (R[1, 0] - R[0, 1]) / s
        x = (R[0, 2] + R[2, 0]) / s
        y = (R[1, 2] + R[2, 1]) / s
        z = 0.25 * s
    return float(x), float(y), float(z), float(w)


# ---------------------------------------------------------------------------
# GraspGenBridgeNode
# ---------------------------------------------------------------------------

class GraspGenBridgeNode(Node):

    NUM_INPUT_POINTS = 1024   # GraspGen expects 1 k points
    TOPK_GRASPS = 5           # generate 5 candidates, publish best

    def __init__(self):
        super().__init__("graspgen_bridge_node")

        self._cb_group = ReentrantCallbackGroup()
        self._lock = threading.Lock()
        self._latest_pc: PointCloud2 = None
        self._running = False
        self._sampler = None

        # ---- Publishers ----
        self._grasp_pub = self.create_publisher(
            PoseStamped, "/graspgen/grasp_pose", 10
        )
        self._status_pub = self.create_publisher(
            String, "/graspgen/status", 10
        )

        # ---- Subscribers ----
        self.create_subscription(
            PointCloud2, "/env_cam/points",
            self._pc_callback, 10,
            callback_group=self._cb_group,
        )
        self.create_subscription(
            Empty, "/graspgen/trigger",
            self._trigger_callback, 10,
            callback_group=self._cb_group,
        )

        # Load models in background (import + checkpoint load takes ~10 s on Jetson)
        self._publish_status("LOADING")
        threading.Thread(target=self._load_models, daemon=True).start()
        self.get_logger().info(
            "GraspGenBridgeNode started. Loading models in background..."
        )

    # -----------------------------------------------------------------------

    def _load_models(self):
        # Add GraspGen repo to path
        if GRASPGEN_PATH not in sys.path:
            sys.path.insert(0, GRASPGEN_PATH)
        try:
            from grasp_gen.grasp_server import GraspGenSampler, load_grasp_cfg
            cfg = load_grasp_cfg(GRIPPER_CFG)
            # Override checkpoint paths if attributes exist on cfg
            if hasattr(cfg, "generator_checkpoint"):
                cfg.generator_checkpoint = GEN_CKPT
            if hasattr(cfg, "discriminator_checkpoint"):
                cfg.discriminator_checkpoint = DISC_CKPT
            self._sampler = GraspGenSampler(cfg)
            self.get_logger().info(
                "GraspGen models loaded. Publish Empty to /graspgen/trigger to run."
            )
            self._publish_status("READY")
        except Exception as exc:
            self.get_logger().error(f"Failed to load GraspGen models: {exc}")
            self._publish_status(f"LOAD_FAILED: {exc}")

    # -----------------------------------------------------------------------

    def _pc_callback(self, msg: PointCloud2):
        with self._lock:
            self._latest_pc = msg

    def _trigger_callback(self, _: Empty):
        with self._lock:
            if self._sampler is None:
                self.get_logger().warn("Models not ready yet — wait for READY status.")
                return
            if self._running:
                self.get_logger().warn("Inference already in progress, ignoring trigger.")
                return
            self._running = True
        threading.Thread(target=self._run_inference, daemon=True).start()

    # -----------------------------------------------------------------------

    def _run_inference(self):
        try:
            self._publish_status("INFERRING")

            with self._lock:
                pc_msg = self._latest_pc

            if pc_msg is None:
                self.get_logger().error("No point cloud received yet.")
                self._publish_status("FAILED: no point cloud")
                return

            # -- Convert PointCloud2 → Nx3 float32 numpy array --
            # read_points returns a structured array with named fields; unpack
            # each point as (x, y, z) explicitly to get a plain float32 Nx3 array.
            pts_raw = list(pc2.read_points(
                pc_msg, field_names=("x", "y", "z"), skip_nans=True
            ))
            pts = np.array([[p[0], p[1], p[2]] for p in pts_raw], dtype=np.float32)
            if len(pts) == 0:
                self.get_logger().error("Point cloud is empty after NaN filtering.")
                self._publish_status("FAILED: empty cloud")
                return
            if len(pts) < 50:
                self.get_logger().error(f"Too few valid points: {len(pts)}")
                self._publish_status("FAILED: too few points")
                return

            # -- Subsample to NUM_INPUT_POINTS --
            if len(pts) > self.NUM_INPUT_POINTS:
                idx = np.random.choice(len(pts), self.NUM_INPUT_POINTS, replace=False)
                pts = pts[idx]
            elif len(pts) < self.NUM_INPUT_POINTS:
                # Upsample with replacement to reach exactly 1024
                extra = self.NUM_INPUT_POINTS - len(pts)
                idx = np.random.choice(len(pts), extra, replace=True)
                pts = np.vstack([pts, pts[idx]])

            self.get_logger().info(
                f"Running GraspGen inference on {len(pts)} points ..."
            )

            # -- GraspGen inference --
            from grasp_gen.grasp_server import GraspGenSampler
            grasps, confidences = GraspGenSampler.run_inference(
                pts, self._sampler, topk_num_grasps=self.TOPK_GRASPS
            )

            if grasps is None or len(grasps) == 0:
                self.get_logger().error("GraspGen returned no grasps.")
                self._publish_status("FAILED: no grasps generated")
                return

            # -- Publish best grasp (index 0 = highest discriminator score) --
            # Move to CPU and convert to numpy (GraspGen returns CUDA tensors).
            import torch
            if isinstance(grasps, torch.Tensor):
                T = grasps[0].cpu().numpy()           # 4x4 SE(3) numpy array
            else:
                T = np.array(grasps[0])
            R = T[:3, :3]
            t = T[:3, 3]
            qx, qy, qz, qw = _rot_to_quat(R)

            pose = PoseStamped()
            pose.header.stamp = rclpy.time.Time().to_msg()   # time 0 = latest TF
            pose.header.frame_id = pc_msg.header.frame_id
            pose.pose.position.x = float(t[0])
            pose.pose.position.y = float(t[1])
            pose.pose.position.z = float(t[2])
            pose.pose.orientation.x = qx
            pose.pose.orientation.y = qy
            pose.pose.orientation.z = qz
            pose.pose.orientation.w = qw

            self._grasp_pub.publish(pose)
            if confidences is not None:
                c = confidences[0]
                conf = float(c.cpu().item() if hasattr(c, 'cpu') else c)
            else:
                conf = -1.0
            self._publish_status(f"PUBLISHED conf={conf:.3f}")
            self.get_logger().info(
                f"Grasp published: pos=({t[0]:.3f}, {t[1]:.3f}, {t[2]:.3f})"
                f"  conf={conf:.3f}  frame={pc_msg.header.frame_id}"
            )

        except Exception as exc:
            import traceback
            self.get_logger().error(
                f"Inference failed: {exc}\n{traceback.format_exc()}"
            )
            self._publish_status(f"FAILED: {exc}")

        finally:
            with self._lock:
                self._running = False

    # -----------------------------------------------------------------------

    def _publish_status(self, status: str):
        msg = String()
        msg.data = status
        self._status_pub.publish(msg)
        self.get_logger().info(f"[GRASPGEN STATUS] {status}")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main(args=None):
    rclpy.init(args=args)
    node = GraspGenBridgeNode()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
