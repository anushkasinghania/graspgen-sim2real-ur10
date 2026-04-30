"""
Capture a point cloud from OAK-D Pro and save as JSON for GraspGen inference.

Usage:
    python3 scripts/capture_oakd_pc.py --output_dir /tmp/oak_captures --filename scene.json

The script:
  1. Streams depth + RGB from OAK-D Pro
  2. Skips 30 warmup frames so auto-exposure settles
  3. Saves the next frame as JSON: {"pc": [[x,y,z],...], "pc_color": [[r,g,b],...]}

Point cloud is in meters, camera frame (Z = forward, X = right, Y = down).
Depth range filtered to [depth_min, depth_max] meters (default 0.2 – 1.5 m).

For GraspGen, point at a single object on a table from ~50-80 cm away.
"""

import argparse
import json
import os
import time

import depthai as dai
import numpy as np
from sklearn.cluster import DBSCAN


def remove_planes_iterative(points, colors, distance_threshold=0.012,
                            max_iterations=300, max_planes=3,
                            min_plane_ratio=0.10):
    """Iterative RANSAC plane removal.

    Removes up to `max_planes` dominant flat surfaces (floor, box top, shelf, etc.).
    Stops early when the best plane covers < min_plane_ratio of remaining points
    (i.e., no dominant flat surface left — only objects remain).
    """
    rng = np.random.default_rng(42)
    for plane_idx in range(max_planes):
        if len(points) < 10:
            break
        best_inliers = []
        for _ in range(max_iterations):
            idx = rng.choice(len(points), 3, replace=False)
            p1, p2, p3 = points[idx]
            normal = np.cross(p2 - p1, p3 - p1)
            norm_len = np.linalg.norm(normal)
            if norm_len < 1e-6:
                continue
            normal /= norm_len
            d = -np.dot(normal, p1)
            dists = np.abs(points @ normal + d)
            inliers = np.where(dists < distance_threshold)[0]
            if len(inliers) > len(best_inliers):
                best_inliers = inliers
        ratio = len(best_inliers) / len(points)
        if ratio < min_plane_ratio:
            print(f"  RANSAC pass {plane_idx+1}: no dominant plane ({ratio:.1%} < {min_plane_ratio:.0%}), stopping")
            break
        keep = np.ones(len(points), dtype=bool)
        keep[best_inliers] = False
        print(f"  RANSAC pass {plane_idx+1}: removed {(~keep).sum()} plane pts ({ratio:.1%}), kept {keep.sum()}")
        points, colors = points[keep], colors[keep]
    return points, colors


def euclidean_cluster(points, colors, eps=0.025, min_pts=15, min_cluster_pts=50):
    """Return the closest cluster to the camera (smallest mean Z) above min size.

    Picks by proximity rather than size — avoids grabbing walls/floor remnants
    that are large but far behind the object.
    """
    labels = DBSCAN(eps=eps, min_samples=min_pts).fit_predict(points)
    valid_labels = [l for l in set(labels) if l >= 0]
    if not valid_labels:
        print("  DBSCAN: no clusters found — returning all points")
        return points, colors

    # Filter to clusters with at least min_cluster_pts points
    big_labels = [l for l in valid_labels
                  if (labels == l).sum() >= min_cluster_pts]
    if not big_labels:
        big_labels = valid_labels  # fallback: no size filter

    # Pick the cluster closest to the camera (smallest mean Z)
    best = min(big_labels, key=lambda l: points[labels == l, 2].mean())
    mask = labels == best
    print(f"  DBSCAN: {len(valid_labels)} clusters, chose closest (mean Z "
          f"{points[mask, 2].mean():.2f}m, {mask.sum()} pts)")
    return points[mask], colors[mask]


def voxel_downsample(points, colors, voxel_size=0.004):
    voxel_coords = np.floor(points / voxel_size).astype(np.int32)
    _, unique_idx = np.unique(voxel_coords, axis=0, return_index=True)
    return points[unique_idx], colors[unique_idx]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_dir", type=str, default="/tmp/oak_captures",
                        help="Directory to save JSON captures")
    parser.add_argument("--filename", type=str, default="scene.json",
                        help="Output filename (must end in .json)")
    parser.add_argument("--depth_min", type=float, default=0.2,
                        help="Minimum depth in meters (clip closer points)")
    parser.add_argument("--depth_max", type=float, default=1.5,
                        help="Maximum depth in meters (clip farther points)")
    parser.add_argument("--warmup_frames", type=int, default=30,
                        help="Number of frames to skip for auto-exposure to settle")
    return parser.parse_args()


