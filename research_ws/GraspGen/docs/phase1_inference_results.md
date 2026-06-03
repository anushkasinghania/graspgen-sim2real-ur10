# Phase 1 — Real Camera Inference Results
**Date:** 2026-03-31
**Status:** ✅ Tests 1a, 1.5, and 1b done. 1c pending retraining on partial PCs.

---

## Testing Plan

This phase has three sub-tests. All use the v3 models (gen + disc on-policy, 227 objects).

| Test | Point Cloud Type | Environment | Status |
|------|-----------------|-------------|--------|
| **1a** | Complete (mesh/synthetic, full 360° surface) | Single object | ✅ Done |
| **1b** | Partial (OAK-D, single-viewpoint) | Cluttered scene on brown box, pick closest object | ✅ Done |
| **1c** | Partial (OAK-D single-viewpoint) | Single + Cluttered | ⬜ Requires retraining first |

### Important: Model was NOT trained on partial point clouds
The config shows `prob_point_cloud: 0.5` but this never ran in practice —
`scene_synthesizer` was not installable on ARM64/Jetson, so the partial PC rendering
branch was never active during training. The v3 model was trained **only on complete
mesh-based point clouds**.

**Consequence:** Testing on partial point clouds (real OAK-D single-viewpoint captures)
is currently out of scope. The model will likely hallucinate or produce poor results on
single-viewpoint depth data because it has never seen incomplete object surfaces.

**To enable partial PC testing**, the model needs to be retrained with partial PC rendering
working — either by fixing the `scene_synthesizer` dependency or by generating rendered
partial views offline on x86 and transferring the dataset.

### What we tested in Phase 1a
The Phase 1a capture (from OAK-D Pro) is technically a partial point cloud (one viewpoint),
but the results showed grasps on table + empty space — confirming the model does not generalize
to partial views out of the box. This was expected.

**Phase 1a was useful as a pipeline integration test** (camera → capture → inference → MeshCat),
not as a quality evaluation.

---

## Hardware Setup

| Component | Detail |
|-----------|--------|
| Camera | OAK-D Pro (tripod-mounted, workspace view) |
| Connection | USB-C camera → LDLrui 10Gbps cable → Honeywell USB 3.1 hub → Jetson USB-A |
| Compute | Jetson AGX Orin 64GB |
| Models | Generator v3 + Disc On-Policy v3 (227 objects, epoch 500) |

**Camera connection note:** Direct USB-A to Jetson fails — the Jetson's USB-A ports route through
an internal USB 2.0 hub (Bus 1), causing enumeration error -71. The Honeywell hub connects via
USB 3.0 (Bus 2) and provides the correct SuperSpeed path.

---

## Results

| Metric | Value |
|--------|-------|
| Grasps found | 87–108 (threshold 0.7–0.8) |
| Max confidence score | 0.997 |
| Min confidence score | 0.713 |
| Inference time (cold) | ~7.2 sec (model loading) |
| Inference time (warm) | **1.85 sec** (model in GPU memory) |
| Point cloud size | ~6,000 pts (after auto-crop + voxel downsample) |

---

## Workflow

### Step 0 — Start services (once per session)
```bash
cd ~/research_ws/GraspGen

# MeshCat 3D viewer server
meshcat-server --zmq-url tcp://127.0.0.1:6000 &

# Live camera stream (RGB + depth in browser)
python3 scripts/camera_stream.py &
# Open: http://192.168.225.165:5000
```

### Step 1 — Position object and capture point cloud
```bash
# Place object on table, point OAK-D Pro at it from ~60-80cm away
python3 scripts/capture_oakd_pc.py \
  --output_dir /tmp/oak_captures \
  --filename obj.json \
  --depth_min 0.5 \
  --depth_max 1.5
# Script auto-crops to nearest object cluster + voxel downsamples to ~3000-6000 pts
```

