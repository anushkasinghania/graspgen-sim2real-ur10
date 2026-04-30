import torch
import numpy as np
import trimesh
import os
from grasp_gen.robot import load_control_points_core, load_default_gripper_config
from pathlib import Path


class GripperModel(object):
    def __init__(self, data_root_dir=None):
        if data_root_dir is None:
            data_root_dir = "/home/ubuntu/robotiq_clean/meshes/collision"
        # Load all collision STLs and combine
        meshes = []
        for stl_file in sorted(Path(data_root_dir).glob("*.STL")):
            m = trimesh.load(str(stl_file))
            meshes.append(m)
        if meshes:
            self.mesh = trimesh.util.concatenate(meshes)
        else:
            # Fallback: create a simple box approximation
            self.mesh = trimesh.primitives.Box(extents=[0.16, 0.16, 0.105])

    def get_gripper_collision_mesh(self):
        return self.mesh

    def get_gripper_visual_mesh(self):
        return self.mesh


def load_control_points() -> torch.Tensor:
    """
    Load the control points for the gripper, used for training.
    Returns a tensor of shape (4, N) where N is the number of control points.
    """
    gripper_config = load_default_gripper_config(Path(__file__).stem)
    control_points = load_control_points_core(gripper_config)
    control_points = np.vstack([control_points, np.zeros(3)])
    control_points = np.hstack([control_points, np.ones([len(control_points), 1])])
    control_points = torch.from_numpy(control_points).float()
    return control_points.T


def load_control_points_for_visualization():
    gripper_config = load_default_gripper_config(Path(__file__).stem)
    control_points = load_control_points_core(gripper_config)
    mid_point = (control_points[0] + control_points[1]) / 2
    control_points = [
        control_points[-2], control_points[0], mid_point,
        [0, 0, 0], mid_point, control_points[1], control_points[-1]
    ]
    return [control_points]
