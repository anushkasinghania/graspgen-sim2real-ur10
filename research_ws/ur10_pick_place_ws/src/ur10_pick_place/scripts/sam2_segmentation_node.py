#!/usr/bin/env python3
"""
sam2_segmentation_node.py
--------------------------
Real-hardware replacement for sim_object_pc_publisher.

Pipeline:
  OAK-D Pro Wide RGB-D stream
       ↓
  User left-clicks target object in live RGB window
       ↓
  SAM2 segments → binary mask
       ↓
  Mask × depth → back-project to 3D using camera intrinsics K
       ↓
  Transform points from camera frame to world frame via TF
       ↓
  Publish PointCloud2 on /env_cam/points  ← same topic as sim

Usage:
  ros2 run ur10_pick_place sam2_segmentation_node \
    --ros-args \
    -p checkpoint:=$HOME/research_ws/segment-anything-2/checkpoints/sam2.1_hiera_small.pt \
    -p model_cfg:=configs/sam2.1/sam2.1_hiera_s.yaml

Per-pick workflow:
  1. Window shows live OAK-D Pro RGB stream
  2. Left-click on target object → green mask appears
  3. Right-click anywhere to clear mask and re-click
  4. Point cloud is published automatically after every new mask
  5. Trigger GraspGen: ros2 topic pub --once /graspgen/trigger std_msgs/msg/Empty "{}"

Parameters:
  checkpoint   (str) — path to SAM2 .pt checkpoint
  model_cfg    (str) — SAM2 model config yaml (relative to SAM2 package)
  depth_scale  (float, default 0.001) — depth image units to metres (1mm → 0.001)
  min_depth_m  (float, default 0.10)  — ignore depth below this (noise filter)
  max_depth_m  (float, default 2.00)  — ignore depth above this
  min_points   (int,   default 50)    — minimum valid 3-D points to publish
"""

import os
import threading
import warnings

# Force Qt to use X11/xcb backend — required on Jetson where Qt platform
# plugin is not auto-detected when launched as a subprocess.
os.environ.setdefault("QT_QPA_PLATFORM", "xcb")

import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
import torch

# SAM2 — suppress the torchvision.io warning that's harmless here
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from sam2.build_sam import build_sam2
    from sam2.sam2_image_predictor import SAM2ImagePredictor

# ROS2 message types
from cv_bridge import CvBridge
from geometry_msgs.msg import TransformStamped
from sensor_msgs.msg import Image, CameraInfo, PointCloud2, PointField
from std_msgs.msg import Header
import sensor_msgs_py.point_cloud2 as pc2
import tf2_ros


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_pc2(xyz_world: np.ndarray, frame_id: str, stamp) -> PointCloud2:
    """Build a PointCloud2 from an (N, 3) float32 array in world frame."""
    fields = [
        PointField(name="x", offset=0, datatype=PointField.FLOAT32, count=1),
        PointField(name="y", offset=4, datatype=PointField.FLOAT32, count=1),
        PointField(name="z", offset=8, datatype=PointField.FLOAT32, count=1),
    ]
    header = Header()
    header.frame_id = frame_id
    header.stamp = stamp
    return pc2.create_cloud(header, fields, xyz_world.tolist())


def _depth_to_cam_xyz(depth_img: np.ndarray, K: np.ndarray,
                      mask: np.ndarray,
                      depth_scale: float,
                      min_depth_m: float,
                      max_depth_m: float) -> np.ndarray:
    """
    Back-project masked depth pixels to 3-D camera-frame points.

    Parameters
    ----------
    depth_img  : (H, W) uint16 or float  — raw depth image
    K          : (3, 3) camera intrinsic matrix
    mask       : (H, W) bool            — SAM2 binary mask (True = object)
    depth_scale: float                  — multiply raw depth to get metres
    Returns
    -------
    xyz : (N, 3) float32 in camera frame
    """
    depth_m = depth_img.astype(np.float32) * depth_scale
    valid = mask & (depth_m > min_depth_m) & (depth_m < max_depth_m)

    rows, cols = np.where(valid)
    if rows.size == 0:
        return np.empty((0, 3), dtype=np.float32)

    z = depth_m[rows, cols]
    fx, fy = K[0, 0], K[1, 1]
    cx, cy = K[0, 2], K[1, 2]
    x = (cols - cx) * z / fx
    y = (rows - cy) * z / fy

    return np.column_stack([x, y, z]).astype(np.float32)


