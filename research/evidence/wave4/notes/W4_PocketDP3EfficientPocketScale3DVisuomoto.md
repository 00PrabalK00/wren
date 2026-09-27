# W4_PocketDP3EfficientPocketScale3DVisuomoto — PocketDP3: Efficient Pocket-Scale 3D Visuomotor Policy (2026, arXiv 2601.22018)
Setup: DP3 point-cloud encoder (FPS-downsampled points → MLP → max-pool) kept; conditional U-Net decoder (~255M) replaced by MLP-Mixer "DiM" blocks (temporal-MLP + channel-MLP + FiLM gated residual), x0-prediction, DDIM 100 train / 2 inference steps. Tiny 0.53M params (K=4, d=64), Base 1.73M (d=128). Sim: RoboTwin2.0 (50 demos/task, 100 scenes/task), Adroit + MetaWorld (10 demos, 3 seeds, SR5 = mean of top-5 checkpoints). Real: AgileX Piper (6-DoF), single global RealSense D455, 50 leader–follower teleop demos, 6-DoF joint-position actions, inference on RTX 4060, 15 trials/task. Trained on RTX 5880 Ada.
Claim: with a compact 3D representation, a <2M-param decoder matches/exceeds huge U-Net decoders; 2-step sampling suffices without distillation.
Evidence:
 - RoboTwin2.0 avg (tasks in paper): DP 29.2; pi0 36.8; DP3 50.8; PocketDP3-tiny 66.0; PocketDP3-base 71.6.
 - Adroit+MetaWorld avg (10 demos): BCRNN 8.8; IBC 2.0; DP 30.0; DP3 73.0; FlowPolicy 72.6; tiny 72.9; base 77.4.
 - Latency (RTX 5880 Ada, batch 1): DP (100 NFE) 460 ms; DP3 (10 NFE) 51.4 ms; Pocket-base/tiny @10 NFE 16.0/14.9 ms; FlowPolicy (1 NFE, ~255M) 7.04 ms; Pocket-base/tiny @2 NFE 4.80/4.23 ms.
 - Real (15 trials): Place Object DP3 53.3 → 73.3; Adjust Bottle 33.3 → 46.7; Stack Blocks Two 6.7 → 20.0 (avg +15.3).
Ablations:
 - Decoder at equal ~1.7M params (Adroit Door/Hammer/Pen, SR5): DiM 54.3/100/48.7 (avg 67.7); vanilla MLP+FiLM 0/0/0 (did not train, loss 2.3e-2); narrow U-Net 25.7/93.3/42.0 (53.7).
 - NFE (5000 episodes, final ckpt; Door/Hammer/Pen avg): 1 step 53.0; 2 steps 58.2; 5 steps 57.7; 10 steps 58.0.
 - Tiny sometimes beats Base (Turn Switch 59 vs 56) — authors: oversized models can amplify optimization noise.
Failure/limitations: authors: DiM capacity may be insufficient for multi-view/multimodal conditioning; loses pixel-aligned spatial bias for sub-mm precision; why 2 steps work is unexplained. Critical: SR5 top-5-checkpoint metric inflates sim numbers; real absolute SRs low (20–73%), single camera, 15 trials; no robustness (lighting/object) tests.
Conflicts: agrees with iDP3/DP3 notes that point-cloud policies work with ~10–50 demos and with DEM (one/two-step heads fine). Supports "small models fine in low data" (0.5–1.7M decoder beats 255M). Contrasts with DP paper's large U-Net default.
Relevance: very high for our compute: identical real regime (low-cost 6-DoF arm, leader–follower, 50 demos, joint-position actions, RealSense, RTX 4060-class inference). A DP3-style encoder on RealSense point cloud (cropped to workspace) + tiny DiM decoder runs in ~5 ms. However real SR is modest and no generalization tests; wrist cam not used.
Decision impact:
 - Q12 model size: 0.5–1.7M-param decoder ≥ 255M U-Net (RoboTwin 71.6 vs 50.8; real +15 pts) — supports tiny heads — confidence M.
 - Q10 latency: 2-step DDIM, 4–5 ms on desktop GPU; real deploy on RTX 4060 — H for feasibility.
 - Q01 action head: diffusion with x0-pred, 2 NFE ≈ 10 NFE (58.2 vs 58.0), 1 NFE drops (53.0) — M.
 - Q04 3D/depth: single-RealSense point-cloud policy with 50 real demos works on low-cost arm (20–73%) — L/M (no RGB baseline in real).
