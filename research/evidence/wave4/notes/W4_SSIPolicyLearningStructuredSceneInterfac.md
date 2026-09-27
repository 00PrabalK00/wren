# W4_SSIPolicyLearningStructuredSceneInterfac — SSI-Policy: Learning Structured Scene Interfaces for Vision-Language Robotic Manipulation (2026, arXiv 2606.26800)
Setup: Perception composer (per-frame, action-free trainable): monocular depth FEATURES (intermediate maps of a depth model), language-grounded layout maps (GroundingDINO boxes), and instruction-conditioned 2D point trajectories (ATM-style track predictor). Fused with raw RGB + proprio into a Diffusion Policy U-Net (8x8 spatial grids, 128-d tokens). Aug: color jitter + random shift + box augmentations (translate/scale/delete/insert). LIBERO: 10 demos/task (tracker pretrained on all 50 videos, RGB+language only), 3 seeds x 20 rollouts/task, 100 denoising steps. Real: ARX-5 6-DoF arm, side-view + wrist RGB, ROS at 10 Hz, absolute joint + gripper actions, 16 denoising steps on RTX 4090; 13 tasks, 50 demos/task (10 for human-transfer tasks + 100 human-hand videos), 20 rollouts/task.
Claim: An RGB-only structured intermediate representation (mono depth + object layout + predicted motion tracks) makes few-demo policies much stronger than raw-RGB diffusion policy.
Evidence:
 - LIBERO 10 demos (Table I avg): R3M-ft 29.13, VPT 16.13, UniPi 36.67, Diffusion Policy 54.50, ATM 63.42, ATM-DP 65.67, MaIL 62.15, SSI 80.42 (Spatial 83.5, Object 95.0, Goal 82.5, Long 60.67).
 - LIBERO 50 demos: SSI 91.25 avg (2nd among no-external-data, 0.65 behind OFT).
 - Real spatial reasoning (Table III, 20 rollouts, same encoders/arch, DP vs SSI): directional lemon placements 55/85, 40/80, 55/100, 10/85; tissue disambiguation 50/60, 50/70; avg 43.3 vs 80.0.
 - Real challenging tasks (Table V; single-task DP vs multi-task SSI): sponge->plate 10/65, carrot->basket 30/75, block->drawer+close 25/40, banana->basket 45/50, wipe+place 35/40; avg 29 vs 54.
 - Human-hand transfer (Table IV; human / robot / human+robot SSI pretraining): pot->stove 45/60/70; broom sweep 40/70/80.
 - Cross-robot (sim, Fig. 5): tracker trained on other arms' videos + 10 target videos 83.0 vs full-shot 83.5.
Ablations (LIBERO 10 demos, avg; Long in parentheses):
 - Depth only (DepthHelps) 63.15 (36.4); motion only ATM 63.42 (39.3); ATM-DP 65.67 (44.0); motion+depth 76.92 (57.7); motion+layout 77.09 (54.2); full 80.42 (60.7).
 - w/o hybrid sampling 78.46.
 - SSI + proprio only (no raw RGB to policy): 79.3 vs 80.4 (SSI carries ~98% of the information).
Failure/limitations: authors: GroundingDINO misses under clutter/occlusion corrupt layout; deformable/bulky objects cause grasp failures; temporal inconsistency of mono depth/detections gives jittery predictions. Critical read: many LIBERO baselines are copied numbers; real DP baselines are single-task vs SSI multi-task (mixed confound, arguably favoring DP); 20 rollouts/task; no lighting/camera-shift tests; inference cost of three perception modules + 100-step diffusion not reported (real uses 16 steps at 10 Hz on a 4090).
Conflicts: Consistent with "structured / object-centric intermediate interfaces help low-data policies" (ARRO, FM-coordination). Monocular depth features as input help (+ on Spatial), echoing FM-coordination L1; contrasts with 3D point-cloud papers in that no depth SENSOR is needed. Motion-track prediction (ATM) as an interface agrees with GeoPredict/Masquerade that predicting future point/keypoint motion is valuable in few-data regimes.
Relevance: Moderately relevant: our regime (50-100 demos, side + wrist cam, absolute joints at 10 Hz) matches their real setup closely. Takeaway: adding object layout (GroundingDINO box map for pumpkin/tray) and depth features as extra input channels to a DP-style policy gave large gains over raw RGB on placement/spatial tasks. Heavy pipeline for 8 GB (depth model + DINO + track transformer + DP) — latency likely the binding constraint. Language: grounding boxes from the instruction provide a cheap route for "second object with language".
Decision impact:
 - Q04 depth/3D: monocular depth features + motion tracks complementary (63.4 -> 76.9 avg, Long 39 -> 58) without depth sensor — M (LIBERO 3 seeds; real only via full system)
 - Q13 data: structured interface at 10 demos beats raw-RGB DP at 10 demos (80.4 vs 54.5) and approaches 50-demo methods — M
 - Q08 language: language-grounded layout maps (GroundingDINO) + instruction-conditioned tracks for multi-task; motion+layout Goal 81.5 — L/M
 - Q14 robustness: real challenging tasks with distractors/large pose variation DP 29 vs SSI 54 (20 rollouts) — L
 - Q10 latency: multiple perception modules; latency not reported — L (-)
