# W3_GLUEGlobalLocalUnifiedEncodingforImitati — GLUE: Global-Local Unified Encoding for Imitation Learning via Key-Patch Tracking (2025, arXiv id not in text)
Setup: Diffusion Policy (CNN U-Net head, single obs, action chunk) conditioned on: learnable CLIP CLS token of full image + cross-attention where global CLIP patch features query CLIP features of 10-20 "key patches" around keypoints. Keypoints: one-time text prompt -> Grounding DINO boxes -> SAM masks -> CLIP/DINO semantic clustering -> keypoints; tracked online with CoTracker3. + 7-D joint state. Sim: MimicGen 8 tasks, 100 demos, 512x512 third-person RGB, 3 seeds, 100 eval configs. Real: Franka, impedance control, SINGLE third-person RealSense (RGB only), SpaceMouse demos at 10 Hz, 50 demos/task, 4 tasks, 20 trials in-dist, 10 trials per OOD condition.
Claim: Fusing tracked object-centric key-patch features with global context makes IL robust to clutter, occlusion and lighting without more data.
Evidence:
 - MimicGen avg (Table I): DP 18.8, DP3 34.4, ACT 34.8, GLUE 52.4 (Stack D1 76.0 vs best 51.3 ACT; StackThree 67.7 vs 25.7; Square 43.0 vs DP3 51.0 — GLUE loses only here; Nut Assembly 12.7).
 - Real in-dist (Table IV, Push/Stack/Place/Fold/avg): DP 20/10/55/60/36.2; ACT 55/50/30/60/48.8; GLUE-S (CLIP global only) 70/55/80/75/70.0; GLUE 80/75/95/90/85.0.
 - Real clutter (Push/Stack/avg): DP 0/0/0; ACT 0/0/0; GLUE-S 50/10/30; GLUE 80/40/60.
 - Real foreground occlusion (Push/Place/avg): DP 0/0/0; ACT 0/0/0; GLUE-S 40/50/45; GLUE 70/70/70.
 - Real illumination (dynamic colored party light; Place/Fold/avg): DP 10/40/25; ACT 10/40/25; GLUE-S 40/60/50; GLUE 70/80/75.
Ablations:
 - Remove local key-patch feature (GLUE-S) in sim: 4 tasks avg 50.0 -> 55.5 with it (Stack 67.4->74.5, StackThree 60.7->67.4, Mug 25.0->29.5, Threading 47.0->50.7).
 - Key-patch count 10/15/20: avg 55.4/57.1/57.4 (stable).
Failure/limitations: Relies on Grounding DINO + SAM + CoTracker at run time (latency/compute not reported); tracking failure under full occlusion not analyzed; 10 trials per OOD condition; baselines DP/ACT use ImageNet ResNet18 at 512x512 with no augmentation stated, so part of GLUE-S's OOD advantage is simply pretrained CLIP vs ResNet (confound). Only one camera (no wrist).
Conflicts: Supports "object-centric / local features improve OOD robustness" (like GloVLA factorization, focus-attention papers). Note GLUE-S (plain learnable CLIP global) already jumps from 0 to 30-50% OOD vs DP/ACT — consistent with papers finding large pretrained encoders more robust than ImageNet ResNet under lighting/clutter, and against claims that scratch/ImageNet ResNet18 is sufficient.
Relevance: Very close regime (single RealSense third-person, 10 Hz, 50 demos, pick-place-into-container "Place Fruit" ~ our pumpkin->tray). Our failure modes (lighting, different pumpkin) match their OOD tests. Practical takeaway: (a) swap ResNet18 for a pretrained CLIP/DINO-class ViT fine-tuned (GLUE-S), (b) optionally add object-centric patches from a text-prompted detector+tracker ("pumpkin", "tray"). Tracker/detector stack adds GPU memory and latency on an 8 GB laptop; CoTracker online is moderately heavy. Wrist cam could provide similar locality more cheaply (not tested).
Decision impact:
 - Q14 robustness: real clutter 0/0 (DP/ACT) vs 60 GLUE; occlusion 0 vs 70; lighting 25 vs 75 — supports object-centric local features + pretrained ViT for OOD — confidence M (10 trials/condition, confounded baselines)
 - Q03 vision encoder: learnable CLIP (GLUE-S) real in-dist 70.0 vs DP-ResNet 36.2 / ACT 48.8; OOD 30-50 vs 0-25 — supports pretrained CLIP-class encoder fine-tuned over ImageNet ResNet — confidence M (not a controlled encoder ablation)
 - Q01 action head: in real, ACT 48.8 > DP 36.2 avg at 50 demos 10 Hz; sim ACT 34.8 ~ DP3 34.4 > DP 18.8 — L
 - Q04 3D: DP3 34.4 ~ ACT 34.8 in MimicGen, beaten by RGB GLUE 52.4 — weakens plain DP3 point clouds — L
