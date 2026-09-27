# W4_CLASSContrastiveLearningviaActionSequenc — CLASS: Contrastive Learning via Action Sequence Supervision for Robot Manipulation (2025, CoRL 2025; arXiv id not in text)
Setup: Sim: Square (200 human demos), Three-Stack (1000), Aloha-Transfer (100, joint pos), LIBERO-Object (50/task ×10), Push-T (206); single global camera 256×256, crop+noise aug only (no color/rotation aug in main); heterogeneous = dynamic moving camera or random colors per episode. Real: Franka + UMI gripper, ONE RealSense D435 on tripod randomly repositioned each demo, 200 VR-teleop demos/task, 3 tasks, 20 trials/method. ResNet-18 + spatial softmax + GroupNorm; DP-CNN head (DDIM 16 steps), To=1, Tp=16, Ta=12; encoder LR 1e-5 vs head 1e-4. Sim: max success over 10 evals, 3 seeds, 50 scenes.
Claim: pre-training the encoder with a soft supervised-contrastive loss where positives = states whose future 16-step action sequences are DTW-similar yields viewpoint/appearance-invariant features; improves DP especially under heterogeneous visuals.
Evidence (DP, nonparam/param):
 - Square Dyn-Cam: ImageNet-DP 0.09/0.21, Random-init 0.06/0.06, R3M 0.04/0.14, DynaMo 0.07/0.05, CLASS 0.64/0.68. Square Fixed: ImageNet 0.72/0.91, CLASS 0.91/0.95.
 - Three-Stack Dyn-Cam: Random 0.05/0.28, ImageNet 0.07/0.61, R3M 0.02/0.36, TCN 0.12/0.71, CLASS 0.76/0.93.
 - Aloha-Transfer (rotating image): ImageNet 0.09/0.20, CLASS 0.61/0.95. Push-T Rand-Color: Random 0.04/0.16, ImageNet 0.15/0.53, CLASS 0.69/0.70.
 - Averages stated: CLASS 85% (MLP) / 91% (DP) vs best baselines 63% / 77%; heterogeneous-only 76%/85% vs 32%/57%.
 - Real (random camera placement, parametric, final subtask): Two-Stack ImageNet-DP 0.10 vs CLASS-DP 0.60; Mug-Hang 0.00 vs 0.65; Toaster-Load 0.05 vs 0.55 (grasp: 0.30 vs 0.80; 0.05 vs 0.80; 1.00 vs 1.00).
Ablations:
 - Soft vs hard positive weighting: hard degrades significantly (figure only).
 - DTW window: success increases up to T=16 (figure); DTW > L2 distance (figure).
 - Positive quantile: tradeoff, 1–2.5% used (figure).
 - Add wrist camera (Dyn-Cam Square, parametric): BC 21→66%, CLASS 68→90%.
 - Add color jitter aug (Rand-Color Push-T): BC 53→78%, CLASS 72→90%.
 - ImageNet init vs scratch for CLASS: scratch drops everywhere, up to 64% relative drop on Rand-Color Push-T (figure).
 - Data scaling 20–1000 demos Three-Stack: CLASS > BC at all sizes (figure only).
 - Inference: Rep-only 5.5 ms, MLP 7.3 ms, DP 84.4 ms (A40).
Failure/limitations: quadratic DTW precompute; no noisy demos; real failure: proceeds to next subtask without grasp (no memory/closed-loop check); camera outside training placement region → big drop (no extrapolation). Critical read: training data itself contains camera diversity — this is "learning invariance from diverse-viewpoint data," not zero-shot robustness from a fixed camera; ImageNet-DP baseline in real is very weak (0.00–0.10) at 200 demos, partly because only a single third-person camera and no wrist cam.
Conflicts: agrees with multiple papers that wrist cam is the cheapest viewpoint-robustness fix (+45 pts for BC here). Shows R3M < ImageNet init for DP (agrees with results questioning robot-specific pretraining). ImageNet init >> scratch under visual variation, consistent with pretrained-encoder recommendations.
Relevance: our camera may move slightly between sessions — CLASS says BC with ImageNet ResNet cannot absorb camera variation even when present in data (200 demos), but an action-similarity contrastive pretraining on our own demos can. Cheap: ResNet-18, in-domain only, runs on 8 GB. With 50–100 demos DTW positives may be sparse (scaling figure suggests still > BC at 20–50 demos). Also: wrist cam + color jitter are strong baselines to do first.
Decision impact:
 - Q09 auxiliary objectives: supports action-sequence-similarity contrastive (soft InfoNCE) pre-training/aux for visual invariance — M (sim 3 seeds + real 20 trials, but large-demo regime).
 - Q11 cameras: supports adding a wrist camera for viewpoint robustness (BC 21→66% Dyn-Cam) — M (sim only).
 - Q03 vision encoder: supports ImageNet-pretrained over scratch (Dyn-Cam 3-Stack 0.28→0.61; Push-T rand 0.16→0.53) and ImageNet ≥ R3M — M.
 - Q05 augmentation: supports color jitter for appearance shift (BC 53→78%) — M (sim).
 - Q14 robustness: camera-pose variation in training data alone does NOT make BC robust (real ImageNet-DP ≤0.10 final); needs representation objective — M.
