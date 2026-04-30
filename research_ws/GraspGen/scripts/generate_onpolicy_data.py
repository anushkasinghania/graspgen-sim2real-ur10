#!/usr/bin/env python3
"""
generate_onpolicy_data.py

Populates positive_grasps_onpolicy / negative_grasps_onpolicy in the H5 discriminator
cache by:
  1. Loading the trained generator (epoch_500.pth)
  2. Running diffusion sampling on every object in the cache
  3. Labelling each generated grasp with trimesh proximity (NO python-fcl required):
       positive  = TCP within contact range of object surface
                   AND pre-grasp TCP not inside / blocking object
       negative  = everything else
  4. Writing results back into the cache H5 in-place

ARM64/Jetson compatible — does NOT use trimesh.collision.CollisionManager.

Usage
-----
python3 scripts/generate_onpolicy_data.py [options]

Key options (defaults match current Jetson paths):
  --ckpt          Path to generator checkpoint  (default: epoch_500.pth)
  --h5            Path to H5 cache to update    (default: cache_train_mesh_dis.h5)
  --num_grasps    Grasps to sample per object   (default: 400)
  --pre_grasp_dist  Metres to back off for approach collision check (default: 0.05)
"""

import argparse
import os
import sys
from pathlib import Path

import h5py
import numpy as np
import torch
import trimesh
from omegaconf import OmegaConf
from tqdm import tqdm

# Make sure the package is importable when run from scripts/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from grasp_gen.dataset.dataset import collate
from grasp_gen.models.generator import GraspGenGenerator
from grasp_gen.robot import get_gripper_info

# ──────────────────────────────────────────────────────────────────────────────
# Defaults (all overridable via CLI)
# ──────────────────────────────────────────────────────────────────────────────
DEFAULT_CKPT       = "/home/ubuntu/GraspDataGen/training_logs/robotiq_3f_gen/epoch_500.pth"
DEFAULT_H5         = "/tmp/graspgen_cache/robotiq_3f/cache_train_mesh_dis.h5"
DEFAULT_GRIPPER    = "robotiq_3f"
DEFAULT_NUM_GRASPS = 400
DEFAULT_PRE_GRASP  = 0.05   # metres
CONFIG_YAML        = str(Path(__file__).resolve().parent / "config.yaml")


# ──────────────────────────────────────────────────────────────────────────────
# Model loading
# ──────────────────────────────────────────────────────────────────────────────

def load_generator(ckpt_path: str, cfg_diffusion) -> GraspGenGenerator:
    model = GraspGenGenerator.from_config(cfg_diffusion)
    ckpt = torch.load(ckpt_path, map_location="cpu")
    state = ckpt["model"]
    # Strip DDP 'module.' prefix when checkpoint was saved with DistributedDataParallel
    state = {k.replace("module.", ""): v for k, v in state.items()}
    model.load_state_dict(state)
    model.cuda().eval()
    print(f"Generator loaded from {ckpt_path}")
    return model


# ──────────────────────────────────────────────────────────────────────────────
# Grasp sampling
# ──────────────────────────────────────────────────────────────────────────────

@torch.no_grad()
def sample_grasps(model: GraspGenGenerator, pc: np.ndarray, num_grasps: int) -> np.ndarray:
    """Run generator diffusion on a point cloud.

    Args:
        pc: (N, 3) float32 point cloud in object frame (already scaled)
        num_grasps: number of grasps to sample

    Returns:
        grasps: (K, 4, 4) float32 in object frame (not centred)
    """
    pc_tensor = torch.from_numpy(pc).float().cuda()
    pc_center = pc_tensor.mean(dim=0)          # (3,)
    pc_centered = pc_tensor - pc_center        # (N, 3)

    data = {
        "task":   "pick",
        "points": pc_centered,
        # collate stacks 'inputs' — zero colour channel appended
        "inputs": torch.cat([pc_centered, torch.zeros_like(pc_centered)], dim=-1),
    }

    model.num_grasps_per_object = num_grasps
    batch = collate([data])
    # Move stacked tensors to GPU
    batch = {k: v.cuda() if isinstance(v, torch.Tensor) else v for k, v in batch.items()}

    outputs, _, _ = model.forward_inference(batch)

    # outputs["grasps_pred"] shape: (1, num_grasps, 4, 4)
    grasps = outputs["grasps_pred"][0].cpu().numpy()   # (num_grasps, 4, 4)
    # Translate back from centred frame to object frame
    grasps[:, :3, 3] += pc_center.cpu().numpy()
    return grasps.astype(np.float32)


