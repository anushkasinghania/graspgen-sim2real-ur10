#!/usr/bin/env python3
"""
Convert GraspDataGen YAML output to GraspGen training format.

Converts Isaac Grasp YAML files to:
1. JSON files compatible with GraspJsonDatasetReader
2. WebDataset tar shards compatible with GraspWebDatasetReader  
3. Train/valid split files
4. UUID index files

Usage:
    python convert_yaml_to_graspgen.py \
        --yaml_dir /path/to/datagen_sim_data/robotiq_3f_clean \
        --object_dir /path/to/objects \
        --output_dir /path/to/graspgen_dataset \
        --gripper_name robotiq_3f \
        --valid_ratio 0.2
"""

import argparse
import json
import os
import glob
import numpy as np
import yaml
import re

try:
    import webdataset as wds
    HAS_WDS = True
except ImportError:
    HAS_WDS = False
    print("Warning: webdataset not installed. Only JSON format will be generated.")


def quat_pos_to_4x4(position, orientation_w, orientation_xyz):
    """Convert position + quaternion (w, xyz) to 4x4 homogeneous matrix."""
    x, y, z = position
    qw = orientation_w
    qx, qy, qz = orientation_xyz

    # Rotation matrix from quaternion
    r00 = 1 - 2*(qy*qy + qz*qz)
    r01 = 2*(qx*qy - qz*qw)
    r02 = 2*(qx*qz + qy*qw)
    r10 = 2*(qx*qy + qz*qw)
    r11 = 1 - 2*(qx*qx + qz*qz)
    r12 = 2*(qy*qz - qx*qw)
    r20 = 2*(qx*qz - qy*qw)
    r21 = 2*(qy*qz + qx*qw)
    r22 = 1 - 2*(qx*qx + qy*qy)

    T = [
        [r00, r01, r02, x],
        [r10, r11, r12, y],
        [r20, r21, r22, z],
        [0.0, 0.0, 0.0, 1.0]
    ]
    return T


def yaml_to_graspgen_json(yaml_path, object_dir):
    """Convert a single YAML file to GraspGen JSON format."""
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)

    if not data or 'grasps' not in data:
        return None

    # Extract object info
    object_file = data.get('object_file', '')
    object_scale = data.get('object_scale', 1.0)
    
    # Extract UUID from object file path
    basename = os.path.splitext(os.path.basename(object_file))[0]
    # Remove common prefixes from datagen naming
    uuid = basename

    grasps = data['grasps']
    transforms = []
    object_in_gripper = []

    for grasp_name, grasp in grasps.items():
        pos = grasp.get('position', [0, 0, 0])
        orient = grasp.get('orientation', {})
        w = orient.get('w', 1.0)
        xyz = orient.get('xyz', [0, 0, 0])
        confidence = grasp.get('confidence', 0.0)

        T = quat_pos_to_4x4(pos, w, xyz)
        transforms.append(T)
        object_in_gripper.append(bool(confidence > 0.5))

    if len(transforms) == 0:
        return None

    graspgen_data = {
        "object": {
            "file": uuid,
            "scale": float(object_scale)
        },
        "grasps": {
            "transforms": transforms,
            "object_in_gripper": object_in_gripper
        }
    }

    num_pos = sum(object_in_gripper)
    num_neg = len(object_in_gripper) - num_pos
    
    return graspgen_data, uuid, num_pos, num_neg