def _world_z_filter(xyz: np.ndarray, z_min: float, z_max: float) -> np.ndarray:
    """Remove points outside [z_min, z_max] in world Z (height above table)."""
    keep = (xyz[:, 2] >= z_min) & (xyz[:, 2] <= z_max)
    return xyz[keep]


def _statistical_outlier_removal(xyz: np.ndarray, k: int, std_multiplier: float) -> np.ndarray:
    """
    Pure-numpy statistical outlier removal (SOR).
    Each point's mean distance to its k nearest neighbours is computed.
    Points whose mean distance exceeds (global_mean + std_multiplier * global_std)
    are removed.  Falls back to the full cloud if too few points for SOR.
    """
    n = xyz.shape[0]
    if n < k + 1:
        return xyz

    # Compute pairwise squared distances in blocks to keep memory reasonable
    block = min(512, n)
    mean_dists = np.zeros(n, dtype=np.float32)
    for start in range(0, n, block):
        end = min(start + block, n)
        diff = xyz[start:end, None, :] - xyz[None, :, :]          # (b, n, 3)
        sq_d = (diff ** 2).sum(axis=-1)                            # (b, n)
        # Exclude self-distance (zero) by partitioning
        k_nearest = np.partition(sq_d, k + 1, axis=1)[:, 1:k + 1] # (b, k)
        mean_dists[start:end] = np.sqrt(k_nearest.mean(axis=1))

    threshold = mean_dists.mean() + std_multiplier * mean_dists.std()
    return xyz[mean_dists <= threshold]


def _apply_tf(xyz_cam: np.ndarray, tf_stamped: TransformStamped) -> np.ndarray:
    """Apply a TF transform (rotation + translation) to (N, 3) points."""
    t = tf_stamped.transform.translation
    r = tf_stamped.transform.rotation

    # quaternion → rotation matrix
    qx, qy, qz, qw = r.x, r.y, r.z, r.w
    R = np.array([
        [1 - 2*(qy*qy + qz*qz),   2*(qx*qy - qz*qw),   2*(qx*qz + qy*qw)],
        [  2*(qx*qy + qz*qw), 1 - 2*(qx*qx + qz*qz),   2*(qy*qz - qx*qw)],
        [  2*(qx*qz - qy*qw),   2*(qy*qz + qx*qw), 1 - 2*(qx*qx + qy*qy)],
    ], dtype=np.float64)
    translation = np.array([t.x, t.y, t.z], dtype=np.float64)

    return (xyz_cam.astype(np.float64) @ R.T + translation).astype(np.float32)


# ---------------------------------------------------------------------------
# Node
# ---------------------------------------------------------------------------

