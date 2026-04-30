import torch
import numpy as np
import trimesh
import os
from grasp_gen.robot import load_control_points_core, load_default_gripper_config, load_visualize_control_points_multi_suction, parse_offset_transform_from_yaml
from pathlib import Path
import trimesh.transformations as tra

class GripperModel(object):
    def __init__(self, data_root_dir=None, simplified=True):
        if data_root_dir is None:
            data_root_dir = f'{Path(__file__).parent.parent.parent}/assets/suction'
        fn_base = data_root_dir + "/suction_cup.obj"
        self.mesh = trimesh.load(fn_base).dump(concatenate=True)
        self.simplified = simplified

    def get_gripper_collision_mesh(self):
        if self.simplified:
            return self.mesh.bounding_cylinder
        else:
            return self.mesh

    def get_gripper_visual_mesh(self):
        return self.mesh


def load_visualize_control_points_suction():
    pts = [
        [0.0, 0, 0],
    ]
    return load_visualize_control_points_multi_suction(pts)

def load_control_points() -> torch.Tensor:
    """
    Load the control points for the gripper, used for training.
    Returns a tensor of shape (4, N) where N is the number of control points.
    """
    gripper_config = load_default_gripper_config(Path(__file__).stem)
    control_points = load_control_points_core(gripper_config)
    control_points = np.hstack([control_points, np.ones([len(control_points), 1])])
    control_points = torch.from_numpy(control_points).float()
    return control_points.T

def load_control_points_for_visualization():

    gripper_config = load_default_gripper_config(Path(__file__).stem)
    # TODO: Move this to gripper python script
    control_points = load_visualize_control_points_suction()

    # NOTE - This is the transform offset from converting a gripper from its original axis to the graspgen convention
    if "transform_offset_from_asset_to_graspgen_convention" in gripper_config:
        offset_transform = parse_offset_transform_from_yaml(gripper_config['transform_offset_from_asset_to_graspgen_convention'])
    else:
        offset_transform = np.eye(4)

    ctrl_pts = [tra.transform_points(cpt, offset_transform) for cpt in control_points]

    depth = gripper_config['depth']

    line_pts = np.array([[0,0,0], [0,0,depth]])
    line_pts = np.expand_dims(line_pts, 0)
    line_pts = [tra.transform_points(cpt, offset_transform) for cpt in line_pts]
    line_pts = line_pts[0]
    ctrl_pts.append(line_pts)
    return ctrl_pts


def get_transform_from_base_link_to_tool_tcp():
    """
    This is because the gripper base_link is coincident with the tool TCP.
    """
    return tra.translation_matrix([0, 0, 0.0])