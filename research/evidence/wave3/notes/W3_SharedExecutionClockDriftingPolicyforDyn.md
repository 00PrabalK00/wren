# W3_SharedExecutionClockDriftingPolicyforDyn — Shared Execution-Clock Drifting Policy for Dynamic Precision Manipulation (SECD) (2026, arXiv 2609.23305)
Setup: Real Franka FR3 (conveyor) and Flexiv Rizon 4s (single/bimanual), wrist RGB cameras only, 224x224, 2 obs steps, DINOv3 ViT-B/16 encoder (fine-tuned at 1e-5) + conditional 1D U-Net; horizon H=16 with relative position + 6D rotation + gripper; 20 Hz commands, execute 8 of 16 before replanning; inference on Jetson AGX Thor. Data: Cup Place 2 h, Fold flat/crumpled 10 h each, Conveyor 3 h. Trials: 100/50/50/100 per method. Method: one-step "drifting" generative policy (single network evaluation) that outputs a progress-indexed action curve + a monotone learned clock (execution rhythm), with demonstration-derived alignment losses. Sim: RoboMimic state-based.
Claim: Making execution timing explicit in a one-step generative policy improves time-critical manipulation while keeping 1-NFE latency.
Evidence (Table I, NFE, latency on Thor, success %: Cup Place / Fold flat / Fold crumpled(90 s) / Conveyor 16 m/min / avg):
 - DP (16 NFE, DDIM): 252 ms; 98.0 / 74.0 / 30.0 / 0.0 / 50.5.
 - OneDP (distilled, 1 NFE): 26 ms; 71.0 / 38.0 / 22.0 / 31.0 / 40.5.
 - Native Drifting (1 NFE): 24 ms; 83.0 / 48.0 / 26.0 / 56.0 / 53.25.
 - SECD (1 NFE): 25 ms; 95.0 / 68.0 / 54.0 / 91.0 / 77.0.
Ablations:
 - Fixed uniform clock (no learned timing) on conveyor: 79/100 vs 91/100.
 - RoboMimic Transport (seed-aggregated): alignment losses +8/+12 pts (best/final) over same-architecture no-alignment variant; Square ~equal.
Failure/limitations: DP's 0% conveyor is a latency artefact (252 ms × 8-step open-loop on a moving target) — not action-quality; DP still best on static precision tasks (Cup Place 98, Fold flat 74). One-step distillation (OneDP) loses a lot of quality (98→71). Large data (2–10 h), big ViT-B.
Conflicts: Agrees with consistency/one-step policy literature that 1-NFE heads can match iterative diffusion only with care; the OneDP drop contradicts claims that distillation is "free". Agrees with async/RTC papers that latency, not model quality, dominates dynamic tasks.
Relevance: For our static pumpkin pick-place, latency matters for smoothness not target interception; DP-style 16-step sampling is still the quality leader on static tasks. If our laptop latency is the bottleneck, few-step flow (or drifting-style one-step generation) is an option but expect a quality cost unless trained natively for 1-step. Also a data point for wrist-camera-only policies succeeding (95% cup place) with relative-pose actions and chunk 16 / execute 8 at 20 Hz.
Decision impact:
 - Q01 action head: 16-step DP best on static precision (98% cup place) but 252 ms; distilled 1-step loses 27 pts; natively-trained 1-step drifting with timing structure 95% at 25 ms — supports few-/one-step generative heads trained natively when latency-bound — confidence M.
 - Q10 latency: at 252 ms inference DP scores 0% on a moving target vs 91% for a 25 ms policy — latency must be addressed explicitly (fewer steps / async) — confidence M (dynamic task, not ours).
 - Q06 chunking: H=16, execute 8 at 20 Hz (0.4 s open loop) works across 4 real tasks — confidence L.
 - Q02 action space: relative EE position + 6D rotation used successfully — confidence L (no ablation).
