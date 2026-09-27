#!/usr/bin/env python3
"""Keep optimizer/training state only in the newest complete checkpoint of each run; models are kept.

    python3 training/prune_checkpoints.py <run_dir> [<run_dir> ...] [--every SECONDS]

training_state (optimizer moments, RNG, step) is only needed to resume from that exact checkpoint, and it is
larger than the model itself, so keeping it in every checkpoint is what filled the disk on 2026-09-27.
"""
import shutil
import sys
import time
from pathlib import Path

args = sys.argv[1:]
every = None
if "--every" in args:
    i = args.index("--every")
    every = float(args[i + 1])
    del args[i:i + 2]
runs = [Path(a).resolve() for a in args]
for run in runs:
    if not (run / "checkpoints").is_dir() or "outputs/train" not in str(run):
        sys.exit(f"not a LeRobot run directory: {run}")


def complete(ckpt):
    ts = ckpt / "training_state"
    return (ckpt / "pretrained_model" / "model.safetensors").is_file() and (ts / "optimizer_state.safetensors").is_file() \
        and (ts / "training_step.json").is_file()


def prune():
    for run in runs:
        ckpts = sorted(p for p in (run / "checkpoints").iterdir() if p.is_dir() and not p.is_symlink() and p.name.isdigit())
        done = [c for c in ckpts if complete(c)]
        if not done:
            continue
        keep = done[-1]
        for c in ckpts:
            ts = c / "training_state"
            # Only older checkpoints; never the newest, which may still be being written.
            if c.name < keep.name and ts.is_dir() and ts.parent.parent == run / "checkpoints":
                shutil.rmtree(ts)
                print(f"{time.strftime('%H:%M')} pruned {ts}", flush=True)


while True:
    prune()
    if every is None:
        break
    time.sleep(every)
