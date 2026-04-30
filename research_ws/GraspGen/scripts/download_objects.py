# Copyright (c) 2025, NVIDIA CORPORATION. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto. Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#
"""
Download specific Objaverse meshes given their UUIDs.

Installation:
    pip install trimesh==4.5.3 objaverse==0.1.7 meshcat==0.0.12 webdataset==0.2.111

Usage:
    # Download from a single text file:
    python download_objects.py --uuid_list /path_to_dataset/splits/franka_panda/train.txt --output_dir /tmp/objs --simplify

    # Download from all text files in a directory:
    python download_objects.py --uuid_list /path_to_dataset/splits/franka_panda/ --output_dir /tmp/objs --simplify
"""
import argparse
import json
import os
import shutil
import glob
import time
import subprocess
from urllib.error import HTTPError
from multiprocessing import Pool, cpu_count

try:
    from objaverse import load_objects
except ImportError:
    print(
        "Objaverse not found, please see the installation instructions in the top of the file"
    )
    exit(1)

from pathlib import Path

MANIFOLD_PATH = "manifold"
SIMPLIFY_PATH = "simplify"


def load_uuid_list(uuid_list_path: str) -> list[str]:
    """
    Load a list of UUIDs from a text file.

    Args:
        uuid_list_path (str): Path to the UUID list file

    Returns:
        list[str]: List of UUIDs
    """
    if not os.path.exists(uuid_list_path):
        raise FileNotFoundError(f"UUID list file not found: {uuid_list_path}")

    if not uuid_list_path.endswith(".txt"):
        raise ValueError(
            f"Unsupported file format: {uuid_list_path}. Only .txt files are supported."
        )

    uuids = []
    with open(uuid_list_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:  # Skip empty lines
                uuids.append(line)
    return uuids


def simplify_mesh(input_path: str, output_path: str) -> bool:
    """
    Process a mesh through manifold and simplify commands.

    Args:
        input_path (str): Path to input mesh file
        output_path (str): Path to save simplified mesh

    Returns:
        bool: True if simplification was successful, False otherwise
    """

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Waterproof the object
    fname_watertight = output_path.replace(".obj", "_watertight.obj")
    completed = subprocess.run(
        ["timeout", "-sKILL", "30", MANIFOLD_PATH, input_path, fname_watertight],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if completed.returncode != 0:
        print(f"Skipping object (manifold failed): {input_path}")
        return False
    # Simplify the object
    completed = subprocess.run(
        [
            "timeout",
            "-sKILL",
            "30",
            SIMPLIFY_PATH,
            "-i",
            fname_watertight,
            "-o",
            output_path,
            "-m",
            "-r",
            "0.02",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    # Clean up temporary watertight file
    if os.path.exists(fname_watertight):
        os.remove(fname_watertight)

    if completed.returncode != 0:
        print(f"Skipping object (simplify failed): {fname_watertight}")
        return False

    return True


def download_with_retry(uuids: list[str], max_retries: int = 5, batch_size: int = 10):
    """
    Download objects with retry logic and batching.

    Args:
        uuids (list[str]): List of UUIDs to download
        max_retries (int): Maximum number of retry attempts
        batch_size (int): Number of objects to download in each batch

    Returns:
        dict: Dictionary mapping UUIDs to object paths
    """
    all_objects = {}
    total_batches = (len(uuids) + batch_size - 1) // batch_size

    for i in range(0, len(uuids), batch_size):
        batch = uuids[i : i + batch_size]
        batch_num = i // batch_size + 1
        print(f"\nProcessing batch {batch_num}/{total_batches} ({len(batch)} objects)")

        for retry in range(max_retries):
            try:
                # Add delay between batches to avoid rate limiting
                if retry > 0:
                    delay = 2**retry  # Exponential backoff
                    print(f"Retry {retry}/{max_retries} after {delay} seconds...")
                    time.sleep(delay)

                batch_objects = load_objects(uids=batch)
                all_objects.update(batch_objects)
                break
            except HTTPError as e:
                if e.code == 429:  # Too Many Requests
                    if retry == max_retries - 1:
                        print(f"Failed to download batch after {max_retries} retries")
                        raise
                    continue
                raise
            except Exception as e:
                if retry == max_retries - 1:
                    print(f"Error downloading batch: {e}")
                    raise
                continue

    return all_objects


def process_single_object(
    obj_path: str, output_dir: str, simplify: bool = False
) -> tuple[bool, str, str | None]:
    """
    Process a single object: copy to destination, convert if needed, and simplify if requested.

    Args:
        obj_path (str): Path to the source object file
        output_dir (str): Directory where the object should be saved
        simplify (bool): Whether to create a simplified version of the mesh

    Returns:
        tuple[bool, str, str | None]: (success, dest_path, simplified_path)
            - success: True if processing succeeded, False otherwise
            - dest_path: Path to the final destination file
            - simplified_path: Path to simplified file (if simplify=True and successful), None otherwise
    """
    try:
        # Create destination path
        dest_path = os.path.join(output_dir, os.path.basename(obj_path))

        shutil.copy2(obj_path, dest_path)

        print(f"Successfully downloaded and saved object, saved to {dest_path}")

        if dest_path.endswith(".glb"):
            import trimesh

            dest_path_obj = dest_path.replace(".glb", ".obj")
            print(f"Converting glb to obj: from {dest_path} to {dest_path_obj}")
            obj_mesh = trimesh.load(obj_path)
            obj_mesh.export(dest_path_obj)
            dest_path = dest_path_obj

        # Process mesh if simplify is enabled
        simplified_path = None
        if simplify:
            simplified_path = os.path.join(
                output_dir, "simplified", os.path.basename(dest_path)
            )
            if simplify_mesh(dest_path, simplified_path):
                print(f"Successfully simplified object, saved to {simplified_path}")
            else:
                simplified_path = None

        return True, dest_path, simplified_path

    except Exception as e:
        print(f"Error processing object: {e}")
        return False, "", None


def process_single_object_with_uuid(
    uuid_obj_tuple: tuple[str, str], output_dir: str, simplify: bool = False
) -> tuple[str, bool, str, str | None]:
    """
    Wrapper function for multiprocessing that includes the UUID.

    Args:
        uuid_obj_tuple (tuple[str, str]): Tuple of (uuid, obj_path)
        output_dir (str): Directory where the object should be saved
        simplify (bool): Whether to create a simplified version of the mesh

    Returns:
        tuple[str, bool, str, str | None]: (uuid, success, dest_path, simplified_path)
    """
    uuid, obj_path = uuid_obj_tuple

    if obj_path is None:
        print(f"Failed to download object {uuid}")
        return uuid, False, "", None

    success, dest_path, simplified_path = process_single_object(
        obj_path, output_dir, simplify
    )
    return uuid, success, dest_path, simplified_path


def download_objaverse_meshes(
    uuids: list[str], output_dir: str, simplify: bool = False, unused_cpu_count: int = 2
):
    """
    Download specific Objaverse meshes given their UUIDs.

    Args:
        uuids (list[str]): List of UUIDs to download
        output_dir (str): Directory where meshes will be saved
        simplify (bool): Whether to simplify the downloaded meshes
        unused_cpu_count (int): Number of CPUs to leave unused for multiprocessing
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Create simplified directory if needed
    if simplify:
        simplified_dir = os.path.join(output_dir, "simplified")
        os.makedirs(simplified_dir, exist_ok=True)

    # Load existing mapping if it exists
    map_uuid_to_path = {}
    mapping_file = os.path.join(output_dir, "map_uuid_to_path.json")
    if os.path.exists(mapping_file):
        try:
            map_uuid_to_path = json.load(open(mapping_file))
        except Exception as e:
            print(f"Error loading existing mapping: {e}")

    # Initialize simplified mapping and load existing if needed
    if simplify:
        map_uuid_to_path_simplified = {}
        mapping_file_simplified = os.path.join(
            output_dir, "map_uuid_to_path_simplified.json"
        )
        if os.path.exists(mapping_file_simplified):
            try:
                map_uuid_to_path_simplified = json.load(open(mapping_file_simplified))
            except Exception as e:
                print(f"Error loading existing simplified mapping: {e}")

    # Filter out UUIDs that are already downloaded
    uuids_to_download = []
    existing_count = 0

    for uuid in uuids:
        # Check if any file in output_dir contains the UUID
        existing_files = glob.glob(os.path.join(output_dir, f"*{uuid}.obj*"))
        if simplify:
            existing_files = glob.glob(os.path.join(simplified_dir, f"*{uuid}.obj*"))

        if existing_files:
            assert (
                len(existing_files) == 1
            ), f"Multiple files found for UUID {uuid}: {existing_files}"
            assert (
                existing_files[0].find(uuid) >= 0
            ), f"UUID {uuid} not found in {existing_files[0]}"
            existing_count += 1

            # Update mapping with existing file
            map_uuid_to_path[uuid] = os.path.basename(existing_files[0])

            # Check for existing simplified file
            if simplify:
                simplified_files = glob.glob(os.path.join(simplified_dir, f"*{uuid}*"))
                if simplified_files:
                    map_uuid_to_path_simplified[uuid] = os.path.basename(
                        simplified_files[0]
                    )
            continue
        uuids_to_download.append(uuid)

    if existing_count > 0:
        print(f"Found {existing_count} existing objects")
        # Update mapping files with all existing objects
        json.dump(map_uuid_to_path, open(mapping_file, "w"))
        if simplify:
            json.dump(map_uuid_to_path_simplified, open(mapping_file_simplified, "w"))

    if not uuids_to_download:
        print("All objects are already downloaded!")
        return

    print(f"Found {len(uuids_to_download)} new UUIDs to download")

    try:
        # Download objects using Objaverse with retry logic
        objects = download_with_retry(uuids_to_download)
    except Exception as e:
        print(f"Error downloading objects: {e}")
        return

    # Prepare data for multiprocessing
    uuid_obj_pairs = [(uuid, objects[uuid]) for uuid in uuids_to_download]

    # Determine number of processes to use
    num_processes = max(1, cpu_count() - unused_cpu_count)

    if num_processes <= 1:
        # Use sequential processing if not enough CPUs
        print("Using sequential processing (not enough CPUs available)")
        results = []
        for uuid, obj_path in uuid_obj_pairs:
            result = process_single_object_with_uuid(
                (uuid, obj_path), output_dir, simplify
            )
            results.append(result)
            # Clean up the original file
            if obj_path and os.path.exists(obj_path):
                os.remove(obj_path)
    else:
        # Use multiprocessing
        print(f"Using multiprocessing with {num_processes} processes")
        with Pool(num_processes) as p:
            # Create a partial function with fixed arguments
            from functools import partial

            process_func = partial(
                process_single_object_with_uuid,
                output_dir=output_dir,
                simplify=simplify,
            )

            results = list(p.imap_unordered(process_func, uuid_obj_pairs))

            # Clean up original files after processing
            for uuid, obj_path in uuid_obj_pairs:
                if obj_path and os.path.exists(obj_path):
                    os.remove(obj_path)

    # Process results and update mappings
    for uuid, success, dest_path, simplified_path in results:
        if success:
            # Update simplified mapping if simplification was successful
            if simplify and simplified_path:
                map_uuid_to_path_simplified[uuid] = os.path.basename(simplified_path)

            # Store only the base name in the mapping
            map_uuid_to_path[uuid] = os.path.basename(dest_path)
        else:
            print(f"Failed to process object {uuid}")

    # Update both mapping files
    json.dump(map_uuid_to_path, open(mapping_file, "w"))
    if simplify:
        json.dump(map_uuid_to_path_simplified, open(mapping_file_simplified, "w"))

    print("Download complete!")


def process_text_file(
    text_path: str, output_dir: str, simplify: bool = False, unused_cpu_count: int = 2
):
    """
    Process a single text file containing UUIDs.

    Args:
        text_path (str): Path to text file containing UUIDs
        output_dir (str): Directory where meshes will be saved
        simplify (bool): Whether to simplify downloaded meshes
        unused_cpu_count (int): Number of CPUs to leave unused for multiprocessing
    """
    print(f"\nProcessing file: {text_path}")
    uuid_list = load_uuid_list(text_path)
    download_objaverse_meshes(uuid_list, output_dir, simplify, unused_cpu_count)


def process_directory(
    dir_path: str, output_dir: str, simplify: bool = False, unused_cpu_count: int = 2
):
    """
    Process all text files in a directory.

    Args:
        dir_path (str): Path to directory containing text files
        output_dir (str): Directory where meshes will be saved
        simplify (bool): Whether to simplify downloaded meshes
        unused_cpu_count (int): Number of CPUs to leave unused for multiprocessing
    """
    # Find all text files in the directory
    text_files = glob.glob(os.path.join(dir_path, "*.txt"))

    if not text_files:
        print(f"No text files found in directory: {dir_path}")
        return

    print(f"Found {len(text_files)} text files in directory: {dir_path}")

    # Combine all UUIDs from all text files
    all_uuids = []
    for text_file in text_files:
        print(f"Loading UUIDs from: {text_file}")
        uuids = load_uuid_list(text_file)
        all_uuids.extend(uuids)
        print(f"Loaded {len(uuids)} UUIDs from {text_file}")

    # Remove duplicates while preserving order
    unique_uuids = list(dict.fromkeys(all_uuids))
    print(f"Total unique UUIDs across all files: {len(unique_uuids)}")

    # Download all objects
    download_objaverse_meshes(unique_uuids, output_dir, simplify, unused_cpu_count)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--uuid_list",
        type=str,
        help="Path to UUID list text file or directory containing text files",
    )
    parser.add_argument("--output_dir", type=str, help="Path to output directory")
    parser.add_argument(
        "--simplify", action="store_true", help="Whether to simplify downloaded meshes"
    )
    parser.add_argument(
        "--unused_cpu_count",
        type=int,
        default=2,
        help="Number of CPUs to leave unused for multiprocessing",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # Check if input is a directory or file
    if os.path.isdir(args.uuid_list):
        process_directory(
            args.uuid_list, args.output_dir, args.simplify, args.unused_cpu_count
        )
    else:
        process_text_file(
            args.uuid_list, args.output_dir, args.simplify, args.unused_cpu_count
        )
