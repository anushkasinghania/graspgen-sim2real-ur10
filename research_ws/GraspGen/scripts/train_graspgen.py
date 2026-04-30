#!/usr/bin/env python3

# Copyright (c) 2025, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""
Training script for GraspGen model.
"""
import os
import signal
import sys
import threading
from datetime import timedelta
from functools import partial
from itertools import chain
from time import sleep, time
import hydra
import numpy as np
import torch
import torch.distributed as dist
import torch.multiprocessing as mp
from matplotlib import pyplot as plt
from omegaconf import DictConfig, OmegaConf
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.nn.utils import clip_grad_norm_
from torch.utils.tensorboard.writer import SummaryWriter
from grasp_gen.dataset.dataset import (
    get_cache_path,
    get_cache_prefix,
    get_pc_setting_name,
    is_valid_cache_dir,
)
from grasp_gen.models.grasp_gen import GraspGenDiscriminator, GraspGenGenerator
from grasp_gen.utils.train_utils import (
    add_to_dict,
    build_optimizer,
    compute_iou,
    get_data_loader,
    save_model,
    to_cpu,
    to_gpu,
    write_scalar_ddp,
)
from grasp_gen.utils.logging_config import get_logger

# Configure logging
logger = get_logger(__name__)


# Global variables
handler_called = False


def train_one_epoch(
    loader,
    model,
    optimizer,
    clip_grad,
    writer,
    epoch,
    global_step,
    cfg,
    batch_idx,
    rank,
):
    global handler_called

    ws = 1
    use_ddp = dist.is_available() and cfg.train.num_gpus > 1
    if use_ddp:
        rank = dist.get_rank()
        ws = dist.get_world_size()

    def signal_handler(sig, _):
        global handler_called
        if not handler_called:
            if sig in [signal.SIGTERM, signal.SIGINT] and rank == 0:
                handler_called = True

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    params = list(chain(*[x["params"] for x in optimizer.param_groups]))
    num_steps = len(loader)
    data_time = torch.tensor(0.0, device=rank)
    step_time = torch.tensor(0.0, device=rank)
    log_time = torch.tensor(0.0, device=rank)

    start = time()
    num_batch_updates = 0
    outputs = {}
    # start_training = False
    # start_training = True

    for i, data in enumerate(loader):

        if handler_called:
            logger.info(
                f"Saving new checkpoints for rank:{rank} epoch: {epoch} batch index: {i}, global_step: {global_step}"
            )
            os.system(f"rm -rf {os.path.join(cfg.train.log_dir, 'last.pth')}")
            save_model(
                epoch - 1,
                model,
                optimizer,
                cfg.train.log_dir,
                use_ddp,
                name="last",
                batch_idx=i,
            )
            logger.info("Terminating training due to a interrupt, sayonara!")
            sys.exit(0)

        # if i == batch_idx:
        # start_training = True

        # print(i, data is not None)
        if hasattr(dist, "is_initialized") and dist.is_initialized():
            dist.barrier()

        # if not start_training:
        #     continue

        if data is None:
            continue

        global_step += 1
        to_gpu(data)
        data_time += time() - start
        start = time()

        optimizer.zero_grad()

        if hasattr(dist, "is_initialized") and dist.is_initialized():
            dist.barrier()
        outputs, losses, stats = model(data, cfg.train)
        if hasattr(dist, "is_initialized") and dist.is_initialized():
            dist.barrier()

        loss = sum([w * v for w, v in losses.values()])

        if hasattr(dist, "is_initialized") and dist.is_initialized():
            dist.barrier()
        loss.backward()
        if hasattr(dist, "is_initialized") and dist.is_initialized():
            dist.barrier()

        grad_has_inf_nan = False
        if clip_grad is not None:
            # print("Clipping gradients")
            grad_norm = clip_grad(params)
            grad_has_inf_nan = grad_norm.isinf() or grad_norm.isnan()
            if use_ddp:
                dist.reduce(grad_norm, dst=0)
            if rank == 0:
                if grad_norm.isinf():
                    logger.warning(
                        "Epoch", epoch, "Step", i + 1, "Gradient contains Inf"
                    )
                elif grad_norm.isnan():
                    logger.warning(
                        "Epoch", epoch, "Step", i + 1, "Gradient contains NaN"
                    )
                else:
                    writer.add_scalar(
                        "train/gradient_norm", grad_norm.item() / ws, global_step
                    )

        if hasattr(dist, "is_initialized") and dist.is_initialized():
            dist.barrier()

        if not grad_has_inf_nan:
            optimizer.step()
            num_batch_updates += 1
        if hasattr(dist, "is_initialized") and dist.is_initialized():
            dist.barrier()

        step_time += time() - start
        start = time()

        if hasattr(dist, "is_initialized") and dist.is_initialized():
            dist.barrier()
        losses["all_loss"] = (1, loss.detach())
        for key in losses:
            val = losses[key][1]
            key = f"train_{key}" if "/" in key else f"train/loss/{key}"
            write_scalar_ddp(writer, key, val, global_step, rank, ws, use_ddp)

        if hasattr(dist, "is_initialized") and dist.is_initialized():
            dist.barrier()
        for key in stats:
            val = stats[key]
            key = f"train_{key}" if "/" in key else f"train/metric/{key}"
            write_scalar_ddp(writer, key, val, global_step, rank, ws, use_ddp)

        log_time += time() - start
        start = time()

        if hasattr(dist, "is_initialized") and dist.is_initialized():
            dist.barrier()

        if (i + 1) % cfg.train.print_freq == 0:
            data_time = data_time.item() / ws / cfg.train.print_freq
            step_time = step_time.item() / ws / cfg.train.print_freq
            log_time = log_time.item() / ws / cfg.train.print_freq
            if rank == 0:
                logger.info(
                    f"Train Epoch {epoch:02d}  {(i+1):04d}/{num_steps:04d}  "
                    f"Data time {data_time:.4f}  Forward time {step_time:.4f}"
                    f"  Logging time {log_time:.4f} Loss {loss.detach():.4f}"
                )
            data_time = torch.tensor(0.0, device=rank)
            step_time = torch.tensor(0.0, device=rank)
            log_time = torch.tensor(0.0, device=rank)

    return global_step


def eval_one_epoch(loader, model, writer, epoch, global_step, cfg):
    global handler_called
    rank = 0
    ws = 1
    use_ddp = dist.is_available() and cfg.train.num_gpus > 1
    if use_ddp:
        rank = dist.get_rank()
        ws = dist.get_world_size()
    num_steps = len(loader)
    num_plots = num_steps // cfg.train.plot_freq
    plot_ids = torch.randperm(num_steps)[:num_plots]
    data_time = torch.tensor(0.0, device=rank)
    step_time = torch.tensor(0.0, device=rank)
    log_time = torch.tensor(0.0, device=rank)

    total = {}
    loss_dict_epoch, stats_epoch, stats_recon_epoch = {}, {}, {}
    start = time()
    outputs = {}
    for i, data in enumerate(loader):

        if handler_called:
            logger.info("Terminating training, sayonara!")
            sys.exit(0)

        if data is None:
            continue

        to_gpu(data)
        data_time += time() - start
        start = time()

        with torch.no_grad():
            outputs, losses, stats = model(data, cfg.train)

            if cfg.train.model_name == "diffusion":
                _, _, stats_recon = model(data, eval=True)
            loss = sum([w * v for w, v in losses.values()])
            losses["all_loss"] = (1, loss.detach())
        step_time += time() - start
        start = time()

        for key in losses:
            add_to_dict(loss_dict_epoch, key, losses[key][1])

        for key in stats:
            add_to_dict(stats_epoch, key, stats[key])

        if cfg.train.model_name == "diffusion":
            for key in stats_recon:
                add_to_dict(stats_recon_epoch, key, stats_recon[key])

        log_time += time() - start
        start = time()

        if (i + 1) % cfg.train.print_freq == 0:
            # if use_ddp:
            #     dist.reduce(data_time, 0)
            #     dist.reduce(step_time, 0)
            #     dist.reduce(log_time, 0)
            if rank == 0:
                data_time = data_time.item() / ws / cfg.train.print_freq
                step_time = step_time.item() / ws / cfg.train.print_freq
                log_time = log_time.item() / ws / cfg.train.print_freq
                logger.info(
                    f"Valid Epoch {epoch:02d}  {(i+1):04d}/{num_steps:04d}  "
                    f"Data time {data_time:.4f}  Forward time {step_time:.4f}"
                    f"  Logging time {log_time:.4f}"
                )
            data_time = torch.tensor(0.0, device=rank)
            step_time = torch.tensor(0.0, device=rank)
            log_time = torch.tensor(0.0, device=rank)

    total["steps"] = torch.tensor(max(i + 1, 1) if "i" in locals() else 1, device=rank)
    if use_ddp:
        for key in total:
            dist.reduce(total[key], 0)

    for key, val in loss_dict_epoch.items():
        write_scalar_ddp(
            writer, f"valid/loss/{key}", val, global_step, rank, total["steps"], use_ddp
        )

    for key, val in stats_epoch.items():
        write_scalar_ddp(
            writer,
            f"valid/metric/noise/{key}",
            val,
            global_step,
            rank,
            total["steps"],
            use_ddp,
        )

    if cfg.train.model_name == "diffusion":
        for key, val in stats_recon_epoch.items():
            write_scalar_ddp(
                writer,
                f"valid/metric/reconstruction/{key}",
                val,
                global_step,
                rank,
                total["steps"],
                use_ddp,
            )


def init_seeds(seed):
    # refer to https://pytorch.org/docs/stable/notes/randomness.html
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":16:8"
    torch.use_deterministic_algorithms(mode=True, warn_only=True)


def train(rank, cfg):

    if cfg.data.random_seed != -1:
        seed = cfg.data.random_seed
        logger.info(f"Setting seed to {seed}")
        init_seeds(seed)

    torch.backends.cudnn.benchmark = True
    torch.set_num_threads(1)
    use_ddp = dist.is_available() and cfg.train.num_gpus > 1
    if use_ddp:
        os.environ["MASTER_ADDR"] = "127.0.0.1"
        os.environ["MASTER_PORT"] = cfg.train.port
        os.environ["NCCL_BLOCKING_WAIT"] = "0"  # ADDed later
        dist.init_process_group(
            "nccl",
            timeout=timedelta(seconds=7200000),
            rank=rank,
            world_size=cfg.train.num_gpus,
        )
        torch.cuda.set_device(rank)

    scenes = None
    if cfg.train.num_scenes is not None:
        scenes = np.arange(cfg.train.num_scenes)

    train_sampler, train_loader = get_data_loader(
        cfg.train, cfg.data, "train", scenes, use_ddp, training=True
    )
    valid_sampler, valid_loader = get_data_loader(
        cfg.train, cfg.data, "valid", scenes, use_ddp, training=False
    )

    if cfg.train.model_name == "diffusion":
        model = GraspGenGenerator.from_config(cfg.diffusion).to(rank)
    elif cfg.train.model_name == "discriminator":
        model = GraspGenDiscriminator.from_config(cfg.discriminator).to(rank)
    optimizer = build_optimizer(cfg, model)

    total_params = sum(p.numel() for p in model.parameters())
    logger.info(f"Number of parameters in {cfg.train.model_name} model: {total_params}")

    init_epoch = 0
    init_batch_idx = 0

    logger.info(f"Attempting to load checkpoint from {cfg.train.checkpoint}")
    try:
        if cfg.train.checkpoint is not None:
            if os.path.exists(cfg.train.checkpoint):
                ckpt = torch.load(cfg.train.checkpoint, map_location="cpu")
                init_epoch = ckpt["epoch"]
                model.load_state_dict(ckpt["model"])
                optimizer.load_state_dict(ckpt["optimizer"])
                logger.info(f"Loading from checkpoint {cfg.train.checkpoint}")
                init_batch_idx = ckpt["batch_idx"] if "batch_idx" in ckpt else 0
            else:
                logger.warning(f"Checkpoint file not found {cfg.train.checkpoint}")
    except (RuntimeError, EOFError) as e:
        logger.error(e)
        logger.error("Checkpoint last.pth is most likly corrupted")
        import glob

        ckpt_dir = cfg.train.log_dir
        if ckpt_dir.endswith("/"):
            ckpt_dir = ckpt_dir.rstrip("/")

        ckpt_list = [
            ckpt for ckpt in glob.glob(ckpt_dir + "/*.pth") if ckpt.find("last") < 0
        ]
        highest_ckpt_idx = sorted(
            [
                int(os.path.basename(ckpt_file).split("epoch_")[1].split(".pth")[0])
                for ckpt_file in ckpt_list
            ]
        )[-1]
        ckpt_file = os.path.join(ckpt_dir, f"epoch_{str(highest_ckpt_idx)}.pth")

        ckpt = torch.load(ckpt_file, map_location="cpu")
        init_epoch = ckpt["epoch"]
        model.load_state_dict(ckpt["model"])
        optimizer.load_state_dict(ckpt["optimizer"])
        logger.info(f"Loading from checkpoint {ckpt_file}")
        init_batch_idx = ckpt["batch_idx"] if "batch_idx" in ckpt else 0

    batch_idx = init_batch_idx

    if use_ddp:
        # https://github.com/Lightning-AI/lightning/issues/6789
        model = torch.nn.SyncBatchNorm.convert_sync_batchnorm(model)
        model = DDP(model, device_ids=[rank], output_device=rank)

    clip_grad = None
    if cfg.optimizer.grad_clip > 0:
        clip_grad = partial(clip_grad_norm_, max_norm=cfg.optimizer.grad_clip)

    writer = None
    if rank == 0:
        writer = SummaryWriter(cfg.train.log_dir)
    if rank == 0:
        # Save training configuration to YAML file
        config_save_path = os.path.join(cfg.train.log_dir, "config.yaml")
        with open(config_save_path, "w") as f:
            OmegaConf.save(cfg, f)
        logger.info(f"Saved training configuration to {config_save_path}")

    global_step = init_epoch * len(train_loader) + batch_idx
    start = time()

    logger.info(
        f"Training starting at epoch {init_epoch+1} and batch index {batch_idx}"
    )

    for epoch in range(init_epoch, cfg.train.num_epochs):

        model.train()

        if use_ddp:
            train_sampler.set_epoch(epoch)

        global_step = train_one_epoch(
            train_loader,
            model,
            optimizer,
            clip_grad,
            writer,
            epoch + 1,
            global_step,
            cfg,
            batch_idx,
            rank,
        )

        batch_idx = 0  # Reset to 0 after first (and every) epoch

        if (epoch + 1) % cfg.train.save_freq == 0 and rank == 0:
            save_model(epoch + 1, model, optimizer, cfg.train.log_dir, use_ddp)
            os.system(f"rm -rf {os.path.join(cfg.train.log_dir, 'last.pth')}")
            save_model(
                epoch + 1, model, optimizer, cfg.train.log_dir, use_ddp, name="last"
            )

        if (epoch + 1) % cfg.train.eval_freq == 0 or cfg.data.prefiltering:
            model.eval()
            if use_ddp:
                valid_sampler.set_epoch(epoch)
            eval_one_epoch(valid_loader, model, writer, epoch + 1, global_step, cfg)

        if cfg.data.prefiltering:
            logger.info(
                "Prefiltering mode. Exiting Train script since we iterated one pass over the dataset"
            )
            break

    total_time = torch.tensor(time() - start).to(rank)
    if use_ddp:
        dist.reduce(total_time, 0)
    total_time = total_time.item() / cfg.train.num_gpus
    if rank == 0:
        try:
            logger.info(f"Total training time: {timedelta(seconds=total_time)}")
        except Exception as e:
            logger.error(f"Error logging total training time: {e}")
            pass


@hydra.main(config_path=".", config_name="config", version_base="1.3")
def main(cfg: DictConfig) -> None:

    # TODO - Unify this later to a single gripper name and variable
    if cfg.train.model_name == "diffusion":
        assert (
            cfg.diffusion.gripper_name == cfg.data.gripper_name
        ), "Gripper names must be the same for diffusion and data loader"
    elif cfg.train.model_name == "discriminator":
        assert (
            cfg.discriminator.gripper_name == cfg.data.gripper_name
        ), "Gripper names must be the same for discriminator and data loader"

    # These are just set by default now. TODO - once stable, remove these from config
    cfg.data.prefiltering = False
    cfg.data.preload_dataset = True
    cache_dir = get_cache_path(cfg.data.cache_dir, cfg.data.root_dir)

    # Detect number of available GPUs and set cfg.train.num_gpus
    num_gpus_available = torch.cuda.device_count()
    cfg.train.num_gpus = num_gpus_available
    logger.info(
        f"Detected {num_gpus_available} GPU(s) available, setting cfg.train.num_gpus = {num_gpus_available}"
    )

    if not is_valid_cache_dir(cfg.data):
        logger.info("Cache is imcomplete. Running in prefiltering mode first!")
        num_gpus_original = cfg.train.num_gpus
        num_workers_original = cfg.train.num_workers
        visualize_batch_original = cfg.data.visualize_batch
        os.makedirs(cache_dir, exist_ok=True)
        cfg.data.prefiltering = True
        cfg.train.num_gpus = 1
        cfg.train.num_workers = 0
        cfg.data.visualize_batch = False
        logger.info("Prefiltering mode. Running with 1 GPU")
        train(0, cfg)
        assert os.path.exists(cache_dir)
        cfg.data.prefiltering = False
        cfg.train.num_gpus = num_gpus_original
        cfg.train.num_workers = num_workers_original
        cfg.data.visualize_batch = visualize_batch_original
        logger.info(
            f"Prefiltering mode done. Running with original number of {num_gpus_original} GPUs"
        )
        sleep(2)

    if cfg.train.debug:
        train(0, cfg)
    else:
        mp.spawn(train, args=(cfg,), nprocs=cfg.train.num_gpus, join=True)


if __name__ == "__main__":
    main()
