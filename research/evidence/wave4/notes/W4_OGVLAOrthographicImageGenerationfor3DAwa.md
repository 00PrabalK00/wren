# W4_OGVLAOrthographicImageGenerationfor3DAwa — OG-VLA: Orthographic Image Generation for 3D-Aware Vision-Language Action Model (2025, arXiv 2506.01196)
Setup: Keyframe policy (motion planner between keyframes). Input: one or more posed RGB-D views → point cloud → rendered into canonical orthographic views → vision backbone + LLM + image diffusion generator that draws the next EE position/orientation as image annotations. Sim: ARNOLD (8 tasks, ~500 demos/task, 2 keyframes/demo, SE(3) aug ×10; 20 episodes × 3 runs per split), COLOSSEUM (100 demos/task, all-perturbation test). Real: Franka, single front-facing RGB-D camera, 4 tasks, 3–5 demos each (22 total) with human-annotated keyframes, fine-tuned from ARNOLD checkpoint, 10 episodes per split. Per-step latency 4.5 s.
Claim: canonical orthographic re-rendering of unprojected RGB-D gives camera-view invariance, and VLM/diffusion priors give object/scene generalization with few demos.
Evidence:
 - ARNOLD overall (Novel Pose / Object / Scene / State): PerAct 34.0 / 16.7 / 21.0 / 6.5; OG-VLA@30k 31.2 / 21.7 / 20.8 / 8.5; OG-VLA@100k 37.7 / 24.8 / 28.8 / 10.0.
 - vs VLAs, ARNOLD Pickup Object (Pose/Object/Scene/State): pi0-FAST LoRA 25/25/20/10; pi0-FAST full 35/50/35/30; pi0.5 full 0/5/0/0; OG-VLA LoRA 95/90/80/0.
 - COLOSSEUM all-perturbation avg: R3M 0.6, MVP 0.8, 3DDA 5.3, RVT 6.4, PerAct 7.2, OG-VLA 10.5.
 - Real (10 episodes): Pickup 100 / novel obj 80 / novel scene (distractors, lighting, background, table) 90; Put in drawer 90/70/80; Open drawer 60/30/50; Close drawer 90/50/90. pi0-FAST full FT with joint actions on same 3–5 demos: failed all tasks (only reached block 30%).
 - Latency: OG-VLA 4.5 s/step × 2 steps = 10.2 s episode; pi0.5 0.2 s × 80 steps = 70.3 s.
Ablations (ARNOLD @30k): faded-reconstruction generation 23.8 vs no-reconstruction 12.8 vs full reconstruction 20.8 (novel scene); tiling ortho views 24.8 vs 31.2 untiled; no LLM 20.0 vs 31.2; instruction bypassing LLM −9.5; text-action or action-token heads "failed to learn".
Failure/limitations: keyframe + motion planner (not closed-loop), occlusions, slow per-step, long-horizon error accumulation (COLOSSEUM 10.5% absolute). pi0.5 at 0% in ARNOLD is suspicious (authors blame action-frequency mismatch). Real eval 10 trials, 3–5 demos.
Conflicts: consistent with 3D-keyframe literature (PerAct/RVT) on few-shot efficiency and with Lan-o3dp/GSL on 3D representations aiding camera/scene robustness; contrasts with continuous-control VLAs that need 50+ demos.
Relevance: paradigm mismatch (keyframes + planner, calibrated RGB-D) with our joint-space continuous teleop BC. Useful signals: (1) re-projecting the RealSense point cloud into a canonical (robot-base) frame gives camera-pose invariance; (2) SE(3) augmentation is possible only with a 3D representation — this is why 3–5 demos suffice; (3) pi0-class VLAs failed with 3–5 real demos.
Decision impact:
 - Q04 3D/depth: canonical 3D re-rendering + SE(3) aug enables 3–5 demo real learning with novel-scene robustness (80–90%) where pi0-FAST fails — confidence L/M (keyframe paradigm, 10 trials).
 - Q14 robustness: novel scene (lighting+background+distractors) 50–90% real; COLOSSEUM all-perturbation still only 10.5% — L.
 - Q11 cameras: canonical orthographic views from a single camera give view invariance (claimed; no explicit camera-shift numbers in main text) — L.
