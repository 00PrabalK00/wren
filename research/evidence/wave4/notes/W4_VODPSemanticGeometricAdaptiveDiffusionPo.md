# W4_VODPSemanticGeometricAdaptiveDiffusionPo — VO-DP: Semantic-Geometric Adaptive Diffusion Policy for Vision-Only Robotic Manipulation (2025, arXiv 2510.15530)
Setup: Single-view RGB policy: VGGT encoder — DINOv2 patch tokens (semantic) + output of 24th Alternating-Attention block (geometric, 2C-dim) — fused by residual cross-attention (geo query, sem key/value) + FFN, compressed by a 3-block ResNet + adaptive pooling, concatenated with joint state -> DP (DDPM) head, chunk N=8, history T=3 (VO-DP) or T=1 (VO-DP-1). Freeze/fine-tune status of VGGT not stated. Sim: RoboTwin (14 bimanual tasks, D435-like 240x320), 100 demos/task, 100 test scenes x 3; 8xA100 training, 300 epochs. Real: Realman RM65-B + Inspire gripper, ONE RealSense L515 (RGB for VO-DP, point cloud for DP3), 4 tasks, 200 teleop demos/task spread over a 4x4 grid of 3 cm cells; main eval 60 trials/task; robustness tests 20 grid positions each (VO-DP only).
Claim: Features from a 3D-geometry foundation model (VGGT) make a single-RGB diffusion policy match point-cloud DP3 in sim and beat it in the real world.
Evidence:
 - RoboTwin avg: DP 34.8, DP3 64.0, VO-DP (T=3) 63.9, VO-DP-1 (T=1) 64.6. Pick Apple Messy DP 31.0 -> >80; Block Hammer Beat DP 0.7 -> 85.0.
 - Real (Table V, 60 trials each; DP / DP3 / VO-DP-1): small cube pick-place 23.3 / 73.3 / 96.7; big cube 16.7 / 68.3 / 91.7; cover cuboid 3.3 / 75.0 / 93.3; stack cubes 1.7 / 53.3 / 70.0; avg 11.2 / 67.5 / 87.9.
 - Robustness (VO-DP-1 only, 20 trials, small cube task): size (train 3 cm) 3.0 cm 85, 2.5 cm 60, 5.0 cm 50; color (train orange) orange 85, blue 50, green 40, yellow 90; lighting normal 85, random color/intensity switch 80, blinking 85; background covered with white/pink/blue paper 90/80/95 vs 85 original.
Ablations (5 RoboTwin tasks, avg):
 - Semantic only (w/o geo) 71.1; geometric only (w/o sem) 63.9; fused 80.0 (task-dependent: DBPE and BSE better WITHOUT geo).
 - Geo-token downsampling MLP 79.7 vs avg-pool 80.0.
 - History T=3 63.9 vs T=1 64.6 (no benefit from 3-frame history).
 - Demos 20 -> 50 -> 100 (Fig. 4): VO-DP scales more steeply (Pick Apple Messy 3.0 -> 80.0; Block Hammer 4.7 -> 85.0) than DP and DP3 — VO-DP is WORSE at 20 demos on these tasks.
Failure/limitations: authors: VGGT features sparse, generic; VGGT inference relatively slow (no latency given). Critical read: DP baseline real 11.2% with 200 demos is very weak (likely ResNet-from-scratch, no aug?) — inflates the gap; DP3 used a hand-defined crop region; robustness tests lack baseline comparisons, so "robust" is unreferenced; color shift still costs 35-45 pts on distant colors; one camera, fixed viewpoint (no camera-shift test).
Conflicts: Contradicts iDP3/DP3 claim that point clouds are needed for robustness — here a 3D-aware RGB foundation encoder beats real DP3 (67.5 vs 87.9) and DP3 degrades from sim due to depth noise (agrees with Chronos's D435 depth complaint). Agrees with FM-coordination that object-color shift remains a key weakness for RGB features (blue 50, green 40). No-history-benefit (T=1 >= T=3) agrees with copycat/history-harm literature.
Relevance: High for Q03/Q04: our RealSense depth may be less valuable than a strong geometry-aware pretrained RGB encoder; lighting and background robustness looks good with VGGT features (80-95%) — exactly our lighting failure — but novel-colored pumpkin would still be a risk. VGGT (~1.2B params) is heavy for 8 GB inference at 10-30 Hz; would need feature caching/distillation or a smaller DINOv2 + depth-feature alternative. 200 demos used in real (above our 50-100); at 20 demos VO-DP underperformed in sim.
Decision impact:
 - Q03 vision encoder: supports pretrained geometry-aware foundation features (VGGT/DINOv2 fusion) over from-scratch ResNet DP (real 11.2 -> 87.9) — M (60 trials/task, but weak DP baseline)
 - Q04 3D vs RGB: RGB+VGGT features beat real point-cloud DP3 (87.9 vs 67.5); depth noise hurts DP3 in real — M
 - Q14 robustness: lighting switch/blinking 80-85 vs 85 normal; background paper 80-95; novel colors 40-50 vs 85 (no baseline) — L/M
 - Q07 history: T=1 64.6 vs T=3 63.9 — L
 - Q13 data: foundation-feature policy needs >=50-100 demos to shine (PAM 3.0 at 20 demos -> 80 at 100) — L
 - Q10 latency: VGGT slow (authors), not quantified — L (-)
