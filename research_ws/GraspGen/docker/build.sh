VER=1.0
docker build -f docker/graspgen_cuda121.dockerfile . --network=host -t graspgen:$VER -t graspgen:latest