### Step 2 — Run inference
```bash
# Kill camera stream first (camera can't be shared between processes)
pkill -f camera_stream

echo "" | python3 scripts/demo_object_pc.py \
  --sample_data_dir /tmp/oak_captures \
  --gripper_config config/grippers/robotiq_3f_infer.yaml \
  --grasp_threshold 0.7 \
  --num_grasps 200
```

### Step 3 — View 3D grasps
Open: `http://192.168.225.165:7000/static/`
- Green frames = high confidence grasps
- Red frames = lower confidence grasps
- White/gray dots = point cloud

### Step 4 — Restart live stream
```bash
python3 scripts/camera_stream.py &
```

---

## Scripts Created

| Script | Purpose |
|--------|---------|
| `scripts/capture_oakd_pc.py` | Captures point cloud from OAK-D Pro using depthai 3.x. Auto-crops to nearest object cluster (2% percentile Z + ±12cm X/Y box). Voxel downsamples to ~4mm resolution. Saves as JSON. |
| `scripts/camera_stream.py` | Flask web server streaming live RGB + depth colormap from OAK-D Pro. Port 5000. |
| `scripts/preview_oakd.py` | Saves a single RGB + depth snapshot as JPEG files (no browser needed). |
| `config/grippers/robotiq_3f_infer.yaml` | Inference config pointing at v3 gen + disc on-policy checkpoints. |

**Modifications to existing scripts:**
- `scripts/demo_object_pc.py`: removed crash on missing `grasp_poses` in JSON; added pre-downsampling to 4096 pts to prevent OOM in knn.

---

## Known Limitation — Grasps on Table and Empty Space

**Observation:** Grasps appear on the table surface and floating above the object.

**Root cause:** GraspGen was trained on individually segmented object point clouds (~1024 pts, object only). The capture pipeline gives it a table + object combined cloud. The model treats the entire scene as "the object" and generates grasps across the whole point cloud including the table plane. Some grasps in empty space are diffusion hallucinations — normal behavior with noisy/incomplete input.

**Fix:** Phase 1.5 — add table plane removal + object clustering before inference.

---

## Phase 1.5 — Table Removal + Object Isolation

**Status: ✅ Done (2026-03-31)**
**Results:** 75 grasps, scores 0.726–0.994, inference 1.07 sec. Grasps on object only — no table/empty-space grasps.

**Goal:** Produce a clean single-object point cloud so GraspGen only generates grasps on the actual object.

### Pipeline steps (now live in `capture_oakd_pc.py`):

1. **Voxel downsample** at 4mm — reduces ~1.8M pts → ~150K for speed
2. **Z-crop** to nearest surface + 40cm — discards background walls/floor behind the object
3. **RANSAC** (300 iter, 12mm threshold) — removes dominant flat plane (floor/table)
4. **DBSCAN** (eps=25mm, min_pts=15) — clusters remaining points; picks the **closest cluster to camera** (smallest mean Z) — this is the object in the foreground

Key: picking by closest-to-camera (not largest cluster) avoids grabbing wall/floor remnants that may be large connected surfaces.

### Results
| Metric | Value |
|--------|-------|
| Grasps found | 75 |
| Score range | 0.726 – 0.994 |
| Max confidence | 0.994 |
| Inference time | 1.07 sec (warm) |
| Object point cloud size | ~1,797 pts |

### Dependencies
```bash
pip install scikit-learn   # for DBSCAN (already installed)
```

---

## What Phase 1 Confirms

1. **Model works on real data** — generates confident grasps from a live OAK-D Pro stream on Jetson AGX Orin
2. **Inference speed is acceptable** — 1.85 sec warm, well under the 2 sec target
3. **Preprocessing gap identified** — needs table removal + object segmentation (Phase 1.5) before the full robot pipeline (Phase 5)
4. **Camera setup confirmed** — OAK-D Pro via Honeywell hub works reliably

---

## Test 1b — Cluttered Scene, Pick Closest Object

**Status: ✅ Done (2026-03-31)**

**Scene:** Multiple objects on a brown box, OAK-D Pro on tripod.

