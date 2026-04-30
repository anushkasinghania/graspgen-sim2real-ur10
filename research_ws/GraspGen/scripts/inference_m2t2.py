#!/usr/bin/env python3

# Copyright (c) 2024, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.
"""
Inference script for M2T2.
"""
import os
from functools import partial
from pathlib import Path
from time import time

import h5py
import hydra
import numpy as np
import torch
import torch.multiprocessing as mp
import trimesh.transformations as tra
from h5py._hl.files import File
from omegaconf import DictConfig
from scene_synthesizer.assets import Asset, BoxAsset, TrimeshAsset
from scene_synthesizer.scene import Scene
from torch_cluster import fps

from grasp_gen.dataset.eval_utils import (
    check_collision,
    get_logger,
    get_timestamp,
    log_worker,
    write_info,
    write_to_h5,
)
from grasp_gen.utils.meshcat_utils import (
    create_visualizer,
    get_color_from_score,
    visualize_grasp,
    visualize_mesh,
    visualize_pointcloud,
)
from grasp_gen.models.m2t2 import M2T2
from grasp_gen.utils.train_utils import get_data_loader, to_cpu, to_gpu


def load_scene(inputs):
    scene = Scene()
    if "table" in inputs:
        table = BoxAsset(inputs["table"]["size"])
        transform = tra.translation_matrix(inputs["table"]["pos"])
        scene.add_object("table", table, transform)
    if "robot_table" in inputs:
        table = BoxAsset(inputs["robot_table"]["size"])
        transform = tra.translation_matrix(inputs["robot_table"]["pos"])
        scene.add_object("robot_table", table, transform)
    if "robot" in inputs:
        robot = Asset(
            f"{Path(__file__).parent.parent}/assets/franka/franka_panda.urdf",
            configuration=inputs["robot"]["config"],
        )
        scene.add_object("robot", robot, inputs["robot"]["pose"])
    return scene


def select_grasp(contacts, confidence, args):
    seed_mask = confidence > args.seed_thresh
    seed_idx = torch.zeros(0).long()
    if seed_mask.sum() > 0:
        ratio = min(args.num_seed_grasps / seed_mask.sum(), 1.0)
        seed_idx = fps(contacts[seed_mask], ratio=ratio)
        # num = min(args.num_seed_grasps, seed_mask.sum())
        # seed_idx = furthest_point_sample(
        #     contacts[seed_mask].unsqueeze(0).cuda(), num
        # ).squeeze(0).cpu()
        seed_idx = np.where(seed_mask)[0][seed_idx]
    more_idx = confidence[~seed_mask].argsort()[::-1]
    num = max(args.max_num_grasps - seed_idx.shape[0], 0)
    more_idx = np.where(~seed_mask)[0][more_idx[:num]]
    selected = np.zeros_like(seed_mask)
    selected[np.concatenate([seed_idx, more_idx])] = True
    return selected


