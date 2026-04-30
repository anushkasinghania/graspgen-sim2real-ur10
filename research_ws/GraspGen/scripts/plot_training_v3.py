"""
Plot training curves for GraspGen v3 (Robotiq 3F, 227 objects).

Outputs saved to ~/GraspDataGen/training_logs/plots_v3/:
  1. onpolicy_disc_v3_individual.png  — all metrics for disc_onpolicy_v3
  2. v3_combined_all_runs.png         — loss + key metrics across all 3 runs
"""

import os, glob
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from collections import defaultdict
from tensorboard.backend.event_processing.event_file_loader import LegacyEventFileLoader

# ── paths ────────────────────────────────────────────────────────────────────
LOG_DIR = os.path.expanduser("~/GraspDataGen/training_logs")
OUT_DIR = os.path.join(LOG_DIR, "plots_v3")
os.makedirs(OUT_DIR, exist_ok=True)

RUN_PATHS = {
    "Generator v3":               os.path.join(LOG_DIR, "robotiq_3f_gen_v3"),
    "Discriminator GT v3":        os.path.join(LOG_DIR, "robotiq_3f_disc_v3"),
    "Discriminator On-Policy v3": os.path.join(LOG_DIR, "robotiq_3f_disc_onpolicy_v3"),
}

# ── fast loader: reads all event files in a directory, returns {tag: (steps, vals)} ──
def load_run(run_dir):
    """Parse all tfevents files in run_dir. Returns dict tag -> (steps_arr, vals_arr)."""
    data = defaultdict(list)  # tag -> [(step, value), ...]
    event_files = sorted(glob.glob(os.path.join(run_dir, "events.out.tfevents.*")))
    for ef in event_files:
        try:
            loader = LegacyEventFileLoader(ef)
            for event in loader.Load():
                if not hasattr(event, "summary"):
                    continue
                step = event.step
                for v in event.summary.value:
                    tag = v.tag
                    if v.HasField("simple_value"):
                        data[tag].append((step, v.simple_value))
        except Exception:
            continue
    # Convert to sorted numpy arrays, deduplicate by step (keep last)
    out = {}
    for tag, pairs in data.items():
        pairs.sort(key=lambda x: x[0])
        seen, steps, vals = set(), [], []
        for s, v in pairs:
            if s not in seen:
                seen.add(s)
                steps.append(s)
                vals.append(v)
        out[tag] = (np.array(steps), np.array(vals))
    return out

