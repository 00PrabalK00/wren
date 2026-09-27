# W3_NormalizingFlowsareCapableModelsforBiman — Normalizing Flows are Capable Models for Bi-manual Visuomotor Policy (2025, arXiv 2509.21073)
Setup: NF-P = pretrained ResNet18 image embedding + latest action -> conditional Neural Spline Flow (10 coupling layers, ~100M params). Sim: RoboTwin 2.0, 50 tasks, 50 clean scripted demos each, head camera only, 100 trials/task. Real: dual Kuka iiwa 7, single RealSense D435i scene cam (wrist cams not used), VR teleop, 150 demos (Stack Blocks Two) and 100 demos (Towel Folding), 20 trials each; obs/pred horizon 4 with temporal stride s=6 and Stochastic Batch Selection (best of 128 by likelihood). Training ~50 min on one RTX 4090 for 100 demos.
Claim: a normalizing-flow policy matches or beats Diffusion Policy with single-pass inference and exact likelihoods usable for sample selection or refinement.
Evidence:
 - RoboTwin 2.0 avg (50 tasks): NF-P with gradient refinement 38.06% vs DP 28.04% (DP from official leaderboard). E.g. Open Microwave 77 vs 5, Handover Mic 100 vs 53.
 - Real (Table I, 20 trials): Stack Blocks Two DP 15% vs NF-P 60%; Towel Folding DP 55% vs NF-P 75%. DP often failed to start (35% and 45% initial failures) or looped between sub-goals.
 - Latency: NF-P SBS <20 ms per action sequence; gradient-refined 455 ms, which the authors say is still faster than their DP.
 - Data scaling 10–500 episodes on 4 tasks: NF-P scales like DP (figure only).
Ablations (Beat Block Hammer, 100 trials, Table II): GR 51, SBS 50, raw NF sampling 37. Stride s=1 37, s=2 48, s=4 51, s=8 46. Sampling std 1.0 41, 0.75 47, 0.5 51. No action chunking (single action) 28.
Failure/limitations: DP baseline is not tuned by the authors (sim numbers from the leaderboard, real DP-C). DP was given an 8-minute window per sub-goal vs 30 s for NF-P, so the real comparison protocol is uneven. Only 2 real tasks, 20 trials. No robustness tests. RoboTwin demos are scripted (unimodal-ish).
Conflicts: consistent with many results that chunking is essential (28 vs 51). The "DP fails to start / stalls" pathology in real data matches reports of DP pausing under noisy teleop. Strided sampling is a form of temporal downsampling of noisy teleop data, which relates to the ACT note that higher rates help fine skills. Here, skipping frames (s=4–6) removed jitter/pauses and helped.
Relevance: medium. Single scene RealSense + ResNet18 + ~100M-param head fits an 8 GB GPU, and <20 ms inference directly addresses our 2 s SmolVLA latency. The stride trick is directly relevant to our jittery SO-101 leader-arm teleop: train on subsampled action targets (effective ~3–7 Hz spacing at 30 fps recording) rather than every frame. Exact likelihood could also flag OOD states (lighting/camera shifts), though that is not tested.
Decision impact:
 - Q01 action head: + normalizing flow (single pass, best-of-N by likelihood) competitive with or better than DP on real teleop data (60 vs 15, 75 vs 55) — confidence L-M (uneven baseline protocol)
 - Q06 chunking: + predicting chunks vs single action 51 vs 28 — confidence M (sim)
 - Q06 temporal stride: + strided targets s=4 51 vs s=1 37 (filters teleop jitter/pauses) — confidence M (sim, one task)
 - Q10 latency: + single-pass generative head <20 ms — confidence M
