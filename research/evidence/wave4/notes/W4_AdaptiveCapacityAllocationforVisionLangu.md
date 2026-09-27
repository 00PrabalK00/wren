# W4_AdaptiveCapacityAllocationforVisionLangu — Adaptive Capacity Allocation for Vision Language Action Fine-tuning (LoRA-SP) (2026, arXiv 2603.07404)
Setup: AgileX PiPER 7-DoF (unseen embodiment for VLA pretraining), 4 real tasks (Open pot, Pour block, Press button, Pick-Place grape), 120 human teleop demos/task (480 total), 2 RGB cams (side view + wrist). Backbones π0 (3.5B, flow matching) and SmolVLA. Baselines: Full FT, LoRA r∈{8..128}, LoRA-MoE, AdaLoRA. Success-rate granularity 6.7% → 15 trials per task/cell. Compute/latency not reported.
Claim: VLA adaptation to a new embodiment needs high and layer-varying LoRA rank (vision tower highest); a router-gated SVD-style adapter (LoRA-SP, init r=128, η=0.9) matches full FT and beats fixed LoRA in multi-task by up to 31.6%.
Evidence (multi-task, Table I; Open/Pour/Press/PickPlace):
 - SmolVLA: Full FT 73.3/86.7/100/86.7; LoRA-SP 86.7/86.7/100/93.3; LoRA r=128 40.0/20.0/93.3/86.7; AdaLoRA 6.7/0.0/40.0/20.0.
 - π0: Full FT 80.0/86.7/80.0/86.7; LoRA-SP 80.0/80.0/93.3/80.0; LoRA r=128 73.3/26.7/80.0/60.0.
 - Single-task SmolVLA (Table II): LoRA r=8 0.0/6.7/26.7/20.0 → r=16 53.3/60/80/60 → r=128 86.7/80/100/100; Full FT 86.7/86.7/100/100. π0 LoRA r=8 6.7/0/0/20 vs Full FT 86.7/80/86.7/93.3.
Ablations:
 - Spectral loss removed → active rank (vision, lang, action) 83,107,57 vs 84,35,34; success 73.3/66.7/100/73.3 vs 86.7/86.7/100/93.3.
 - Energy target η: 0.5 → 6.7/13.3/93.3/13.3; 0.7 → 53.3/80/100/53.3; 0.9 → 86.7/86.7/100/93.3; 0.99 (rank 114) → 80/86.7/100/100.
 - Layer-wise learned rank (Fig. 6, qualitative): vision tower consistently needs highest rank; language low; action expert variable.
 - Spectral analysis (Fig. 4, figure only): OOD embodiment (PiPER) requires higher rank than in-domain (DROID/Franka) in all modules.
Failure/limitations: 15 trials/cell, single seed, no robustness (lighting/object/camera) tests; no latency/memory numbers; multi-task LoRA collapse may partly be a tuning artifact (same LR for all ranks?). Full FT beats all LoRA baselines, so the "method" gain is mainly vs weak PEFT.
Conflicts: SmolVLA's default recipe freezes the VLM vision encoder and trains only the action expert (+projections); this paper shows the vision tower is where adaptation capacity is needed for a new robot/camera — consistent with works finding frozen encoders underperform fine-tuned ones in-domain (e.g. ACT/DP train end-to-end). Agrees with OpenVLA findings that low-rank LoRA underperforms on new embodiments.
Relevance: Directly relevant — SmolVLA fine-tune on an unseen low-cost arm with side+wrist cams and ~120 demos/task, our exact regime. Suggests: if we keep SmolVLA, (a) small-rank LoRA is a bad idea, (b) unfreezing/adapting the vision tower matters, (c) full FT at 8 GB is hard for π0 but feasible-ish for SmolVLA (~450M). Says nothing about robustness or latency.
Decision impact:
 - Q12 model size/fine-tuning: supports full FT (or high-rank ≥64 adapters) of a small VLA (SmolVLA) over low-rank LoRA; SmolVLA full FT ≈ π0 full FT on this regime — M (real robot, 15 trials, 4 tasks)
 - Q03 vision encoder: supports fine-tuning (not freezing) the vision encoder for a new embodiment/cameras — L/M (inferred from learned rank allocation, not a direct freeze ablation)
 - Q13 data: 120 demos/task sufficient for 80–100% on simple PiPER tasks with SmolVLA full FT — L
