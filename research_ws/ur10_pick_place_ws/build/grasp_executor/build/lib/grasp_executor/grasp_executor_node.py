#!/usr/bin/env python3
"""
grasp_executor_node.py
----------------------
Subscribes to /graspgen/grasp_pose (geometry_msgs/PoseStamped) published by
the GraspGen inference pipeline and executes a pick-and-place cycle:

  1. Move to pre-grasp pose  (10 cm above the grasp along the approach axis)
  2. Open Robotiq 3F gripper
  3. Move to grasp pose
  4. Close gripper
  5. Lift object 15 cm
  6. Move to place pose
  7. Open gripper

Motion planning strategy (matches reference pick_node.py pattern):
  - Subscribe to /joint_states for the CURRENT arm configuration.
  - For every Cartesian waypoint, call /compute_ik SEEDED with the current
    joint state.  KDL then finds the CLOSEST IK solution — naturally staying
    in the same elbow-up/down configuration rather than flipping arms.
  - Plan in JOINT SPACE to the resulting joint angles via MoveGroup action.
  - This avoids the OMPL "Unable to sample any valid states for goal tree"
    error that occurs when OMPL samples random EEF orientations and KDL
    cannot find collision-free solutions for most of them.

Gripper control uses the FollowJointTrajectory action served by
gripper_trajectory_controller.

Publishes status strings to /grasp_executor/status.

Hardware: UR10 arm + Robotiq 3F, ROS2 Humble (RViz + MoveIt only, no Gazebo).
Robot base mounted on table at z=1.015 m (world frame).
"""

import copy
import math
import threading
import time


def _normalize_joints_to_seed(joint_dict: dict, seed: dict) -> dict:
    """
    Wrap IK joint angles to be within ±π of the seed values.

    KDL returns kinematically equivalent solutions that may be ±2π away from
    the seed (e.g. lift=5.027 instead of -1.256).  OMPL sees these as requiring
    a full revolution and cannot plan a valid path in the allotted time.
    This normalisation keeps every joint within one half-turn of the seed so
    OMPL sees a short, local motion.
    """
    result = {}
    for name, angle in joint_dict.items():
        s = seed.get(name, 0.0)
        diff = angle - s
        # Wrap diff into (-π, π]
        diff = (diff + math.pi) % (2.0 * math.pi) - math.pi
        result[name] = s + diff
    return result

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.duration import Duration
from builtin_interfaces.msg import Duration as BuiltinDuration

import numpy as np

from geometry_msgs.msg import PoseStamped, Vector3
from sensor_msgs.msg import JointState, PointCloud2
import sensor_msgs_py.point_cloud2 as pc2_reader
from std_msgs.msg import String, Empty as EmptyMsg
from shape_msgs.msg import SolidPrimitive
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

from moveit_msgs.action import MoveGroup
from geometry_msgs.msg import Pose as GeoPose
from moveit_msgs.msg import (
    MotionPlanRequest,
    Constraints,
    JointConstraint,
    PositionConstraint,
    WorkspaceParameters,
    MoveItErrorCodes,
    PlanningOptions,
    PlanningScene,
    AllowedCollisionMatrix,
    AllowedCollisionEntry,
    CollisionObject,
    AttachedCollisionObject,
)
from geometry_msgs.msg import Point
from moveit_msgs.srv import GetPositionIK, ApplyPlanningScene

from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration as RosDuration


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ARM_GROUP = "ur10_manipulator"
GRIPPER_GROUP = "robotiq_gripper"

ARM_JOINTS = [
    "shoulder_pan_joint",
    "shoulder_lift_joint",
    "elbow_joint",
    "wrist_1_joint",
    "wrist_2_joint",
    "wrist_3_joint",
]

GRIPPER_JOINTS = [
    "robotiq_finger_a_joint_1",
    "robotiq_finger_b_joint_1",
    "robotiq_finger_c_joint_1",
]

GRIPPER_OPEN_POS  = 0.0495   # rad  (simulation JTC — fingers open)
GRIPPER_CLOSE_POS = 0.9      # rad  (simulation JTC — partial close)

# Home / ready pose — user-specified joint angles (degrees → radians).
# Matches the physical setup: arm clear of workspace, gripper facing workspace.
#   shoulder_pan=80°  shoulder_lift=-90°  elbow=69°
#   wrist_1=-69°      wrist_2=-90°        wrist_3=-15°
HOME_JOINTS = {
    "shoulder_pan_joint":  1.3963,   #  80°
    "shoulder_lift_joint": -1.5708,  # -90°
    "elbow_joint":          1.2043,  #  69°
    "wrist_1_joint":       -1.2043,  # -69°
    "wrist_2_joint":       -1.5708,  # -90°
    "wrist_3_joint":       -0.2618,  # -15°
}

# Wrist-cam multi-view scan poses (physically measured on teach pendant).
# Pose 1 (centre): wrist cam directly above pick tray, looking down.
# Pose 2 (left):   shoulder_pan +15° → camera shifted left, reveals left/front face.
# Pose 3 (right):  shoulder_pan -15° → camera shifted right, reveals right/back face.
# Only shoulder_pan changes — lift/elbow/wrist kept constant for safe motion.
#
# NOTE: pan=+85.5° is only 5.5° from home (pan=80°). Direct trajectory used — no OMPL.
SCAN_JOINTS = {                      # Pose 1 — centre top view (physically measured on teach pendant, 2026-04-30)
    "shoulder_pan_joint":  1.3122,   # +75.19°
    "shoulder_lift_joint": -1.7635,  # -101.06°
    "elbow_joint":          1.4432,  # +82.69°
    "wrist_1_joint":       -1.2795,  # -73.32°
    "wrist_2_joint":       -1.5636,  # -89.58°
    "wrist_3_joint":       -0.2465,  # -14.12°
}
SCAN_JOINTS_L = {                    # Pose 2 — wrist_cam tilt left  (wrist_2 +15° = -74.58°)
    "shoulder_pan_joint":  1.3122,   # same as pose 1 — only wrist_2 moves
    "shoulder_lift_joint": -1.7635,
    "elbow_joint":          1.4432,
    "wrist_1_joint":       -1.2795,
    "wrist_2_joint":       -1.3017,  # -74.58° = -89.58° + 15°
    "wrist_3_joint":       -0.2465,
}
SCAN_JOINTS_R = {                    # Pose 3 — wrist_cam tilt right (wrist_2 -15° = -104.58°)
    "shoulder_pan_joint":  1.3122,   # same as pose 1 — only wrist_2 moves
    "shoulder_lift_joint": -1.7635,
    "elbow_joint":          1.4432,
    "wrist_1_joint":       -1.2795,
    "wrist_2_joint":       -1.8255,  # -104.58° = -89.58° - 15°
    "wrist_3_joint":       -0.2465,
}

# Place zone — place_tray measured: centre (−0.4775, 0.662) in world/base_link frame.
# Yellow crate is on the LEFT side of the robot (−X direction).
# Yellow crate: lx=49.5 cm (X axis, LENGTH), ly=32.4 cm (Y axis, WIDTH), H=15 cm.
# centre X = −0.4775 m  (confirmed: planning_scene_setup.py x=−0.4775 is correct).
# Three slots spaced along Y (shorter axis, ly=0.324 → ±15 cm from centre).
PLACE_SLOTS = [
    (-0.4775, 0.662),  # slot 0 — CENTRE (real hw always lands here; first sim pick)
    (-0.4775, 0.512),  # slot 1 — near edge  (y centre − 0.15)
    (-0.4775, 0.812),  # slot 2 — far edge   (y centre + 0.15)
]

# Joint-space tolerance for IK plan goals (radians).
# Loose for hover/lift, tight for plunge — prevents Z-depth accumulation error.
LOOSE_TOL = 0.02    # faster planning, OK for approach/lift
TIGHT_TOL = 0.003   # consistent Z depth at grasp/place

# IK orientation: top-down approach — gripper Z pointing straight down.
# Quaternion for 180° around X: (x=1, y=0, z=0, w=0).
IK_ORIENTATION_X = 1.0
IK_ORIENTATION_Y = 0.0
IK_ORIENTATION_Z = 0.0
IK_ORIENTATION_W = 0.0

# Links allowed to touch the attached collision object (fingers + palm + wrist).
# Without this list, MoveIt would report self-collision as soon as the object
# is attached because every gripper link would collide with the can geometry.
GRIPPER_TOUCH_LINKS = [
    "robotiq_palm",
    "robotiq_finger_a_link_0", "robotiq_finger_a_link_1",
    "robotiq_finger_a_link_2", "robotiq_finger_a_link_3",
    "robotiq_finger_b_link_0", "robotiq_finger_b_link_1",
    "robotiq_finger_b_link_2", "robotiq_finger_b_link_3",
    "robotiq_finger_c_link_0", "robotiq_finger_c_link_1",
    "robotiq_finger_c_link_2", "robotiq_finger_c_link_3",
    "tool0", "wrist_3_link",
    # wrist_2_link: at a low grasp height (z=0.175 m above floor) the wrist
    # joints sit very close to the object top.  MoveIt's FCL detects a contact
    # between the attached cylinder and wrist_2_link in this compact configuration.
    # Including it here suppresses that false-positive so the start state is valid.
    "wrist_2_link",
]

# Trays sit directly on the floor (only the robot is on a 5 cm stand).
# Floor surface is at Z=0.00 m in world/base_link frame.
# pick_tray  top: 0.00 + 0.12 = 0.12 m   (brown cardboard, H=12 cm)
# place_tray top: 0.00 + 0.15 = 0.15 m   (yellow crate,   H=15 cm)
# Objects sit on pick tray: bottom at Z=0.12, centre at Z=0.12+height/2.
TABLE_TOP_Z = 0.120       # pick tray top surface (floor at Z=0, tray H=12 cm)
PLACE_TRAY_TOP_Z = 0.150  # place tray top surface (floor at Z=0, tray H=15 cm)

# Gripper geometry — tool0 down to robotiq_palm link (top of gripper body).
# Physical stack: 0.02 m adapter plate + 0.03 m FTS = 0.05 m total.
# FTS was previously omitted from the URDF → gripper 3 cm too low → tray collision.
# ur_to_robotiq_mount joint in ur.urdf now set to xyz="0 0 0.05" to match reality.
TOOL0_TO_PALM_Z = 0.050   # m — distance from tool0 down to robotiq_palm LINK (top of gripper body)

