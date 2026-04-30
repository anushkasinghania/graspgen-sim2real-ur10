# Copyright (c) 2025, NVIDIA CORPORATION. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto. Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
from pathlib import Path

import argparse
import glob
import json
import os
import omegaconf

import numpy as np
import omegaconf
import torch
import trimesh.transformations as tra
from IPython import embed

from grasp_gen.grasp_server import GraspGenSampler, load_grasp_cfg
from grasp_gen.utils.meshcat_utils import (
    create_visualizer,
    get_color_from_score,
    get_normals_from_mesh,
    make_frame,
    visualize_grasp,
    visualize_mesh,
    visualize_pointcloud,
)
from grasp_gen.utils.point_cloud_utils import point_cloud_outlier_removal


def parse_args():
    parser = argparse.ArgumentParser(
        description="Visualize grasps on a single object point cloud after GraspGen inference"
    )
    parser.add_argument(
        "--sample_data_dir",
        type=str,
        default="/code/realrobot_pc/final/",
        help="Directory containing JSON files with point cloud data",
    )
    parser.add_argument(
        "--gripper_config",
        type=str,
        default="",
        help="Path to gripper configuration YAML file",
    )
    parser.add_argument(
        "--grasp_threshold",
        type=float,
        default=0.8,
        help="Threshold for valid grasps. If -1.0, then the top 100 grasps will be ranked and returned",
    )
    parser.add_argument(
        "--num_grasps",
        type=int,
        default=200,
        help="Number of grasps to generate",
    )
    parser.add_argument(
        "--return_topk",
        action="store_true",
        help="Whether to return only the top k grasps",
    )
    parser.add_argument(
        "--topk_num_grasps",
        type=int,
        default=-1,
        help="Number of top grasps to return when return_topk is True",
    )

    return parser.parse_args()


def process_point_cloud(pc, grasps, grasp_conf):
    """Process point cloud and grasps by centering them."""
    scores = get_color_from_score(grasp_conf, use_255_scale=True)
    print(f"Scores with min {grasp_conf.min():.3f} and max {grasp_conf.max():.3f}")

    # Ensure grasps have correct homogeneous coordinate
    grasps[:, 3, 3] = 1

    # Center point cloud and grasps
    T_subtract_pc_mean = tra.translation_matrix(-pc.mean(axis=0))
    pc_centered = tra.transform_points(pc, T_subtract_pc_mean)
    grasps_centered = np.array(
        [T_subtract_pc_mean @ np.array(g) for g in grasps.tolist()]
    )

    return pc_centered, grasps_centered, scores


if __name__ == "__main__":
    args = parse_args()

    if args.gripper_config == "":
        raise ValueError("Gripper config is required")

    if not os.path.exists(args.gripper_config):
        raise ValueError(f"Gripper config {args.gripper_config} does not exist")

    # Handle return_topk logic
    if args.return_topk and args.topk_num_grasps == -1:
        args.topk_num_grasps = 100

    json_files = glob.glob(os.path.join(args.sample_data_dir, "*.json"))
    vis = create_visualizer()

    grasp_cfg = load_grasp_cfg(args.gripper_config)

    # Gripper-only configs do not have `data`
    if hasattr(grasp_cfg, "data") and "gripper_name" in grasp_cfg.data:
        gripper_name = grasp_cfg.data.gripper_name
    else:
    # fallback: infer from filename
        gripper_name = Path(args.gripper_config).stem


    # Initialize GraspGenSampler once
    grasp_sampler = GraspGenSampler(grasp_cfg)

    for json_file in json_files:
        print(f"Processing {json_file}")
        vis.delete()

        # Load data from JSON
        data = json.load(open(json_file, "rb"))
        pc = np.array(data["pc"])
        pc_color = np.array(data["pc_color"])

        # Center the point cloud (grasp_poses/grasp_conf are optional in the JSON)
        T_subtract_pc_mean = tra.translation_matrix(-pc.mean(axis=0))
        pc_centered = tra.transform_points(pc, T_subtract_pc_mean)

        # Visualize original point cloud
        visualize_pointcloud(vis, "pc", pc_centered, pc_color, size=0.0025)

        # Downsample to max 4096 points before outlier removal
        # (knn is O(N^2) — full room scans will OOM)
        max_points = 4096
        if len(pc_centered) > max_points:
            idx = np.random.choice(len(pc_centered), max_points, replace=False)
            pc_centered = pc_centered[idx]
            pc_color = pc_color[idx]

        # Filter point cloud
        pc_filtered, pc_removed = point_cloud_outlier_removal(
            torch.from_numpy(pc_centered)
        )
        pc_filtered = pc_filtered.numpy()
        pc_removed = pc_removed.numpy()
        visualize_pointcloud(vis, "pc_removed", pc_removed, [255, 0, 0], size=0.003)

        # Run inference on filtered point cloud
        grasps_inferred, grasp_conf_inferred = GraspGenSampler.run_inference(
            pc_filtered,
            grasp_sampler,
            grasp_threshold=args.grasp_threshold,
            num_grasps=args.num_grasps,
            topk_num_grasps=args.topk_num_grasps,
        )

        if len(grasps_inferred) > 0:
            grasp_conf_inferred = grasp_conf_inferred.cpu().numpy()
            grasps_inferred = grasps_inferred.cpu().numpy()
            grasps_inferred[:, 3, 3] = 1
            scores_inferred = get_color_from_score(
                grasp_conf_inferred, use_255_scale=True
            )
            print(
                f"Inferred {len(grasps_inferred)} grasps, with scores ranging from {grasp_conf_inferred.min():.3f} - {grasp_conf_inferred.max():.3f}"
            )

            # Visualize inferred grasps
            for j, grasp in enumerate(grasps_inferred):
                visualize_grasp(
                    vis,
                    f"grasps_objectpc_filtered/{j:03d}/grasp",
                    grasp,
                    color=scores_inferred[j],
                    gripper_name=gripper_name,
                    linewidth=0.6,
                )

        else:
            print("No grasps found from inference! Skipping to next object...")

        input("Press Enter to continue to next object...")