def record_grasps(log, cfg, gripper, inputs, output_file=None):

    args = cfg.eval

    if args.debug and output_file is None:
        vis = create_visualizer()

    start = time()
    scene = load_scene(inputs["scene_info"])
    assets = inputs["scene_info"].pop("assets")
    scales = inputs["scene_info"].pop("scales")
    poses = inputs["scene_info"].pop("poses")
    objects = {}

    for i, (name, asset, scale, pose) in enumerate(
        zip(inputs["names"], assets, scales, poses)
    ):
        mesh_asset = Asset(f"{asset}", scale=scale)
        scene.add_object(asset=mesh_asset, obj_id=name, transform=pose)
        objects[name] = {"asset": asset, "scale": scale, "pose": pose}
    outputs = {"scene_info": inputs["scene_info"], "objects": objects}
    scene_mesh = scene.scene.dump(concatenate=True)

    num_pts = inputs["points"].shape[1]
    all_conf = np.zeros((num_pts,))
    all_grasps = np.zeros((num_pts, 4, 4))
    all_contacts = np.zeros((num_pts, 3))
    proposal_ids = np.zeros((num_pts,)).astype("uint8")

    for i, (mask, confidence, grasps, contacts) in enumerate(
        zip(
            inputs["grasping_masks"],
            inputs["confidence"],
            inputs["grasps"],
            inputs["contacts"],
        )
    ):
        replace = confidence.numpy() > all_conf[mask.numpy()]
        mask[np.where(mask)[0][~replace]] = False
        all_conf[mask] = confidence[replace].numpy()
        all_grasps[mask] = grasps[replace].numpy()
        all_contacts[mask] = contacts[replace].numpy()
        proposal_ids[mask] = np.full(mask.sum(), i)
    all_grasps = inputs["cam_pose"] @ all_grasps
    all_contacts = tra.transform_points(all_contacts, inputs["cam_pose"])
    all_grasps[:, :3, 3] -= all_grasps[:, :3, 2] * args.retract
    grasp_mask = all_conf > 0
    collision = check_collision(scene_mesh, gripper, all_grasps[grasp_mask])
    collision_rate = collision.mean() if collision.shape[0] > 0 else np.nan
    all_col = np.zeros((num_pts,)).astype("bool")
    all_col[grasp_mask] = collision

    assert len(poses) == 1
    T_move_back_to_obj_frame = tra.inverse_matrix(poses[0])
    T_move_from_obj_frame_to_origin = tra.inverse_matrix(T_move_back_to_obj_frame)

    grasps_output, num_grasps = {}, []

    # for i, (name, mask, gt_grasps) in enumerate(zip(
    #     inputs['names'], inputs['obj_masks'], inputs['gt_grasps']
    # )):
    #     mask = mask.numpy() & grasp_mask
    #     if args.seed_thresh is not None and mask.sum() > args.max_num_grasps:
    #         selected = select_grasp(
    #             inputs['points'][mask], all_conf[mask], args
    #         )
    #         mask[np.where(mask)[0][~selected]] = False
    #     num_grasps.append(mask.sum())

    #     if type(gt_grasps) == torch.tensor:
    #         gt_grasps = gt_grasps.numpy()
    #     grasps_output[name] = {
    #         'pred_grasps': T_move_back_to_obj_frame @ all_grasps[mask],
    #         'contacts': all_contacts[mask],
    #         'confidence': all_conf[mask],
    #         'collision': all_col[mask],
    #         'proposal_ids': proposal_ids[mask],
    #         'gt_grasps': T_move_back_to_obj_frame @ inputs['cam_pose'] @ gt_grasps
    #     }
    gt_grasps = inputs["gt_grasps"]
    for i, (name, mask) in enumerate(zip(inputs["names"], inputs["obj_masks"])):
        mask = mask.numpy() & grasp_mask
        if args.seed_thresh is not None and mask.sum() > args.max_num_grasps:
            selected = select_grasp(inputs["points"][mask], all_conf[mask], args)
            mask[np.where(mask)[0][~selected]] = False
        num_grasps.append(mask.sum())

        if type(gt_grasps) == torch.tensor:
            gt_grasps = gt_grasps.numpy()
        grasps_output[name] = {
            "pred_grasps": T_move_back_to_obj_frame @ all_grasps[mask],
            "contacts": all_contacts[mask],
            "confidence": all_conf[mask],
            "collision": all_col[mask],
            "proposal_ids": proposal_ids[mask],
            "gt_grasps": T_move_back_to_obj_frame @ inputs["cam_pose"] @ gt_grasps,
        }

    outputs["grasps"] = grasps_output

    log.info(
        f"Scene {inputs['scene']} Collision rate {collision_rate} "
        f"Total {sum(num_grasps)} Average {np.mean(num_grasps)} grasps"
    )

    gripper_name = cfg.data.gripper_name
    from grasp_gen.robot import get_gripper_info

    gripper_info = get_gripper_info(gripper_name)
    gripper_mesh = gripper_info.collision_mesh

    if args.debug and output_file is None:

        pc = inputs["points"].cpu().numpy()

        # visualize_pointcloud(
        #     vis,
        #     f"point_cloud",
        #     pc,
        #     [245, 66, 90],
        #     size=0.005
        #     )
        # visualize_pointcloud(
        #     vis,
        #     f"point_cloud",
        #     tra.transform_points(pc, T_move_back_to_obj_frame),
        #     [245, 66, 90],
        #     size=0.005
        #     )

        # visualize_mesh(vis, 'scene_mesh', scene_mesh, color=[192, 192, 192], transform=T_move_back_to_obj_frame)
        for name, outputs in grasps_output.items():
            print(f"{name} has {outputs['pred_grasps'].shape[0]} grasps")
            if outputs["pred_grasps"].shape[0] > 0:
                print(
                    f"Confidence min {outputs['confidence'].min()} "
                    f"max {outputs['confidence'].max()}\n"
                    f"Collision rate {outputs['collision'].mean()}"
                )
            color = np.random.randint(0, 256, (3,))

            max_grasps_visualize = 20
            grasps_pred = outputs["pred_grasps"]
            grasps_gt = outputs["gt_grasps"]
            collision = outputs["collision"]
            confidence = outputs["confidence"]
            contacts = outputs["contacts"]

            if len(grasps_pred) > 1:
                mask = np.random.randint(0, len(grasps_pred), max_grasps_visualize)

                grasps_pred = grasps_pred[mask]
                collision = collision[mask]
                confidence = confidence[mask]
                contacts = contacts[mask]

            mask = np.random.randint(0, len(grasps_gt), max_grasps_visualize)
            grasps_gt = grasps_gt[mask]

            dual_plot = False

            if dual_plot:

                T_gt_shift = tra.translation_matrix([0, 0, 0.50])
                T_pred_shift = tra.translation_matrix([0, 0, 0.00])
                visualize_mesh(
                    vis,
                    "mesh_gt",
                    scene_mesh,
                    color=[169, 169, 169],
                    transform=T_gt_shift,
                )
                visualize_mesh(
                    vis,
                    "mesh_pred",
                    scene_mesh,
                    color=[169, 169, 169],
                    transform=T_pred_shift,
                )

                visualize_pointcloud(
                    vis, f"{name}/pred/contacts", contacts, [0, 255, 0], size=0.01
                )

                for j, grasp in enumerate(grasps_pred):
                    visualize_grasp(
                        vis,
                        f"{name}/pred/grasp_{j:03d}",
                        T_move_from_obj_frame_to_origin @ grasp,
                        [0, 0, 255],
                        gripper_name=cfg.data.gripper_name,
                        linewidth=0.2,
                    )
                for j, grasp in enumerate(grasps_gt):
                    visualize_grasp(
                        vis,
                        f"{name}/gt/grasp_{j:03d}",
                        T_gt_shift @ T_move_from_obj_frame_to_origin @ grasp,
                        [0, 255, 0],
                        gripper_name=cfg.data.gripper_name,
                        linewidth=0.2,
                    )
            else:

                visualize_mesh(vis, "scene_mesh", scene_mesh, color=[192, 192, 192])

                visualize_pointcloud(
                    vis, f"{name}/pred/contacts", contacts, [0, 255, 0], size=0.01
                )

                for j, grasp in enumerate(grasps_pred):
                    visualize_grasp(
                        vis,
                        f"{name}/pred/grasp_{j:03d}",
                        T_move_from_obj_frame_to_origin @ grasp,
                        [0, 0, 255],
                        gripper_name=cfg.data.gripper_name,
                        linewidth=0.2,
                    )
                for j, grasp in enumerate(grasps_gt):
                    visualize_grasp(
                        vis,
                        f"{name}/gt/grasp_{j:03d}",
                        T_move_from_obj_frame_to_origin @ grasp,
                        [0, 255, 0],
                        gripper_name=cfg.data.gripper_name,
                        linewidth=0.2,
                    )

                collision = np.logical_not(collision)
                collision = collision.astype(np.float32)
                collision_colors = get_color_from_score(collision, use_255_scale=True)
                collision_colors = collision_colors.astype(np.int32)

                # if len(grasps_pred) > 1:
                #     if  output_file is None:
                #         for j, g in enumerate(grasps_pred):
                #             print(j)
                #             visualize_mesh(
                #                 vis, "gripper", gripper,
                #                 transform=T_move_from_obj_frame_to_origin @ g, color=collision_colors[j].tolist()
                #             )

                #             if j == 15:
                #                 break
                #             input()

        input()

    if output_file is not None:
        key_id = inputs["scene"]

        saved_data_dict = {}

        from grasp_gen.dataset.dataset import load_object_grasp_data

        object_grasp_data = load_object_grasp_data(
            key_id,
            cfg.data.object_root_dir,
            cfg.data.grasp_root_dir,
            cfg.data.dataset_version,
            load_discriminator_dataset=False,
            gripper_info=gripper_info,
        )

        asset_path_rel = "/".join(object_grasp_data.object_asset_path.split("/")[-3:])
        saved_data_dict["asset_path"] = asset_path_rel
        saved_data_dict["asset_scale"] = object_grasp_data.object_scale

        saved_data_dict.update(grasps_output["obj0"])

        print(
            f"Pred {saved_data_dict['pred_grasps'].shape}, Gt {saved_data_dict['gt_grasps'].shape} grasp number"
        )

        del saved_data_dict["proposal_ids"]

        grp = output_file.create_group(key_id)
        start = time()
        write_info(grp, saved_data_dict)
        end = time()
        print(f"Writing scene {key_id} data took", end - start, "s")

    time_taken = time() - start
    log.info(
        f"Scene {inputs['scene']} took {round(time_taken,2)} s, saved to {output_file}"
    )