**Result:**
| Metric | Value |
|--------|-------|
| Grasps found | 126 |
| Score range | 0.708 – 0.997 |
| Max confidence | 0.997 |
| Inference time | 1.08 sec (warm) |
| Isolated cluster size | 198 pts |
| Cluster dimensions | ~6cm × 8.8cm × 3.6cm |

**Pipeline used (capture_oakd_pc.py):**
1. Voxel downsample 4mm
2. Z-crop to nearest + 40cm
3. **Iterative RANSAC** (up to 3 passes, 12mm threshold, stops when dominant plane < 10%) — removed floor then brown box top surface
4. DBSCAN (eps=25mm) → pick closest cluster to camera

**Key insight — iterative RANSAC:** The scene had two flat surfaces: the floor and the brown box top. A single RANSAC pass only removed the floor. Running RANSAC iteratively removed both planes, leaving only the objects. Each pass removed ~20% of remaining points before the threshold was met.

**Object selection approach used:** Closest cluster to camera (by minimum mean Z). This selects the object in the foreground — no color filter or click selection needed for single-target use.

---

## Test 1c — Partial Point Cloud (Future, Requires Retraining)

**Status: Out of scope until retraining.**

To test on partial point clouds (real OAK-D single-viewpoint), the model must first be
retrained with partial PC rendering active. Options:

1. **Fix scene_synthesizer on Jetson** — unlikely, ARM64 dependency issues
2. **Generate partial PC dataset on x86** — render partial views offline, transfer to Jetson
3. **Use a different partial PC generation method** — e.g., ray casting from a fixed camera pose using trimesh (no scene_synthesizer dependency)

Once retrained with partial PCs, the full pipeline becomes:
```
OAK-D → raw depth → table removal → clustering → single object partial PC → GraspGen
```

---

---

## How the Full Pipeline Works (Offline Testing)

The current pipeline is a **two-step offline process** — not live streaming to grasps.
The camera cannot be shared between the capture and inference processes.

```
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 1 — CAPTURE  (scripts/capture_oakd_pc.py)                      │
│                                                                      │
│  OAK-D Pro (live depth + RGB)                                       │
│      ↓ 30 warmup frames (auto-exposure settle)                      │
│      ↓ grab one depth frame (~1.8M raw points)                      │
│      ↓ filter invalid/out-of-range points                           │
│      ↓ voxel downsample 4mm  (~150K pts)                            │
│      ↓ Z-crop to nearest surface + 40cm  (remove background)        │
│      ↓ iterative RANSAC  (removes floor, box top, etc.)             │
│      ↓ DBSCAN → pick closest cluster = foreground object            │
│      ↓ save to /tmp/oak_captures/scene.json                         │
│                                                                      │
│  Camera is closed at this point.                                    │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ STEP 2 — INFERENCE  (scripts/demo_object_pc.py)                     │
│                                                                      │
│  Load scene.json  (object point cloud only)                        │
│      ↓ center point cloud                                           │
│      ↓ outlier removal (knn-based)                                  │
│      ↓ GraspGen: Generator diffuses 200 grasp poses                 │
│      ↓ Discriminator scores each → keep grasps > 0.7 threshold     │
│      ↓ send to MeshCat (port 7000) for 3D visualization             │
└─────────────────────────────────────────────────────────────────────┘
```

**Why two steps?** DepthAI locks the USB device exclusively — two processes cannot both
open the camera. Capture must fully close before inference can start.

**For the real robot (Phase 5):** This becomes a live loop via ROS2:
```
OAK-D Pro → /oak_pro/stereo/points (ROS2 topic, continuous)
    → GraspGen bridge node (sub/pub, runs inference on demand)
    → /graspgen/grasp_pose → MoveIt2 → UR10 arm
```

---

## Next Steps

1. ~~Phase 1.5~~ ✅ Done
2. ~~Test 1b~~ ✅ Done
3. **Phase 2** — UR10 arm bringup with `ros-humble-ur` + MoveIt2
4. **Future** — retrain with partial PCs → Test 1c
