# W3_GeoPropGroundingRobotStateinVisionforGen — GeoProp: Grounding Robot State in Vision for Generalist Manipulation (2026, arXiv id not in text)
Setup: Plug-in adapter for Diffusion Policy (ResNet-18 from scratch or ImageNet ViT-B/16; obs horizon 2, chunk 32, 224x224, 100 epochs) and pi0 (3B, 30k steps). Sim: MetaWorld 50 tasks x 25 scripted demos (per-task), RLBench 6 tasks x 100 demos, RoboTwin 7 (and 15) tasks x 50 demos; 25 rollouts/task (MetaWorld 2 seeds x 25). Real: Mobile ALOHA (2x 6-DoF arms), single front RealSense, 4 household tasks x 50 teleop demos, 20 trials/task. Adapter: project EE 3D position into image with calibrated extrinsics, FiLM-modulate the co-located feature cell, bilinear-sample a "grounded state token", plus a look-ahead token sampled at quadratic-extrapolated EE position from 4-frame history. +2-3% params.
Claim: Proprioception fed as a global vector (concat or attention) is poorly used and can hurt; grounding it in image features at the projected EE location helps consistently.
Evidence:
 - DP sim (Table 1/B.6-8), Vanilla / No-Proprio / GeoProp: ResNet-18 MetaWorld-50 68.8/70.1/76.6, RLBench 66.0/68.0/79.3, RoboTwin 53.7/53.7/62.9, overall avg 66.8/68.1/75.3; ViT-B MetaWorld 64.6/64.0/72.6, RLBench 65.3/70.7/79.3, RoboTwin 41.1/42.9/52.0, overall 71.0 for GeoProp (+9.0 vs Vanilla).
 - pi0 RoboTwin-7: No-Proprio 61.7, Vanilla 64.0, GeoProp 68.0; RoboTwin-15: 66.4 -> 70.9.
 - Real DP-ResNet18 (Paper/Coffee/Desk/Table/avg): No-Proprio 25/40/35/15/28.8; Vanilla 35/35/55/30/38.8; GeoProp 50/55/60/35/50.0. Real pi0: No-Proprio 45/40/60/25/42.5; Vanilla 40/45/55/35/43.8; GeoProp 55/55/65/40/53.8.
Ablations:
 - Components (15 MetaWorld tasks): Vanilla 61.2; grounding only 64.8; +look-ahead 66.4; +FiLM 66.0; full 68.5.
 - Simpler spatial priors: No-Proprio 59.5; RC-PE (dense relative-coordinate PE) 60.8; Gaussian heatmap channel of projected EE 61.7; GeoProp-Base 64.8.
 - Parameter-matched bigger proprio MLP: +0.5 pp DP, +0.1 pp pi0 -> not capacity.
 - Data scale (pi0 RoboTwin): gain +2.3/+4.0/+2.8 at 25/50/100 demos (Vanilla 46.3/64.0/77.7).
 - Small-object precision tasks (MetaWorld): +22.3 pp avg; Box Close (EE occluded by lid) 48 -> 40 with ResNet.
 - Calibration drift (test-time synthetic extrinsic perturbation): stays above baselines up to 2.5 cm translation / 1.5 deg rotation; depth-axis translation and pitch/yaw rotation hurt most (figure only).
Failure/limitations: needs camera intrinsics+extrinsics; only EE position grounded; single fixed camera; gains invert when EE is occluded or tasks saturated; look-ahead assumes smooth motion. Real: 20 trials/task, absolute success modest (<=65%).
Conflicts: "Vanilla proprio ~= or < no-proprio" in sim echoes copycat / causal-confusion literature (proprio shortcuts) — but in the real world here vanilla proprio helped DP (28.8 -> 38.8), so dropping proprio is not supported on real hardware. Grounding also resembles AimBot/visual reticle overlays.
Relevance: Our scene RealSense can be calibrated to SO-101 base (URDF FK gives EE position), so a GeoProp-style token or at least a heatmap channel is cheap (+2-3% params). BUT our failure mode includes "slightly moved camera": the method depends on extrinsics and degrades beyond ~2.5 cm / 1.5 deg drift — must recalibrate after any camera move, or apply only to wrist cam (fixed relative to EE, calibration trivially stable). DP-ResNet18 real 50-demo regime matches ours.
Decision impact:
 - Q07 observation/proprio: global proprio vector often <= no-proprio in sim (DP-R18 66.8 vs 68.1), real DP 38.8 vs 28.8 (helps); grounded proprio 50.0 — supports keeping proprio but injecting it spatially; weak support for copycat concern — confidence M
 - Q14 robustness (camera shift): projection-based conditioning tolerates <=2.5 cm / 1.5 deg extrinsic error, degrades beyond — weakens calibration-dependent features for our moved-camera failure — confidence M (synthetic drift, sim)
 - Q03/Q11 fusion: localized feature sampling beats heatmap channel (64.8 vs 61.7) — L
 - Q12 model size: adding capacity to proprio encoder gives +0.5 pp only — L
