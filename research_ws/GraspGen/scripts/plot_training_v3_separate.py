"""
Generates 4 separate publication-quality training plots:
  plot_gen_v3.png            — Generator v3
  plot_disc_gt_v3.png        — Discriminator GT v3
  plot_disc_onpolicy_v3.png  — Discriminator On-Policy v3
  plot_combined_loss_ap.png  — Overlay: loss & AP of all 3 runs on shared axes
"""

import os, glob
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from collections import defaultdict
from tensorboard.backend.event_processing.event_file_loader import LegacyEventFileLoader

BASE    = os.path.expanduser("~/GraspDataGen/training_logs")
OUT_DIR = os.path.join(BASE, "plots_v3")
os.makedirs(OUT_DIR, exist_ok=True)

# ── loader ────────────────────────────────────────────────────────────────────
def load_run(run_dir):
    data = defaultdict(list)
    for ef in sorted(glob.glob(os.path.join(run_dir, "events.out.tfevents.*"))):
        try:
            for event in LegacyEventFileLoader(ef).Load():
                if not hasattr(event, "summary"): continue
                for v in event.summary.value:
                    if v.HasField("simple_value"):
                        data[v.tag].append((event.step, v.simple_value))
        except: pass
    out = {}
    for tag, pairs in data.items():
        pairs.sort()
        seen, steps, vals = set(), [], []
        for s, v in pairs:
            if s not in seen:
                seen.add(s); steps.append(s); vals.append(v)
        out[tag] = (np.array(steps), np.array(vals))
    return out