def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    print("Connecting to OAK-D Pro...")

    with dai.Pipeline() as pipeline:
        # --- Stereo depth (auto-creates left/right mono cameras) ---
        stereo = pipeline.create(dai.node.StereoDepth)
        stereo.build(autoCreateCameras=True)
        stereo.setDepthAlign(dai.CameraBoardSocket.CAM_A)  # align depth to color camera
        stereo.setLeftRightCheck(True)
        stereo.setSubpixel(False)  # simpler, lower latency

        # --- Color camera ---
        color = pipeline.create(dai.node.ColorCamera)
        color.setBoardSocket(dai.CameraBoardSocket.CAM_A)
        color.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        color.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
        color.setFps(15)

        # --- Point cloud node (XYZ from depth) ---
        pc_node = pipeline.create(dai.node.PointCloud)
        stereo.depth.link(pc_node.inputDepth)

        # --- Output queues ---
        pc_queue = pc_node.outputPointCloud.createOutputQueue(maxSize=4, blocking=False)
        rgb_queue = color.isp.createOutputQueue(maxSize=4, blocking=False)

        pipeline.start()
        print("Pipeline started. Camera warming up...")

        # Warm up: let AE/AWB settle
        for i in range(args.warmup_frames):
            pc_queue.get()
            rgb_queue.get()
            if i % 10 == 0:
                print(f"  Warmup {i}/{args.warmup_frames}...")

        print("Capturing frame...")
        pc_msg = pc_queue.get()
        rgb_msg = rgb_queue.get()

    # --- Process point cloud ---
    points = pc_msg.getPoints()          # shape (N, 3), units: mm
    points = points.astype(np.float32) / 1000.0  # convert to meters

    # Filter invalid (zero) and out-of-range points
    valid = (
        (points[:, 2] > args.depth_min) &
        (points[:, 2] < args.depth_max) &
        np.all(np.isfinite(points), axis=1)
    )
    points = points[valid]

    # --- Get RGB colors aligned to depth ---
    rgb_frame = rgb_msg.getCvFrame()  # H_rgb x W_rgb x 3 (RGB)
    H_rgb, W_rgb = rgb_frame.shape[:2]
    H_depth = pc_msg.getHeight()
    W_depth = pc_msg.getWidth()

    all_indices = np.arange(H_depth * W_depth)
    row_idx = all_indices // W_depth
    col_idx = all_indices % W_depth
    rgb_row = np.clip((row_idx * H_rgb / H_depth).astype(int), 0, H_rgb - 1)
    rgb_col = np.clip((col_idx * W_rgb / W_depth).astype(int), 0, W_rgb - 1)
    colors_all = rgb_frame[rgb_row, rgb_col]  # (N_all, 3) uint8 RGB
    colors = colors_all[valid].astype(np.float32)

    # Phase 1.5: Table removal + object isolation
    if len(points) > 100:
        print(f"Raw point cloud: {len(points)} pts")

        # Step 1: voxel downsample first for speed
        points, colors = voxel_downsample(points, colors, voxel_size=0.004)
        print(f"After voxel downsample (4mm): {len(points)} pts")

        # Step 2: Z-crop to nearest surface + 40cm — focuses on the object in front
        # of the camera and discards background walls/floor far behind it.
        z_near = np.percentile(points[:, 2], 1)
        z_crop_mask = points[:, 2] < z_near + 0.40
        points, colors = points[z_crop_mask], colors[z_crop_mask]
        print(f"After Z-crop (nearest + 40cm, z>{z_near:.2f}m): {len(points)} pts")

        # Step 3: Iterative RANSAC — removes all dominant flat planes
        # (floor, then box/table top, then any shelf — stops when no plane dominates)
        points, colors = remove_planes_iterative(points, colors,
                                                 distance_threshold=0.012,
                                                 max_iterations=300,
                                                 max_planes=3,
                                                 min_plane_ratio=0.10)
        print(f"After plane removal: {len(points)} pts")

        # Step 4: DBSCAN — keep only the largest object cluster
        if len(points) > 30:
            points, colors = euclidean_cluster(points, colors, eps=0.025, min_pts=15)
            print(f"After object clustering: {len(points)} pts")

    print(f"Captured {len(points)} points after depth filtering [{args.depth_min}m – {args.depth_max}m]")

    if len(points) == 0:
        print("ERROR: No points captured! Check camera connection and depth range.")
        return

    # --- Save ---
    out_path = os.path.join(args.output_dir, args.filename)
    data = {
        "pc": points.tolist(),
        "pc_color": colors.tolist(),
    }
    with open(out_path, "w") as f:
        json.dump(data, f)

    print(f"Saved to: {out_path}")
    print(f"Point cloud stats:")
    print(f"  X: [{points[:,0].min():.3f}, {points[:,0].max():.3f}] m")
    print(f"  Y: [{points[:,1].min():.3f}, {points[:,1].max():.3f}] m")
    print(f"  Z: [{points[:,2].min():.3f}, {points[:,2].max():.3f}] m")


if __name__ == "__main__":
    main()
