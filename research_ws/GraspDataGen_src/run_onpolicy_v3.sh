#!/bin/bash
# Full on-policy pipeline for v3 dataset (227 objects)
# Steps: disc GT training → on-policy data gen → disc on-policy training
set -e

SCRIPTS=~/research_ws/GraspGen/scripts
LOGS=~/GraspDataGen/training_logs
CACHE=/tmp/graspgen_cache_v3
DATA_ROOT=/home/ubuntu/GraspDataGen/graspgen_dataset_v3/splits/robotiq_3f
OBJ_ROOT=/home/ubuntu/GraspDataGen/objects_v3
GRASP_ROOT=/home/ubuntu/GraspDataGen/graspgen_dataset_v3/grasp_data/robotiq_3f

echo "============================================================"
echo "STEP 1: Discriminator GT training (v3 dataset)"
echo "Started: $(date)"
echo "============================================================"

# Pre-create denylist stub so prefilter results are preserved after first scan
mkdir -p $CACHE/robotiq_3f
[ -f $CACHE/robotiq_3f/denylist_mesh_dis.json ] || echo '{}' > $CACHE/robotiq_3f/denylist_mesh_dis.json

cd $SCRIPTS
python3 train_graspgen.py \
  train.model_name=discriminator \
  data.root_dir=$DATA_ROOT \
  data.object_root_dir=$OBJ_ROOT \
  data.grasp_root_dir=$GRASP_ROOT \
  data.gripper_name=robotiq_3f \
  data.dataset_version=v2 \
  data.dataset_cls=ObjectPickDataset \
  data.cache_dir=$CACHE/ \
  data.num_grasps_per_object=100 \
  data.prob_point_cloud=-1 \
  data.load_discriminator_dataset=True \
  diffusion.gripper_name=robotiq_3f \
  discriminator.gripper_name=robotiq_3f \
  train.log_dir=$LOGS/robotiq_3f_disc_v3/ \
  train.num_epochs=500 \
  "data.discriminator_ratio=[0.50,0.45,0.00,0.05,0.0,0.0,0.0]"

echo "============================================================"
echo "STEP 1 complete: $(date)"
echo "============================================================"

echo "============================================================"
echo "STEP 2: Generating on-policy data with v3 generator"
echo "Started: $(date)"
echo "============================================================"

# Recreate denylist stub so on-policy disc training won't rebuild cache
echo '{}' > $CACHE/robotiq_3f/denylist_mesh_dis.json

python3 $SCRIPTS/generate_onpolicy_data.py \
  --ckpt $LOGS/robotiq_3f_gen_v3/epoch_500.pth \
  --h5   $CACHE/robotiq_3f/cache_train_mesh_dis.h5 \
  --num_grasps 300

echo "============================================================"
echo "STEP 2 complete: $(date)"
echo "============================================================"

echo "============================================================"
echo "STEP 3: Discriminator on-policy training (v3)"
echo "Started: $(date)"
echo "============================================================"

# Ensure denylist stub still present so cache is NOT rebuilt (would wipe on-policy data)
[ -f $CACHE/robotiq_3f/denylist_mesh_dis.json ] || echo '{}' > $CACHE/robotiq_3f/denylist_mesh_dis.json

python3 $SCRIPTS/train_graspgen.py \
  train.model_name=discriminator \
  data.root_dir=$DATA_ROOT \
  data.object_root_dir=$OBJ_ROOT \
  data.grasp_root_dir=$GRASP_ROOT \
  data.gripper_name=robotiq_3f \
  data.dataset_version=v2 \
  data.dataset_cls=ObjectPickDataset \
  data.cache_dir=$CACHE/ \
  data.num_grasps_per_object=100 \
  data.prob_point_cloud=-1 \
  data.load_discriminator_dataset=True \
  diffusion.gripper_name=robotiq_3f \
  discriminator.gripper_name=robotiq_3f \
  train.log_dir=$LOGS/robotiq_3f_disc_onpolicy_v3/ \
  train.num_epochs=500 \
  "data.discriminator_ratio=[0.25,0.20,0.00,0.05,0.0,0.25,0.25]"

echo "============================================================"
echo "STEP 3 complete — full on-policy pipeline done: $(date)"
echo "============================================================"
