import numpy as np
import torch
from pathlib import Path

from grasp_gen.grasp_server import GraspGenSampler
from grasp_gen.grasp_server import load_grasp_cfg
import numpy as np

# -------------------------
# CONFIG
# -------------------------
GRIPPER_CFG = "config/grippers/robotiq_3f.yaml"
OBJECT_PC = "assets/objects/cube.ply"   # example
NUM_GRASPS = 500

# -------------------------
# LOAD CONFIG
# -------------------------
cfg = load_grasp_cfg(GRIPPER_CFG)

# IMPORTANT:
# For now, force inference-only mode
cfg.eval = {
    "model_name": "diffusion-discriminator",
    "checkpoint": None
}

sampler = GraspGenSampler(cfg)

# -------------------------
# LOAD POINT CLOUD
# -------------------------
# Temporary synthetic point cloud (cube)
def create_dummy_point_cloud(n=2048):
    return np.random.uniform(-0.05, 0.05, size=(n, 3)).astype(np.float32)

object_pc = create_dummy_point_cloud()


# -------------------------
# GENERATE GRASPS
# -------------------------
grasps, confidences = GraspGenSampler.run_inference(
    pc,
    sampler,
    num_grasps=NUM_GRASPS,
    grasp_threshold=-1.0
)

# -------------------------
# SAVE
# -------------------------
out_dir = Path("generated_grasps/robotiq_3f")
out_dir.mkdir(parents=True, exist_ok=True)

np.save(out_dir / "grasps.npy", grasps.cpu().numpy())
np.save(out_dir / "confidences.npy", confidences.cpu().numpy())

print(f"Generated {len(grasps)} Robotiq-3F grasps")

