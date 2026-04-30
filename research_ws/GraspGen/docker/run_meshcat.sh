#!/bin/bash
docker run \
  --gpus all \
  -e NVIDIA_DRIVER_CAPABILITIES=compute,graphics,utility \
  --runtime nvidia \
  -e NVIDIA_DISABLE_REQUIRE=1 \
  graspgen:latest \
  meshcat-server
