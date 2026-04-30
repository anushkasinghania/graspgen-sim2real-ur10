# Copyright (c) 2025, NVIDIA CORPORATION. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto. Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#
# Author: Adithya Murali
"""
Inference script for GraspGen.
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
from inference_m2t2 import load_scene, record_worker
from omegaconf import DictConfig
from scene_synthesizer.assets import Asset, BoxAsset, TrimeshAsset
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
from grasp_gen.robot import get_gripper_info
from grasp_gen.utils.train_utils import get_data_loader, to_cpu, to_gpu
from grasp_gen.dataset.webdataset_utils import GraspWebDatasetReader, is_webdataset


def record_grasps_diffusion(log, cfg, gripper, inputs, output_file=None):

    args = cfg.eval
    if args.debug and output_file is None:
        from grasp_gen.utils.meshcat_utils import create_visualizer, visualize_mesh

        vis = create_visualizer()

    start = time()
    scene = load_scene(inputs["scene_info"])
    assets = inputs["scene_info"].pop("assets")
    scales = inputs["scene_info"].pop("scales")
    poses = inputs["scene_info"].pop("poses")
    objects = {}

    if "names" not in inputs:
        inputs["names"] = ["obj0"]

    for i, (name, asset, scale, pose) in enumerate(
        zip(inputs["names"], assets, scales, poses)
    ):
        if asset.find("/lustre") >= 0:
            asset_abs = os.path.join(cfg.data.object_root_dir, asset)
        mesh_asset = Asset(f"{asset}", scale=scale)
        scene.add_object(asset=mesh_asset, obj_id=name, transform=pose)
        objects[name] = {"asset": asset, "scale": scale, "pose": pose}
    outputs = {"scene_info": inputs["scene_info"], "objects": objects}
    scene_mesh = scene.scene.dump(concatenate=True)

    num_grasps = inputs["grasps_pred"].shape[0]
    all_grasps = inputs["grasps_pred"].cpu().numpy()
    grasps_gt = inputs["gt_grasps"]
    if type(grasps_gt) == torch.tensor:
        grasps_gt = inputs["gt_grasps"].cpu().numpy()
    if "labels" in inputs:
        labels = inputs["labels"].cpu().numpy()
        label_mask = np.where(labels.flatten())[0]
        grasps_gt = grasps_gt[label_mask]

    if "confidence" in inputs:
        all_conf = inputs["confidence"]
        if len(all_conf.shape) == 2:
            all_conf = all_conf.squeeze(1)
    else:
        all_conf = np.ones(num_grasps)

    if "likelihood" in inputs:
        all_likelihood = inputs["likelihood"]
        if len(all_likelihood.shape) == 2:
            all_likelihood = all_likelihood.squeeze(1)

    all_grasps = inputs["cam_pose"] @ all_grasps
    grasp_mask = all_conf >= 0
    if (
        cfg.data.gripper_name.find("suction") >= 0
    ):  # The mesh is not relevant for this yet, there is a bug?
        collision = np.zeros(all_grasps.shape[0])  # Do not check for collisions
    else:
        collision = check_collision(scene_mesh, gripper, all_grasps)

    # from IPython import embed; embed()

    # from grasp_gen.utils.meshcat_utils import visualize_mesh, create_visualizer, visualize_grasp
    # import glob
    # import os
    # import json
    # import trimesh
    # import numpy as np
    # vis = create_visualizer()
    # vis.delete()

    # visualize_mesh(vis, 'scene_mesh', scene_mesh, transform=np.eye(4), color=[128, 128, 128])
    # visualize_mesh(vis, 'gripper_mesh', gripper, transform=np.eye(4), color=[128, 128, 128])

    # for i, g in enumerate(all_grasps):
    #     visualize_mesh(vis, 'gripper_mesh', gripper, transform=g, color=[128, 128, 128])
    #     input()
    # print(f"Num of colliding grasps {collision.sum()}")

    collision_rate = collision.mean() if num_grasps > 0 else np.nan
    all_col = np.zeros((num_grasps,)).astype("bool")
    all_col[grasp_mask] = collision
    assert len(poses) == 1
    import trimesh.transformations as tra

    T_move_back_to_obj_frame = tra.inverse_matrix(poses[0])
    T_move_from_obj_frame_to_origin = tra.inverse_matrix(T_move_back_to_obj_frame)

    grasps_output, num_grasps = {}, []

    num_grasps.append(all_grasps.shape[0])

    grasps_output["obj0"] = {
        "pred_grasps": T_move_back_to_obj_frame @ all_grasps,
        "confidence": all_conf,
        "likelihood": all_likelihood,
        "collision": all_col,
        "gt_grasps": T_move_back_to_obj_frame @ inputs["cam_pose"] @ grasps_gt,
    }

    log.info(
        f"Scene {inputs['scene']} Collision rate {collision_rate} "
        f"Total {sum(num_grasps)} Average {np.mean(num_grasps)} grasps"
    )

    new_grasps = []
    from copy import deepcopy as copy

    for g in all_grasps:
        new_grasp = copy(np.array(g.tolist()))
        new_grasp[:3, 3] += T_move_back_to_obj_frame[:3, 3]
        new_grasps.append(new_grasp)
    new_grasps = np.array(new_grasps)
    grasps_output["obj0"]["pred_grasps"] = new_grasps

    gripper_name = cfg.data.gripper_name
    from grasp_gen.robot import get_gripper_info

    gripper_info = get_gripper_info(gripper_name)
    gripper_mesh = gripper_info.collision_mesh

    if args.debug and output_file is None:
        if "xyz" in inputs:
            pc = inputs["xyz"][0].reshape(-1, 3).cpu().numpy()
        else:
            pc = inputs["points"][0].reshape(-1, 3).cpu().numpy()

        import trimesh.transformations as tra

        pc_color = inputs["rgb"].reshape(-1, 3).float().cpu().numpy()
        grasps_pred = grasps_output["obj0"]["pred_grasps"]
        grasps_gt = grasps_output["obj0"]["gt_grasps"]

        # grasps_pred = np.array([T_move_from_obj_frame_to_origin @ g for g in grasps_pred])
        # grasps_gt = np.array([T_move_from_obj_frame_to_origin @ g for g in grasps_gt])

        grasps_per_iteration = inputs["grasps_per_iteration"].cpu().numpy()
        # NOTE: For some reason, grasps_pred tensor is not working, so all_grasps is used below

        # Plotting args
        dual_plot = False
        step_diffusion_iterations = False
        if dual_plot:
            assert not step_diffusion_iterations
        plot_reverse = True
        plot_thresholded = True
        plot_mesh = True
        use_likelihood_as_score = False

        if use_likelihood_as_score:
            scores = all_likelihood.cpu().numpy()
            score_range = scores.max() - scores.min()
            scores = (scores - scores.min()) / score_range
            scores = get_color_from_score(scores, use_255_scale=True)
        else:
            scores = get_color_from_score(all_conf.cpu().numpy(), use_255_scale=True)

        print(f"Confidence, max: {all_conf.max()}, min {all_conf.min()}")
        print(f"Likelihood, max: {all_likelihood.max()}, min {all_likelihood.min()}")

        if dual_plot:

            delta = 0.75

            # T_gt_shift = tra.translation_matrix([0, 0, delta]) @ T_move_back_to_obj_frame
            # T_pred_shift = tra.translation_matrix([0, 0, 0.00]) @ T_move_back_to_obj_frame
            T_gt_shift = (
                tra.translation_matrix([0, 0, delta]) @ T_move_from_obj_frame_to_origin
            )
            T_pred_shift = (
                tra.translation_matrix([0, 0, 0.00]) @ T_move_from_obj_frame_to_origin
            )
            # visualize_pointcloud(
            #     vis, 'pc_gt', tra.transform_points(pc, T_gt_shift), [169, 169, 169], size=0.008
            # )

            # visualize_pointcloud(
            #     vis, 'pc_pred', tra.transform_points(pc, T_pred_shift), [169, 169, 169], size=0.008
            # )
            visualize_mesh(
                vis,
                "mesh_gt",
                scene_mesh,
                color=[169, 169, 169],
                transform=tra.translation_matrix([0, 0, delta]),
            )
            visualize_mesh(
                vis,
                "mesh_pred",
                scene_mesh,
                color=[169, 169, 169],
                transform=tra.translation_matrix([0, 0, 0.00]),
            )
            # visualize_mesh(vis, "mesh_gt_thresh", scene_mesh, color=[169, 169, 169], transform=tra.translation_matrix([0, 0, -delta]))

            for j, grasp in enumerate(grasps_gt):
                visualize_grasp(
                    vis,
                    f"gt/grasp_{j:03d}",
                    T_gt_shift @ grasp,
                    [0, 150, 40],
                    gripper_name=cfg.data.gripper_name,
                    linewidth=0.5,
                )

                if plot_mesh:
                    visualize_mesh(
                        vis,
                        f"meshes/gt/grasp_{j:03d}",
                        gripper_mesh,
                        color=[0, 255, 0],
                        transform=T_gt_shift @ grasp.astype(np.float32),
                    )

            if plot_thresholded:
                threshold = cfg.eval.mask_thresh
                print(f"Thresholding grasps at {threshold}")
                mask_thresh = all_conf.cpu().numpy() > threshold
                grasps_thresholded = all_grasps[mask_thresh]

                for j, grasp in enumerate(grasps_thresholded):
                    visualize_grasp(
                        vis,
                        f"thresh/grasp_{j:03d}",
                        grasp,
                        [0, 150, 250],
                        gripper_name=cfg.data.gripper_name,
                        linewidth=0.8,
                    )

                    if plot_mesh:
                        visualize_mesh(
                            vis,
                            f"meshes/pred/grasp_{j:03d}",
                            gripper_mesh,
                            color=[0, 150, 250],
                            transform=grasp.astype(np.float32),
                        )
            else:

                # NOTE: For some reason, grasps_pred tensor is not working, so all_grasps is used below
                for j, grasp in enumerate(all_grasps):
                    visualize_grasp(
                        vis,
                        f"pred/grasp_{j:03d}",
                        grasp,
                        scores[j],
                        gripper_name=cfg.data.gripper_name,
                        linewidth=0.2,
                    )
                    if plot_mesh:
                        visualize_mesh(
                            vis,
                            f"meshes/pred/grasp_{j:03d}",
                            gripper_mesh,
                            color=scores[j],
                            transform=grasp.astype(np.float32),
                        )

        else:

            if plot_thresholded:
                threshold = cfg.eval.mask_thresh
                if all_conf.cpu().numpy().max() <= threshold:
                    threshold = max(0, all_conf.cpu().numpy().max() - 0.10)
                mask_thresh = all_conf.cpu().numpy() > threshold

                grasps_visualized = all_grasps[mask_thresh]
                scores_visualized = scores[mask_thresh]
                print(
                    f"Thresholding grasps at {threshold}. {grasps_visualized.shape[0]}/{all_grasps.shape[0]} grasps remaining to visualize"
                )

                for j, grasp in enumerate(grasps_visualized):
                    visualize_grasp(
                        vis,
                        f"pred_thresholded/grasp_{j:03d}",
                        grasp,
                        color=[0, 150, 250],
                        gripper_name=cfg.data.gripper_name,
                        linewidth=0.2,
                    )
                    if j < 10:
                        if plot_mesh:
                            visualize_mesh(
                                vis,
                                f"pred_thresholded_meshes/grasp_{j:03d}",
                                gripper_mesh,
                                color=[0, 40, 150],
                                transform=grasp,
                            )

            visualize_mesh(vis, "scene_mesh", scene_mesh, color=[192, 192, 192])
            # if not step_diffusion_iterations:
            #     visualize_pointcloud(
            #         vis, 'pc', pc, [245, 66, 90], size=0.008
            #     )

            for j, grasp in enumerate(all_grasps):
                visualize_grasp(
                    vis,
                    f"pred/grasp_{j:03d}",
                    grasp,
                    scores[j],
                    gripper_name=cfg.data.gripper_name,
                    linewidth=0.2,
                )
                if j < 10:
                    if plot_mesh:
                        visualize_mesh(
                            vis,
                            f"pred_meshes/grasp_{j:03d}",
                            gripper_mesh,
                            color=[0, 40, 150],
                            transform=grasp,
                        )

            for j, grasp in enumerate(grasps_gt):
                visualize_grasp(
                    vis,
                    f"gt/grasp_{j:03d}",
                    T_move_from_obj_frame_to_origin @ grasp,
                    [0, 150, 40],
                    gripper_name=cfg.data.gripper_name,
                    linewidth=0.5,
                )

        if step_diffusion_iterations:
            timesteps = list(range(len(grasps_per_iteration)))
            if plot_reverse:
                timesteps.reverse()
            for t in timesteps:
                print(t)
                grasps_t = grasps_per_iteration[t]
                for j, g in enumerate(grasps_t):
                    if j < 10:
                        visualize_grasp(
                            vis,
                            f"t/grasp_{j:03d}",
                            g,
                            [200, 0, 0],
                            gripper_name=cfg.data.gripper_name,
                            linewidth=0.2,
                        )
                        visualize_mesh(
                            vis,
                            f"meshes_t/grasp_{j:03d}",
                            gripper_mesh,
                            color=[0, 150, 250],
                            transform=g.astype(np.float32),
                        )
                input()
        input()

    print(f"[DEBUG] output_file: {output_file}")
    if output_file is not None:
        key_id = inputs["scene"]

        saved_data_dict = {}

        # gripper_info = get_gripper_info(cfg.data.gripper_name)
        from grasp_gen.dataset.dataset import load_object_grasp_data
        from grasp_gen.dataset.dataset_utils import GraspJsonDatasetReader
        from grasp_gen.dataset.webdataset_utils import (
            GraspWebDatasetReader,
            is_webdataset,
        )

        # Initialize the appropriate grasp dataset reader
        if is_webdataset(cfg.data.grasp_root_dir):
            grasp_dataset_reader = GraspWebDatasetReader(cfg.data.grasp_root_dir)
        else:
            grasp_dataset_reader = GraspJsonDatasetReader(cfg.data.grasp_root_dir)

        error_code, object_grasp_data = load_object_grasp_data(
            key_id,
            cfg.data.object_root_dir,
            cfg.data.grasp_root_dir,
            cfg.data.dataset_version,
            load_discriminator_dataset=False,
            gripper_info=gripper_info,
            grasp_dataset_reader=grasp_dataset_reader,
        )

        if object_grasp_data is not None:

            if cfg.data.gripper_name == "franka_panda":
                asset_path_rel = "/".join(
                    object_grasp_data.object_asset_path.split("/")[-3:]
                )
            if cfg.data.gripper_name == "intrinsic_suction":
                asset_path_rel = "/".join(
                    object_grasp_data.object_asset_path.split("/")[-2:]
                )
            else:
                asset_path_rel = "/".join(
                    object_grasp_data.object_asset_path.split("/")[-3:]
                )

            print(f"[DEBUG] asset_path_rel: {asset_path_rel}")

            if cfg.data.gripper_name == "intrinsic_suction":
                offset_transform = tra.inverse_matrix(gripper_info.offset_transform)
                grasps_output["obj0"]["pred_grasps"] = np.array(
                    [g @ offset_transform for g in grasps_output["obj0"]["pred_grasps"]]
                )
                grasps_output["obj0"]["gt_grasps"] = np.array(
                    [g @ offset_transform for g in grasps_output["obj0"]["gt_grasps"]]
                )

            saved_data_dict["asset_path"] = asset_path_rel
            saved_data_dict["asset_scale"] = object_grasp_data.object_scale

            saved_data_dict.update(grasps_output["obj0"])
            print(
                f"Pred {saved_data_dict['pred_grasps'].shape}, Gt {saved_data_dict['gt_grasps'].shape} grasp number"
            )

            grp = output_file.create_group(key_id)
            start = time()
            write_info(grp, saved_data_dict)
            end = time()
            print(f"Writing scene {key_id} data took", end - start, "s")

    time_taken = time() - start
    log.info(
        f"Scene {inputs['scene']} took {round(time_taken,2)} s, saved to {output_file}"
    )


@hydra.main(config_path=".", config_name="config", version_base="1.3")
def main(cfg: DictConfig) -> None:

    # scenes = np.arange(cfg.eval.first_scene, cfg.eval.last_scene)

    # For SIMPLER dataset, just iterate over scenes
    scenes = None
    sampler, loader = get_data_loader(
        cfg.eval,
        cfg.data,
        cfg.eval.split,
        scenes,
        use_ddp=False,
        training=False,
        inference=True,
    )
    # model = foundation_grasp.from_config(cfg.foundation_grasp)
    from grasp_gen.models.grasp_gen import GraspGen, GraspGenGenerator

    if cfg.eval.model_name == "diffusion":
        model = GraspGenGenerator.from_config(cfg.diffusion)
    elif cfg.eval.model_name == "diffusion-discriminator":
        model = GraspGen.from_config(cfg.diffusion, cfg.discriminator)
    else:
        raise NotImplementedError(f"Model name not implemented {cfg.eval.model_name}")

    if cfg.eval.model_name == "diffusion-discriminator":
        model.load_state_dict(cfg.eval.checkpoint, cfg.discriminator.checkpoint)
    else:
        ckpt = torch.load(cfg.eval.checkpoint, map_location="cpu")
        model.load_state_dict(ckpt)
    model = model.cuda().eval()

    # gripper = PandaGripper().hand
    gripper_info = get_gripper_info(cfg.data.gripper_name)
    gripper = gripper_info.collision_mesh
    if cfg.eval.output_dir is not None:
        os.makedirs(cfg.eval.output_dir, exist_ok=True)

    mp.set_start_method("spawn", force=True)
    log_queue = mp.Queue()
    log_proc = mp.Process(target=log_worker, args=(log_queue,))
    log_proc.start()
    log = get_logger("main", log_queue)

    output_file = None
    h5_handle = None
    if cfg.eval.output_dir is not None:
        os.makedirs(cfg.eval.output_dir, exist_ok=True)

        h5_file_name = (
            f"{cfg.eval.exp_name}_{cfg.data.gripper_name}_{cfg.eval.split}.h5"
        )
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

    record_fn = record_grasps_diffusion
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
            outputs, _, stats = model.infer(data, return_metrics=True)

        print(
            f"Stats, L2 error:{stats['error_trans_l2'].item()} recall: {stats['recall'].item()} phi3 {stats['error_rot_phi3'].item()} "
        )

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
                # 'names': data['names'][j],
                # 'points': data['xyz'][j]
            }

            if cfg.eval.task == "pick":
                inputs.update(
                    {
                        # 'obj_masks': data['instance_masks'][j].bool(),
                        "gt_grasps": data["grasps_ground_truth"][j],
                        "grasps_pred": outputs["grasps_pred"][j],
                        "likelihood": outputs["likelihood"][j],
                        "grasps_per_iteration": outputs["grasps_per_iteration"][j],
                        "confidence": outputs["grasp_confidence"][j],
                        "grasping_masks": outputs["grasping_masks"][j],
                        "contacts": outputs["grasp_contacts"][j],
                    }
                )

                # For GraspGenGenerator
                for key in ["seg", "rgb", "xyz", "points", "bbox", "labels"]:
                    if key in data:
                        inputs.update({key: data[key][j]})

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
                f"Record time {record_time / num_scenes} "
                f"num scenes {num_scenes}"
            )
            data_time, infer_time, record_time, num_scenes = 0, 0, 0, 0

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