# Robotiq 3F palm body height: from robotiq_palm link (mount face) down to finger base.
# This is the rigid gripper housing. Fingers attach at the bottom of this body.
# tool0 → 5 cm → palm link (top) → 23 cm → finger base (actual grasp point)
# User physically measured total tool0→finger_base ≈ 28 cm → palm body = 28 - 5 = 23 cm
GRIPPER_PALM_HEIGHT = 0.230  # m — robotiq_palm link to finger attachment point

# Combined offset: tool0 down to the finger base (actual grasping point).
TOOL0_TO_FINGER_BASE_Z = TOOL0_TO_PALM_Z + GRIPPER_PALM_HEIGHT  # = 0.210 m

# Minimum clearance: finger base must stay this far above pick tray surface.
GRASP_CLEARANCE = 0.020   # m

# Minimum tool0 Z: finger base ≥ 2 cm above tray surface.
# finger_base_z = tool0_z - TOOL0_TO_FINGER_BASE_Z → tool0_z_min below.
GRASP_Z_MIN = TABLE_TOP_Z + GRASP_CLEARANCE + TOOL0_TO_FINGER_BASE_Z  # = 0.350 m

# ── TUNABLE GRASP HEIGHT OFFSET ──────────────────────────────────────────────
# Controls how high tool0 is above the object centre during the grasp.
# Formula: gz = obj_cz + GRASP_HEIGHT_OFFSET
#
# Physical meaning:
#   GRASP_HEIGHT_OFFSET = 0.21 m → finger base exactly at object centre (theoretical minimum)
#   GRASP_HEIGHT_OFFSET = 0.40 m → finger base 19 cm ABOVE object centre (very safe, start here)
#
# How to tune:
#   Start at 0.40 → gripper stops well above object → reduce by 0.05 each trial
#   Target range: 0.21–0.28 m (fingers wrap around object mid-height)
#
# ▶ EDIT THIS VALUE between trials ◀
GRASP_HEIGHT_OFFSET = 0.28   # m  ← TOOL0_TO_FINGER_BASE_Z (0.28m): finger base at object centre

# ── Cluttered pick scene — 6 real dataset objects ────────────────────────────
# FetchBench-style layout: target front-center, distractors surrounding it.
# All on pick tray (bottom at z=0.12 m), cz = 0.12 + height/2.
# Min surface gap between any pair: 6.6 cm (tin_can ↔ mug). No overlaps.
#
#   tin_can      r=37mm h=110mm  (0.60,  0.00, 0.175)  ← PICK TARGET
#   bottle_large r=30mm h=240mm  (0.60,  0.15, 0.240)  15 cm left,  tall
#   boba_tea_cup r=25mm h= 90mm  (0.75,  0.00, 0.165)  15 cm behind, short
#   mug          r=38mm h= 95mm  (0.50, -0.10, 0.168)  front-left,  wide
#   spray_bottle r=22mm h=200mm  (0.72,  0.15, 0.220)  behind-left, tall-narrow
#   small_can    r=32mm h= 70mm  (0.68, -0.15, 0.155)  right,       short
#
# GraspGen gets ONLY tin_can's PC (mirrors SAM2 segmentation in real hardware).
# All 5 distractors are MoveIt collision objects the arm plans around.

# Pick targets — objects that will be grasped and placed.
SCENE_PICK_OBJECTS = {
    "tin_can": (0.60, 0.00, 0.175, 0.037, 0.110),  # cz = 0.12 + 0.055
}

# Real GraspDataGen objects used as collision-only distractors (never picked).
# In real hardware these appear in the MoveIt scene from NVBlox depth mapping.
DISTRACTOR_OBJECTS = {
    "bottle_large": (0.60,  0.15, 0.240, 0.030, 0.240),  # cz = 0.12 + 0.120
    "boba_tea_cup": (0.75,  0.00, 0.165, 0.025, 0.090),  # cz = 0.12 + 0.045
    "mug":          (0.50, -0.10, 0.168, 0.038, 0.095),  # cz = 0.12 + 0.048
    "spray_bottle": (0.72,  0.15, 0.220, 0.022, 0.200),  # cz = 0.12 + 0.100
    "small_can":    (0.68, -0.15, 0.155, 0.032, 0.070),  # cz = 0.12 + 0.035
}

# PRE-GRASP height (sim only — real hardware computes this dynamically from point cloud).
# Sim objects rest on pick tray at z=0.12 (old sim reference); bottle_large top=0.360 m.
PRE_GRASP_Z_WORLD = 0.41   # sim: 5 cm above bottle_large top (0.360 m)


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _offset_pose(pose_stamped: PoseStamped, dz: float) -> PoseStamped:
    """Return a copy of *pose_stamped* translated by *dz* along world Z."""
    result = copy.deepcopy(pose_stamped)
    result.pose.position.z += dz
    return result


def _with_ik_orientation(pose_stamped: PoseStamped) -> PoseStamped:
    """Return a copy with orientation set to top-down (180° around X)."""
    result = copy.deepcopy(pose_stamped)
    result.pose.orientation.x = IK_ORIENTATION_X
    result.pose.orientation.y = IK_ORIENTATION_Y
    result.pose.orientation.z = IK_ORIENTATION_Z
    result.pose.orientation.w = IK_ORIENTATION_W
    return result


# ---------------------------------------------------------------------------
# GraspExecutorNode
# ---------------------------------------------------------------------------

