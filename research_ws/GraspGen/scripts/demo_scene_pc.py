# Copyright (c) 2025, NVIDIA CORPORATION. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto. Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

import argparse
import glob
import json
import os
import time

import numpy as np
import omegaconf
import torch
import trimesh.transformations as tra
from tqdm import tqdm

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
from grasp_gen.utils.point_cloud_utils import (
    point_cloud_outlier_removal_with_color,
    filter_colliding_grasps,
)
from grasp_gen.robot import get_gripper_info


def process_grasps_for_visualization(pc, grasps, grasp_conf, pc_colors=None):
    """Process grasps and point cloud for visualization by centering them."""
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

    return pc_centered, grasps_centered, scores, T_subtract_pc_mean


def parse_args():
    parser = argparse.ArgumentParser(
        description="Visualize grasps on a scene point cloud after GraspGen inference, for entire scene"
    )
    parser.add_argument(
        "--sample_data_dir",
        type=str,
        default="",
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
        default=0.80,
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
    parser.add_argument(
        "--filter_collisions",
        action="store_true",
        help="Whether to filter grasps based on collision detection with scene point cloud",
    )
    parser.add_argument(
        "--collision_threshold",
        type=float,
        default=0.02,
        help="Distance threshold for collision detection (in meters)",
    )
    parser.add_argument(
        "--max_scene_points",
        type=int,
        default=8192,
        help="Maximum number of scene points to use for collision checking (for speed optimization)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.sample_data_dir == "":
        raise ValueError("sample_data_dir is required")
    if args.gripper_config == "":
        raise ValueError("gripper_config is required")

    if not os.path.exists(args.sample_data_dir):
        raise FileNotFoundError(
            f"sample_data_dir {args.sample_data_dir} does not exist"
        )

    # Handle return_topk logic
    if args.return_topk and args.topk_num_grasps == -1:
        args.topk_num_grasps = 100

    json_files = glob.glob(os.path.join(args.sample_data_dir, "*.json"))

    # Load gripper config and get gripper name
    grasp_cfg = load_grasp_cfg(args.gripper_config)
    gripper_name = grasp_cfg.data.gripper_name

    # Get gripper collision mesh for collision filtering
    gripper_info = None
    gripper_collision_mesh = None
    if args.filter_collisions:
        gripper_info = get_gripper_info(gripper_name)
        gripper_collision_mesh = gripper_info.collision_mesh
        print(f"Using gripper: {gripper_name}")
        print(
            f"Gripper collision mesh has {len(gripper_collision_mesh.vertices)} vertices"
        )

    # Initialize GraspGenSampler once
    grasp_sampler = GraspGenSampler(grasp_cfg)

    vis = create_visualizer()

    for json_file in json_files:
        print(json_file)
        vis.delete()

        data = json.load(open(json_file, "rb"))

        obj_pc = np.array(data["object_info"]["pc"])
        obj_pc_color = np.array(data["object_info"]["pc_color"])
        grasps = np.array(data["grasp_info"]["grasp_poses"])
        grasp_conf = np.array(data["grasp_info"]["grasp_conf"])

        full_pc_key = "pc_color" if "pc_color" in data["scene_info"] else "full_pc"
        xyz_scene = np.array(data["scene_info"][full_pc_key])[0]
        xyz_scene_color = np.array(data["scene_info"]["img_color"]).reshape(1, -1, 3)[
            0, :, :
        ]

        # Remove object points from scene point cloud, as we may use this for collision checking later. It is okay if grasps are close to the object point cloud.
        xyz_seg = np.array(data["scene_info"]["obj_mask"]).reshape(-1)
        xyz_scene = xyz_scene[xyz_seg != 1]
        xyz_scene_color = xyz_scene_color[xyz_seg != 1]

        VIZ_BOUNDS = [[-1.5, -1.25, -0.15], [1.5, 1.25, 2.0]]
        mask_within_bounds = np.all((xyz_scene > VIZ_BOUNDS[0]), 1)
        mask_within_bounds = np.logical_and(
            mask_within_bounds, np.all((xyz_scene < VIZ_BOUNDS[1]), 1)
        )
        # mask_within_bounds = np.ones(xyz_scene.shape[0]).astype(np.bool_)

        xyz_scene = xyz_scene[mask_within_bounds]
        xyz_scene_color = xyz_scene_color[mask_within_bounds]

        visualize_pointcloud(vis, "pc_scene", xyz_scene, xyz_scene_color, size=0.0025)

        obj_pc, pc_removed, obj_pc_color, obj_pc_color_removed = (
            point_cloud_outlier_removal_with_color(
                torch.from_numpy(obj_pc), torch.from_numpy(obj_pc_color)
            )
        )
        obj_pc = obj_pc.cpu().numpy()
        pc_removed = pc_removed.cpu().numpy()
        obj_pc_color = obj_pc_color.cpu().numpy()
        obj_pc_color_removed = obj_pc_color_removed.cpu().numpy()

        visualize_pointcloud(vis, "pc_obj", obj_pc, obj_pc_color, size=0.005)

        grasps, grasp_conf = GraspGenSampler.run_inference(
            obj_pc,
            grasp_sampler,
            grasp_threshold=args.grasp_threshold,
            num_grasps=args.num_grasps,
            topk_num_grasps=args.topk_num_grasps,
        )

        if len(grasps) > 0:
            grasp_conf = grasp_conf.cpu().numpy()
            grasps = grasps.cpu().numpy()
            grasps[:, 3, 3] = 1

            # Process grasps for visualization (centering)
            obj_pc_centered, grasps_centered, scores, T_center = (
                process_grasps_for_visualization(
                    obj_pc, grasps, grasp_conf, obj_pc_color
                )
            )

            # Center scene point cloud using same transformation
            xyz_scene_centered = tra.transform_points(xyz_scene, T_center)

            # Apply collision filtering if requested
            collision_free_mask = None
            collision_free_grasps = grasps_centered
            collision_free_scores = scores
            colliding_grasps = None

            if args.filter_collisions:
                print("Applying collision filtering...")
                collision_start = time.time()

                # Downsample scene point cloud for faster collision checking
                if len(xyz_scene_centered) > args.max_scene_points:
                    indices = np.random.choice(
                        len(xyz_scene_centered), args.max_scene_points, replace=False
                    )
                    xyz_scene_downsampled = xyz_scene_centered[indices]
                    print(
                        f"Downsampled scene point cloud from {len(xyz_scene_centered)} to {len(xyz_scene_downsampled)} points"
                    )
                else:
                    xyz_scene_downsampled = xyz_scene_centered
                    print(
                        f"Scene point cloud has {len(xyz_scene_centered)} points (no downsampling needed)"
                    )

                # Filter collision grasps
                collision_free_mask = filter_colliding_grasps(
                    scene_pc=xyz_scene_downsampled,
                    grasp_poses=grasps_centered,
                    gripper_collision_mesh=gripper_collision_mesh,
                    collision_threshold=args.collision_threshold,
                )

                collision_time = time.time() - collision_start
                print(f"Collision detection took: {collision_time:.2f} seconds")

                # Separate collision-free and colliding grasps
                collision_free_grasps = grasps_centered[collision_free_mask]
                colliding_grasps = grasps_centered[~collision_free_mask]
                collision_free_scores = scores[collision_free_mask]

                print(
                    f"Found {len(collision_free_grasps)}/{len(grasps_centered)} collision-free grasps"
                )

            # Visualize collision-free grasps
            grasps_to_visualize = (
                collision_free_grasps if args.filter_collisions else grasps_centered
            )
            scores_to_use = collision_free_scores

            for j, grasp in enumerate(grasps_to_visualize):
                color = scores_to_use[j] if not args.filter_collisions else [0, 185, 0]

                visualize_grasp(
                    vis,
                    f"grasps/{j:03d}/grasp",
                    tra.inverse_matrix(T_center) @ grasp,
                    color=color,
                    gripper_name=gripper_name,
                    linewidth=1.5,
                )

            # Visualize colliding grasps in red if collision filtering is enabled
            if args.filter_collisions and colliding_grasps is not None:
                for j, grasp in enumerate(
                    colliding_grasps[:20]
                ):  # Limit to first 20 for clarity
                    visualize_grasp(
                        vis,
                        f"colliding/{j:03d}/grasp",
                        tra.inverse_matrix(T_center) @ grasp,
                        color=[255, 0, 0],
                        gripper_name=gripper_name,
                        linewidth=0.4,
                    )

                if len(colliding_grasps) > 0:
                    print(
                        f"Showing {min(20, len(colliding_grasps))} colliding grasps in red"
                    )

            # # NOTE: Purely for debugging purposes. Steps through each grasp and visualizes the gripper collision mesh at the grasp location.
            # # Visualize gripper collision mesh at grasp locations
            # if args.filter_collisions and gripper_collision_mesh is not None:
            #     print("\nStarting gripper collision mesh visualization...")

            #     # Combine all grasps with their colors and labels
            #     all_debug_grasps = []

            #     # Add collision-free grasps (green)
            #     for i, grasp in enumerate(collision_free_grasps):
            #         all_debug_grasps.append({
            #             'pose': tra.inverse_matrix(T_center) @ grasp,
            #             'color': [0, 255, 0],  # Green for collision-free
            #             'label': f"collision_free_{i:03d}",
            #             'type': 'collision-free'
            #         })

            #         if i > 5:
            #             break

            #     # Add colliding grasps (red)
            #     if colliding_grasps is not None:
            #         for i, grasp in enumerate(colliding_grasps):
            #             all_debug_grasps.append({
            #                 'pose': tra.inverse_matrix(T_center) @ grasp,
            #                 'color': [255, 0, 0],  # Red for colliding
            #                 'label': f"colliding_{i:03d}",
            #                 'type': 'colliding'
            #             })
            #             if i > 5:
            #                 break

            #     print(f"Total grasps to visualize: {len(all_debug_grasps)}")

            #     # Step through each grasp with tqdm progress bar
            #     for grasp_info in tqdm(all_debug_grasps, desc="Visualizing gripper meshes"):
            #         # Clear previous gripper mesh (if it exists)
            #         try:
            #             vis["gripper_mesh"].delete()
            #         except:
            #             pass  # Gripper mesh doesn't exist yet

            #         # Visualize gripper mesh at grasp pose using transform parameter
            #         visualize_mesh(
            #             vis,
            #             "gripper_mesh",
            #             gripper_collision_mesh,
            #             color=grasp_info['color'],
            #             transform=grasp_info['pose']
            #         )

            #         print(f"\nShowing {grasp_info['type']} grasp: {grasp_info['label']}")
            #         user_input = input("Press Enter for next grasp, 'q' to quit gripper visualization, 's' to skip to next scene: ")

            #         if user_input.lower() == 'q':
            #             try:
            #                 vis["gripper_mesh"].delete()
            #             except:
            #                 pass
            #             break
            #         elif user_input.lower() == 's':
            #             try:
            #                 vis["gripper_mesh"].delete()
            #             except:
            #                 pass
            #             break

            #     # Clean up gripper mesh
            #     try:
            #         vis["gripper_mesh"].delete()
            #     except:
            #         pass
            #     print("Gripper mesh visualization completed.")

            input("Press Enter to continue to next scene...")
        else:
            print("No grasps found! Skipping to next scene...")
