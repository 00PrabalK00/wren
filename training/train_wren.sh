#!/usr/bin/env bash
# Train our own policy, "SO-101 flow policy v1" (So101/so101_policy, research/FINAL_REPORT.md sections 3-4).
#
#   bash training/train_wren.sh [run_name] [steps] [batch_size] [dataset_name] [extra lerobot-train args...]
#   python3 so101/dashboard.py logs/<run_name>.log     # live progress in another terminal
#
# DINOv2 ViT-S (encoder frozen for the first 1k steps, then lr 1e-5) + transformer trunk + flow-matching DiT
# expert with training-time RTC; AdamW 1e-4 with cosine decay; EMA weights are used for inference.
# Same photometric augmentation as the ACT baseline (hue off); crop/shift/rotation and scene-token dropout
# happen inside the model. The plugin is found via the .pth file in the venv pointing at ~/So101.
set -euo pipefail
# Paths (venv, data/, outputs/, logs/) are relative to the training workspace.
cd "${SO101_WORKSPACE:-/home/zuci/ripple-research}"
RUN=${1:-so101flow_pumpkin_v1}
STEPS=${2:-60000}
BS=${3:-16}
DATA=${4:-so101_pumpkin_v1}
OUT=outputs/train/$RUN
mkdir -p logs
if [ -d "$OUT/checkpoints/last" ]; then
  exec env -u PYTHONPATH .venv-smolvla/bin/lerobot-train --resume=true \
    --policy.discover_packages_path=so101_policy \
    --config_path="$OUT/checkpoints/last/pretrained_model/train_config.json" --num_workers=2 "${@:5}" >> "logs/$RUN.log" 2>&1
fi
echo "INFO cfg.steps=$STEPS" > "logs/$RUN.log"
env -u PYTHONPATH .venv-smolvla/bin/lerobot-train \
  --policy.discover_packages_path=so101_policy \
  --policy.type=so101flow \
  --policy.push_to_hub=false \
  --policy.device=cuda \
  --policy.scheduler_decay_steps="$STEPS" \
  --dataset.repo_id=local/$DATA \
  --dataset.root=data/lerobot/$DATA \
  --dataset.image_transforms.enable=true \
  --dataset.image_transforms.max_num_transforms=3 \
  --dataset.image_transforms.tfs='{
    "brightness": {"weight": 1.0, "type": "ColorJitter", "kwargs": {"brightness": [0.6, 1.4]}},
    "contrast":   {"weight": 1.0, "type": "ColorJitter", "kwargs": {"contrast": [0.6, 1.4]}},
    "saturation": {"weight": 1.0, "type": "ColorJitter", "kwargs": {"saturation": [0.5, 1.5]}},
    "sharpness":  {"weight": 1.0, "type": "SharpnessJitter", "kwargs": {"sharpness": [0.5, 1.5]}}
  }' \
  --output_dir="$OUT" \
  --job_name="$RUN" \
  --steps="$STEPS" \
  --batch_size="$BS" \
  --num_workers=2 \
  --log_freq=100 \
  --save_freq=5000 \
  --wandb.enable=false \
  --seed=1000 "${@:5}" >> "logs/$RUN.log" 2>&1
