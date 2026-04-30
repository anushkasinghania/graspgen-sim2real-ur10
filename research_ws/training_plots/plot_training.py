#!/usr/bin/env python3
"""Generate individual per-metric training graphs for GraspGen Robotiq 3F runs."""

import os, datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

LOGS = '/home/ubuntu/GraspDataGen/training_logs'
OUT  = '/home/ubuntu/training_plots'
os.makedirs(f'{OUT}/gen_v3',  exist_ok=True)
os.makedirs(f'{OUT}/disc_v3', exist_ok=True)
os.makedirs(f'{OUT}/disc_onpolicy_v3', exist_ok=True)

plt.style.use('seaborn-whitegrid')
plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor':   '#f8f9fa',
    'axes.edgecolor':   '#aaa',
    'axes.labelcolor':  '#222',
    'axes.titlecolor':  '#111',
    'xtick.color':      '#444',
    'ytick.color':      '#444',
    'grid.color':       '#ddd',
    'grid.linestyle':   '--',
    'grid.alpha':       0.7,
    'text.color':       '#111',
    'legend.facecolor': 'white',
    'legend.edgecolor': '#ccc',
    'font.size':        10,
})

TRAIN_COLOR = '#e07b39'
VALID_COLOR = '#2a7ab5'

def load(run, tag):
    ea = EventAccumulator(os.path.join(LOGS, run), size_guidance={'scalars': 0})
    ea.Reload()
    events = ea.Scalars(tag)
    steps = np.array([e.step  for e in events])
    vals  = np.array([e.value for e in events])
    return steps, vals

