# W3_ProgVLAProgressAwareRobotManipulationSki — ProgVLA: Progress-Aware Robot Manipulation Skill Learning (2026, arXiv 2605.28231)
Setup: LIBERO (40 tasks x 50 demos, agent+wrist cams) and Meta-World MT49 (50 demos/task, 1 cam), 50 eval episodes/task; real: AgileX PiPER 6-DoF + gripper, leader/follower teleop (SO-101-like paradigm), wrist RealSense D405 + agent RealSense D435, RGB 112x112 center crop, 10 tasks x 50 demos in 2 environments, 10 trials/task. Model 109M total / 74M trainable: ViT-S DUNE (or DINOv3) vision fine-tuned, frozen T5 text, per-modality + post-fusion Perceiver resamplers, flow-matching action-chunk expert; progress heads (Q, V expectile, success classifier) reweight FM loss (advantage-weighted). NO robot pretraining. Train on 1 H100 (real: 8.5 h); runs "real time" on laptop RTX 3500 (no latency numbers). Single seed.
Claim: A 0.1B from-scratch (except ViT-S + T5) flow-matching VLA with token compression and progress-weighted imitation matches/exceeds SmolVLA/pi0/OpenVLA on LIBERO/Meta-World, especially long-horizon.
Evidence:
 - LIBERO avg 91.1 (Spatial 87.6, Object 96.0, Goal 92.0, Long 88.6) vs SmolVLA-2.25B +2.4 avg, +11.6 on Long; vs OpenVLA-7B +14.6 avg (baselines imported, not rerun; ProgVLA had 2000 vs 1693 demos).
 - Meta-World: +20.9 medium / +7.0 hard / +15.6 very hard vs SmolVLA-2.25B; +10.3 overall.
 - Real PiPER, 50 demos/task, in-distribution only: 68% avg over 100 trials (per task 50–80%). Failures (32): clutter obstruction 10, gripper-open timeout 8, wrong object (language grounding) 4.
Ablations (LIBERO avg / Long):
 - full 91.1 / 88.6
 - w/o progress objectives (plain FM) 88.8 / 85.1 (−2.3)
 - w/o post-fusion context resampler 75.1 / 51.2 (−16)
 - DINOv3 instead of DUNE 88.7 / 81.0 (−2.4)
 - frozen DUNE 77.6 / 60.6 (−13.5) → fine-tuning the ViT-S is essential.
Failure/limitations: baselines imported with protocol differences; single seed (±1–2 pts noise, so progress-objective gain is small but consistent); real eval in-distribution only, no lighting/object/camera shift tests; no latency measurements; progress target is just normalized time-to-go.
Conflicts: Frozen-vs-finetuned: agrees with works showing end-to-end fine-tuning of the encoder beats frozen features for in-domain success (e.g. Theia/"what makes pretrained visual reps" style results), but contrasts with robustness papers arguing frozen foundation features preserve invariance under shift — ProgVLA only tests in-distribution, so it cannot speak to robustness. SmolVLA comparison suggests pretraining on cross-embodiment data is not needed for benchmark-level success at 50 demos/task when the model is small and the encoder is a strong SSL ViT.
Relevance: Very close hardware analogue (low-cost 6-DoF leader/follower, wrist + RealSense agent cam, 50 demos/task, laptop GPU inference). Suggests a ~100M model with ViT-S DINOv3/DUNE fine-tuned + FM head is a viable SmolVLA replacement fitting 8 GB; 112x112 images suffice for pick-place. Action space: joint-angle displacements (delta joints) + absolute gripper. Real success 68% in-distribution — not a robustness proof.
Decision impact:
 - Q03 vision encoder: pretrained SSL ViT-S (DUNE ≈ DINOv3) fine-tuned end to end; freezing costs −13.5 pts (−28 on long) — supports fine-tune pretrained DINO-family — confidence M (sim ablation, single seed).
 - Q12 model size: 0.1B from-scratch-policy competitive with 0.45–2.25B SmolVLA and 7B OpenVLA at 50 demos/task — supports small (~100M) models — confidence M (imported baselines).
 - Q01 action head: flow matching works at 100M; advantage/success reweighting adds +2.3 — weak support for FM — confidence L.
 - Q09 auxiliary objectives: progress/value heads used for loss reweighting give small consistent gain (+2.3 avg, +3.5 long) — confidence L (single seed).
 - Q02 action space: delta joint displacement used successfully on PiPER real robot — confidence L (no ablation).
