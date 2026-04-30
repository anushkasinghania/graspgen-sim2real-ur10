#!/usr/bin/env bash

# Fixed parameters
export NGPU=1
export NWORKER=4
export NEPOCH=5000
export BATCH=8
export PRINT_FREQ=10
export PLOT_FREQ=10
export SAVE_FREQ=2000
export DATASET_NAME="objaverse"
export DATASET_VERSION="v2"
export NUM_GRASPS_PER_OBJ=300
export POSE_REPR="mlp"
export BACKBONE="ptv3"
export ROTATION_REPR="r3_so3"
export TOPK_RATIO=0.75
export NUM_POINTS=2048
export NOISE_SCALE=3.27
export NAME="meshandpc"
export PROBABILITY_SAMPLE_PARTIAL_POINTCLOUD=0.50
export NUM_REDUNDANT_DATAPOINTS=7
export GRIPPER_NAME="franka_panda"
export OBJECT_DATASET_DIR="/object_dataset"
export GRASP_DIR="/grasp_dataset"
export CODE_DIR="/code"
export RESULTS_DIR="/results"
export GRASP_DATASET_DIR="$GRASP_DIR/grasp_data/$GRIPPER_NAME"
export SPLIT_DATASET_DIR="$GRASP_DIR/splits/$GRIPPER_NAME"
export METHOD="grasp_gen"
export RATIO="[0.25,0.24,0.00,0.01,0.00,0.25,0.25]"
export PYOPENGL_PLATFORM="osmesa"
export LOG_DIR="$RESULTS_DIR/logs/${GRIPPER_NAME}_dis_test"
export CACHE_DIR="$RESULTS_DIR/cache"
export CHECKPOINT="$LOG_DIR/last.pth"
export CONSOLE_LOG="$LOG_DIR/console_log.txt"

echo "Running Training for $GRIPPER_NAME"

rm -rf $LOG_DIR
mkdir -p $LOG_DIR
mkdir -p $CACHE_DIR

cd $CODE_DIR && cd $CODE_DIR/scripts && \
    python train_graspgen.py \
    data.num_points=$NUM_POINTS \
    data.load_contact=False \
    data.dataset_cls="ObjectPickDataset" \
    data.rotation_augmentation=True \
    data.cache_dir=$CACHE_DIR \
    data.root_dir=$SPLIT_DATASET_DIR \
    data.object_root_dir=$OBJECT_DATASET_DIR \
    data.grasp_root_dir=$GRASP_DATASET_DIR \
    data.dataset_name=$DATASET_NAME \
    data.dataset_version=$DATASET_VERSION \
    data.prob_point_cloud=$PROBABILITY_SAMPLE_PARTIAL_POINTCLOUD \
    data.redundancy=$NUM_REDUNDANT_DATAPOINTS \
    data.gripper_name=$GRIPPER_NAME \
    train.log_dir=$LOG_DIR \
    train.batch_size=$BATCH \
    train.num_gpus=$NGPU \
    train.num_epochs=$NEPOCH \
    train.num_workers=$NWORKER \
    train.print_freq=$PRINT_FREQ \
    train.plot_freq=$PLOT_FREQ \
    train.save_freq=$SAVE_FREQ \
    train.checkpoint=$CHECKPOINT \
    train.model_name='discriminator' \
    optimizer.type="ADAMW" \
    optimizer.grad_clip=-1 \
    optimizer.lr=0.00001 \
    discriminator.gripper_name=$GRIPPER_NAME \
    discriminator.topk_ratio=$TOPK_RATIO \
    discriminator.obs_backbone=$BACKBONE \
    discriminator.grasp_repr=$ROTATION_REPR \
    discriminator.pose_repr=$POSE_REPR \
    discriminator.kappa=$NOISE_SCALE \
    discriminator.ptv3.grid_size=0.01 \
    data.num_grasps_per_object=$NUM_GRASPS_PER_OBJ \
    data.load_discriminator_dataset=True \
    data.discriminator_ratio=$RATIO | tee $CONSOLE_LOG
