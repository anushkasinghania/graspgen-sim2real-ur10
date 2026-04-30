"""
Preview OAK-D Pro — saves RGB snapshot + depth colormap as images.

Usage:
    python3 scripts/preview_oakd.py --output_dir /tmp/oak_preview
Then open /tmp/oak_preview/rgb.jpg and /tmp/oak_preview/depth.jpg
"""

import argparse
import os
import depthai as dai
import numpy as np

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_dir", type=str, default="/tmp/oak_preview")
    parser.add_argument("--warmup_frames", type=int, default=20)
    return parser.parse_args()

def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    with dai.Pipeline() as pipeline:
        # Color camera
        color = pipeline.create(dai.node.ColorCamera)
        color.setBoardSocket(dai.CameraBoardSocket.CAM_A)
        color.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        color.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
        color.setFps(15)

        # Stereo depth
        stereo = pipeline.create(dai.node.StereoDepth)
        stereo.build(autoCreateCameras=True)
        stereo.setDepthAlign(dai.CameraBoardSocket.CAM_A)

        # Output queues
        rgb_queue = color.isp.createOutputQueue(maxSize=4, blocking=False)
        depth_queue = stereo.depth.createOutputQueue(maxSize=4, blocking=False)

        pipeline.start()
        print(f"Warming up ({args.warmup_frames} frames)...")

        for _ in range(args.warmup_frames):
            rgb_queue.get()
            depth_queue.get()

        print("Capturing preview...")
        rgb_msg = rgb_queue.get()
        depth_msg = depth_queue.get()

    rgb = rgb_msg.getCvFrame()        # H x W x 3, RGB uint8
    depth = depth_msg.getCvFrame()    # H x W, uint16 in mm

    # Save RGB
    rgb_path = os.path.join(args.output_dir, "rgb.jpg")
    if HAS_CV2:
        cv2.imwrite(rgb_path, cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
    else:
        # Save as raw numpy if no cv2
        np.save(rgb_path.replace(".jpg", ".npy"), rgb)
        rgb_path = rgb_path.replace(".jpg", ".npy")

    # Save depth as colormap for visualization
    depth_vis = (depth / depth.max() * 255).astype(np.uint8)
    depth_path = os.path.join(args.output_dir, "depth.jpg")
    if HAS_CV2:
        depth_color = cv2.applyColorMap(depth_vis, cv2.COLORMAP_JET)
        cv2.imwrite(depth_path, depth_color)
    else:
        np.save(depth_path.replace(".jpg", ".npy"), depth)
        depth_path = depth_path.replace(".jpg", ".npy")

    print(f"RGB saved:   {rgb_path}")
    print(f"Depth saved: {depth_path}")
    print(f"Depth range: {depth[depth>0].min()/1000:.2f}m – {depth.max()/1000:.2f}m")
    print(f"Image size:  {rgb.shape[1]}x{rgb.shape[0]}")

if __name__ == "__main__":
    main()