class GraspExecutorNode(Node):

    def __init__(self):
        super().__init__("grasp_executor_node")

        self._cb_group = ReentrantCallbackGroup()

        # ---- Publishers ----
        self._status_pub = self.create_publisher(String, "/grasp_executor/status", 10)
        # Notify sim_pc_publisher to exclude a placed object from the point cloud.
        self._picked_pub = self.create_publisher(String, "/grasp_executor/picked_object", 10)
        # Re-trigger GraspGen automatically after each successful pick-and-place.
        self._trigger_pub = self.create_publisher(EmptyMsg, "/graspgen/trigger", 10)
        # SAM2 scan control: /sam2/reset clears state for new pick; /sam2/scan
        # signals that arm arrived at a new scan pose → accumulate wrist_cam frame.
        self._sam2_scan_pub     = self.create_publisher(EmptyMsg, "/sam2/scan",      10)
        self._sam2_reset_pub    = self.create_publisher(EmptyMsg, "/sam2/reset",     10)
        self._sam2_armready_pub = self.create_publisher(EmptyMsg, "/sam2/arm_ready", 10)
        # Event set when /env_cam/points is received (user has clicked in SAM2 window)
        self._pc_received_event = threading.Event()

        # ---- Subscribers ----
        self._grasp_sub = self.create_subscription(
            PoseStamped,
            "/graspgen/grasp_pose",
            self._grasp_callback,
            10,
            callback_group=self._cb_group,
        )

        # /pick/start — scan with wrist cam then trigger GraspGen inference.
        # Use this instead of publishing /graspgen/trigger directly.
        self._pick_start_sub = self.create_subscription(
            EmptyMsg,
            "/pick/start",
            self._pick_start_cb,
            10,
            callback_group=self._cb_group,
        )

        # Joint state subscriber — used to seed IK with current configuration.
        # Seeding KDL with the current joints makes it find the NEAREST solution,
        # naturally staying in the same elbow-up/down branch.
        self._current_joints: dict = {}
        self._joint_state_sub = self.create_subscription(
            JointState,
            "/joint_states",
            self._joint_state_callback,
            20,
            callback_group=self._cb_group,
        )

        # ---- Service clients ----
        # /compute_ik: resolve Cartesian pose → joint configuration
        self._ik_client = self.create_client(
            GetPositionIK, "/compute_ik",
            callback_group=self._cb_group,
        )
        # /apply_planning_scene: temporarily modify the ACM so OMPL can plan
        # a path that ends inside the pick object's collision volume (grasp step).
        self._apply_scene_client = self.create_client(
            ApplyPlanningScene, "/apply_planning_scene",
            callback_group=self._cb_group,
        )

        # ---- MoveGroup action client (arm planning+execution) ----
        self._move_group_client = ActionClient(
            self, MoveGroup, "/move_action",
            callback_group=self._cb_group,
        )

        # ---- Direct arm trajectory client (bypasses OMPL for scan poses) ----
        # Used exclusively in _scan_then_trigger for known-safe scan poses.
        # OMPL generates convoluted joint-space paths for large pan swings that
        # TOTPS turns into 60-80 s trajectories; MoveIt then cancels execution on
        # timeout.  Direct JTC sends a single-segment spline with an explicit,
        # physically reasonable duration and never times out incorrectly.
        self._arm_direct_client = ActionClient(
            self,
            FollowJointTrajectory,
            "/scaled_joint_trajectory_controller/follow_joint_trajectory",
            callback_group=self._cb_group,
        )

        # ---- Gripper JTC action client ----
        self._gripper_client = ActionClient(
            self,
            FollowJointTrajectory,
            "/gripper_trajectory_controller/follow_joint_trajectory",
            callback_group=self._cb_group,
        )

        # ---- real_hardware mode ----
        self.declare_parameter("real_hardware", False)
        self._real_hardware: bool = self.get_parameter("real_hardware").value
        self.get_logger().info(
            f"Mode: {'REAL HARDWARE' if self._real_hardware else 'SIMULATION'}"
        )

        # Latest segmented object point cloud (from SAM2 node via /oakd_pro/points).
        # Populated in real_hardware mode only; used to estimate object geometry.
        self._latest_pc: np.ndarray | None = None
        self._pc_lock = threading.Lock()

        if self._real_hardware:
            best_effort = QoSProfile(
                reliability=ReliabilityPolicy.BEST_EFFORT,
                durability=DurabilityPolicy.VOLATILE,
                depth=1,
            )
            self._pc_sub = self.create_subscription(
                PointCloud2, "/env_cam/points",
                self._pc_callback, best_effort,
                callback_group=self._cb_group,
            )
            self.get_logger().info(
                "Real hardware: subscribed to /env_cam/points for geometry estimation."
            )
            # Robotiq 3F gripper via TCP (activates now, deactivates on shutdown)
            from grasp_executor.robotiq_3f_gripper import RobotiqGripper3F
            self.declare_parameter("gripper_ip",   "192.168.1.105")
            self.declare_parameter("gripper_port",  502)
            g_ip   = self.get_parameter("gripper_ip").value
            g_port = self.get_parameter("gripper_port").value
            self.get_logger().info(f"Connecting to Robotiq 3F at {g_ip}:{g_port} ...")
            self._real_gripper = RobotiqGripper3F(ip=g_ip, port=g_port)
            ok = self._real_gripper.activate()
            if ok:
                self.get_logger().info("Robotiq 3F gripper activated.")
            else:
                self.get_logger().error(
                    "Gripper activation FAILED — check IP/cable and retry.")
        else:
            self._real_gripper = None

        # ---- State flags ----
        self._executing  = False
        self._home_done  = False   # auto-home runs once after servers ready
        self._placed_objects: set = set()   # tracks objects placed this session (sim)
        self._lock = threading.Lock()

        # Server readiness flags — polled by timer in executor context.
        self._move_group_ready = False
        self._gripper_ready    = False
        self._ik_ready         = False
        self._server_check_timer = self.create_timer(0.5, self._check_servers)

        self.get_logger().info(
            "GraspExecutorNode started. Will auto-home after servers ready, "
            "then wait for /graspgen/grasp_pose ..."
        )
        self._publish_status("IDLE")

    # -----------------------------------------------------------------------
    # Server readiness check (timer, runs in executor)
    # -----------------------------------------------------------------------

    def _check_servers(self):
        if not self._move_group_ready and self._move_group_client.server_is_ready():
            self._move_group_ready = True
            self.get_logger().info("MoveGroup action server is ready.")
        if not self._gripper_ready:
            if self._real_hardware:
                # TCP gripper — no ROS action server; mark ready immediately
                self._gripper_ready = True
                self.get_logger().info("Gripper: TCP mode (no action server needed).")
            elif self._gripper_client.server_is_ready():
                self._gripper_ready = True
                self.get_logger().info("Gripper action server is ready.")
        if not self._ik_ready and self._ik_client.service_is_ready():
            self._ik_ready = True
            self.get_logger().info("/compute_ik service is ready.")
        if self._move_group_ready and self._gripper_ready and self._ik_ready:
            self.destroy_timer(self._server_check_timer)
            # Auto-home: always move to the ready pose on startup so the arm
            # is in a known, consistent position regardless of where the
            # previous run left it.
            if not self._home_done:
                self._home_done = True
                threading.Thread(target=self._auto_home, daemon=True).start()

    # -----------------------------------------------------------------------
    # Auto-home on startup
    # -----------------------------------------------------------------------

    def _auto_home(self):
        """
        Move the arm to the ready pose immediately after all servers become
        available.  This guarantees a consistent starting position on every
        launch, regardless of where the previous run left the arm.

        Runs in a background thread (launched by _check_servers timer).
        Waits for /joint_states to be populated first.
        """
        self.get_logger().info("Auto-home: waiting for joint states ...")
        deadline = time.monotonic() + 15.0
        while time.monotonic() < deadline:
            if self._have_all_joints():
                break
            time.sleep(0.1)
        if not self._have_all_joints():
            self.get_logger().warn("Auto-home: joint states never arrived — skipping.")
            return

        self.get_logger().info("Auto-home: moving to ready pose ...")
        ok = self._move_to_joint_goal(HOME_JOINTS, tolerance=LOOSE_TOL)
        if ok:
            self.get_logger().info("Auto-home complete — arm is in ready pose.")
            self._publish_status("READY_HOME")
        else:
            self.get_logger().warn("Auto-home failed (arm may be in wrong position).")
        self._publish_status("IDLE")

    def _pick_start_cb(self, _msg):
        """
        /pick/start handler — runs the wrist-cam scan then triggers GraspGen.

        Multi-view wrist-cam scan sequence (wrist_cam only — no env_cam TF calibration needed):
          1. Reset SAM2 node state (clear previous pick)
          2. Move to SCAN_JOINTS (pose 1 — top view above tray)
          3. Wait up to 60 s for user to click object in SAM2 window
             (SAM2 publishes pose-1 cloud → _pc_received_event fires)
          4. Move to SCAN_JOINTS_L (pose 2 — wrist_2 tilt left -74.9°), signal SAM2
          5. Wait 2.5 s for SAM2 to capture wrist_cam depth at this pose
          6. Move to SCAN_JOINTS_R (pose 3 — wrist_2 tilt right -104.9°), signal SAM2
          7. Wait 2.5 s for SAM2 to capture wrist_cam depth at this pose
          8. Return to HOME_JOINTS
          9. Publish /graspgen/trigger → GraspGen infers on complete 3-view cloud
        """
        self.get_logger().info("[pick/start] Multi-view wrist-cam scan starting...")
        self._publish_status("SCANNING")
        threading.Thread(target=self._scan_then_trigger, daemon=True).start()

    def _scan_then_trigger(self):
        # Step 1 — clear SAM2 state from any previous pick
        self._pc_received_event.clear()
        self._sam2_reset_pub.publish(EmptyMsg())
        time.sleep(0.3)

        # Allow tray collisions globally (belt-and-suspenders with allow_objects below).
        self._set_pick_object_collision("pick_tray",  True)
        self._set_pick_object_collision("place_tray", True)

        # Objects excluded from OMPL's local planning context for every scan motion.
        # Using allow_objects (planning_scene_diff) is the reliable method — it
        # bypasses the global ACM and removes these objects from the planner's view
        # for each individual call, regardless of global scene state.
        #
        # Why floor? At SCAN_JOINTS (lift=-102.3°) the elbow dips to z≈0.05 m,
        # near the floor collision boundary (z=0). OMPL rejects intermediate
        # configurations where links touch the floor, creating an unsolvable problem.
        # The real arm never contacts the floor — the MoveIt model is conservative.
        #
        # Why trays? The upper arm (lift=-90°, z≈0.1 m) overlaps the tray z-range
        # (0–0.12 m) during the 165° pan sweep, causing false-positive collisions.
        SCAN_ALLOW = ["pick_tray", "place_tray", "floor"]

        # All scan motions use _move_direct_joints (bypasses OMPL/TOTPS entirely).
        # OMPL was generating 60-80 s trajectories for these motions; MoveIt then
        # cancelled execution on timeout. Direct JTC sends one cubic-spline segment
        # with an explicit duration — predictable, never causes a false timeout.
        #
        # pan=+85.5° is only 5.5° from HOME (80°). All scan motions are small.
        # Duration guide (works at UR speed slider ≥25%):
        #   HOME ↔ SCAN_JOINTS (≤15° per joint): 12 s
        #   Between scan poses (15° pan only):    10 s
        #
        # Scan poses are physically verified on teach pendant — no collision check needed.

        # Wait for arm direct controller before starting (guards against startup race)
        deadline = time.monotonic() + 10.0
        while time.monotonic() < deadline:
            if self._arm_direct_client.server_is_ready():
                break
            time.sleep(0.3)
        if not self._arm_direct_client.server_is_ready():
            self.get_logger().error("[scan] Arm direct controller not ready — aborting.")
            self._publish_status("FAILED: arm direct controller not ready")
            return

        try:
            # Move to scan pose 1 — shoulder_pan is only 5.5° from home (80°→85.5°).
            # lift/elbow/wrist changes are all ≤15°. No intermediate via-point needed.
            self.get_logger().info(
                "[scan] Moving to scan pose 1 (pan=+85.5°, 12 s)...")
            ok = self._move_direct_joints(SCAN_JOINTS, duration_sec=12.0)
            if not ok:
                self.get_logger().error("[scan] Scan pose 1 motion failed — aborting.")
                self._publish_status("FAILED: scan pose 1 failed")
                return

            time.sleep(0.5)

            # Signal SAM2 node: arm is now at scan pose — clicks are now valid
            self._sam2_armready_pub.publish(EmptyMsg())
            self.get_logger().info(
                "[scan] Arm at pose 1 — SAM2 unlocked. Waiting for user click (60 s)...")

            # Wait for user click (up to 60 s)
            self._publish_status("WAITING FOR CLICK")
            clicked = self._pc_received_event.wait(timeout=60.0)
            if not clicked:
                self.get_logger().error("[scan] No user click in 60 s — aborting.")
                self._publish_status("FAILED: click timeout")
                return
            self.get_logger().info("[scan] Click received — pose-1 cloud ready.")

            # Pose 2 — wrist_cam tilt left: wrist_2 +15° → -74.9° (only wrist moves)
            self.get_logger().info("[scan] Moving to scan pose 2 (wrist_2=-74.9°, 5 s)...")
            self._publish_status("SCANNING L")
            ok = self._move_direct_joints(SCAN_JOINTS_L, duration_sec=5.0)
            if ok:
                time.sleep(0.5)
                self._sam2_scan_pub.publish(EmptyMsg())
                self.get_logger().info("[scan] Pose 2 — accumulating wrist_cam (2.5 s)...")
                time.sleep(2.5)
            else:
                self.get_logger().warn("[scan] Pose 2 motion failed — skipping left view.")

            # Pose 3 — wrist_cam tilt right: wrist_2 -15° → -104.9° (only wrist moves)
            self.get_logger().info("[scan] Moving to scan pose 3 (wrist_2=-104.9°, 5 s)...")
            self._publish_status("SCANNING R")
            ok = self._move_direct_joints(SCAN_JOINTS_R, duration_sec=5.0)
            if ok:
                time.sleep(0.5)
                self._sam2_scan_pub.publish(EmptyMsg())
                self.get_logger().info("[scan] Pose 3 — accumulating wrist_cam (2.5 s)...")
                time.sleep(2.5)
            else:
                self.get_logger().warn("[scan] Pose 3 motion failed — skipping right view.")

            time.sleep(0.5)

            # Return home — reverse of approach (small joint changes, 12 s)
            self.get_logger().info("[scan] Returning to home (12 s)...")
            self._move_direct_joints(HOME_JOINTS, duration_sec=12.0)

            # Trigger GraspGen on the complete accumulated cloud
            self.get_logger().info("[scan] All scan poses done — triggering GraspGen inference...")
            self._trigger_pub.publish(EmptyMsg())
            self._publish_status("IDLE")

        finally:
            # Always restore tray ACM — trays must block arm during grasp approach
            self._set_pick_object_collision("pick_tray",  False)
            self._set_pick_object_collision("place_tray", False)

    def _joint_state_callback(self, msg: JointState):
        for name, pos in zip(msg.name, msg.position):
            self._current_joints[name] = pos

    def _have_all_joints(self) -> bool:
        return all(n in self._current_joints for n in ARM_JOINTS)

    def _find_pick_object(self, gx: float, gy: float) -> str:
        """Return the nearest UNPLACED scene object ID to the grasp XY position."""
        best_id = None
        best_dist = float("inf")
        for obj_id, (cx, cy, *_) in SCENE_PICK_OBJECTS.items():
            if obj_id in self._placed_objects:
                continue   # skip already-placed objects
            d = math.sqrt((gx - cx) ** 2 + (gy - cy) ** 2)
            if d < best_dist:
                best_dist = d
                best_id = obj_id
        if best_id is None:
            # All placed — fallback (should not happen; caller checks remaining)
            best_id = next(iter(SCENE_PICK_OBJECTS))
            best_dist = 0.0
        self.get_logger().info(
            f"Nearest unplaced object to grasp ({gx:.3f}, {gy:.3f}): "
            f"'{best_id}' dist={best_dist:.3f} m  "
            f"(placed: {sorted(self._placed_objects)})"
        )
        return best_id

    # -----------------------------------------------------------------------
    # Point cloud callback + geometry estimation (real hardware only)
    # -----------------------------------------------------------------------

    def _pc_callback(self, msg: PointCloud2):
        """Store latest segmented object cloud (from SAM2 node) as (N,3) array."""
        pts = list(pc2_reader.read_points(
            msg, field_names=("x", "y", "z"), skip_nans=True))
        if pts:
            arr = np.array(pts)
            # read_points returns structured array; unpack named fields
            if arr.dtype.names:
                arr = np.column_stack([arr["x"], arr["y"], arr["z"]])
            with self._pc_lock:
                self._latest_pc = arr.astype(np.float32)
            # Signal _scan_then_trigger that the user has clicked (pose-1 cloud received)
            self._pc_received_event.set()

    def _estimate_object_geometry(self):
        """
        Estimate bounding cylinder of the target object from the latest point cloud.

        Uses robust statistics (percentiles) to reject outlier points from
        depth noise or partial occlusion.

        Returns (cx, cy, cz, radius, height) in world frame, or None if no cloud.
          cx, cy : XY centre of the object (median of cloud XY)
          cz     : Z centre = (z5 + z95) / 2
          radius : 90th-percentile XY distance from centre (outer bound)
          height : z95 - z5  (visible height; may be less than physical height
                   if camera can't see the bottom — use conservatively)
        """
        with self._pc_lock:
            pc = self._latest_pc
        if pc is None or len(pc) < 20:
            self.get_logger().warn(
                "Object geometry estimation: no point cloud received yet. "
                "Make sure SAM2 node has clicked the object and published /oakd_pro/points."
            )
            return None

        x, y, z = pc[:, 0], pc[:, 1], pc[:, 2]
        cx = float(np.median(x))
        cy = float(np.median(y))
        z95 = float(np.percentile(z, 95))
        # Pin cylinder bottom to tray surface (TABLE_TOP_Z) rather than using z5
        # from the cloud.  The wrist camera looks straight down and sees mostly the
        # object top; stereo depth near the object-tray boundary is noisy, so z5
        # often lands 1-3 cm above the tray, making the cylinder float in RViz.
        # Pinning to the known tray surface ensures the collision shape sits correctly.
        z_bottom = TABLE_TOP_Z
        height = max(0.03, z95 - z_bottom)    # at least 3 cm
        cz     = z_bottom + height / 2.0      # centre between tray surface and cloud top
        dists  = np.sqrt((x - cx)**2 + (y - cy)**2)
        radius = float(np.percentile(dists, 90))
        radius = max(0.02, radius)             # at least 2 cm

        self.get_logger().info(
            f"Estimated object: centre=({cx:.3f},{cy:.3f},{cz:.3f}) "
            f"r={radius:.3f}m h={height:.3f}m  (from {len(pc)} cloud points)"
        )
        return (cx, cy, cz, radius, height)

    def _add_object_to_scene(self, obj_id: str,
                             cx: float, cy: float, cz: float,
                             radius: float, height: float):
        """Add (or replace) a cylinder collision object in the MoveIt scene."""
        co = CollisionObject()
        co.id = obj_id
        co.header.frame_id = "world"
        co.header.stamp = rclpy.time.Time().to_msg()
        co.primitives.append(
            SolidPrimitive(type=SolidPrimitive.CYLINDER,
                           dimensions=[height, radius]))
        p = GeoPose()
        p.position.x = cx
        p.position.y = cy
        p.position.z = cz
        p.orientation.w = 1.0
        co.primitive_poses.append(p)
        co.operation = CollisionObject.ADD

        scene = PlanningScene()
        scene.is_diff = True
        scene.world.collision_objects.append(co)
        req = ApplyPlanningScene.Request()
        req.scene = scene
        future = self._apply_scene_client.call_async(req)
        ok = self._wait_future(future, timeout_sec=5.0)
        if ok:
            self.get_logger().info(
                f"Added '{obj_id}' to MoveIt scene at "
                f"({cx:.3f},{cy:.3f},{cz:.3f}) r={radius:.3f}m h={height:.3f}m"
            )
        else:
            self.get_logger().warn(f"Failed to add '{obj_id}' to scene (timeout).")

    # -----------------------------------------------------------------------
    # Subscription callback
    # -----------------------------------------------------------------------

    def _grasp_callback(self, msg: PoseStamped):
        with self._lock:
            if self._executing:
                self.get_logger().warn("Already executing — ignoring new pose.")
                return
            self._executing = True
        thread = threading.Thread(
            target=self._execute_grasp_sequence, args=(msg,), daemon=True
        )
        thread.start()

    # -----------------------------------------------------------------------
    # Main pick-and-place sequence
    # -----------------------------------------------------------------------

    def _execute_grasp_sequence(self, grasp_pose: PoseStamped):
        try:
            self._publish_status("EXECUTING")
            grasp_pose.header.stamp = rclpy.time.Time().to_msg()
            if not grasp_pose.header.frame_id:
                grasp_pose.header.frame_id = "world"

            # Wait for all services/actions and joint states
            deadline = time.monotonic() + 30.0
            while time.monotonic() < deadline:
                if (self._move_group_ready and self._gripper_ready
                        and self._ik_ready and self._have_all_joints()):
                    break
                time.sleep(0.1)
            if not (self._move_group_ready and self._gripper_ready
                    and self._ik_ready):
                self._publish_status("FAILED: servers not ready")
                return
            if not self._have_all_joints():
                self._publish_status("FAILED: no joint states received")
                return

            # ── Real hardware: estimate object geometry from SAM2 point cloud ──────
            if self._real_hardware:
                obj_geom = self._estimate_object_geometry()
                if obj_geom is None:
                    self._publish_status(
                        "FAILED: no point cloud — click object in SAM2 window first")
                    return
                obj_cx, obj_cy, obj_cz, obj_radius, obj_height = obj_geom
                PICK_OBJECT_ID = "real_target"
                # Add the estimated object to MoveIt scene so it participates in
                # collision checking during lift and place.
                self._add_object_to_scene(
                    PICK_OBJECT_ID, obj_cx, obj_cy, obj_cz, obj_radius, obj_height)
                # PRE_GRASP_Z: 5 cm clearance above estimated object top.
                # Hard floor at 0.65 m — IK is reliable at this height (confirmed empirically);
                # below ~0.60 m KDL converges to a wrong local minimum (elbow≈2.1 rad, wrong FK).
                pre_grasp_z = max(0.65, obj_cz + obj_height / 2.0 + 0.05)
            else:
                obj_geom = None
                pre_grasp_z = PRE_GRASP_Z_WORLD   # sim constant (0.41 m)

            # ACM: only allow pick-object collisions now (needed so IK/planner can
            # approach it in step 1b). Trays are kept as collision obstacles during
            # approach — OMPL must route AROUND the tray, not through it.
            # pick_tray/place_tray ACM will be enabled just before grasp/place descent.
            if self._real_hardware:
                self._set_pick_object_collision(PICK_OBJECT_ID, True)
            else:
                for _d in DISTRACTOR_OBJECTS:
                    self._set_pick_object_collision(_d, True)
                for _p in SCENE_PICK_OBJECTS:
                    self._set_pick_object_collision(_p, True)

            # 1a. Move to ready pose (arm pointing straight up — clear of workspace).
            # Robot is floor-mounted at z=0; objects at z≈0.90–0.97 m (on 0.85 m table).
            # From arm-up ready pose, jumping to pre-grasp at z=1.10 is only ~0.2 m
            # downward — KDL handles this without a forward-look intermediate step.
            self.get_logger().info("Step 1a: moving to ready pose (joint goal)")
            # Step 1a allow_objects: remove only pick-object and previously-placed
            # objects so the arm can swing to home freely without being blocked by
            # the estimated pick-object geometry. Trays remain as collision obstacles.
            if self._real_hardware:
                all_scene = [PICK_OBJECT_ID]
            else:
                all_scene = (list(SCENE_PICK_OBJECTS.keys())
                             + list(DISTRACTOR_OBJECTS.keys())
                             + list(self._placed_objects))
            if not self._move_to_joint_goal(HOME_JOINTS, tolerance=LOOSE_TOL,
                                            allow_objects=all_scene):
                self._publish_status("FAILED: ready pose motion failed")
                return

            # 1b. Move to pre-grasp: fixed world Z=PRE_GRASP_Z_WORLD, XY from grasp pose.
            # Strategy: compute expected shoulder pan from grasp XY so KDL converges
            # to a forward-hemisphere solution instead of a backward one.
            # avoid_collisions=False prevents IK rejection from nearby scene objects
            # (e.g. bottle_large's collision sphere next to the target XY).
            # After IK we validate pan is within ±π/2 of expected; if not, retry with
            # a perturbed "forward-reach" seed that guides KDL away from the backward branch.
            pre_grasp = copy.deepcopy(grasp_pose)
            pre_grasp.pose.position.z = pre_grasp_z   # sim: 0.41m  real: estimated
            pre_grasp = _with_ik_orientation(pre_grasp)

            gx = grasp_pose.pose.position.x
            gy = grasp_pose.pose.position.y
            gz = grasp_pose.pose.position.z

            # Sanity check: grasp must be reachable (within arm reach ≈1.5m, above floor).
            # Real hardware: world=base_link (identity TF confirmed).
            # pick_tray centred at (0.00, 0.655) — X=0 (centred), Y=65.5 cm forward.
            # Near edge Y=0.32 m, far edge Y=0.99 m (0.99 = near_edge + tray_depth, NOT centre).
            # Floor at Z=0.00 m (robot on 5 cm stand). Tray top at Z=0.12 m.
            reach_sq = gx * gx + gy * gy
            if not (reach_sq < 1.5**2 and gz > -0.04 and gz < 0.80):
                self._publish_status(
                    f"FAILED: grasp pose ({gx:.3f},{gy:.3f},{gz:.3f}) out of arm reach"
                    " — check wrist_cam depth / SAM2 mask quality")
                return

            # Clamp grasp Z so finger base stays ≥ GRASP_CLEARANCE (2 cm) above the tray.
            # finger_base_z = gz - TOOL0_TO_FINGER_BASE_Z → minimum gz = GRASP_Z_MIN = 0.350 m.
            # GraspGen can output poses near the object bottom — this prevents fingers hitting tray.
            if gz < GRASP_Z_MIN:
                self.get_logger().warn(
                    f"GraspGen gz={gz:.3f} < GRASP_Z_MIN={GRASP_Z_MIN:.3f} "
                    f"(finger base would be {TABLE_TOP_Z + GRASP_CLEARANCE - (gz - TOOL0_TO_FINGER_BASE_Z):.3f} m below tray clearance) "
                    f"— clamping to {GRASP_Z_MIN:.3f}")
                gz = GRASP_Z_MIN
                grasp_pose.pose.position.z = gz

            # Ensure finger base is at object centre height so fingers grasp mid-object.
            # Full offset: tool0 → 5 cm (adapter+FTS) → palm link → 16 cm (palm body) → finger base.
            # gz_obj_min positions the finger base at obj_cz (object centre) so fingers
            # wrap around the object from the sides rather than reaching below it.
            # TOOL0_TO_FINGER_BASE_Z = 0.21 m accounts for both adapter+FTS and palm body.
            # Only applies in real_hardware mode where obj_cz is known from point cloud.
            if self._real_hardware and obj_geom is not None:
                gz_obj_min = obj_cz + GRASP_HEIGHT_OFFSET
                if gz < gz_obj_min:
                    self.get_logger().warn(
                        f"GraspGen gz={gz:.3f} raised to gz_obj_min={gz_obj_min:.3f} "
                        f"(obj_cz={obj_cz:.3f} + GRASP_HEIGHT_OFFSET={GRASP_HEIGHT_OFFSET:.3f}) "
                        f"— applying tunable grasp height offset")
                    gz = gz_obj_min
                    grasp_pose.pose.position.z = gz

            # Ensure pre_grasp_z is above gz — after all gz clamps are applied.
            # pre_grasp_z was computed from object geometry before gz was raised,
            # so it can end up BELOW gz (arm would go up instead of down during descent).
            pre_grasp_z = max(pre_grasp_z, gz + 0.05)

            # Compute expected shoulder_pan to seed IK.
            # Real hardware: world = base_link (confirmed identity TF). Standard formula:
            #   expected_pan = atan2(world_y, world_x)
            # Real pick_tray centred at (0.00, 0.655) → expected_pan = atan2(0.655, 0) = 90°.
            # NOTE: simulation assumed yaw=-π/2 rotation (tray at +X); that was sim-only.
            expected_pan = math.atan2(gy, gx)
            # Clamp to the forward hemisphere (arm can reach 60°-160° for this robot layout)
            expected_pan = max(math.radians(60), min(math.radians(160), expected_pan))

            self.get_logger().info(
                f"Step 1b: GraspGen pose world=({gx:.3f},{gy:.3f},{gz:.3f}) "
                f"pre_grasp_z={pre_grasp_z:.3f} expected_pan={math.degrees(expected_pan):.1f}°")

            # IK seed mimicking real scan configuration (arm was just here).
            # wrist_2=-1.5708 (-90°) matches the real arm — critical for KDL
            # to find the correct branch (wrong wrist_2 seed → bad solutions).
            seed_reach = {
                "shoulder_pan_joint":  expected_pan,
                "shoulder_lift_joint": -1.8,
                "elbow_joint":          1.5,
                "wrist_1_joint":       -1.5,
                "wrist_2_joint":       -1.5708,  # -90° — match real hardware
                "wrist_3_joint":        0.0,
            }

            def _ik_valid(joints):
                """Reject solutions where arm points wrong way or bends backward."""
                if joints is None:
                    return False
                pan  = joints.get("shoulder_pan_joint", 0.0)
                lift = joints.get("shoulder_lift_joint", 0.0)
                pan_ok  = abs(pan - expected_pan) <= math.pi / 3  # ±60°
                # Lift must be negative: arm must slope forward+down toward tray.
                # lift > -0.3 rad (-17°) means arm is nearly horizontal or upward
                # — that is the wrong elbow branch (arm going backward over robot).
                lift_ok = lift < -0.3
                if not pan_ok:
                    self.get_logger().warn(
                        f"IK: pan={math.degrees(pan):.1f}° bad "
                        f"(expected {math.degrees(expected_pan):.1f}°, "
                        f"diff={math.degrees(abs(pan-expected_pan)):.1f}°)")
                if not lift_ok:
                    self.get_logger().warn(
                        f"IK: lift={math.degrees(lift):.1f}° bad (must be < -17°)")
                return pan_ok and lift_ok

            joints_1b = None
            # Attempt 1: collision-aware IK seeded from HOME (closest standard config)
            seed_fwd = dict(HOME_JOINTS)
            seed_fwd["shoulder_pan_joint"] = expected_pan
            self.get_logger().info("IK attempt 1: collision-aware, HOME seed")
            j = self._call_ik(pre_grasp, avoid_collisions=True, seed_joints=seed_fwd)
            if _ik_valid(j):
                joints_1b = j
            # Attempt 2: collision-aware IK with forward-reach seed
            if joints_1b is None:
                self.get_logger().info("IK attempt 2: collision-aware, reach seed")
                j = self._call_ik(pre_grasp, avoid_collisions=True, seed_joints=seed_reach)
                if _ik_valid(j):
                    joints_1b = j
            # Attempt 3: collision-free IK with forward-reach seed
            if joints_1b is None:
                self.get_logger().info("IK attempt 3: collision-free, reach seed")
                j = self._call_ik(pre_grasp, avoid_collisions=False, seed_joints=seed_reach)
                if _ik_valid(j):
                    joints_1b = j
            # Attempt 4: collision-free IK seeded from SCAN_JOINTS (arm was just there)
            if joints_1b is None:
                scan_seed = dict(SCAN_JOINTS)
                scan_seed["shoulder_pan_joint"] = expected_pan
                self.get_logger().info("IK attempt 4: collision-free, SCAN_JOINTS seed")
                j = self._call_ik(pre_grasp, avoid_collisions=False, seed_joints=scan_seed)
                if _ik_valid(j):
                    joints_1b = j

            if joints_1b is None:
                self._publish_status("FAILED: pre-grasp IK — all 4 attempts failed")
                return

            # Step 1b allow_objects: remove only the pick target from the planning diff.
            # Keep trays as collision obstacles so OMPL routes ABOVE the tray,
            # not through it. Removing pick_tray/place_tray here was previously
            # allowing the arm to swing through the tray during approach.
            if self._real_hardware:
                pre_grasp_allow = ["real_target"]
            else:
                pre_grasp_allow = (list(SCENE_PICK_OBJECTS.keys())
                                   + list(DISTRACTOR_OBJECTS.keys())
                                   + list(self._placed_objects))
            if not self._move_to_joint_goal(joints_1b, tolerance=LOOSE_TOL,
                                            allow_objects=pre_grasp_allow):
                self._publish_status("FAILED: pre-grasp motion failed")
                return

            # 2. Open gripper
            self.get_logger().info("Step 2: opening gripper")
            if not self._set_gripper(GRIPPER_OPEN_POS):
                self._publish_status("FAILED: gripper open failed")
                return

            # 3. Move to grasp pose — the gripper intentionally enters the pick
            # object's collision zone.  Pass allow_objects so the planner uses a
            # temporary scene diff (PlanningOptions.planning_scene_diff) that
            # removes the pick object for THIS call only.  Global scene unchanged.
            # TIGHT_TOL ensures repeatable Z depth.
            if self._real_hardware:
                # Real hardware: PICK_OBJECT_ID already set above from geometry estimation.
                # Use GraspGen's pose directly — camera calibration gives accurate position.
                # The point cloud centre may differ slightly from GraspGen's output;
                # trust GraspGen for grasp XY/Z (that is what GraspGen is trained for).
                self.get_logger().info(
                    f"Real hardware: using GraspGen pose directly at "
                    f"({grasp_pose.pose.position.x:.3f}, "
                    f"{grasp_pose.pose.position.y:.3f}, "
                    f"{grasp_pose.pose.position.z:.3f})"
                )
                grasp_allow = [PICK_OBJECT_ID, "pick_tray", "place_tray"]
            else:
                # Simulation: identify nearest known object, snap to its centre.
                # GraspGen's returned XY in sim can be offset from object centre;
                # snapping ensures the arm descends to the correct location.
                PICK_OBJECT_ID = self._find_pick_object(
                    grasp_pose.pose.position.x, grasp_pose.pose.position.y
                )
                cx, cy, cz, _, _ = SCENE_PICK_OBJECTS[PICK_OBJECT_ID]
                grasp_pose.pose.position.x = cx
                grasp_pose.pose.position.y = cy
                grasp_pose.pose.position.z = cz
                self.get_logger().info(
                    f"Sim: grasp position snapped to {PICK_OBJECT_ID} centre "
                    f"({cx:.3f}, {cy:.3f}, {cz:.3f})"
                )
                grasp_allow = ([PICK_OBJECT_ID, "pick_tray"]
                               + list(DISTRACTOR_OBJECTS.keys()))

            # Enable tray ACM just before descent — the gripper enters the tray
            # volume during steps 3-5 (grasp, close, lift). This is safe because
            # the arm is already directly above the tray at pre_grasp_z.
            self._set_pick_object_collision("pick_tray", True)
            self._set_pick_object_collision("place_tray", True)

            grasp_target = _with_ik_orientation(grasp_pose)
            self.get_logger().info("Step 3: moving to grasp pose")
            step3_ok = self._move_to_pose(grasp_target, tolerance=TIGHT_TOL,
                                          avoid_collisions=False,
                                          allow_objects=grasp_allow)
            if not step3_ok:
                self._publish_status("FAILED: grasp motion failed")
                return

            # 4. Close gripper
            self.get_logger().info("Step 4: closing gripper")
            if not self._set_gripper(GRIPPER_CLOSE_POS):
                self._publish_status("FAILED: gripper close failed")
                return

            # 4b. Attach pick object to palm — removes from world scene and
            # re-adds as attached object so it tracks the arm in RViz.
            if self._real_hardware:
                self._attach_pick_object(
                    PICK_OBJECT_ID, grasp_pose.pose.position.z,
                    obj_radius=obj_radius, obj_height=obj_height, obj_cz=obj_cz
                )
            else:
                self._attach_pick_object(PICK_OBJECT_ID, grasp_pose.pose.position.z)
            # Allow MoveIt's scene monitor time to propagate the attach before
            # step 5 checks the start state.  Without this delay, the scene
            # monitor may still see the object in the world (not attached),
            # which causes "start tree could not be initialized" (error 999999).
            time.sleep(0.5)

            # 5. Lift to pre-grasp height.
            # Pick object is ATTACHED so it's no longer a world collision object.
            # Also exclude remaining scene objects so the arm can lift through the
            # neighbour's height range (e.g. bottle_large top=0.890 > grasp z).
            # IMPORTANT: include PICK_OBJECT_ID in lift_allow too — there is a small
            # propagation delay between _attach_pick_object() and MoveIt's scene update.
            # During that window, the world scene still has the object and the arm (at
            # grasp pose) is seen as "in collision" → start-state rejection.
            # Removing it via the diff ensures the start state is always valid.
            if self._real_hardware:
                lift_allow = [PICK_OBJECT_ID, "pick_tray", "place_tray"]
            else:
                remaining_scene = [k for k in SCENE_PICK_OBJECTS if k != PICK_OBJECT_ID]
                lift_allow = ([PICK_OBJECT_ID, "pick_tray"]
                              + remaining_scene + list(DISTRACTOR_OBJECTS.keys()))
            lift_pose = copy.deepcopy(grasp_pose)
            lift_pose.pose.position.z = pre_grasp_z   # same height as pre-grasp
            lift_pose = _with_ik_orientation(lift_pose)
            self.get_logger().info("Step 5: lifting to pre-grasp height")
            step5_ok = self._move_to_pose(lift_pose, tolerance=LOOSE_TOL,
                                          avoid_collisions=False,
                                          allow_objects=lift_allow)
            if not step5_ok:
                self._publish_status("FAILED: lift motion failed")
                return
            self.get_logger().info("Step 5 done — object attached, moving to place")

            # Restore distractor collision checking before the place sweep (sim only).
            # In sim, distractors were globally allowed so the arm could descend past
            # them. For step 6 OMPL must route around them, so restore allow=False.
            # In real hardware there are no registered distractor collision objects.
            if not self._real_hardware:
                for _d in DISTRACTOR_OBJECTS:
                    self._set_pick_object_collision(_d, False)

            # 6. Move to place pose.
            # place_z: keep the same gripper-to-object Z relationship as during grasp,
            # but position the object so its bottom sits on the place tray surface.
            #
            # Derivation:
            #   palm_frame_z = (gz - TOOL0_TO_PALM_Z) - obj_cz   [stored in attached object]
            #   At place: object bottom = PLACE_TRAY_TOP_Z
            #   → obj_centre_at_place = PLACE_TRAY_TOP_Z + obj_height/2
            #   → palm_at_place = obj_centre_at_place + palm_frame_z
            #   → place_z = palm_at_place + TOOL0_TO_PALM_Z
            #   Simplified: place_z = gz - obj_cz + PLACE_TRAY_TOP_Z + obj_height/2
            if self._real_hardware:
                place_z = gz - obj_cz + PLACE_TRAY_TOP_Z + obj_height / 2.0
            else:
                _, _, _cz, _, _obj_h = SCENE_PICK_OBJECTS.get(
                    PICK_OBJECT_ID, (0, 0, 0.175, 0.037, 0.110)
                )
                place_z = gz - _cz + PLACE_TRAY_TOP_Z + _obj_h / 2.0
            # Use a different slot for each object so they don't stack on each other.
            slot_idx = min(len(self._placed_objects), len(PLACE_SLOTS) - 1)
            place_slot_x, place_slot_y = PLACE_SLOTS[slot_idx]
            place = PoseStamped()
            place.header.frame_id = "world"
            place.header.stamp = rclpy.time.Time().to_msg()
            place.pose.position.x = place_slot_x
            place.pose.position.y = place_slot_y
            place.pose.position.z = place_z
            place.pose.orientation.x = IK_ORIENTATION_X
            place.pose.orientation.y = IK_ORIENTATION_Y
            place.pose.orientation.z = IK_ORIENTATION_Z
            place.pose.orientation.w = IK_ORIENTATION_W
            self.get_logger().info(
                f"Step 6: placing at ({place_slot_x}, {place_slot_y}, {place_z:.3f}) "
                f"on table (slot {slot_idx})"
            )
            # Distractors are NOT excluded here (sim) — OMPL must route around them.
            # In real hardware there are no registered distractor collision objects.
            if self._real_hardware:
                place_allow = [PICK_OBJECT_ID, "place_tray", "pick_tray"]
            else:
                remaining_picks = [k for k in SCENE_PICK_OBJECTS if k != PICK_OBJECT_ID]
                place_allow = ([PICK_OBJECT_ID, "place_tray", "pick_tray"]
                               + list(self._placed_objects) + remaining_picks)
            if not self._move_to_pose(place, tolerance=TIGHT_TOL,
                                       avoid_collisions=False,
                                       allow_objects=place_allow):
                self._publish_status("FAILED: place motion failed")
                return

            # 7. Open gripper (release) — wait 0.5 s for arm to fully settle at place pose
            time.sleep(0.5)
            self.get_logger().info("Step 7: opening gripper (release)")
            if not self._set_gripper(GRIPPER_OPEN_POS):
                self._publish_status("FAILED: gripper release failed")
                return

            # 7b. Detach object from gripper — re-adds to world scene at place XY.
            self._detach_pick_object(
                PICK_OBJECT_ID,
                place_x=place_slot_x,
                place_y=place_slot_y,
            )

            # 8. Return to ready (home) pose — clear workspace for next pick.
            self.get_logger().info("Step 8: returning to ready pose")
            # Step 8: return to home.
            if self._real_hardware:
                home_allow = [PICK_OBJECT_ID, "place_tray", "pick_tray"]
            else:
                home_allow = (list(self._placed_objects) + [PICK_OBJECT_ID,
                              "place_tray", "pick_tray"]
                              + [k for k in SCENE_PICK_OBJECTS if k != PICK_OBJECT_ID])
            self._move_to_joint_goal(HOME_JOINTS, tolerance=LOOSE_TOL,
                                     allow_objects=home_allow)

            self.get_logger().info("Grasp sequence completed successfully!")
            self._publish_status("SUCCESS")

            if self._real_hardware:
                # Real hardware: one pick per trigger. User clicks SAM2 window and
                # triggers again manually for the next object.
                self.get_logger().info(
                    "Pick complete. Click next object in SAM2 window, then trigger again."
                )
            else:
                # Simulation: track placed objects; auto-trigger next if more remain.
                self._placed_objects.add(PICK_OBJECT_ID)
                picked_msg = String()
                picked_msg.data = PICK_OBJECT_ID
                self._picked_pub.publish(picked_msg)

                remaining = [k for k in SCENE_PICK_OBJECTS if k not in self._placed_objects]
                if remaining:
                    self.get_logger().info(
                        f"Objects remaining: {remaining} — auto-triggering next pick in 3 s"
                    )
                    time.sleep(3.0)
                    self._trigger_pub.publish(EmptyMsg())
                else:
                    self.get_logger().info(
                        "All scene objects placed! Send /graspgen/trigger to start new cycle."
                    )
                    self._placed_objects.clear()
                    self._reset_world_scene()

        except Exception as exc:
            self.get_logger().error(f"Exception during grasp sequence: {exc}")
            self._publish_status(f"FAILED: {exc}")

        finally:
            # Restore all ACM entries regardless of success/failure.
            self._set_pick_object_collision("pick_tray", False)
            self._set_pick_object_collision("place_tray", False)
            if self._real_hardware:
                self._set_pick_object_collision("real_target", False)
            else:
                for _d in DISTRACTOR_OBJECTS:
                    self._set_pick_object_collision(_d, False)
                for _p in SCENE_PICK_OBJECTS:
                    self._set_pick_object_collision(_p, False)
            with self._lock:
                self._executing = False

    # -----------------------------------------------------------------------
    # World scene reset (between demo cycles)
    # -----------------------------------------------------------------------

    def _reset_world_scene(self):
        """
        Re-add all SCENE_PICK_OBJECTS to the world at their original pick
        positions after a completed demo cycle.

        After _detach_pick_object(), the picked object is re-added at the
        PLACE position.  The next trigger snaps the grasp to the PICK
        position (from SCENE_PICK_OBJECTS), so the world scene must have
        the object back at its pick position for MoveIt's start-state
        validation to be consistent.
        """
        if not self._apply_scene_client.service_is_ready():
            self.get_logger().warn("_reset_world_scene: /apply_planning_scene not ready.")
            return

        scene = PlanningScene()
        scene.is_diff = True
        for obj_id, (cx, cy, cz, radius, height) in SCENE_PICK_OBJECTS.items():
            co = CollisionObject()
            co.id = obj_id
            co.header.frame_id = "world"
            co.header.stamp = rclpy.time.Time().to_msg()
            co.primitives.append(
                SolidPrimitive(type=SolidPrimitive.CYLINDER,
                               dimensions=[height, radius]))
            p = GeoPose()
            p.position.x = cx
            p.position.y = cy
            p.position.z = cz
            p.orientation.w = 1.0
            co.primitive_poses.append(p)
            co.operation = CollisionObject.ADD
            scene.world.collision_objects.append(co)

        req = ApplyPlanningScene.Request()
        req.scene = scene
        future = self._apply_scene_client.call_async(req)
        ok = self._wait_future(future, timeout_sec=5.0)
        if ok:
            self.get_logger().info(
                "World scene reset: SCENE_PICK_OBJECTS restored to original pick positions.")
        else:
            self.get_logger().warn("World scene reset may have failed (timeout).")

    # -----------------------------------------------------------------------
    # Allowed Collision Matrix (ACM) helpers
    # -----------------------------------------------------------------------

    def _set_pick_object_collision(self, object_name: str, allow: bool):
        """
        Allow or restore collision checking between the robot and a planning-scene
        object.  Used around grasp/lift steps so OMPL can plan a path that enters
        the pick object's collision volume.

        allow=True  → OMPL ignores collisions with `object_name` (grasp step)
        allow=False → restore normal collision checking (after lift)

        Uses /apply_planning_scene with an ACM diff that sets a default-entry
        for the named object, which propagates to ALL robot link pairs in one call.
        Hardware-compatible: no objects are removed from the scene.
        """
        scene = PlanningScene()
        scene.is_diff = True
        acm = AllowedCollisionMatrix()
        acm.default_entry_names = [object_name]
        acm.default_entry_values = [allow]
        scene.allowed_collision_matrix = acm

        req = ApplyPlanningScene.Request()
        req.scene = scene

        if not self._apply_scene_client.service_is_ready():
            self.get_logger().warn(
                "/apply_planning_scene not ready — skipping ACM update.")
            return

        future = self._apply_scene_client.call_async(req)
        ok = self._wait_future(future, timeout_sec=5.0)
        if ok and future.result() and future.result().success:
            state = "ALLOWED" if allow else "RESTORED"
            self.get_logger().info(
                f"ACM: collision with '{object_name}' → {state}")
        else:
            self.get_logger().warn(
                f"ACM update for '{object_name}' allow={allow} may have failed.")

    # -----------------------------------------------------------------------
    # Pick-object attach / detach helpers (visual pick-and-place in RViz)
    # -----------------------------------------------------------------------

    def _attach_pick_object(self, object_id: str, grasp_z: float,
                            obj_radius: float = None, obj_height: float = None,
                            obj_cz: float = None):
        """
        Attach the pick object to robotiq_palm after gripper close.

        Removes the object from the world collision scene and re-adds it as an
        AttachedCollisionObject on robotiq_palm so it visually tracks the arm
        in RViz and participates in collision checking during lift/place.

        In sim: geometry looked up from SCENE_PICK_OBJECTS.
        In real hardware: geometry passed directly from point-cloud estimate.

        Palm-frame offset: palm is 0.02 m below tool0 (along world -Z at top-down grasp).
        Object centre offset = (grasp_z - 0.020) - obj_cz, expressed in palm +Z (= world -Z).
        """
        if not self._apply_scene_client.service_is_ready():
            self.get_logger().warn("_attach_pick_object: /apply_planning_scene not ready.")
            return

        # Geometry: use passed values if provided (real hardware), else look up from sim dict
        if obj_radius is None or obj_height is None or obj_cz is None:
            _cx, _cy, cz, obj_radius, obj_height = SCENE_PICK_OBJECTS.get(
                object_id, (0.0, 0.0, 0.175, 0.037, 0.110)
            )
        else:
            cz = obj_cz
        palm_world_z = grasp_z - TOOL0_TO_PALM_Z   # palm is TOOL0_TO_PALM_Z (0.05 m) below tool0
        # IK orientation (x=1,y=0,z=0,w=0) = 180° around X → palm +Z = world -Z.
        # An object ABOVE the palm in world (cz > palm_world_z) is in palm -Z.
        # palm_frame_z = palm_world_z - cz  (negative when object is above palm).
        # Old code used max(0.0, ...) which forced the cylinder to palm-centre,
        # shifting it 2 cm low and extending it into the wrist_2_link volume.
        palm_frame_z = palm_world_z - cz  # correct signed offset; may be negative

        # Build attached collision object
        aco = AttachedCollisionObject()
        aco.link_name = "robotiq_palm"
        aco.object.id = object_id
        aco.object.header.frame_id = "robotiq_palm"
        aco.object.header.stamp = rclpy.time.Time().to_msg()
        aco.object.primitives.append(
            SolidPrimitive(type=SolidPrimitive.CYLINDER,
                           dimensions=[obj_height, obj_radius]))
        p = GeoPose()
        p.position.z = palm_frame_z
        p.orientation.w = 1.0
        aco.object.primitive_poses.append(p)
        aco.object.operation = CollisionObject.ADD
        aco.touch_links = GRIPPER_TOUCH_LINKS

        # Remove from world scene
        co = CollisionObject()
        co.id = object_id
        co.header.frame_id = "world"
        co.header.stamp = rclpy.time.Time().to_msg()
        co.operation = CollisionObject.REMOVE

        scene = PlanningScene()
        scene.is_diff = True
        scene.robot_state.is_diff = True
        scene.robot_state.attached_collision_objects.append(aco)
        scene.world.collision_objects.append(co)

        req = ApplyPlanningScene.Request()
        req.scene = scene
        future = self._apply_scene_client.call_async(req)
        ok = self._wait_future(future, timeout_sec=5.0)
        if ok:
            self.get_logger().info(
                f"Attached '{object_id}' to robotiq_palm — will track arm in RViz.")
        else:
            self.get_logger().warn(f"Attach '{object_id}' may have failed (timeout).")

    def _detach_pick_object(self, object_id: str, place_x: float, place_y: float):
        """
        Detach the pick object from the gripper and re-add it to the world
        planning scene at the place position (resting on table top).

        Called after gripper open (step 7) so the object appears at its new
        location in RViz and re-enters collision checking for future plans.
        """
        if not self._apply_scene_client.service_is_ready():
            self.get_logger().warn("_detach_pick_object: /apply_planning_scene not ready.")
            return

        # Detach from robot
        aco = AttachedCollisionObject()
        aco.link_name = "robotiq_palm"
        aco.object.id = object_id
        aco.object.operation = CollisionObject.REMOVE

        # Look up per-object geometry
        _cx, _cy, _cz, obj_radius, obj_height = SCENE_PICK_OBJECTS.get(
            object_id, (0.0, 0.0, 0.705, 0.037, 0.110)
        )
        # Re-add to world at place X, Y, resting on table top
        place_z = TABLE_TOP_Z + obj_height / 2.0   # object centre above table
        co = CollisionObject()
        co.id = object_id
        co.header.frame_id = "world"
        co.header.stamp = rclpy.time.Time().to_msg()
        co.primitives.append(
            SolidPrimitive(type=SolidPrimitive.CYLINDER,
                           dimensions=[obj_height, obj_radius]))
        p = GeoPose()
        p.position.x = place_x
        p.position.y = place_y
        p.position.z = place_z
        p.orientation.w = 1.0
        co.primitive_poses.append(p)
        co.operation = CollisionObject.ADD

        scene = PlanningScene()
        scene.is_diff = True
        scene.robot_state.is_diff = True
        scene.robot_state.attached_collision_objects.append(aco)
        scene.world.collision_objects.append(co)

        req = ApplyPlanningScene.Request()
        req.scene = scene
        future = self._apply_scene_client.call_async(req)
        ok = self._wait_future(future, timeout_sec=5.0)
        if ok:
            self.get_logger().info(
                f"Detached '{object_id}' — re-added to world at "
                f"({place_x:.2f}, {place_y:.2f}, {place_z:.3f}).")
        else:
            self.get_logger().warn(f"Detach '{object_id}' may have failed (timeout).")

    # -----------------------------------------------------------------------
    # Future waiting (thread-safe, no spin_until_future_complete)
    # -----------------------------------------------------------------------

    @staticmethod
    def _wait_future(future, timeout_sec: float) -> bool:
        event = threading.Event()
        future.add_done_callback(lambda _: event.set())
        return event.wait(timeout=timeout_sec)

    # -----------------------------------------------------------------------
    # IK → joint goal (Cartesian motion via compute_ik + joint planning)
    # -----------------------------------------------------------------------

    def _call_ik(self, target_pose: PoseStamped, timeout_sec: float = 2.0,
                 avoid_collisions: bool = True,
                 seed_joints: dict = None):
        """
        Call /compute_ik seeded with current joint state (or explicit seed).

        Seeding KDL with the current joints biases the solution toward the
        nearest configuration — keeping the arm in the same elbow-up/down
        branch rather than finding a solution that crosses through the table.

        seed_joints: explicit dict {joint_name: rad} to use as IK seed instead of
          self._current_joints. Pass this when the current joints might not yet
          reflect the latest commanded position (race condition in /joint_states).

        avoid_collisions=False is used when intentionally entering the pick
        object's collision zone (grasp and lift steps).

        Returns a dict {joint_name: position_rad} on success, None on failure.
        """
        req = GetPositionIK.Request()
        req.ik_request.group_name       = ARM_GROUP
        req.ik_request.ik_link_name     = "tool0"
        req.ik_request.pose_stamped     = target_pose
        req.ik_request.avoid_collisions = avoid_collisions
        req.ik_request.timeout          = BuiltinDuration(
            sec=int(timeout_sec),
            nanosec=int((timeout_sec % 1) * 1e9),
        )

        # Seed with provided joints OR current joint state.
        # IMPORTANT: passing seed_joints avoids a race condition where
        # /joint_states hasn't been updated yet after executing the prior motion.
        source = seed_joints if seed_joints is not None else self._current_joints
        req.ik_request.robot_state.joint_state.name = ARM_JOINTS
        req.ik_request.robot_state.joint_state.position = [
            source.get(n, 0.0) for n in ARM_JOINTS
        ]

        future = self._ik_client.call_async(req)
        if not self._wait_future(future, timeout_sec=10.0):
            self.get_logger().error("IK service call timed out.")
            return None

        resp = future.result()
        if resp is None or resp.error_code.val != 1:
            code = resp.error_code.val if resp else "None"
            self.get_logger().error(f"IK failed, error_code={code}")
            return None

        joint_dict = {}
        for name, pos in zip(resp.solution.joint_state.name,
                              resp.solution.joint_state.position):
            if name in ARM_JOINTS:
                joint_dict[name] = pos

        if len(joint_dict) != len(ARM_JOINTS):
            self.get_logger().error("IK response missing some arm joints.")
            return None

        # Normalise angles to within ±π of the seed so OMPL does not see a
        # full-revolution motion (KDL may return e.g. lift=5.027 instead of
        # the equivalent -1.256, making the planned path impossibly long).
        joint_dict = _normalize_joints_to_seed(joint_dict, source)

        self.get_logger().info(
            f"IK solution (normalised): pan={joint_dict.get('shoulder_pan_joint', 0):.3f} "
            f"lift={joint_dict.get('shoulder_lift_joint', 0):.3f} "
            f"elbow={joint_dict.get('elbow_joint', 0):.3f}"
        )
        return joint_dict

    def _move_to_pose(
        self,
        target_pose: PoseStamped,
        tolerance: float = LOOSE_TOL,
        avoid_collisions: bool = True,
        seed_joints: dict = None,
        allow_objects: list = None,
    ) -> bool:
        """
        Move arm to a Cartesian pose by:
          1. Computing IK seeded with current joint state (or explicit seed).
          2. Planning and executing to the resulting joint configuration.

        allow_objects: collision-object IDs to remove from scene for this plan only.
        """
        joints = self._call_ik(target_pose, avoid_collisions=avoid_collisions,
                               seed_joints=seed_joints)
        if joints is None:
            return False
        return self._move_to_joint_goal(joints, tolerance=tolerance,
                                        allow_objects=allow_objects)

    # -----------------------------------------------------------------------
    # Joint-space planning and execution (MoveGroup action)
    # -----------------------------------------------------------------------

    def _move_direct_joints(self, joint_positions: dict, duration_sec: float) -> bool:
        """
        Move arm by sending a single-segment JointTrajectory directly to the
        scaled_joint_trajectory_controller, completely bypassing MoveIt/OMPL.

        Use ONLY for verified-safe scan poses (confirmed on teach pendant).
        No collision checking is performed — the caller guarantees safety.

        duration_sec: how long to give the controller to reach the target.
          Allow 20 s for large pan swings (165°), 8 s for small adjustments.
          The UR speed slider further scales execution time; these values assume
          the slider is at ≥25%.  The result_timeout waits 3× duration as buffer.
        """
        traj = JointTrajectory()
        traj.joint_names = ARM_JOINTS

        pt = JointTrajectoryPoint()
        pt.positions      = [float(joint_positions.get(n, 0.0)) for n in ARM_JOINTS]
        pt.velocities     = [0.0] * len(ARM_JOINTS)
        pt.accelerations  = [0.0] * len(ARM_JOINTS)
        pt.time_from_start = RosDuration(
            sec=int(duration_sec),
            nanosec=int((duration_sec % 1) * 1e9),
        )
        traj.points = [pt]

        goal = FollowJointTrajectory.Goal()
        goal.trajectory = traj

        self.get_logger().info(
            f"[direct] pan={math.degrees(joint_positions.get('shoulder_pan_joint',0)):.1f}° "
            f"lift={math.degrees(joint_positions.get('shoulder_lift_joint',0)):.1f}° "
            f"elbow={math.degrees(joint_positions.get('elbow_joint',0)):.1f}°  "
            f"dur={duration_sec:.0f}s"
        )

        future = self._arm_direct_client.send_goal_async(goal)
        if not self._wait_future(future, timeout_sec=30.0):
            self.get_logger().error("[direct] Goal send timed out.")
            return False

        goal_handle = future.result()
        if not goal_handle or not goal_handle.accepted:
            self.get_logger().error("[direct] Goal rejected.")
            return False

        result_future = goal_handle.get_result_async()
        # Allow 3× the planned duration for speed-slider variability
        result_timeout = duration_sec * 3.0 + 30.0
        if not self._wait_future(result_future, timeout_sec=result_timeout):
            self.get_logger().error(
                f"[direct] Result timed out after {result_timeout:.0f} s.")
            return False

        result = result_future.result().result
        if result.error_code == FollowJointTrajectory.Result.SUCCESSFUL:
            self.get_logger().info("[direct] Arm trajectory succeeded.")
            return True
        else:
            self.get_logger().error(
                f"[direct] Arm trajectory failed, code={result.error_code}")
            return False

    def _move_to_joint_goal(
        self,
        joint_positions: dict,
        planning_time: float = 10.0,
        tolerance: float = LOOSE_TOL,
        allow_objects: list = None,
        min_ee_z: float = None,
    ) -> bool:
        """
        Plan and execute a joint-space goal via the MoveGroup action.

        allow_objects: list of collision-object IDs to temporarily remove from
        the planning scene for THIS call only (via PlanningOptions.planning_scene_diff).
        The global scene is NOT modified — this is hardware-compatible because the
        planner is told to ignore objects the gripper intentionally enters (pick targets).
        """
        constraints = Constraints()
        constraints.name = "joint_goal"
        for name, pos in joint_positions.items():
            jc = JointConstraint()
            jc.joint_name    = name
            jc.position      = float(pos)
            jc.tolerance_above = tolerance
            jc.tolerance_below = tolerance
            jc.weight          = 1.0
            constraints.joint_constraints.append(jc)

        workspace = WorkspaceParameters()
        workspace.header.frame_id = "base_link"
        workspace.min_corner = Vector3(x=-2.0, y=-2.0, z=-0.5)
        workspace.max_corner = Vector3(x= 2.0, y= 2.0, z= 2.5)

        plan_request = MotionPlanRequest()
        plan_request.workspace_parameters              = workspace
        plan_request.start_state.is_diff              = True
        plan_request.goal_constraints                  = [constraints]
        plan_request.pipeline_id                       = "ompl"
        plan_request.planner_id                        = "RRTConnectkConfigDefault"
        plan_request.group_name                        = ARM_GROUP
        plan_request.num_planning_attempts             = 5
        plan_request.allowed_planning_time             = planning_time
        plan_request.max_velocity_scaling_factor       = 0.15
        plan_request.max_acceleration_scaling_factor   = 0.1

        # Optional Z floor: keep tool0 above min_ee_z throughout the path.
        # Prevents OMPL from planning arcs that dip the gripper through the tray.
        if min_ee_z is not None:
            pc = PositionConstraint()
            pc.header.frame_id = "world"
            pc.link_name = "tool0"
            # Large box: 4m x 4m in XY, 2m tall, bottom edge at min_ee_z
            box = SolidPrimitive()
            box.type = SolidPrimitive.BOX
            box.dimensions = [4.0, 4.0, 2.0]
            pc.constraint_region.primitives.append(box)
            box_pose = GeoPose()
            box_pose.position.z = min_ee_z + 1.0  # centre at min_ee_z+1.0 → bottom=min_ee_z
            box_pose.orientation.w = 1.0
            pc.constraint_region.primitive_poses.append(box_pose)
            pc.weight = 1.0
            path_c = Constraints()
            path_c.position_constraints.append(pc)
            plan_request.path_constraints = path_c

        planning_options           = PlanningOptions()
        planning_options.plan_only = False
        planning_options.replan    = False

        # Temporarily remove pick objects from the scene for THIS plan only.
        # PlanningOptions.planning_scene_diff is a local override — it does NOT
        # modify the global MoveIt scene, so it is fully hardware-compatible.
        if allow_objects:
            diff = PlanningScene()
            diff.is_diff = True
            for obj_id in allow_objects:
                co = CollisionObject()
                co.id = obj_id
                co.operation = CollisionObject.REMOVE
                diff.world.collision_objects.append(co)
            planning_options.planning_scene_diff = diff
            self.get_logger().info(
                f"Planning with scene diff: removed {allow_objects} for this call only.")

        goal          = MoveGroup.Goal()
        goal.request  = plan_request
        goal.planning_options = planning_options

        self.get_logger().info(
            f"Joint goal: pan={joint_positions.get('shoulder_pan_joint',0):.3f} "
            f"lift={joint_positions.get('shoulder_lift_joint',0):.3f} "
            f"tol={tolerance:.3f}"
        )

        future = self._move_group_client.send_goal_async(goal)
        if not self._wait_future(future, timeout_sec=30.0):
            self.get_logger().error("MoveGroup goal send timed out.")
            return False

        goal_handle = future.result()
        if not goal_handle or not goal_handle.accepted:
            self.get_logger().error("MoveGroup goal rejected.")
            return False

        result_future = goal_handle.get_result_async()
        # Wait at least planning_time + 90 s (execution buffer).
        # With planning_time=60, the fixed 60 s wait expired before execution finished.
        result_timeout = planning_time + 90.0
        if not self._wait_future(result_future, timeout_sec=result_timeout):
            self.get_logger().error(
                f"MoveGroup result timed out after {result_timeout:.0f} s "
                f"(planning_time={planning_time:.0f} s).")
            return False

        result = result_future.result().result
        if result.error_code.val == MoveItErrorCodes.SUCCESS:
            self.get_logger().info("Joint goal succeeded.")
            return True
        else:
            self.get_logger().error(
                f"Joint goal failed, error code: {result.error_code.val}"
            )
            return False

    # -----------------------------------------------------------------------
    # Gripper control (FollowJointTrajectory action)
    # -----------------------------------------------------------------------

    def _set_gripper(self, position: float, duration_sec: float = 2.0) -> bool:
        """
        Open or close the gripper.

        Real hardware mode: routes to RobotiqGripper3F TCP controller.
          position == GRIPPER_OPEN_POS  → gripper.open()
          position == GRIPPER_CLOSE_POS → gripper.close()

        Simulation mode: sends FollowJointTrajectory action to simulated controller.
        """
        if self._real_hardware:
            if self._real_gripper is None:
                self.get_logger().error("Real gripper not initialised!")
                return False
            # Re-activate if connection was lost (e.g. after E-stop)
            if not self._real_gripper.is_active():
                self.get_logger().warn("Gripper not active — re-activating...")
                ok = self._real_gripper.activate()
                if not ok:
                    self.get_logger().error("Gripper re-activation failed!")
                    return False
                self.get_logger().info("Gripper re-activated.")
            if position <= GRIPPER_OPEN_POS + 0.05:
                self.get_logger().info("Real gripper: OPEN")
                return self._real_gripper.open()
            else:
                self.get_logger().info("Real gripper: CLOSE")
                return self._real_gripper.close()

        # ── Simulation: FollowJointTrajectory action ──────────────────────
        deadline = time.monotonic() + 10.0
        while not self._gripper_ready and time.monotonic() < deadline:
            time.sleep(0.2)
        if not self._gripper_ready:
            self.get_logger().error("Gripper action server not available!")
            return False

        traj = JointTrajectory()
        traj.joint_names = GRIPPER_JOINTS

        pt = JointTrajectoryPoint()
        pt.positions      = [position, position, position]
        pt.velocities     = [0.0, 0.0, 0.0]
        pt.time_from_start = RosDuration(
            sec=int(duration_sec),
            nanosec=int((duration_sec % 1) * 1e9),
        )
        traj.points = [pt]

        goal = FollowJointTrajectory.Goal()
        goal.trajectory = traj

        future = self._gripper_client.send_goal_async(goal)
        if not self._wait_future(future, timeout_sec=15.0):
            self.get_logger().error("Gripper goal send timed out.")
            return False

        if not future.result() or not future.result().accepted:
            self.get_logger().error("Gripper goal rejected.")
            return False

        result_future = future.result().get_result_async()
        if not self._wait_future(result_future, timeout_sec=15.0):
            self.get_logger().error("Gripper result timed out.")
            return False

        if not result_future.result():
            self.get_logger().error("Gripper result future failed.")
            return False

        error_code = result_future.result().result.error_code
        if error_code == FollowJointTrajectory.Result.SUCCESSFUL:
            return True
        else:
            self.get_logger().error(f"Gripper trajectory failed, code={error_code}")
            return False

    # -----------------------------------------------------------------------
    # Node lifecycle — deactivate gripper on shutdown
    # -----------------------------------------------------------------------

    def destroy_node(self):
        """Deactivate gripper before shutting down so it returns to standby."""
        if self._real_hardware and self._real_gripper is not None:
            self.get_logger().info("Shutting down: deactivating Robotiq 3F gripper ...")
            self._real_gripper.shutdown()
        super().destroy_node()

    # -----------------------------------------------------------------------
    # Status publisher
    # -----------------------------------------------------------------------

    def _publish_status(self, status: str):
        msg      = String()
        msg.data = status
        self._status_pub.publish(msg)
        self.get_logger().info(f"[STATUS] {status}")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main(args=None):
    rclpy.init(args=args)
    node     = GraspExecutorNode()
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