def smooth(y, w=9):
    if len(y) < w: return y
    pad = np.pad(y, (w//2, w//2), mode="edge")
    return np.convolve(pad, np.ones(w)/w, mode="valid")[:len(y)]

def plot_tag(ax, run, tag, label, color, alpha_raw=0.2, lw=2.0):
    if tag not in run: return False
    s, v = run[tag]
    ax.plot(s, smooth(v), color=color, lw=lw, label=label, zorder=3)
    ax.plot(s, v, color=color, lw=0.4, alpha=alpha_raw, zorder=2)
    return True

def finish(ax, title, ylabel="", legend_loc="best"):
    ax.set_title(title, fontsize=12, fontweight="bold", pad=8)
    ax.set_xlabel("Epoch", fontsize=10)
    if ylabel: ax.set_ylabel(ylabel, fontsize=10)
    ax.legend(fontsize=9, loc=legend_loc, framealpha=0.9)
    ax.grid(True, alpha=0.25, linestyle="--")
    ax.spines[["top","right"]].set_visible(False)

print("Loading runs…")
gen  = load_run(f"{BASE}/robotiq_3f_gen_v3")
dgt  = load_run(f"{BASE}/robotiq_3f_disc_v3")
dop  = load_run(f"{BASE}/robotiq_3f_disc_onpolicy_v3")
print("  done.")

# ══════════════════════════════════════════════════════════════════════════════
# PLOT 1 — Generator v3
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle("Generator v3 — Training Curves\nRobotiq 3F  |  227 Objects  |  500 Epochs  |  92/180 train objects cached",
             fontsize=13, fontweight="bold")

# [0,0] Total loss
ax = axes[0][0]
plot_tag(ax, gen, "train/loss/all_loss",  "Train", "#1565C0")
plot_tag(ax, gen, "valid/loss/all_loss",  "Valid",  "#42A5F5")
finish(ax, "Total Loss (Noise Prediction × 2)", "Loss")

# [0,1] Noise pred loss only
ax = axes[0][1]
plot_tag(ax, gen, "train/loss/noise_pred", "Train", "#6A1B9A")
plot_tag(ax, gen, "valid/loss/noise_pred", "Valid",  "#CE93D8")
finish(ax, "Noise Prediction Loss", "Loss")

# [0,2] Rotation error
ax = axes[0][2]
plot_tag(ax, gen, "train/metric/error_rot_geodesic",                "Train (geodesic)", "#C62828")
plot_tag(ax, gen, "valid/metric/noise/error_rot_geodesic",          "Valid noise",       "#EF9A9A")
plot_tag(ax, gen, "valid/metric/reconstruction/error_rot_geodesic", "Valid recon",       "#FF8F00", lw=1.4)
finish(ax, "Rotation Error (rad)", "Radians")

# [1,0] Translation error
ax = axes[1][0]
plot_tag(ax, gen, "train/metric/error_trans_l2",                "Train",       "#2E7D32")
plot_tag(ax, gen, "valid/metric/noise/error_trans_l2",          "Valid noise",  "#81C784")
plot_tag(ax, gen, "valid/metric/reconstruction/error_trans_l2", "Valid recon",  "#FF8F00", lw=1.4)
finish(ax, "Translation Error (m)", "Metres")

# [1,1] Rotation phi3
ax = axes[1][1]
plot_tag(ax, gen, "train/metric/error_rot_phi3",                "Train",      "#00695C")
plot_tag(ax, gen, "valid/metric/noise/error_rot_phi3",          "Valid noise", "#80CBC4")
plot_tag(ax, gen, "valid/metric/reconstruction/error_rot_phi3", "Valid recon", "#FF8F00", lw=1.4)
finish(ax, "Rotation Error φ₃", "φ₃")

# [1,2] Precision & Recall
ax = axes[1][2]
plot_tag(ax, gen, "valid/metric/reconstruction/recall",    "Recall",    "#1565C0")
plot_tag(ax, gen, "valid/metric/reconstruction/precision", "Precision", "#C62828")
finish(ax, "Valid Reconstruction — Recall & Precision", "Score")

plt.tight_layout()
p = f"{OUT_DIR}/plot_gen_v3.png"
plt.savefig(p, dpi=160, bbox_inches="tight")
plt.close()
print(f"Saved: {p}")

# ══════════════════════════════════════════════════════════════════════════════
# PLOT 2 — Discriminator GT v3
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle("Discriminator GT v3 — Training Curves\nRobotiq 3F  |  227 Objects  |  500 Epochs  |  ratio=[0.50, 0.45, 0.00, 0.05, 0, 0, 0]",
             fontsize=13, fontweight="bold")

ax = axes[0][0]
plot_tag(ax, dgt, "train/loss/bce_topk", "Train BCE", "#E65100")
plot_tag(ax, dgt, "valid/loss/bce_topk", "Valid BCE",  "#FFCC80")
finish(ax, "BCE Top-K Loss", "Loss")

ax = axes[0][1]
plot_tag(ax, dgt, "train/metric/ap",       "Train AP", "#1565C0")
plot_tag(ax, dgt, "valid/metric/noise/ap", "Valid AP",  "#90CAF9")
finish(ax, "Average Precision (AP)", "AP")

ax = axes[0][2]
plot_tag(ax, dgt, "train/metric/topk_ratio_pos_true", "Pos GT (train)",  "#2E7D32")
plot_tag(ax, dgt, "train/metric/topk_ratio_neg_true", "Neg GT (train)",  "#B71C1C")
plot_tag(ax, dgt, "valid/metric/noise/topk_ratio_pos_true", "Pos GT (valid)", "#81C784")
plot_tag(ax, dgt, "valid/metric/noise/topk_ratio_neg_true", "Neg GT (valid)", "#EF9A9A")
finish(ax, "Top-K Class Ratios (GT)", "Ratio")

ax = axes[1][0]
plot_tag(ax, dgt, "train/metric/loss_pos_true",    "Pos GT",       "#2E7D32")
plot_tag(ax, dgt, "train/metric/loss_neg_true",    "Neg GT",       "#B71C1C")
plot_tag(ax, dgt, "train/metric/loss_neg_freespace","Neg Freespace","#FF8F00")
finish(ax, "Per-Class Training Loss", "Loss")

ax = axes[1][1]
plot_tag(ax, dgt, "valid/metric/noise/loss_pos_true",    "Pos GT",        "#2E7D32")
plot_tag(ax, dgt, "valid/metric/noise/loss_neg_true",    "Neg GT",        "#B71C1C")
plot_tag(ax, dgt, "valid/metric/noise/loss_neg_freespace","Neg Freespace", "#FF8F00")
finish(ax, "Per-Class Validation Loss", "Loss")

ax = axes[1][2]
plot_tag(ax, dgt, "train/metric/topk_ratio_neg_freespace", "Neg Freespace", "#FF8F00")
finish(ax, "Top-K Ratio — Freespace Negatives", "Ratio")
ax.set_ylim(bottom=0)

plt.tight_layout()
p = f"{OUT_DIR}/plot_disc_gt_v3.png"
plt.savefig(p, dpi=160, bbox_inches="tight")
plt.close()
print(f"Saved: {p}")

# ══════════════════════════════════════════════════════════════════════════════
# PLOT 3 — Discriminator On-Policy v3
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle("Discriminator On-Policy v3 — Training Curves\nRobotiq 3F  |  227 Objects  |  500 Epochs  |  ratio=[0.25, 0.20, 0.00, 0.05, 0, 0.25, 0.25]",
             fontsize=13, fontweight="bold")

ax = axes[0][0]
plot_tag(ax, dop, "train/loss/bce_topk", "Train BCE", "#2E7D32")
plot_tag(ax, dop, "valid/loss/bce_topk", "Valid BCE",  "#A5D6A7")
finish(ax, "BCE Top-K Loss", "Loss")

ax = axes[0][1]
plot_tag(ax, dop, "train/metric/ap",       "Train AP", "#1565C0")
plot_tag(ax, dop, "valid/metric/noise/ap", "Valid AP",  "#90CAF9")
finish(ax, "Average Precision (AP)", "AP")

ax = axes[0][2]
plot_tag(ax, dop, "train/metric/topk_ratio_pos_true",          "Pos GT (train)",         "#2E7D32")
plot_tag(ax, dop, "train/metric/topk_ratio_neg_true",          "Neg GT (train)",         "#B71C1C")
plot_tag(ax, dop, "train/metric/topk_ratio_pos_true_onpolicy", "Pos On-Policy (train)",  "#00838F")
plot_tag(ax, dop, "train/metric/topk_ratio_neg_true_onpolicy", "Neg On-Policy (train)",  "#AD1457")
finish(ax, "Top-K Class Ratios (Train)", "Ratio")

ax = axes[1][0]
plot_tag(ax, dop, "train/metric/loss_pos_true",          "Pos GT",         "#2E7D32")
plot_tag(ax, dop, "train/metric/loss_neg_true",          "Neg GT",         "#B71C1C")
plot_tag(ax, dop, "train/metric/loss_pos_true_onpolicy", "Pos On-Policy",  "#00838F")
plot_tag(ax, dop, "train/metric/loss_neg_true_onpolicy", "Neg On-Policy",  "#AD1457")
finish(ax, "Per-Class Training Loss", "Loss")

ax = axes[1][1]
plot_tag(ax, dop, "valid/metric/noise/loss_pos_true",    "Pos GT",        "#2E7D32")
plot_tag(ax, dop, "valid/metric/noise/loss_neg_true",    "Neg GT",        "#B71C1C")
plot_tag(ax, dop, "valid/metric/noise/loss_neg_freespace","Neg Freespace", "#FF8F00")
finish(ax, "Per-Class Validation Loss", "Loss")

ax = axes[1][2]
plot_tag(ax, dop, "valid/metric/noise/topk_ratio_pos_true",          "Pos GT",         "#2E7D32")
plot_tag(ax, dop, "valid/metric/noise/topk_ratio_neg_true",          "Neg GT",         "#B71C1C")
plot_tag(ax, dop, "valid/metric/noise/topk_ratio_pos_true_onpolicy", "Pos On-Policy",  "#00838F")
plot_tag(ax, dop, "valid/metric/noise/topk_ratio_neg_true_onpolicy", "Neg On-Policy",  "#AD1457")
finish(ax, "Top-K Class Ratios (Validation)", "Ratio")

plt.tight_layout()
p = f"{OUT_DIR}/plot_disc_onpolicy_v3.png"
plt.savefig(p, dpi=160, bbox_inches="tight")
plt.close()
print(f"Saved: {p}")

# ══════════════════════════════════════════════════════════════════════════════
# PLOT 4 — Combined Loss & AP overlay (all 3 runs on same axes)
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle("GraspGen v3 — All Runs: Loss & Average Precision Overlay\nRobotiq 3F  |  227 Objects",
             fontsize=13, fontweight="bold")

ax = axes[0]
plot_tag(ax, gen, "train/loss/all_loss",  "Generator (train)",        "#1565C0")
plot_tag(ax, gen, "valid/loss/all_loss",  "Generator (valid)",         "#90CAF9", lw=1.4)
plot_tag(ax, dgt, "train/loss/bce_topk", "Disc GT (train)",           "#E65100")
plot_tag(ax, dgt, "valid/loss/bce_topk", "Disc GT (valid)",            "#FFCC80", lw=1.4)
plot_tag(ax, dop, "train/loss/bce_topk", "Disc On-Policy (train)",    "#2E7D32")
plot_tag(ax, dop, "valid/loss/bce_topk", "Disc On-Policy (valid)",     "#A5D6A7", lw=1.4)
finish(ax, "Training Loss — All Runs", "Loss", legend_loc="upper right")

ax = axes[1]
plot_tag(ax, dgt, "train/metric/ap",       "Disc GT (train AP)",          "#E65100")
plot_tag(ax, dgt, "valid/metric/noise/ap", "Disc GT (valid AP)",           "#FFCC80", lw=1.4)
plot_tag(ax, dop, "train/metric/ap",       "Disc On-Policy (train AP)",   "#2E7D32")
plot_tag(ax, dop, "valid/metric/noise/ap", "Disc On-Policy (valid AP)",    "#A5D6A7", lw=1.4)
finish(ax, "Average Precision — Discriminators", "AP", legend_loc="lower right")

plt.tight_layout()
p = f"{OUT_DIR}/plot_combined_loss_ap.png"
plt.savefig(p, dpi=160, bbox_inches="tight")
plt.close()
print(f"Saved: {p}")

print("\nAll 4 plots done.")
