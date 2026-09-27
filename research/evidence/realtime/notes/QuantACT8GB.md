# QuantACT8GB — Bimanual Manipulation Within an 8 GB Budget: Zero-Copy Sensing and Quantized ACT on an Entry-Level Jetson (Singh et al., Aug 2026, arXiv 2608.03938)
Setup: BIMANUAL SO-101 (2 leader + 2 follower), 3 USB RGB cams 640×480 at 10 fps (head + 2 wrist), 10 Hz control, LeRobot; 100 teleop demos at 10 Hz of a deformable beanbag pick-and-place. Training on RTX 3070 (offline); deployment on Jetson Orin Nano Super 8 GB (MAXN_SUPER). ACT (52.6M params, ResNet18, chunk 100, n_action_steps=100, no TE) vs LeRobot Diffusion Policy. ACT exported to ONNX → TensorRT FP16/INT8 (entropy calibration with ~100 observations). 20 trials per precision.
Evidence:
 - ACT 100k steps: 19/20; Diffusion Policy 200k steps: 0/10 (did not converge to a usable policy on this budget).
 - ACT latency (Orin Nano): FP32 PyTorch eager 114.02 ms mean (p95 144.73 ms); TensorRT FP16 17.93 ms (6.4×); INT8 12.65 ms (9.0×; 28% faster than FP16, +39% throughput). Success FP32/FP16/INT8 = 19/20, 18/20, 19/20 (no detectable difference).
 - INT8 calibration quantised the ResNet18 but accepted 0 of 145 transformer layers (fell back to FP16) → file only 0.9% smaller; vision backbone dominates ACT cost. Worst-case per-action deviation up to 16.98% on one dimension, yet no success change on this forgiving task.
 - Chunking coupling: with n_action_steps=100 inference runs once per 10 s, so FP32 (114 ms > 100 ms period) is still feasible; per-step re-prediction (needed for ACT temporal ensembling) is infeasible in FP32 at 10 Hz (ceiling 8.77 Hz) but easy in FP16/INT8.
 - Zero-copy GStreamer/NVMM capture: mean pipeline latency unchanged (99.25 vs 99.09 ms, camera-rate-bound at 10 fps); max 117.31→101.52 ms; peak single-core CPU 98.0→77.0%, peak all-core 73.8→33.2%.
Ablations: precision (above); sensing path (above).
Failure/limitations: one forgiving task; n=20; FP32 baseline is PyTorch eager, so 6.4× mixes precision with TensorRT graph compilation. Critical read: DP failure attributed to convergence cost at this step budget, not an accuracy ceiling (authors).
Conflicts: DP 0/10 at 100 demos on SO-101 vs DP successes elsewhere (e.g., 50–60 demo labs) — likely tuning/budget; agrees with SO101-Benchmark that ACT is a strong baseline on SO-101.
Relevance: VERY HIGH (same arm, same 10 Hz rate, 8 GB class, LeRobot): (a) a 52M ACT runs in 12–18 ms with TensorRT even on a Jetson Orin Nano — an RTX 5060 laptop should be far faster; (b) with 10 fps cameras, the camera itself bounds the loop at ~100 ms per frame; (c) CPU-side capture (3 USB cams) can saturate a core and add jitter.
Decision impact:
 - Q10 latency: TensorRT FP16 gives ~6× over eager PyTorch at unchanged success; INT8 adds ~28% — M (n=20, one task).
 - Q10 async: long open-loop chunks (100 steps) hide slow inference; per-step re-prediction/TE requires fast inference — M.
 - Q02 fps: at 10 fps the camera, not the model, sets the observation rate — M.
