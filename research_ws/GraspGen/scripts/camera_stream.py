"""
Live OAK-D Pro web viewer — streams RGB + depth side by side in browser.

Usage:
    python3 scripts/camera_stream.py

Then open in browser:
    http://<jetson-ip>:5000
"""

import threading
import time
import cv2
import numpy as np
import depthai as dai
from flask import Flask, Response, render_template_string

app = Flask(__name__)

# Shared latest frames
latest_rgb = None
latest_depth = None
frame_lock = threading.Lock()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>OAK-D Pro Live View</title>
    <style>
        body { background: #1a1a1a; color: white; font-family: monospace; text-align: center; margin: 0; padding: 20px; }
        h1 { color: #00ff88; }
        .frames { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; }
        .frame-box { background: #2a2a2a; padding: 10px; border-radius: 8px; }
        img { max-width: 640px; width: 100%; border-radius: 4px; }
        .label { color: #888; margin-top: 8px; font-size: 14px; }
        .info { color: #00ff88; margin: 10px 0; font-size: 13px; }
    </style>
</head>
<body>
    <h1>OAK-D Pro Live View</h1>
    <p class="info">Point camera at object, then run inference for grasp visualization at http://&lt;jetson-ip&gt;:7000</p>
    <div class="frames">
        <div class="frame-box">
            <img src="/stream/rgb" />
            <div class="label">RGB Camera</div>
        </div>
        <div class="frame-box">
            <img src="/stream/depth" />
            <div class="label">Depth Map (blue=far, red=close)</div>
        </div>
    </div>
</body>
</html>
"""

def generate_stream(stream_type):
    while True:
        with frame_lock:
            frame = latest_rgb if stream_type == "rgb" else latest_depth
        if frame is not None:
            _, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buf.tobytes() + b"\r\n")
        time.sleep(0.033)  # ~30fps cap

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/stream/<stream_type>")
def stream(stream_type):
    return Response(generate_stream(stream_type),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

def camera_loop():
    global latest_rgb, latest_depth
    print("Starting OAK-D Pro pipeline...")
    with dai.Pipeline() as pipeline:
        color = pipeline.create(dai.node.ColorCamera)
        color.setBoardSocket(dai.CameraBoardSocket.CAM_A)
        color.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        color.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)
        color.setFps(15)

        stereo = pipeline.create(dai.node.StereoDepth)
        stereo.build(autoCreateCameras=True)
        stereo.setDepthAlign(dai.CameraBoardSocket.CAM_A)

        rgb_queue = color.isp.createOutputQueue(maxSize=2, blocking=False)
        depth_queue = stereo.depth.createOutputQueue(maxSize=2, blocking=False)

        pipeline.start()
        print("Camera running. Open http://0.0.0.0:5000 in browser.")

        while True:
            rgb_msg = rgb_queue.get()
            depth_msg = depth_queue.get()

            rgb = rgb_msg.getCvFrame()  # BGR
            depth_raw = depth_msg.getCvFrame()  # uint16 mm

            # Resize to 640x360 for streaming
            rgb_small = cv2.resize(rgb, (640, 360))

            # Depth colormap
            depth_norm = cv2.normalize(depth_raw, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
            depth_color = cv2.applyColorMap(depth_norm, cv2.COLORMAP_JET)
            depth_small = cv2.resize(depth_color, (640, 360))

            with frame_lock:
                latest_rgb = rgb_small
                latest_depth = depth_small

if __name__ == "__main__":
    cam_thread = threading.Thread(target=camera_loop, daemon=True)
    cam_thread.start()
    time.sleep(3)  # let camera init
    print("\n=== Open in browser: http://192.168.225.165:5000 ===\n")
    app.run(host="0.0.0.0", port=5000, threaded=True)