def smooth(y, w=7):
    if len(y) < w:
        return y
    kernel = np.ones(w) / w
    pad = np.pad(y, (w // 2, w // 2), mode="edge")
    return np.convolve(pad, kernel, mode="valid")[: len(y)]

def plot_tag(ax, run_data, tag, label, color, lw=1.8):
    if tag not in run_data:
        return
    steps, vals = run_data[tag]
    ax.plot(steps, smooth(vals), color=color, lw=lw, label=label)
    ax.plot(steps, vals, color=color, lw=0.35, alpha=0.22)

def style_ax(ax, title, xlabel="Epoch"):
    ax.set_title(title, fontsize=10, fontweight="bold")
    ax.set_xlabel(xlabel, fontsize=9)
    ax.legend(fontsize=8, loc="best")
    ax.grid(True, alpha=0.28)
    ax.spines[["top", "right"]].set_visible(False)

# ── load all runs ─────────────────────────────────────────────────────────────
print("Loading event files…")
runs = {name: load_run(path) for name, path in RUN_PATHS.items()}
print("  Gen tags:     ", len(runs["Generator v3"]))
print("  Disc GT tags: ", len(runs["Discriminator GT v3"]))
print("  Disc OP tags: ", len(runs["Discriminator On-Policy v3"]))

# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 1 — On-Policy Discriminator v3  (3 rows × 2 cols)
# ═══════════════════════════════════════════════════════════════════════════════
d = runs["Discriminator On-Policy v3"]

fig, axes = plt.subplots(3, 2, figsize=(16, 13))
fig.suptitle(
    "Discriminator On-Policy v3 — Training Curves\n"
    "Robotiq 3F  |  227 Objects  |  500 Epochs",
    fontsize=14, fontweight="bold",
)

# [0,0] Loss
ax = axes[0][0]
plot_tag(ax, d, "train/loss/bce_topk", "Train loss", "#E53935")
plot_tag(ax, d, "valid/loss/bce_topk", "Valid loss", "#EF9A9A")
style_ax(ax, "BCE Top-K Loss")

# [0,1] Average Precision
ax = axes[0][1]
plot_tag(ax, d, "train/metric/ap",       "Train AP", "#1976D2")
plot_tag(ax, d, "valid/metric/noise/ap", "Valid AP", "#90CAF9")
style_ax(ax, "Average Precision (AP)")

# [1,0] GT class ratios
ax = axes[1][0]
plot_tag(ax, d, "train/metric/topk_ratio_pos_true", "Pos GT",  "#2E7D32")
plot_tag(ax, d, "train/metric/topk_ratio_neg_true", "Neg GT",  "#C62828")
style_ax(ax, "Train — Top-K Ratios (Ground-Truth)")

# [1,1] On-policy class ratios
ax = axes[1][1]
plot_tag(ax, d, "train/metric/topk_ratio_pos_true_onpolicy", "Pos On-Policy", "#00838F")
plot_tag(ax, d, "train/metric/topk_ratio_neg_true_onpolicy", "Neg On-Policy", "#AD1457")
style_ax(ax, "Train — Top-K Ratios (On-Policy)")

# [2,0] Per-class loss
ax = axes[2][0]
plot_tag(ax, d, "train/metric/loss_pos_true",          "Pos GT loss",         "#2E7D32")
plot_tag(ax, d, "train/metric/loss_neg_true",          "Neg GT loss",         "#C62828")
plot_tag(ax, d, "train/metric/loss_pos_true_onpolicy", "Pos On-Policy loss",  "#00838F")
plot_tag(ax, d, "train/metric/loss_neg_true_onpolicy", "Neg On-Policy loss",  "#AD1457")
style_ax(ax, "Train — Per-Class Loss")

# [2,1] Valid class ratios
ax = axes[2][1]
plot_tag(ax, d, "valid/metric/noise/topk_ratio_pos_true",          "Pos GT",         "#2E7D32")
plot_tag(ax, d, "valid/metric/noise/topk_ratio_neg_true",          "Neg GT",         "#C62828")
plot_tag(ax, d, "valid/metric/noise/topk_ratio_pos_true_onpolicy", "Pos On-Policy",  "#00838F")
plot_tag(ax, d, "valid/metric/noise/topk_ratio_neg_true_onpolicy", "Neg On-Policy",  "#AD1457")
style_ax(ax, "Valid — Top-K Class Ratios")

plt.tight_layout()
out1 = os.path.join(OUT_DIR, "onpolicy_disc_v3_individual.png")
plt.savefig(out1, dpi=150, bbox_inches="tight")
plt.close()
print(f"Saved: {out1}")


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 2 — Combined: all 3 v3 runs  (3 rows × 3 cols)
# ═══════════════════════════════════════════════════════════════════════════════
g   = runs["Generator v3"]
dgt = runs["Discriminator GT v3"]
dop = runs["Discriminator On-Policy v3"]

fig, axes = plt.subplots(3, 3, figsize=(18, 13))
fig.suptitle(
    "GraspGen v3 — Full Training Pipeline\n"
    "Robotiq 3F  |  227 Objects  |  Generator · Discriminator GT · Discriminator On-Policy",
    fontsize=14, fontweight="bold",
)

# ── Row 0: Generator ─────────────────────────────────────────────────────────
ax = axes[0][0]
plot_tag(ax, g, "train/loss/all_loss", "Train", "#1565C0")
plot_tag(ax, g, "valid/loss/all_loss", "Valid",  "#90CAF9")
style_ax(ax, "Generator — Total Loss")
axes[0][0].set_ylabel("GENERATOR", fontsize=9, fontweight="bold", color="#555")

ax = axes[0][1]
plot_tag(ax, g, "train/metric/error_rot_geodesic",                    "Train", "#1565C0")
plot_tag(ax, g, "valid/metric/reconstruction/error_rot_geodesic",     "Valid",  "#90CAF9")
style_ax(ax, "Generator — Rotation Error (rad)")

ax = axes[0][2]
plot_tag(ax, g, "train/metric/error_trans_l2",                        "Train", "#1565C0")
plot_tag(ax, g, "valid/metric/reconstruction/error_trans_l2",         "Valid",  "#90CAF9")
style_ax(ax, "Generator — Translation Error (m)")

# ── Row 1: Discriminator GT ───────────────────────────────────────────────────
ax = axes[1][0]
plot_tag(ax, dgt, "train/loss/bce_topk", "Train", "#E65100")
plot_tag(ax, dgt, "valid/loss/bce_topk", "Valid",  "#FFCC80")
style_ax(ax, "Disc GT — BCE Loss")
axes[1][0].set_ylabel("DISC GT", fontsize=9, fontweight="bold", color="#555")

ax = axes[1][1]
plot_tag(ax, dgt, "train/metric/ap",       "Train AP", "#E65100")
plot_tag(ax, dgt, "valid/metric/noise/ap", "Valid AP",  "#FFCC80")
style_ax(ax, "Disc GT — Average Precision")

ax = axes[1][2]
plot_tag(ax, dgt, "train/metric/topk_ratio_pos_true", "Pos GT",  "#2E7D32")
plot_tag(ax, dgt, "train/metric/topk_ratio_neg_true", "Neg GT",  "#B71C1C")
style_ax(ax, "Disc GT — Top-K Class Ratios")

# ── Row 2: Discriminator On-Policy ────────────────────────────────────────────
ax = axes[2][0]
plot_tag(ax, dop, "train/loss/bce_topk", "Train", "#2E7D32")
plot_tag(ax, dop, "valid/loss/bce_topk", "Valid",  "#A5D6A7")
style_ax(ax, "Disc On-Policy — BCE Loss")
axes[2][0].set_ylabel("DISC ON-POLICY", fontsize=9, fontweight="bold", color="#555")

ax = axes[2][1]
plot_tag(ax, dop, "train/metric/ap",       "Train AP", "#2E7D32")
plot_tag(ax, dop, "valid/metric/noise/ap", "Valid AP",  "#A5D6A7")
style_ax(ax, "Disc On-Policy — Average Precision")

ax = axes[2][2]
plot_tag(ax, dop, "train/metric/topk_ratio_pos_true",          "Pos GT",         "#2E7D32")
plot_tag(ax, dop, "train/metric/topk_ratio_neg_true",          "Neg GT",         "#B71C1C")
plot_tag(ax, dop, "train/metric/topk_ratio_pos_true_onpolicy", "Pos On-Policy",  "#00838F")
plot_tag(ax, dop, "train/metric/topk_ratio_neg_true_onpolicy", "Neg On-Policy",  "#AD1457")
style_ax(ax, "Disc On-Policy — Top-K Class Ratios")

plt.tight_layout()
out2 = os.path.join(OUT_DIR, "v3_combined_all_runs.png")
plt.savefig(out2, dpi=150, bbox_inches="tight")
plt.close()
print(f"Saved: {out2}")
print("\nAll done. Plots in:", OUT_DIR)