class SAM2SegmentationNode(Node):

    def __init__(self):
        super().__init__("sam2_segmentation_node")

        # Parameters
        self.declare_parameter("checkpoint", "")
        self.declare_parameter("model_cfg", "configs/sam2.1/sam2.1_hiera_s.yaml")
        self.declare_parameter("depth_scale", 0.001)   # OAK-D depth is in mm
        self.declare_parameter("min_depth_m", 0.10)
        self.declare_parameter("max_depth_m", 2.00)
        self.declare_parameter("min_points", 50)
        self.declare_parameter("fusion_radius_m", 0.25)  # keep wrist-cam pts within this radius of wrist_cam centroid
        # World-frame height filter: discard points on or below the tray surface and
        # above the maximum expected object height.  Keeps only the object body.
        # Trays sit on floor; floor surface at Z=0.00 m → pick_tray top = 0.00+0.12 = 0.12 m.
        self.declare_parameter("world_z_min_m", 0.12)   # just above pick_tray top surface
        self.declare_parameter("world_z_max_m", 0.65)   # above tallest expected object on tray
        # Statistical outlier removal: remove points whose mean neighbour distance
        # exceeds (mean + nb_std_dev * std) across all pairwise-approximate distances.
        self.declare_parameter("sor_neighbours", 20)    # k-neighbours to average
        self.declare_parameter("sor_std_dev", 1.5)      # std-dev multiplier threshold

        ckpt = self.get_parameter("checkpoint").value
        cfg  = self.get_parameter("model_cfg").value
        self._depth_scale    = self.get_parameter("depth_scale").value
        self._min_depth      = self.get_parameter("min_depth_m").value
        self._max_depth      = self.get_parameter("max_depth_m").value
        self._min_pts        = self.get_parameter("min_points").value
        self._fusion_radius  = self.get_parameter("fusion_radius_m").value
        self._world_z_min    = self.get_parameter("world_z_min_m").value
        self._world_z_max    = self.get_parameter("world_z_max_m").value
        self._sor_k          = self.get_parameter("sor_neighbours").value
        self._sor_std        = self.get_parameter("sor_std_dev").value

        if not ckpt or not os.path.isfile(ckpt):
            self.get_logger().fatal(
                f"SAM2 checkpoint not found: '{ckpt}'\n"
                "Pass: --ros-args -p checkpoint:=/path/to/sam2.1_hiera_small.pt"
            )
            raise SystemExit(1)

        # Load SAM2 model
        self.get_logger().info(f"Loading SAM2 from {ckpt} ...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.get_logger().info(f"SAM2 device: {device}")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model = build_sam2(cfg, ckpt, device=device)
            self._predictor = SAM2ImagePredictor(model)
        self.get_logger().info("SAM2 loaded.")

        # State — wrist_cam (primary camera — TF derived from robot FK, no manual calibration)
        self._bridge          = CvBridge()
        self._wrist_K         = None   # wrist_cam intrinsic matrix (3×3)
        self._wrist_cam_frame = None   # wrist_cam frame_id from CameraInfo
        self._wrist_depth     = None   # latest wrist_cam depth image
        self._wrist_rgb_img   = None   # latest wrist_cam BGR image (for display + SAM2)
        self._mask            = None   # current SAM2 binary mask (H×W bool) from pose-1 click
        self._click_pt        = None   # pending click (u, v, positive) or None
        self._lock            = threading.Lock()

        # Multi-view point cloud accumulation
        self._accumulated_cloud = None  # (N,3) float32, world frame — grows across scan poses
        self._scan_active       = False # True while executor is collecting poses 2,3 — gates display_cb publish
        self._arm_at_pose1      = False # True only after executor signals arm is at scan pose 1 — gates clicks

        # SAM2 runs in a background thread so the display timer (cv2.waitKey)
        # keeps firing at 30 Hz — this ensures every click is delivered by OpenCV.
        self._sam2_busy      = False  # True while SAM2 inference is running
        self._mask_dirty     = False  # True when SAM2 just updated mask → publish once

        # Last published object centroid in world frame (displayed in window)
        self._last_centroid   = None   # (x, y, z) float or None

        # TF
        self._tf_buffer   = tf2_ros.Buffer()
        self._tf_listener = tf2_ros.TransformListener(self._tf_buffer, self)

        # QoS — best effort matches OAK-D driver default
        best_effort = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
            depth=1,
        )

        # Subscribers — wrist_cam only (TF derived from robot FK — no manual calibration)
        self.create_subscription(Image, "/wrist_cam/rgb/image_raw",
                                 self._wrist_rgb_cb, best_effort)
        self.create_subscription(Image, "/wrist_cam/stereo/image_raw",
                                 self._wrist_depth_cb, best_effort)
        self.create_subscription(CameraInfo, "/wrist_cam/rgb/camera_info",
                                 self._wrist_info_cb, 10)

        # Control topics published by grasp_executor during multi-view scan
        from std_msgs.msg import Empty as EmptyMsg
        self.create_subscription(EmptyMsg, "/sam2/scan",
                                 self._scan_cb, 10)       # arm arrived at pose 2/3 → accumulate
        self.create_subscription(EmptyMsg, "/sam2/reset",
                                 self._reset_cb, 10)      # new pick → clear state
        self.create_subscription(EmptyMsg, "/sam2/arm_ready",
                                 self._arm_ready_cb, 10)  # arm at pose 1 → unlock clicks

        # Publisher — same topic as sim_object_pc_publisher
        self._pc_pub = self.create_publisher(PointCloud2, "/env_cam/points", 10)

        # OpenCV window — runs in main thread via timer
        self._window = "SAM2 - click target object (R=reset, Q=quit)"
        cv2.namedWindow(self._window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self._window, 960, 540)
        cv2.setMouseCallback(self._window, self._mouse_cb)

        # Display timer (10 Hz — reduced from 30 Hz to keep Jetson CPU/GPU load
        # manageable during SAM2 CUDA inference; 10 Hz is still smooth for clicking)
        self.create_timer(1.0 / 10.0, self._display_cb)

        self.get_logger().info(
            "SAM2 node ready.\n"
            "  Left-click  — segment target object\n"
            "  Right-click — add negative prompt (background)\n"
            "  R key       — reset mask / start over\n"
            "  Q key       — quit"
        )

    # ------------------------------------------------------------------
    # Callbacks
    # ------------------------------------------------------------------

    def _wrist_info_cb(self, msg: CameraInfo):
        if self._wrist_K is None:
            self._wrist_K = np.array(msg.k, dtype=np.float64).reshape(3, 3)
            self._wrist_cam_frame = msg.header.frame_id
            self.get_logger().info(
                f"Wrist-cam intrinsics received. frame_id='{self._wrist_cam_frame}'"
            )

    def _wrist_rgb_cb(self, msg: Image):
        bgr = self._bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        with self._lock:
            self._wrist_rgb_img = bgr

    def _wrist_depth_cb(self, msg: Image):
        enc = msg.encoding
        if enc in ("16UC1", "mono16"):
            depth = self._bridge.imgmsg_to_cv2(msg, desired_encoding="16UC1")
        elif enc in ("32FC1",):
            depth = self._bridge.imgmsg_to_cv2(msg, desired_encoding="32FC1")
        else:
            depth = self._bridge.imgmsg_to_cv2(msg)
        with self._lock:
            self._wrist_depth = depth

    def _mouse_cb(self, event, u, v, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            with self._lock:
                self._click_pt = (u, v, True)   # True = positive prompt
        elif event == cv2.EVENT_RBUTTONDOWN:
            with self._lock:
                self._click_pt = (u, v, False)  # False = negative prompt

    # ------------------------------------------------------------------
    # Display + SAM2 inference (runs in ROS2 timer → main thread)
    # ------------------------------------------------------------------

    def _display_cb(self):
        with self._lock:
            rgb            = self._wrist_rgb_img
            depth          = self._wrist_depth
            click          = self._click_pt
            mask           = self._mask
            centroid       = self._last_centroid
            scan_active    = self._scan_active
            arm_at_pose1   = self._arm_at_pose1
            n_acc          = 0 if self._accumulated_cloud is None else self._accumulated_cloud.shape[0]
            mask_dirty     = self._mask_dirty
            sam2_busy      = self._sam2_busy
            self._click_pt = None   # consume
            if mask_dirty:
                self._mask_dirty = False  # consume the dirty flag immediately

        if rgb is None:
            blank = np.zeros((540, 960, 3), dtype=np.uint8)
            cv2.putText(blank, "wrist_cam not ready — check T3 camera launch",
                        (20, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 100), 2)
            cv2.imshow(self._window, blank)
            cv2.waitKey(1)
            return

        # --- Gate clicks: only process when arm is confirmed at scan pose 1 ---
        if click is not None and arm_at_pose1 and not scan_active and self._wrist_K is not None:
            if not sam2_busy:
                # Camera is mounted upside-down: convert display-space click (on the
                # 180°-rotated image) back to raw image pixel coordinates for SAM2.
                h_img, w_img = rgb.shape[:2]
                u_d, v_d, positive = click
                click_raw = (w_img - 1 - u_d, h_img - 1 - v_d, positive)
                # Launch SAM2 inference in background so cv2.waitKey keeps firing at 30 Hz.
                with self._lock:
                    self._sam2_busy = True
                threading.Thread(
                    target=self._sam2_thread_fn,
                    args=(rgb, depth, click_raw),
                    daemon=True,
                ).start()
            # If busy (inference in progress), drop this click — user can re-click after mask appears.
        elif click is not None and not arm_at_pose1:
            self.get_logger().warn(
                "Click ignored — arm not at scan pose yet. Send /pick/start first."
            )

        # Publish pose-1 cloud: retry every display tick until centroid is set.
        # mask_dirty (one-shot after SAM2) triggers the first attempt; subsequent
        # ticks keep retrying while centroid is None, so transient TF timeouts,
        # momentary depth gaps, or first-attempt failures don't cause a 60 s abort.
        if (mask is not None and centroid is None and depth is not None
                and arm_at_pose1 and not scan_active):
            try:
                self._publish_pc_pose1(depth, mask)
            except Exception as e:
                self.get_logger().error(f"[pose-1] publish exception: {e}")

        # --- Render overlay ---
        # Camera is mounted upside-down: rotate display 180° so the user sees the
        # scene right-side-up and can click on the correct object.
        display = cv2.rotate(rgb.copy(), cv2.ROTATE_180)

        # Draw SAM2 mask when at pose 1 — also rotate mask to display space
        if mask is not None and arm_at_pose1 and not scan_active:
            display_mask = cv2.rotate(mask.astype(np.uint8), cv2.ROTATE_180).astype(bool)
            overlay = display.copy()
            overlay[display_mask] = [0, 200, 0]
            cv2.addWeighted(overlay, 0.4, display, 0.6, 0, display)
            contours, _ = cv2.findContours(
                display_mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(display, contours, -1, (0, 255, 0), 2)

        # Status bar (top)
        if scan_active:
            status = f"SCANNING poses 2/3 — {n_acc} pts accumulated — DO NOT CLICK"
            colour = (0, 165, 255)   # orange
        elif arm_at_pose1 and sam2_busy:
            status = "SAM2 PROCESSING... (2-5 s) — do not click again"
            colour = (0, 200, 255)   # yellow-ish — inference in progress
        elif arm_at_pose1 and mask is None:
            status = "ARM AT SCAN POSE — LEFT-CLICK the target object"
            colour = (0, 255, 0)     # green
        elif arm_at_pose1 and mask is not None:
            status = "Object selected — R=reset/reclick | waiting for scan to continue..."
            colour = (0, 255, 200)
        else:
            status = "Send /pick/start first — arm must move to scan pose before clicking"
            colour = (80, 80, 80)    # grey — blocked state

        # Semi-transparent dark bar at top
        cv2.rectangle(display, (0, 0), (display.shape[1], 38), (0, 0, 0), -1)
        cv2.addWeighted(display, 0.6, display, 0.4, 0, display)
        cv2.putText(display, status,
                    (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.62, colour, 2)

        # Centroid readout (bottom)
        if centroid is not None:
            cx, cy, cz = centroid
            cv2.putText(display,
                        f"Object centroid (world): x={cx:.3f}  y={cy:.3f}  z={cz:.3f} m  |  {n_acc} pts",
                        (10, display.shape[0] - 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.60, (0, 255, 255), 2)

        cv2.imshow(self._window, display)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == ord('Q'):
            self.get_logger().info("Q pressed — shutting down SAM2 node.")
            rclpy.shutdown()
        elif key == ord('r') or key == ord('R'):
            with self._lock:
                self._mask              = None
                self._accumulated_cloud = None
                self._last_centroid     = None
                self._scan_active       = False
                self._mask_dirty        = False
                self._sam2_busy         = False
                # Keep _arm_at_pose1 = True so user can re-click without re-triggering
            self.get_logger().info("Mask reset — re-click the target object.")

    def _sam2_thread_fn(self, bgr: np.ndarray, depth, click: tuple):
        """
        Background thread: run SAM2 inference so the display timer (cv2.waitKey)
        is never blocked.  Sets _mask_dirty = True when done so _display_cb
        publishes the cloud exactly once per new mask.
        """
        u, v, positive = click
        with self._lock:
            prev_mask = self._mask
        try:
            new_mask = self._run_sam2(bgr, u, v, positive, prev_mask)
            with self._lock:
                self._mask       = new_mask
                self._mask_dirty = True
        except Exception as e:
            self.get_logger().error(f"SAM2 inference failed: {e}")
        finally:
            with self._lock:
                self._sam2_busy = False

    def _reset_cb(self, _msg):
        """Executor signals start of new pick — clear all state."""
        with self._lock:
            self._mask              = None
            self._accumulated_cloud = None
            self._last_centroid     = None
            self._scan_active       = False
            self._arm_at_pose1      = False   # block clicks until arm_ready arrives
            self._mask_dirty        = False
            self._sam2_busy         = False
        self.get_logger().info("[sam2/reset] State cleared — waiting for arm to reach scan pose.")

    def _arm_ready_cb(self, _msg):
        """Executor signals arm has arrived at scan pose 1 — allow user to click."""
        with self._lock:
            self._arm_at_pose1 = True
        self.get_logger().info("[sam2/arm_ready] Arm at scan pose — click the target object now.")

    def _scan_cb(self, _msg):
        """
        Executor has arrived at an additional scan pose (2 or 3).
        Capture current wrist_cam depth, back-project, spatially filter around
        the pose-1 centroid, and accumulate into the growing cloud.
        Republishes the combined cloud to /env_cam/points.
        """
        with self._lock:
            depth    = self._wrist_depth
            K        = self._wrist_K
            frame    = self._wrist_cam_frame
            centroid = self._last_centroid
            acc      = self._accumulated_cloud
            self._scan_active = True

        if depth is None or K is None or frame is None:
            self.get_logger().warn("[sam2/scan] Wrist-cam depth not available yet — skipping.")
            return
        if centroid is None:
            self.get_logger().warn("[sam2/scan] No pose-1 centroid yet — did user click? Skipping.")
            return

        # Back-project all valid wrist-cam depth pixels (no mask — full frame)
        full_mask = np.ones(depth.shape, dtype=bool)
        xyz_cam = _depth_to_cam_xyz(depth, K, full_mask,
                                    self._depth_scale, self._min_depth, self._max_depth)
        if xyz_cam.shape[0] == 0:
            self.get_logger().warn("[sam2/scan] No valid depth pixels at this pose.")
            return

        # Transform to world frame using current robot FK TF
        try:
            tf_wrist = self._tf_buffer.lookup_transform(
                "world", frame, rclpy.time.Time(),
                timeout=rclpy.duration.Duration(seconds=0.5),
            )
        except (tf2_ros.LookupException, tf2_ros.ExtrapolationException,
                tf2_ros.ConnectivityException) as e:
            self.get_logger().warn(f"[sam2/scan] Wrist TF lookup failed: {e}")
            return

        xyz_world = _apply_tf(xyz_cam, tf_wrist)

        # Spatial filter: keep only points within fusion_radius of pose-1 centroid
        c = np.array(centroid, dtype=np.float32)
        dist = np.linalg.norm(xyz_world - c, axis=1)
        xyz_world = xyz_world[dist < self._fusion_radius]

        if xyz_world.shape[0] == 0:
            self.get_logger().warn("[sam2/scan] Spatial filter removed all points at this pose.")
            return

        # Height clamp — remove tray surface + ceiling noise
        xyz_world = _world_z_filter(xyz_world, self._world_z_min, self._world_z_max)

        # Accumulate
        if acc is not None:
            combined = np.vstack([acc, xyz_world])
        else:
            combined = xyz_world

        # SOR on full accumulated cloud
        combined = _statistical_outlier_removal(combined, self._sor_k, self._sor_std)

        with self._lock:
            self._accumulated_cloud = combined

        # Publish updated cloud so RViz shows progress
        stamp = self.get_clock().now().to_msg()
        pc_msg = _build_pc2(combined, frame_id="world", stamp=stamp)
        self._pc_pub.publish(pc_msg)

        self.get_logger().info(
            f"[sam2/scan] Accumulated {combined.shape[0]} pts total "
            f"(added {xyz_world.shape[0]} from this pose)."
        )

    # ------------------------------------------------------------------
    # SAM2 inference
    # ------------------------------------------------------------------

    def _run_sam2(self, bgr: np.ndarray, u: int, v: int, positive: bool,
                  prev_mask) -> np.ndarray:
        """
        Run SAM2 with a single click prompt.
        Returns binary mask (H, W, bool).
        """
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

        with torch.inference_mode():
            self._predictor.set_image(rgb)

            point_coords = np.array([[u, v]], dtype=np.float32)
            point_labels = np.array([1 if positive else 0], dtype=np.int32)

            masks, scores, _ = self._predictor.predict(
                point_coords=point_coords,
                point_labels=point_labels,
                multimask_output=True,
            )

        # Pick mask with highest score
        best = np.argmax(scores)
        mask = masks[best].astype(bool)

        label = "positive" if positive else "negative"
        self.get_logger().info(
            f"SAM2: {label} click ({u},{v}) → "
            f"mask pixels={mask.sum()}, score={scores[best]:.3f}"
        )
        return mask

    # ------------------------------------------------------------------
    # Point cloud publish
    # ------------------------------------------------------------------

    def _publish_pc_pose1(self, depth: np.ndarray, mask: np.ndarray):
        """
        Pose-1 point cloud: apply SAM2 mask to wrist_cam depth, back-project,
        height-filter, SOR, store as accumulated cloud, and publish.
        Called from _display_cb at 30 Hz while arm is stationary at scan pose 1.
        """
        if self._wrist_K is None or self._wrist_cam_frame is None:
            self.get_logger().warn_once(
                "Wrist-cam intrinsics not received yet — waiting for /wrist_cam/rgb/camera_info"
            )
            return

        # Back-project masked pixels using wrist_cam intrinsics
        xyz_cam = _depth_to_cam_xyz(
            depth, self._wrist_K, mask,
            self._depth_scale, self._min_depth, self._max_depth
        )
        if xyz_cam.shape[0] < self._min_pts:
            self.get_logger().warn(
                f"Only {xyz_cam.shape[0]} valid depth points in SAM2 mask — skipping."
            )
            return

        # Transform to world frame using robot FK TF (automatically correct — no manual calibration)
        try:
            tf_wrist = self._tf_buffer.lookup_transform(
                "world", self._wrist_cam_frame,
                rclpy.time.Time(),
                timeout=rclpy.duration.Duration(seconds=0.2),
            )
        except (tf2_ros.LookupException, tf2_ros.ExtrapolationException,
                tf2_ros.ConnectivityException) as e:
            self.get_logger().warn(
                f"Wrist-cam TF lookup failed: {e}\n"
                "Ensure ur_robot_driver is running and joint states are being published."
            )
            return

        # Debug: log the actual TF so we can verify/calibrate the camera mounting.
        # TF world→wrist_cam gives: translation = camera position in world frame,
        # rotation columns = camera X/Y/Z axes in world frame.
        r = tf_wrist.transform.rotation
        t = tf_wrist.transform.translation
        qx, qy, qz, qw = r.x, r.y, r.z, r.w
        # Column 0 = camera +X (image right) in world; col1 = camera +Y (image down) in world
        # Column 2 = camera +Z (depth direction) in world — should be ~(0,0,-1) looking down
        cam_x_world = (1-2*(qy*qy+qz*qz),   2*(qx*qy+qz*qw),   2*(qx*qz-qy*qw))
        cam_y_world = (  2*(qx*qy-qz*qw), 1-2*(qx*qx+qz*qz),   2*(qy*qz+qx*qw))
        cam_z_world = (  2*(qx*qz+qy*qw),   2*(qy*qz-qx*qw), 1-2*(qx*qx+qy*qy))
        self.get_logger().info(
            f"[TF debug] cam pos=({t.x:.3f},{t.y:.3f},{t.z:.3f})\n"
            f"  cam +X (img right) in world: ({cam_x_world[0]:.3f},{cam_x_world[1]:.3f},{cam_x_world[2]:.3f})\n"
            f"  cam +Y (img down)  in world: ({cam_y_world[0]:.3f},{cam_y_world[1]:.3f},{cam_y_world[2]:.3f})\n"
            f"  cam +Z (depth dir) in world: ({cam_z_world[0]:.3f},{cam_z_world[1]:.3f},{cam_z_world[2]:.3f}) "
            f"(should be ~(0,0,-1))"
        )

        xyz_world = _apply_tf(xyz_cam, tf_wrist)

        # Height clamp — remove tray surface + ceiling noise
        xyz_world = _world_z_filter(xyz_world, self._world_z_min, self._world_z_max)
        if xyz_world.shape[0] < self._min_pts:
            self.get_logger().warn(
                f"After height filter: {xyz_world.shape[0]} pts — object may be below z_min={self._world_z_min:.2f}m. "
                "Check world_z_min_m param or arm scan pose height."
            )
            return

        # SOR — remove depth noise spikes
        xyz_world = _statistical_outlier_removal(xyz_world, self._sor_k, self._sor_std)

        # Store as accumulated cloud and centroid
        centroid = xyz_world.mean(axis=0)
        with self._lock:
            self._accumulated_cloud = xyz_world
            self._last_centroid = (float(centroid[0]), float(centroid[1]), float(centroid[2]))

        # Publish so RViz + executor can detect that click has happened
        stamp = self.get_clock().now().to_msg()
        pc_msg = _build_pc2(xyz_world, frame_id="world", stamp=stamp)
        self._pc_pub.publish(pc_msg)

        self.get_logger().info(
            f"[pose-1] Published {xyz_world.shape[0]} pts, "
            f"centroid=({centroid[0]:.3f}, {centroid[1]:.3f}, {centroid[2]:.3f}) m"
        )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(args=None):
    rclpy.init(args=args)
    node = SAM2SegmentationNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