# ──────────────────────────────────────────────────────────────────────────────
# Collision labelling  (FCL-free, ARM64/Jetson compatible)
# ──────────────────────────────────────────────────────────────────────────────

def label_grasps(
    grasps: np.ndarray,
    object_mesh: trimesh.Trimesh,
    gripper_mesh: trimesh.Trimesh,   # kept for API compat; not used in proximity path
    pre_grasp_dist: float = 0.05,
):
    """Label grasps as positive or negative using trimesh proximity (no FCL).

    Uses the grasp TCP position (translation column) as a proxy for gripper location:

    Positive  = TCP within ``contact_thresh`` of object surface
                AND pre-grasp TCP is NOT inside / blocking the object
    Negative  = everything else

    ``contact_thresh`` adapts to object size:  clip(obj_radius * 0.5, 1cm, 5cm)

    Args:
        grasps:         (N, 4, 4) grasp transforms in object frame
        object_mesh:    trimesh object mesh (scaled)
        gripper_mesh:   ignored (kept for interface compatibility)
        pre_grasp_dist: back-off distance along approach axis for the approach check

    Returns:
        pos_grasps, neg_grasps: filtered (M, 4, 4) float32 arrays
    """
    if len(grasps) == 0:
        empty = np.zeros((0, 4, 4), dtype=np.float32)
        return empty, empty

    tcp_positions = grasps[:, :3, 3].astype(np.float64)   # (N, 3)
    approach_axes = grasps[:, :3, 2].astype(np.float64)   # (N, 3)

    # Pre-grasp TCP: backed off along the approach axis
    pre_tcp = tcp_positions - pre_grasp_dist * approach_axes  # (N, 3)

    # Adaptive contact threshold scaled to the object's bounding sphere
    obj_verts = np.asarray(object_mesh.vertices, dtype=np.float64)
    obj_radius = float(np.linalg.norm(obj_verts - object_mesh.centroid, axis=1).max())
    contact_thresh = float(np.clip(obj_radius * 0.5, 0.01, 0.05))

    # ── Batched proximity queries (BVH — fast, no FCL needed) ────────────────
    _, tcp_dists, _  = trimesh.proximity.closest_point(object_mesh, tcp_positions)
    _, pre_dists, _  = trimesh.proximity.closest_point(object_mesh, pre_tcp)

    # Grasp contact: TCP within adaptive threshold of object surface
    grasp_contact = tcp_dists < contact_thresh

    # Approach blocked: pre-grasp TCP already ≤3 mm from surface (too tight)
    approach_blocked = pre_dists < 0.003

    # For watertight meshes, also block if pre-grasp TCP is physically inside the object
    if object_mesh.is_watertight:
        approach_blocked = approach_blocked | object_mesh.contains(pre_tcp)

    positive_mask = grasp_contact & ~approach_blocked
    return grasps[positive_mask].astype(np.float32), grasps[~positive_mask].astype(np.float32)


# ──────────────────────────────────────────────────────────────────────────────
# H5 helpers
# ──────────────────────────────────────────────────────────────────────────────

def _read_obj_meta(h5_path: str, obj_key: str):
    with h5py.File(h5_path, "r") as f:
        gd = f[obj_key]["grasp_data"]
        asset_path = gd["object_asset_path"][...].item().decode("utf-8")
        scale      = float(gd["object_scale"][...])
    return asset_path, scale


