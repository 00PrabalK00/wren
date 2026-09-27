#!/usr/bin/env bash
# Train the ACT baseline (Stage 1 of research/FINAL_REPORT.md) on the SO101 pumpkin dataset with LeRobot's trainer.
#
#   bash training/train_act_baseline.sh [run_name] [steps] [batch_size] [dataset_name] [extra lerobot-train args...]
#   python3 so101/dashboard.py logs/<run_name>.log     # live progress in another terminal
#
# ACT from scratch with an ImageNet ResNet-18: 2 s chunks (20 steps at 10 fps), CVAE with kl 10, lr 1e-5.
# No temporal ensembling at train time; the real-time runner decides how many steps of each chunk to execute.
# Photometric augmentation is widened for the lighting shift, with hue disabled (hue changes the pumpkin's colour).
set -euo pipefail
# Paths (venv, data/, outputs/, logs/) are relative to the training workspace.
cd "${SO101_WORKSPACE:-/home/zuci/ripple-research}"
RUN=${1:-act_pumpkin_v1}
STEPS=${2:-80000}
BS=${3:-8}
DATA=${4:-so101_pumpkin_v1}
OUT=outputs/train/$RUN
mkdir -p logs
if [ -d "$OUT/checkpoints/last" ]; then
  # Resume from the saved train config (see train_smolvla_run.sh for why only these two flags are given).
  exec env -u PYTHONPATH .venv-smolvla/bin/lerobot-train --resume=true \
    --config_path="$OUT/checkpoints/last/pretrained_model/train_config.json" --num_workers=2 "${@:5}" >> "logs/$RUN.log" 2>&1
fi
echo "INFO cfg.steps=$STEPS" > "logs/$RUN.log"
env -u PYTHONPATH .venv-smolvla/bin/lerobot-train \
  --policy.type=act \
  --policy.push_to_hub=false \
  --policy.device=cuda \
  --policy.chunk_size=20 \
  --policy.n_action_steps=20 \
  --policy.use_vae=true \
  --policy.kl_weight=10.0 \
  --policy.optimizer_lr=1e-5 \
  --policy.optimizer_lr_backbone=1e-5 \
  --dataset.repo_id=local/$DATA \
  --dataset.root=data/lerobot/$DATA \
  --dataset.image_transforms.enable=true \
  --dataset.image_transforms.max_num_transforms=3 \
  --dataset.image_transforms.tfs='{
    "brightness": {"weight": 1.0, "type": "ColorJitter", "kwargs": {"brightness": [0.6, 1.4]}},
    "contrast":   {"weight": 1.0, "type": "ColorJitter", "kwargs": {"contrast": [0.6, 1.4]}},
    "saturation": {"weight": 1.0, "type": "ColorJitter", "kwargs": {"saturation": [0.5, 1.5]}},
    "sharpness":  {"weight": 1.0, "type": "SharpnessJitter", "kwargs": {"sharpness": [0.5, 1.5]}},
    "affine":     {"weight": 1.0, "type": "RandomAffine", "kwargs": {"degrees": [-5.0, 5.0], "translate": [0.05, 0.05]}}
  }' \
  --output_dir="$OUT" \
  --job_name="$RUN" \
  --steps="$STEPS" \
  --batch_size="$BS" \
  --num_workers=2 \
  --log_freq=100 \
  --save_freq=10000 \
  --wandb.enable=false \
  --seed=1000 "${@:5}" >> "logs/$RUN.log" 2>&1
