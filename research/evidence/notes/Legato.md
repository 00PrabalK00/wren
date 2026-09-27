# Legato — Learning Native Continuation for Action Chunking Flow Policies (2026, arXiv 2602.12978)
Setup: flow-matching VLA policies (dual-arm robot), 5 real tasks (stack bowls, pour, pick&place-all, fold towel, open drawer), 120 s cutoff; metrics: task score, completion time, jerk (NLDLJ), spectral arc length (NSPARC), overlap RMSE. Compared vs RTC and training-time RTC.
Method (simple to implement — Algorithm 1): during training build a per-timestep guidance schedule ω (full guidance for first d steps, linear ramp over r steps, then 0); noise start = ω⊙A + (1−ω)⊙ε; target velocity reshaped v = (1 − κ⊙(1−t))⊙(A−ε), κ=ω/Δt; condition the decoder on ω (append as an extra action-feature channel); randomize (d, r) during training. Inference: reference = previous chunk's remaining actions padded; before EVERY denoising step blend Y=(1−ω)⊙X+ω⊙Aref then Euler step. Same N steps train/test.
Evidence: ~10% better smoothness and ~10% shorter completion vs RTC across 5 tasks; suppresses spurious multimodal switching (RTC alternated grasp goals / arm choice between chunks; Legato stayed consistent). One-shot prefix guidance insufficient — per-step guidance required. Schedule conditioning lets one model handle varying latency.
Limitations: flow-based only; dual-arm VLA scale; no small-model test; improvement over RTC is moderate (~10%).
Relevance: gives us a training-time recipe that is cheap (no guidance backprop at inference unlike RTC) and handles variable latency — our laptop latency varies (power mode!). Must use a flow head.
Decision impact:
 - execution continuity: train with Legato-style schedule conditioning — SUPPORTED — M (one paper, real robot, consistent gains).
 - action_head: flow matching — SUPPORTED — H (both RTC & Legato require it).