def smooth(vals, w=20):
    if len(vals) < w:
        return vals
    kernel = np.ones(w) / w
    padded = np.pad(vals, (w//2, w//2), mode='edge')
    return np.convolve(padded, kernel, mode='valid')[:len(vals)]

def save_graph(run, ttag, vtag, title, xlabel, ylabel, filename):
    fig, ax = plt.subplots(figsize=(8, 4.5), facecolor='white')
    plotted = False

    if ttag:
        try:
            s, v = load(run, ttag)
            ax.plot(s, v, color=TRAIN_COLOR, alpha=0.18, linewidth=0.8)
            ax.plot(s, smooth(v), color=TRAIN_COLOR, linewidth=2.2,
                    label='Train', solid_capstyle='round')
            plotted = True
        except:
            ax.text(0.5, 0.5, 'No train data yet', transform=ax.transAxes,
                    ha='center', va='center', color='#aaa', fontsize=11)

    if vtag:
        try:
            s, v = load(run, vtag)
            ax.plot(s, v, color=VALID_COLOR, alpha=0.25, linewidth=0.8)
            ax.plot(s, smooth(v), color=VALID_COLOR, linewidth=2.2,
                    label='Validation', linestyle='--', solid_capstyle='round')
            plotted = True
        except:
            pass

    ax.set_title(title, fontsize=12, fontweight='bold', pad=10, color='#111')
    ax.set_xlabel(xlabel, fontsize=9, color='#555', labelpad=5)
    ax.set_ylabel(ylabel, fontsize=9, color='#555', labelpad=5)
    if plotted:
        ax.legend(fontsize=9, framealpha=0.9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(filename, dpi=130, bbox_inches='tight', facecolor='white')
    plt.close()

STEP_LABEL = 'Training Step  (1 step = 1 batch of 8 objects)'

# ══════════════════════════════════════════════════════════
# GENERATOR v3  — individual graphs
# ══════════════════════════════════════════════════════════
print("=== Generator v3 individual graphs ===")
run = 'robotiq_3f_gen_v3'
gen_graphs = [
    ('train/loss/all_loss',             'valid/loss/all_loss',
     'Total Loss',
     STEP_LABEL, 'Loss  (lower is better)',
     f'{OUT}/gen_v3/01_total_loss.png'),

    ('train/loss/noise_pred',            'valid/loss/noise_pred',
     'Noise Prediction Loss  ★ Core Diffusion Objective',
     STEP_LABEL, 'Loss  (lower is better)',
     f'{OUT}/gen_v3/02_noise_pred_loss.png'),

    ('train/metric/error_trans_l2',      'valid/metric/reconstruction/error_trans_l2',
     'Translation Error (L2)  — Gripper Position Accuracy',
     STEP_LABEL, 'Error  [metres]  (lower is better)',
     f'{OUT}/gen_v3/03_error_trans_l2.png'),

    ('train/metric/error_rot_geodesic',  'valid/metric/reconstruction/error_rot_geodesic',
     'Rotation Error (Geodesic)  — Gripper Orientation Accuracy',
     STEP_LABEL, 'Error  [radians]  (lower is better)',
     f'{OUT}/gen_v3/04_error_rot_geodesic.png'),

    ('train/metric/error_rot_phi3',      'valid/metric/reconstruction/error_rot_phi3',
     'Rotation Error (phi3)  — Gripper Orientation Accuracy',
     STEP_LABEL, 'Error  [degrees]  (lower is better)',
     f'{OUT}/gen_v3/05_error_rot_phi3.png'),

    (None,                               'valid/metric/reconstruction/recall',
     'Validation Recall  — Coverage of Ground-Truth Grasps',
     STEP_LABEL, 'Recall  [0–1]  (higher is better)',
     f'{OUT}/gen_v3/06_recall.png'),

    (None,                               'valid/metric/reconstruction/precision',
     'Validation Precision  — Quality of Proposed Grasps',
     STEP_LABEL, 'Precision  [0–1]  (higher is better)',
     f'{OUT}/gen_v3/07_precision.png'),
]
for ttag, vtag, title, xlabel, ylabel, fname in gen_graphs:
    save_graph(run, ttag, vtag, title, xlabel, ylabel, fname)
    print(f"  → {os.path.basename(fname)}")

# ══════════════════════════════════════════════════════════
# DISCRIMINATOR v3  — individual graphs
# ══════════════════════════════════════════════════════════
print("\n=== Discriminator v3 individual graphs ===")
run = 'robotiq_3f_disc_v3'
disc_graphs = [
    ('train/loss/all_loss',                        'valid/loss/all_loss',
     'Total Loss',
     STEP_LABEL, 'Loss  (lower is better)',
     f'{OUT}/disc_v3/01_total_loss.png'),

    ('train/loss/bce_topk',                        'valid/loss/bce_topk',
     'BCE TopK Loss  ★ Core Classification Objective',
     STEP_LABEL, 'Loss  (lower is better)',
     f'{OUT}/disc_v3/02_bce_topk_loss.png'),

    ('train/metric/ap',                             'valid/metric/noise/ap',
     'Average Precision (AP)  ★ Key Quality Metric',
     STEP_LABEL, 'AP  [0–1]  (higher → 1.0 is better)',
     f'{OUT}/disc_v3/03_average_precision.png'),

    ('train/metric/topk_ratio_pos_true',            'valid/metric/noise/topk_ratio_pos_true',
     'TopK Ratio — Positive (Good) Grasps  ↑ want HIGH',
     STEP_LABEL, 'Ratio  [0–1]',
     f'{OUT}/disc_v3/04_topk_pos_true.png'),

    ('train/metric/topk_ratio_neg_true',            'valid/metric/noise/topk_ratio_neg_true',
     'TopK Ratio — Negative (Bad) Grasps  ↓ want LOW',
     STEP_LABEL, 'Ratio  [0–1]',
     f'{OUT}/disc_v3/05_topk_neg_true.png'),

    ('train/metric/topk_ratio_neg_hncolliding',     'valid/metric/noise/topk_ratio_neg_hncolliding',
     'TopK Ratio — Hard Negative Colliding Grasps  ↓ want LOW',
     STEP_LABEL, 'Ratio  [0–1]',
     f'{OUT}/disc_v3/06_topk_neg_colliding.png'),

    ('train/metric/topk_ratio_neg_freespace',       'valid/metric/noise/topk_ratio_neg_freespace',
     'TopK Ratio — Free Space Grasps  ↓ want LOW',
     STEP_LABEL, 'Ratio  [0–1]',
     f'{OUT}/disc_v3/07_topk_neg_freespace.png'),

    ('train/metric/loss_pos_true',                  'valid/metric/noise/loss_pos_true',
     'Loss on Positive (Good) Grasps  ↓ want LOW',
     STEP_LABEL, 'Loss  (lower is better)',
     f'{OUT}/disc_v3/08_loss_pos_true.png'),

    ('train/metric/loss_neg_true',                  'valid/metric/noise/loss_neg_true',
     'Loss on Negative (Bad) Grasps  ↓ want LOW',
     STEP_LABEL, 'Loss  (lower is better)',
     f'{OUT}/disc_v3/09_loss_neg_true.png'),

    ('train/metric/loss_neg_freespace',             'valid/metric/noise/loss_neg_freespace',
     'Loss on Free Space Grasps  ↓ want LOW',
     STEP_LABEL, 'Loss  (lower is better)',
     f'{OUT}/disc_v3/10_loss_neg_freespace.png'),
]
for ttag, vtag, title, xlabel, ylabel, fname in disc_graphs:
    save_graph(run, ttag, vtag, title, xlabel, ylabel, fname)
    print(f"  → {os.path.basename(fname)}")

# ══════════════════════════════════════════════════════════
# ON-POLICY DISCRIMINATOR  — individual graphs (if data exists)
# ══════════════════════════════════════════════════════════
print("\n=== On-Policy Discriminator v3 individual graphs ===")
run = 'robotiq_3f_disc_onpolicy_v3'
onpolicy_graphs = [
    ('train/loss/all_loss',             'valid/loss/all_loss',
     'Total Loss',
     STEP_LABEL, 'Loss  (lower is better)',
     f'{OUT}/disc_onpolicy_v3/01_total_loss.png'),

    ('train/loss/bce_topk',             'valid/loss/bce_topk',
     'BCE TopK Loss  ★ Core Classification Objective',
     STEP_LABEL, 'Loss  (lower is better)',
     f'{OUT}/disc_onpolicy_v3/02_bce_topk_loss.png'),

    ('train/metric/ap',                  'valid/metric/noise/ap',
     'Average Precision (AP)  ★ Key Quality Metric',
     STEP_LABEL, 'AP  [0–1]  (higher → 1.0 is better)',
     f'{OUT}/disc_onpolicy_v3/03_average_precision.png'),

    ('train/metric/topk_ratio_pos_true', 'valid/metric/noise/topk_ratio_pos_true',
     'TopK Ratio — Positive (Good) Grasps  ↑ want HIGH',
     STEP_LABEL, 'Ratio  [0–1]',
     f'{OUT}/disc_onpolicy_v3/04_topk_pos_true.png'),

    ('train/metric/topk_ratio_neg_true', 'valid/metric/noise/topk_ratio_neg_true',
     'TopK Ratio — Negative (Bad) Grasps  ↓ want LOW',
     STEP_LABEL, 'Ratio  [0–1]',
     f'{OUT}/disc_onpolicy_v3/05_topk_neg_true.png'),
]
for ttag, vtag, title, xlabel, ylabel, fname in onpolicy_graphs:
    save_graph(run, ttag, vtag, title, xlabel, ylabel, fname)
    print(f"  → {os.path.basename(fname)}")

# Write timestamp
with open(f'{OUT}/last_updated.txt', 'w') as f:
    f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

print("\nAll individual graphs saved.")