def record_worker(rank, queue, log_queue, record_fn, gripper, args, output_file):
    log = get_logger(f"Worker {rank:02d}", log_queue)
    log.info("Started")
    while True:
        inputs = queue.get()
        if inputs is None:
            break
        record_fn(log, args, gripper, inputs, output_file)
        queue.task_done()


@hydra.main(config_path=".", config_name="config", version_base="1.3")
def main(cfg: DictConfig) -> None:
    scenes = np.arange(cfg.eval.first_scene, cfg.eval.last_scene)
    sampler, loader = get_data_loader(
        cfg.eval,
        cfg.data,
        cfg.eval.split,
        scenes,
        use_ddp=False,
        training=False,
        inference=True,
    )
    model = M2T2.from_config(cfg.m2t2)
    ckpt = torch.load(cfg.eval.checkpoint, map_location="cpu")
    ckpt_mapped = {}
    for key, val in ckpt["model"].items():
        new_key = key.replace("backbone", "scene_encoder")
        new_key = new_key.replace("transformer", "contact_decoder")
        new_key = new_key.replace("contact_mlp", "grasp_mlp")
        new_key = new_key.replace("con_mask_head", "grasp_mask_head")
        new_key = new_key.replace(".feature_proj", ".scene_feature_proj")
        ckpt_mapped[new_key] = val
    model.load_state_dict(ckpt_mapped)
    model = model.cuda().eval()

    from grasp_gen.robot import get_gripper_info

    gripper_info = get_gripper_info(cfg.data.gripper_name)
    gripper = gripper_info.collision_mesh

    mp.set_start_method("spawn")
    log_queue = mp.Queue()
    log_proc = mp.Process(target=log_worker, args=(log_queue,))
    log_proc.start()
    log = get_logger("main", log_queue)

    output_file = None
    h5_handle = None
    if cfg.eval.output_dir is not None:
        os.makedirs(cfg.eval.output_dir, exist_ok=True)

        h5_file_name = f"{cfg.eval.exp_name}_{cfg.data.gripper_name}_{cfg.data.dataset_name}_{cfg.eval.split}.h5"
        output_file_path = os.path.join(cfg.eval.output_dir, h5_file_name)
        log.info(f"Saving to {output_file_path}")
        os.system(f"rm {output_file_path}")  # For safety

        output_file = h5py.File(output_file_path, "a")

        misc_data = {
            "gripper_name": cfg.data.gripper_name,
            "dataset_name": cfg.data.dataset_name,
            "dataset_version": cfg.data.dataset_version,
            "model": cfg.eval.exp_name,
        }
        grp = output_file.create_group("misc")
        write_info(grp, misc_data)
        h5_handle = output_file.create_group("objects")

        # Evaluate all grasps
        log.info(f"Evaluating all grasps without thresholding")
        cfg.eval.object_thresh = -1.0
        cfg.eval.mask_thresh = -1.0

    record_fn = record_grasps
    if not cfg.eval.debug:
        queue = mp.JoinableQueue()
        procs = [
            mp.Process(
                target=record_worker,
                args=(i, queue, log_queue, record_fn, gripper, cfg, h5_handle),
            )
            for i in range(cfg.eval.num_procs)
        ]
        for p in procs:
            p.start()

    data_time, infer_time, record_time, num_scenes = 0, 0, 0, 0
    start = time()
    for i, data in enumerate(loader):
        if data is None:
            continue
        to_gpu(data)
        num_scenes += len(data["scene"])
        data_time += time() - start

        start = time()
        with torch.no_grad():
            outputs = model.infer(data, cfg.eval)
        infer_time += time() - start
        start = time()

        to_cpu(data)
        to_cpu(outputs)
        for j in range(len(data["scene"])):
            if cfg.eval.cam_coord:
                cam_pose = data["cam_pose"][j].numpy()
            else:
                cam_pose = np.eye(4)
            inputs = {
                "scene": data["scene"][j].split("/")[-1],
                "scene_info": data["scene_info"][j],
                "cam_pose": cam_pose,
                "names": data["names"][j],
                "points": data["points"][j],
            }
            inputs.update(
                {
                    "gt_grasps": data["grasps_ground_truth"][j],
                    "confidence": outputs["grasp_confidence"][j],
                    "grasping_masks": outputs["grasping_masks"][j],
                }
            )

            if "instance_masks" in data:
                inputs.update(
                    {
                        "obj_masks": data["instance_masks"][j].bool(),
                    }
                )

            if "grasps" in outputs:
                inputs.update(
                    {
                        "grasps": outputs["grasps"][j],
                    }
                )

            if "grasp_contacts" in outputs:
                inputs.update(
                    {
                        "contacts": outputs["grasp_contacts"][j],
                    }
                )

            if cfg.eval.debug:
                record_fn(log, cfg, gripper, inputs, h5_handle)
            else:
                queue.put(inputs)

        record_time += time() - start
        start = time()
        if (i + 1) % cfg.eval.print_freq == 0:
            log.info(
                f"{i+1}/{len(loader)} "
                f"Data time {data_time / num_scenes} "
                f"Inference time {infer_time / num_scenes} "
                f"Record time {record_time / num_scenes}"
            )
            data_time, infer_time, record_time, num_scenes = 0, 0, 0, 0

    if output_file is not None:
        output_file.close()

    if not cfg.eval.debug:
        queue.join()
        print("All work completed")
        for _ in range(cfg.eval.num_procs * 2):
            queue.put(None)
        for p in procs:
            p.join()
    log_queue.put(None)
    log_proc.join()


if __name__ == "__main__":
    main()
