# W4_HoloBrain0TechnicalReport — HoloBrain-0 Technical Report (2026, Horizon Robotics; arXiv id not in text)
Setup: VLA with multi-view RGB + depth + camera intrinsics/extrinsics ("Spatial Enhancer" → 3D positional embeddings, depth loss), URDF-aware Joint-Graph Attention action expert (20.8M), hybrid relative-joint + per-joint SE(3) actions, diffusion/flow action chunks. Two sizes: HB-GD 0.2B total (GroundingDINO-Tiny, 75M trainable) and HB-QW 1.1B (Qwen2.5-VL-3B with only first LM layer kept). Pretrain 200k steps on multi-embodiment + human data; real: dual-arm Piper, 7 basic tasks × 200 episodes (single multi-task model) + 3 long-horizon tasks (~30 h data/task), ~20 trials/task with fixed pre-defined object poses.
Claim: embodiment priors (camera params, depth, kinematics) + test-driven data collection + SimpleRTC async inference give SOTA; a 0.2B model rivals 3B+ VLAs.
Evidence:
 - Real avg success over 10 tasks: π0 45.39, π0.5 69.16, HB-GD (0.2B) 74.81, HB-QW (1.1B) 77.18 (progress 68.34 / 84.46 / 88.07 / 87.32). Fold clothes π0.5 50 → HB-QW 75; fold box 65 → 95.
 - RoboTwin 2.0 randomized (50 tasks): HB-GD 90.8%, HB-QW 92.3% (stated as above all prior VLAs).
 - LIBERO 97.4% (QW); LIBERO-Plus zero-shot (camera/robot/lang/light/bg/noise/layout): HB-GD 74.0 vs OpenVLA-OFT 69.6, X-VLA 69.7 (per-axis numbers not parseable from text).
Ablations:
 - Co-training 7 basic tasks with diverse "Grasp Anything" data: avg success 72.40 → 75.00; Stack blocks three 46.67→66.67, Place to slot 26.67→33.33, Place empty cup 70→70.
 - SimpleRTC (inpaint previous unexecuted chunk for first d=latency steps, then linear/quad/exp blend over window L) + teacher forcing (replace first N noisy action steps with GT during training): async+SimpleRTC beats synchronous in success and completion time on cloth folding (figure only); TF ratio 5% HURTS, higher ratios help; 25% used by default.
 - No ablation isolating depth / camera-parameter inputs or URDF attention in the text I could find.
Failure/limitations: technical report; ~20 trials/task, fixed evaluation poses; data regime (200 eps/task + large pretraining) far above ours; many design pieces untested individually.
Conflicts: 0.2B ≈ 1.1B (74.8 vs 77.2) supports "small model suffices once pretrained" and contrasts with scaling claims; SimpleRTC is a gradient-free alternative to RTC (Black et al.) and to temporal ensembling (ACT) for chunk boundaries.
Relevance: SimpleRTC is directly applicable to our jerky chunk boundaries with async inference: freeze the first d = latency/Δt steps to the previous chunk's unexecuted actions and blend over L steps; add training-time teacher forcing (≥25% prefix) so the model sees clean prefixes. The recovery-trajectory (2–3 s clips around failure clusters) and proactive lighting/background/object variation in data collection are a concrete Q13 recipe. 0.2B model is plausible on 8 GB.
Decision impact:
 - Q10 latency/smoothness: supports async inference with prefix-inpainting (SimpleRTC) + teacher-forcing training over synchronous chunk execution — M (real cloth folding, figure only).
 - Q12 model size: supports ~0.2B pretrained model ≈ 1.1B (74.8 vs 77.2 real) and > π0.5 3B (69.2) — M (heavy pretraining, 200 eps/task).
 - Q13 data diversity/recovery: supports test-driven short recovery demos + proactive variation of lighting/background/objects; diverse grasp co-training +2.6 pts avg — L.
 - Q04 depth/3D: ~ depth + camera params used as positional priors; not ablated — L.
