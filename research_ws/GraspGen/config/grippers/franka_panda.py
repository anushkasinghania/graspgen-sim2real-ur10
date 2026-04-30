import torch
import numpy as np
import trimesh
import os
from grasp_gen.robot import load_control_points_core, load_default_gripper_config
from pathlib import Path
import trimesh.transformations as tra
class GripperModel():
    def __init__(self, data_root_dir=None):
        if data_root_dir is None:
            data_root_dir = f'{Path(__file__).parent.parent.parent}/assets/panda_gripper'
        fn_base = data_root_dir + "/hand.stl"
        fn_finger = data_root_dir + "/finger.stl"
        self.base = trimesh.load(fn_base)
        self.finger_l = trimesh.load(fn_finger)
        self.finger_r = self.finger_l.copy()

        # transform fingers relative to the base
        self.finger_l.apply_transform(tra.euler_matrix(0, 0, np.pi))
        self.finger_l.apply_translation([0.04, 0, 0.0584])
        self.finger_r.apply_translation([-0.04, 0, 0.0584])

        self.fingers = trimesh.util.concatenate([self.finger_l, self.finger_r])
        self.mesh = trimesh.util.concatenate([self.fingers, self.base])

    def set_offset(self, offset):
        self.finger_l.apply_translation([offset / 2, 0, 0.0584])
        self.finger_r.apply_translation([-offset / 2, 0, 0.0584])

    def get_gripper_collision_mesh(self):
        return self.mesh

    def get_gripper_visual_mesh(self):
        return self.mesh

def get_gripper_offset_bins():
    # For M2T2-only

    offset_bins = [
        0, 0.00794435329, 0.0158887021, 0.0238330509,
        0.0317773996, 0.0397217484, 0.0476660972,
        0.055610446, 0.0635547948, 0.0714991435, 0.08
    ]

    offset_bin_weights = [
        0.16652107, 0.21488856, 0.37031708, 0.55618503, 0.75124664,
        0.93943357, 1.07824539, 1.19423112, 1.55731375, 3.17161779
    ]
    return offset_bins, offset_bin_weights


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
    return [control_points, ]