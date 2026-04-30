import sys
sys.path.insert(0, "/workspace/GraspGen")

import numpy as np
import torch
from pathlib import Path
import omegaconf

from grasp_gen.grasp_server import GraspGenSampler
from grasp_gen.utils.meshcat_utils import visualize_grasps
from grasp_gen.robot import load_control_points_for_visualization


# ---------- LOAD MODEL CONFIG ----------
model_cfg = omegaconf.OmegaConf.load("scripts/config.yaml")

# IMPORTANT: use CPU-safe defaults (no checkpoints)
model_cfg.eval.model_name = "m2t2"
model_cfg.eval.checkpoint = None


# ---------- CREATE SAMPLER ----------
sampler = GraspGenSampler(model_cfg)


# ---------- DUMMY POINT CLOUD ----------
# Simple cube point cloud (demo purpose)
pc = np.random.uniform(-0.05, 0.05, size=(2048, 3))


# ---------- RUN GRASP INFERENCE ----------
grasps, conf = GraspGenSampler.run_inference(
    object_pc=pc,
    grasp_sampler=sampler,
    num_grasps=30,
)


# ---------- VISUALIZE ----------
gripper_name = "franka_panda"
control_pts = load_control_points_for_visualization(gripper_name)

visualize_grasps(
    grasps,
    control_pts,
    confidences=conf,
)
