#!/usr/bin/env python3
"""Offline latency benchmark for a LeRobot policy checkpoint on this GPU, using real dataset frames.

    python tools/bench_policy_latency.py --checkpoint <.../pretrained_model> [--iters 30]

Reports per-stage timing (preprocess, model) for fp32 and bf16, optionally torch.compile.
"""
import argparse
import statistics
import time

import torch

ap = argparse.ArgumentParser()
ap.add_argument("--checkpoint", required=True)
ap.add_argument("--dataset-root", default="/home/zuci/ripple-research/data/lerobot/so101_pumpkin_v1")
ap.add_argument("--iters", type=int, default=30)
ap.add_argument("--compile", action="store_true")
args = ap.parse_args()

try:
    import so101_policy  # noqa: F401  registers so101flow
except ImportError:
    pass
from lerobot.configs.policies import PreTrainedConfig
from lerobot.datasets.lerobot_dataset import LeRobotDataset
from lerobot.policies.factory import get_policy_class, make_pre_post_processors

cfg = PreTrainedConfig.from_pretrained(args.checkpoint)
policy = get_policy_class(cfg.type).from_pretrained(args.checkpoint).to("cuda").eval()
pre, post = make_pre_post_processors(policy_cfg=policy.config, pretrained_path=args.checkpoint,
                                     preprocessor_overrides={"device_processor": {"device": "cuda"}})
ds = LeRobotDataset("local/so101_pumpkin_v1", root=args.dataset_root)
print(f"policy={cfg.type} params={sum(p.numel() for p in policy.parameters())/1e6:.1f}M "
      f"gpu={torch.cuda.get_device_name(0)}")


def sample(i):
    item = ds[i * 97 % len(ds)]
    batch = {k: v.unsqueeze(0) for k, v in item.items() if k.startswith("observation.")}
    batch["task"] = [item["task"]]
    return batch


def run(label, autocast_dtype=None):
    pre_t, model_t = [], []
    for i in range(args.iters + 5):
        b = sample(i)
        torch.cuda.synchronize(); t0 = time.perf_counter()
        x = pre(b)
        torch.cuda.synchronize(); t1 = time.perf_counter()
        with torch.no_grad(), torch.autocast("cuda", dtype=autocast_dtype, enabled=autocast_dtype is not None):
            if hasattr(policy, "predict_action_chunk"):
                out = policy.predict_action_chunk(x)
            else:
                policy.reset(); out = policy.select_action(x)
        torch.cuda.synchronize(); t2 = time.perf_counter()
        if i >= 5:  # warm-up excluded
            pre_t.append((t1 - t0) * 1e3); model_t.append((t2 - t1) * 1e3)
    print(f"{label:28s} preprocess {statistics.median(pre_t):6.1f} ms | model median {statistics.median(model_t):6.1f} ms "
          f"p90 {sorted(model_t)[int(0.9*len(model_t))-1]:6.1f} ms | out {tuple(out.shape)}")


run("fp32")
run("bf16 autocast", torch.bfloat16)
if args.compile:
    policy = torch.compile(policy, mode="max-autotune-no-cudagraphs")
    run("bf16 + torch.compile", torch.bfloat16)
print(f"peak GPU memory {torch.cuda.max_memory_allocated()/2**30:.2f} GiB")
