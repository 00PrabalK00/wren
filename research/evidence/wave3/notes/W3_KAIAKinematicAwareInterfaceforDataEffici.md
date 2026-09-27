# W3_KAIAKinematicAwareInterfaceforDataEffici — KAI: A Kinematic-Aware Interface for Data-Efficient Articulated Object Manipulation (2025/26, arXiv id not in text)
Setup: Sim: Isaac Sim, 6 articulated tasks (open/close laptop, door, drawer), 800 scripted demos/task with randomized object pose, background, lighting; eval 200 trials/task on unseen seeds, 8 unseen backgrounds/lighting. Real: Franka FR3 + Robotiq, 2x RealSense D455 (wrist + base) RGB-D, 3 tasks, 100 demos/task in ONE clean setting; eval 5 initial states x 3 trials per setting (15 trials/task/setting). Model: DINOv2-base 2D features lifted to 3D + point cloud (1024 pts, FPS) ResNet14 encoder, 24-layer GPT-2 (hidden 384), 304M params (77M trainable), trained 8 h on 32x RTX 4090. Inference on RTX 4080S. Control rate not stated.
Claim: an explicit intermediate prediction (keypoint on moving part + future displacement trajectory) as auxiliary readout, before action tokens, improves sample efficiency and robustness to backgrounds/distractors.
Evidence:
 - Sim Table 1 (800 demos, unseen bg/lighting), avg SR: ACT 58.5, Seer 73.4, DP3 37.3, RISE-2 22.3, ArticuBot 38.5, Ours 82.9, Ours+video 84.6.
 - Seen bg/lighting (Table 8, 3 tasks): ACT 52.5, Seer 78.8, Ours 90.6.
 - Data scaling (Table 6, avg SR at 100/200/400/800 demos): DP3 20.1/13.0/24.3/37.3; Seer 20.2/46.5/60.4/73.4; Ours 42.4/62.6/75.9/82.9; Ours+video 47.6/61.7/76.1/84.6.
 - Real (Table 4, SR avg over 3 tasks, None/Background/Object distractor): DP3 33.3/28.9/24.4; Seer 37.8/26.7/31.1; Ours 66.7/62.2/62.2; Ours+video 73.3/73.3/75.6.
 - Real unseen laptop instance: DP3 46.7, Seer 46.7, Ours 66.7, +video 80.0 (15 trials).
Ablations:
 - Remove KAI (same backbone, action only): 44.1 -> +KAI tokens 75.0 -> +geometric consistency loss 82.9 -> +HOI4D video co-train 84.6 (sim, 800 demos).
 - Replace KAI with future-depth prediction aux (same 3D arch): 49.6 vs 82.9 -> generic visual future prediction is a much weaker aux than task-structured kinematic prediction.
 - DP3 + DINOv2 encoder (same as theirs): 17.7 -> stronger encoder alone does not fix it.
 - Bidirectional instead of causal attention KAI->action: 78.5 vs 82.9.
 - Video co-training: +1.7 sim, +6.6/+11.1/+13.4 real (None/Bg/Obj) — grows with visual distraction.
Failure/limitations: articulated objects only, short horizon, single robot. Real eval is 15 trials per cell (+-~13 pts SE), so real gaps of <15 pts are noise; large gaps (33 vs 67) hold. Uses 32 GPUs; 304M model — not laptop-trainable as described. KAI labels require part bounding boxes / keypoint annotations. DP3 surprisingly weak everywhere (only 37% sim), suggests baseline tuning issues.
Conflicts: DP3 (point cloud) weaker than 2D Seer/ACT here, contradicting DP3/iDP3 claims of 3D superiority — tasks here have randomized lighting/backgrounds and D455 noise; point-cloud-only baseline with FPS 1024 points loses the handle. Future-depth aux underperforms, consistent with the view that generic reconstruction aux helps less than task-structured aux.
Relevance: For pumpkin pick-place the analog of KAI is predicting the object keypoint/grasp point and its future trajectory (object-centric aux). Their clean-single-scene -> cluttered real transfer holding at 62% (vs 67% clean) is encouraging for aux object-localization heads under background shift. Not a drop-in for an 8 GB GPU at 304M, but the aux-head idea is cheap.
Decision impact:
 - Q09 auxiliary objectives: supports object-centric keypoint/trajectory aux head over generic future-depth prediction — M (sim ablation 44->83, depth-aux 49.6; articulated tasks only)
 - Q14 robustness: supports structured object-localization aux for background/distractor robustness — L/M (real 15 trials/cell, 62 vs 27-31 for baselines)
 - Q04 3D: weakens point-cloud-only DP3 (37.3 sim, 24-33 real) vs fused RGB(DINOv2)+3D — L (baseline tuning unclear)
 - Q13 data: aux structure halves demos needed at 100-800 demos (42 vs 20 at 100) — M (sim scripted)