def _write_onpolicy(h5_path: str, obj_key: str, pos: np.ndarray, neg: np.ndarray):
    """Overwrite onpolicy datasets inside an existing H5 file."""
    with h5py.File(h5_path, "a") as f:
        gd = f[obj_key]["grasp_data"]
        for field, arr in (
            ("positive_grasps_onpolicy", pos),
            ("negative_grasps_onpolicy", neg),
        ):
            if field in gd:
                del gd[field]
            data = arr if (arr is not None and len(arr) > 0) else np.zeros((0, 4, 4), dtype=np.float32)
            gd.create_dataset(field, data=data)


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ckpt",           default=DEFAULT_CKPT,       help="Generator checkpoint path")
    parser.add_argument("--h5",             default=DEFAULT_H5,         help="H5 cache file to update")
    parser.add_argument("--gripper",        default=DEFAULT_GRIPPER,    help="Gripper name")
    parser.add_argument("--num_grasps",     type=int, default=DEFAULT_NUM_GRASPS, help="Grasps to generate per object")
    parser.add_argument("--pre_grasp_dist", type=float, default=DEFAULT_PRE_GRASP, help="Pre-grasp back-off distance (m)")
    parser.add_argument("--pc_points",      type=int, default=2048,     help="Points to sample from mesh for PC input")
    args = parser.parse_args()

    # ── Load config & model ───────────────────────────────────────────────────
    cfg = OmegaConf.load(CONFIG_YAML)
    cfg.diffusion.gripper_name        = args.gripper
    cfg.diffusion.num_grasps_per_object = args.num_grasps

    model = load_generator(args.ckpt, cfg.diffusion)

    # ── Load gripper mesh ─────────────────────────────────────────────────────
    gripper_info = get_gripper_info(args.gripper)
    # Copy so check_collision can safely set_transform on it without mutating shared state
    gripper_mesh = gripper_info.collision_mesh.copy()
    print(f"Gripper collision mesh: {len(gripper_mesh.vertices)} verts")

    # ── Enumerate objects ─────────────────────────────────────────────────────
    with h5py.File(args.h5, "r") as f:
        obj_keys = list(f.keys())
    print(f"\nObjects in cache ({len(obj_keys)}): {obj_keys}\n")

    total_pos = total_neg = 0

    for obj_key in tqdm(obj_keys, desc="Generating on-policy data"):
        asset_path, scale = _read_obj_meta(args.h5, obj_key)

        if not os.path.exists(asset_path):
            print(f"  [SKIP] mesh not found: {asset_path}")
            _write_onpolicy(args.h5, obj_key,
                            np.zeros((0, 4, 4), dtype=np.float32),
                            np.zeros((0, 4, 4), dtype=np.float32))
            continue

        # Load and scale object mesh
        obj_mesh = trimesh.load(asset_path, force="mesh")
        obj_mesh.apply_scale(scale)

        # Sample point cloud from scaled mesh surface
        pc, _ = trimesh.sample.sample_surface(obj_mesh, args.pc_points)
        pc = pc.astype(np.float32)

        # Generate grasps with diffusion
        grasps = sample_grasps(model, pc, num_grasps=args.num_grasps)
        print(f"  {obj_key}: {len(grasps)} grasps generated", end="  ")

        # Label via trimesh proximity (FCL-free)
        pos_grasps, neg_grasps = label_grasps(
            grasps, obj_mesh, gripper_mesh, pre_grasp_dist=args.pre_grasp_dist
        )
        print(f"→  {len(pos_grasps)} pos  /  {len(neg_grasps)} neg")
        total_pos += len(pos_grasps)
        total_neg += len(neg_grasps)

        _write_onpolicy(args.h5, obj_key, pos_grasps, neg_grasps)

    print(f"\nDone. Total: {total_pos} positive, {total_neg} negative on-policy grasps.")
    print(f"Cache updated: {args.h5}")
    print()
    print("Next step — retrain discriminator with on-policy data:")
    print(
        "  cd ~/research_ws/GraspGen/scripts && nohup python3 train_graspgen.py \\\n"
        "    train.model_name=discriminator \\\n"
        "    data.load_discriminator_dataset=True \\\n"
        f"    data.onpolicy_dataset_h5_path={args.h5} \\\n"
        "    train.checkpoint=<path/to/disc_last.pth> \\\n"
        "    ... > ~/disc_onpolicy.log 2>&1 &"
    )


if __name__ == "__main__":
    main()
