# Media Guide — Images, Screenshots & Videos

All visual assets (hardware photos, simulation screenshots, training graphs, demo videos)
are stored in Google Drive and are NOT tracked in this git repository due to size.

---

## Google Drive Folder Structure

> **TODO:** Replace the placeholder links below with your actual Google Drive folder links.

| Category | Description | Drive Link |
|----------|-------------|------------|
| Hardware Setup | Robot arm, Robotiq 3F gripper, OAK-D wrist cam, Jetson, cables | _[Add Drive link]_ |
| Simulation Screenshots | RViz pick-and-place, GraspGen grasp poses, planning scene | _[Add Drive link]_ |
| Real Hardware Screenshots | Real robot executing grasps, SAM2 segmentation window | _[Add Drive link]_ |
| Training Graphs | Loss curves, discriminator accuracy, epoch vs metric plots | _[Add Drive link]_ |
| Demo Videos | Sim pipeline run, real pick-and-place, failure cases | _[Add Drive link]_ |
| Thesis Figures | All figures used in the thesis document | _[Add Drive link]_ |

---

## How to Add Drive Links

1. Open Google Drive → right-click the folder → **Share** → **Anyone with the link → Viewer**
2. Copy the link and paste it in the table above in place of `_[Add Drive link]_`
3. Commit and push:
   ```bash
   git add docs/MEDIA_GUIDE.md
   git commit -m "Add Google Drive media links"
   git push origin master
   ```

---

## How to Add Images Directly to the Repo (optional, for small images only)

For images under 5 MB each (e.g., key result figures for README), you can add them directly:

```bash
mkdir -p docs/images/hardware docs/images/simulation docs/images/results docs/images/pipeline

# Copy images from your local machine or Downloads
cp ~/Downloads/<your_image>.jpg docs/images/hardware/

# Then commit
git add docs/images/
git commit -m "Add hardware/result images"
git push origin master
```

Suggested folder structure:
```
docs/images/
├── hardware/       ← Robot, gripper, camera, Jetson setup photos
├── simulation/     ← RViz screenshots, GraspGen sim output
├── results/        ← Success/failure grasp plots, sim2real comparison
└── pipeline/       ← System architecture diagrams, flowcharts
```

---

## Videos

GitHub does **not** support video uploads (25 MB limit). Use one of:

| Platform | Steps |
|----------|-------|
| **Google Drive** | Upload → Share → Anyone with link → paste URL in this file |
| **YouTube (Unlisted)** | Upload as unlisted → copy URL → paste here |

### Demo Video Links

> **TODO:** Add your video links below.

| Video | Description | Link |
|-------|-------------|------|
| Simulation pipeline | GraspGen sim pick-and-place (RViz) | _[Add link]_ |
| Real hardware run | Full real pick-and-place with Robotiq 3F | _[Add link]_ |
| SAM2 segmentation | Click-to-mask on OAK-D wrist cam feed | _[Add link]_ |
| Training results | GraspGen v3 training convergence | _[Add link]_ |
| Failure cases | Grasp failures and edge cases | _[Add link]_ |

---

## Thesis Document

The thesis PDF is included directly in this repo:

- `docs/AnushkaSinghania_Thesis_240614.pdf`

**Title:** Deep Learning-Based Grasp Pose Detection on Point Clouds and Manipulating the Object using Generated Grasp Pose  
**Author:** Anushka Singhania (Reg. No. 24-06-14)  
**Degree:** M.Tech in Automation and Robotics  
**Institute:** DIAT (DU), Pune — May 2026  
**Supervisors:** Prasad Naik (DIAT), Atul Chavan (DRDO R&DE)
