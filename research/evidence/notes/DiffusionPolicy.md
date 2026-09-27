# DiffusionPolicy — Visuomotor Policy Learning via Action Diffusion (2023/24, arXiv 2303.04137)
Setup: 15 tasks / 4 benchmarks (robomimic, Push-T, BlockPush, Kitchen) + real UR5 tasks; CNN (1D temporal U-Net, FiLM obs conditioning) and transformer variants; ResNet-18 from scratch, spatial-softmax pooling, GroupNorm (not BatchNorm — matters with EMA); DDIM 100 train / 10 inference steps → 0.1 s on RTX 3080; receding horizon: obs horizon 2, predict 16, execute 8.
Claim: denoising diffusion over action sequences models multimodal human actions, +46.9% avg over LSTM-GMM, IBC, BET.
Evidence:
 - Multimodality: commits to one mode per rollout; LSTM-GMM/IBC mode-biased, BET mode-switches. Block Push p2 +32%, Kitchen p4 +213%.
 - Real Push-T: DP (CNN, E2E) 95% success, IoU 0.80; T-E2E 80%; LSTM-GMM 20%, IBC 0% (IBC/LSTM get stuck on idle actions).
Ablations:
 - Position (absolute) vs velocity (delta-like) control: DP gains with POSITION control; baselines (BC-RNN, BET) are better with velocity. Position also more latency-robust and less compounding error.
 - Action horizon (executed steps): trade-off consistency vs reactivity; 8 steps optimal at 10 Hz (~0.8 s).
 - Latency: peak performance maintained with up to 4 steps of latency (position control).
 - Vision encoder (robomimic square PH): from scratch R18 0.94 / R34 0.92 / ViT-B 0.22; FROZEN pretrained R18(IN21k) 0.58 / R34 0.40 / CLIP ViT-B 0.70; FINETUNED (10× lower LR) 0.92 / 0.94 / 0.98 (CLIP ViT-B, only 50 epochs).
 - Real Push-T: E2E best; frozen R3M 80% but jittery/stuck; frozen ImageNet poor, abrupt actions.
 - Robust to camera occlusion (3 s hand wave) and object perturbation (re-plans).
Failure/limitations: BC limits with inadequate data; slower inference than single-step policies; DDIM steps needed.
Conflicts: FROZEN pretrained encoders underperform strongly here → contradicts my plan's "frozen DINOv2 + small adapters". Supports "fine-tune pretrained encoder with ~10× lower LR" (CLIP ViT-B best). Caveat: evaluated in-distribution (no lighting/appearance shift) — frozen features may still help OOD robustness (to check: Burns 2023 'What makes PVRs robust', Theia, RoboMP-DINOv2).
Relevance to us: absolute joint position targets + chunk prediction + execute ~0.8 s at 10 Hz is directly our regime; obs history of 2 frames used; GroupNorm matters if EMA used.
Decision impact:
 - vision: frozen encoder — WEAKENED (in-distribution); fine-tune pretrained at low LR — SUPPORTED — H (clear table, but sim + 1 real task).
 - action_space: absolute position targets — SUPPORTED for generative heads — M/H.
 - action_head: generative (diffusion) > GMM/IBC/BET on multimodal human data — SUPPORTED — H.
 - chunking: predict 16, execute ~8 @10 Hz; tolerates ≤4 steps latency — SUPPORTED — H.