def main():
    parser = argparse.ArgumentParser(description="Convert GraspDataGen YAML to GraspGen format")
    parser.add_argument("--yaml_dir", required=True, help="Directory containing YAML files")
    parser.add_argument("--object_dir", required=True, help="Directory containing object meshes")
    parser.add_argument("--output_dir", required=True, help="Output directory for GraspGen dataset")
    parser.add_argument("--gripper_name", default="robotiq_3f", help="Gripper name")
    parser.add_argument("--valid_ratio", type=float, default=0.2, help="Validation split ratio")
    parser.add_argument("--num_shards", type=int, default=1, help="Number of WebDataset shards")
    args = parser.parse_args()

    # Create output directories
    grasp_dir = os.path.join(args.output_dir, "grasp_data", args.gripper_name)
    split_dir = os.path.join(args.output_dir, "splits", args.gripper_name)
    os.makedirs(grasp_dir, exist_ok=True)
    os.makedirs(split_dir, exist_ok=True)

    # Find all YAML files
    yaml_files = sorted(glob.glob(os.path.join(args.yaml_dir, "**/*.yaml"), recursive=True))
    print(f"Found {len(yaml_files)} YAML files")

    # Convert each YAML file
    all_data = {}
    total_pos = 0
    total_neg = 0
    
    for yaml_path in yaml_files:
        result = yaml_to_graspgen_json(yaml_path, args.object_dir)
        if result is None:
            print(f"  Skipping {os.path.basename(yaml_path)} (no grasps)")
            continue
        
        graspgen_data, uuid, num_pos, num_neg = result
        
        if uuid in all_data:
            # Merge grasps from duplicate files
            all_data[uuid]["grasps"]["transforms"].extend(graspgen_data["grasps"]["transforms"])
            all_data[uuid]["grasps"]["object_in_gripper"].extend(graspgen_data["grasps"]["object_in_gripper"])
            num_pos_total = sum(all_data[uuid]["grasps"]["object_in_gripper"])
            num_neg_total = len(all_data[uuid]["grasps"]["object_in_gripper"]) - num_pos_total
            print(f"  Merged {os.path.basename(yaml_path)} -> {uuid} (total: {num_pos_total} pos, {num_neg_total} neg)")
        else:
            all_data[uuid] = graspgen_data
            print(f"  Converted {os.path.basename(yaml_path)} -> {uuid} ({num_pos} pos, {num_neg} neg)")
        
        total_pos += num_pos
        total_neg += num_neg

    print(f"\nTotal: {len(all_data)} objects, {total_pos} positive grasps, {total_neg} negative grasps")

    if len(all_data) == 0:
        print("No data to convert!")
        return

    # Save as individual JSON files (for GraspJsonDatasetReader)
    json_dir = os.path.join(grasp_dir, "json")
    os.makedirs(json_dir, exist_ok=True)
    
    map_uuid_to_path = {}
    for uuid, data in all_data.items():
        json_path = os.path.join(json_dir, f"{uuid}.json")
        with open(json_path, 'w') as f:
            json.dump(data, f)
        map_uuid_to_path[uuid] = f"{uuid}.json"
    
    # Save UUID to path mapping
    with open(os.path.join(json_dir, "map_uuid_to_path.json"), 'w') as f:
        json.dump(map_uuid_to_path, f, indent=2)

    # Create WebDataset tar shards
    if HAS_WDS:
        uuids = list(all_data.keys())
        items_per_shard = max(1, len(uuids) // args.num_shards)
        uuid_index = {}
        
        for shard_idx in range(args.num_shards):
            start = shard_idx * items_per_shard
            end = start + items_per_shard if shard_idx < args.num_shards - 1 else len(uuids)
            
            shard_path = os.path.join(grasp_dir, f"shard_{shard_idx:03d}.tar")
            with wds.TarWriter(shard_path) as sink:
                for uuid in uuids[start:end]:
                    sample = {
                        "__key__": uuid,
                        "grasps.json": json.dumps(all_data[uuid])
                    }
                    sink.write(sample)
                    uuid_index[uuid] = shard_idx
            
            print(f"  Created shard {shard_idx}: {end - start} objects")
        
        # Save UUID index
        with open(os.path.join(grasp_dir, "uuid_index.json"), 'w') as f:
            json.dump(uuid_index, f, indent=2)

    # Create train/valid splits
    uuids = list(all_data.keys())
    np.random.seed(42)
    np.random.shuffle(uuids)
    
    split_idx = int(len(uuids) * (1 - args.valid_ratio))
    train_uuids = uuids[:split_idx]
    valid_uuids = uuids[split_idx:]

    with open(os.path.join(split_dir, "train.txt"), 'w') as f:
        f.write('\n'.join(train_uuids))
    
    with open(os.path.join(split_dir, "valid.txt"), 'w') as f:
        f.write('\n'.join(valid_uuids))

    # Also save as JSON for compatibility
    with open(os.path.join(split_dir, "train_scenes.json"), 'w') as f:
        json.dump(train_uuids, f)
    
    with open(os.path.join(split_dir, "valid_scenes.json"), 'w') as f:
        json.dump(valid_uuids, f)

    print(f"\nDataset created at {args.output_dir}")
    print(f"  Train: {len(train_uuids)} objects")
    print(f"  Valid: {len(valid_uuids)} objects")
    print(f"  Total grasps: {total_pos + total_neg} ({total_pos} pos, {total_neg} neg)")
    print(f"\nTo train GraspGen:")
    print(f"  export GRASP_DATASET_DIR={grasp_dir}")
    print(f"  export SPLIT_DATASET_DIR={split_dir}")
    print(f"  export OBJECT_DATASET_DIR={args.object_dir}")


if __name__ == "__main__":
    main()
