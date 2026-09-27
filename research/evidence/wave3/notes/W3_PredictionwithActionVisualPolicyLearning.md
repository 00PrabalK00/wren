# W3_PredictionwithActionVisualPolicyLearning — Prediction with Action: Visual Policy Learning via Joint Denoising Process (PAD) (2024, arXiv 2411.18179)
Setup: DiT (latent diffusion, SD-VAE latents) jointly denoises k=3 future image latents (interval 4 frames), future depth (real), and k=3 future EEF poses; only first action executed (closed loop, linear-interp planner). CLIP text conditioning. Pretrain 200k steps on BridgeData-v2 videos, then 100k steps adapt; 4×A100, ~3 days. Main model XL/2 661M params. DDIM 75 steps at inference (slow). Sim: MetaWorld 50 tasks, 50 demos/task, single policy, single camera. Real: Panda (SERL setup), WRIST camera only (+depth variant), 200 teleop traj/task, 50 rollouts per task.
Claim: jointly predicting future images and actions in one diffusion process improves multi-task visual policies and generalization; co-training with internet video helps.
Evidence:
 - MetaWorld 50-task avg (Table 1): DP 27.9, RT-1 34.6, SuSIE 41.0, RT-2* 52.2, GR-1 57.4, PAD 72.5.
 - Real in-distribution avg (Table 2, 50 rollouts/task): DP 38, RT-1 43, SuSIE 49, RT-2* 69, PAD 72, PAD-Depth 78.
 - Real unseen objects/backgrounds: +28% over strongest baseline (figure only); baseline "fails on difficult unseen tasks".
Ablations:
 - Remove image prediction (same model, action only): 72.5 → 43.6 on MetaWorld.
 - Remove Bridge video co-training: 72.5 → 59.2.
 - Add depth input + depth prediction (real): 72 → 78.
 - Model/compute (Table 3): B/2 128M 62.4; L/2 449M 68.4; XL/2 661M 72.5; XL/4 (65 tokens) 64.5; XL/8 (17 tokens) 48.2 → success tracks GFLOPs; coarse patches hurt a lot.
Failure/limitations: low control frequency (joint image+action denoising, 75 DDIM steps); single-step execution; heavy compute. Critical read: the DP baseline (27.9 MetaWorld, 38 real) is multi-task with CLIP text, likely not tuned; the "w/o image prediction" ablation keeps a 661M DiT that is then only supervised by a 4–7-D action → overfits, so the gain partly reflects regularizing a huge model rather than a small policy benefiting.
Conflicts: agrees with GR-1, Seer, UVA, LDA-1B (this set) that future prediction aux helps; LDA-1B suggests predicting in DINO feature space instead of VAE latents is better. Model-size trend contradicts "small is enough" only for 50-task multi-task setting.
Relevance: joint image+action diffusion at 661M and 75 DDIM steps is infeasible at our latency target on an 8 GB laptop. Transferable: (1) a future-prediction aux loss regularizes BC with few demos; (2) depth as extra modality +6 pts on real with a WRIST-only camera; (3) B/2 128M still 62.4 on 50 tasks.
Decision impact:
 - Q09 auxiliary objectives: supports joint future-image prediction (43.6 → 72.5 MetaWorld; +internet video co-train 59.2 → 72.5) — confidence M (big effect, but sim + huge model).
 - Q04 depth: adding depth input/prediction on real Panda 72 → 78 (50 rollouts/task) — confidence M.
 - Q12 model size: 128M → 661M: 62.4 → 72.5 multi-task 50 tasks; token count matters more (XL/8 48.2) — confidence L for our single-task regime.
 - Q10 latency: 75-step DDIM joint image denoising → low control rate (authors' limitation) — confidence M (against pixel-space future prediction at inference; use it as training-only aux).
 - Q01 action head: ~ diffusion head; DP baseline weak (27.9) in multi-task — confidence L.
