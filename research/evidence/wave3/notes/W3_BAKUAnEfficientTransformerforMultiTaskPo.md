# W3_BAKUAnEfficientTransformerforMultiTaskPo — BAKU: An Efficient Transformer for Multi-Task Policy Learning (2024, arXiv 2406.07539)
Setup: ~10M-param policy: FiLM-conditioned ResNet-18 (LIBERO-provided, shared across views, 1.5M), MLP proprio encoder, pretrained text encoder, minGPT causal transformer trunk (8 layers, 4 heads, hidden 256), MLP action head (+ GMM/BeT/VQ-BeT/diffusion variants); current obs only; action chunk 10 (sim) / 20 (real) with exponential temporal ensembling; 128×128 images. Sim: LIBERO-90 (50 demos/task, 3rd-person + gripper cam + proprio), Meta-World 30 tasks (35 demos, 1 view), DMC 9 tasks (state, 500 demos); 10 rollouts/task. Real: xArm7, 4 cams incl. wrist, EE-pose actions, 30 tasks, 520 VR-teleop demos (avg 17/task, 10–28), recorded at 30 Hz, deployed at 10 Hz + 100 Hz min-jerk low-level controller, 5 trials/task (fixed object positions). Training on 1× RTX A4000: real 200k steps ≈ 6 h.
Claim: a simple, small, multi-task transformer with chunking + temporal smoothing beats MT-ACT and RT-1 in sim and real.
Evidence:
 - Table 1: LIBERO-90 RT-1 0.16 / MT-ACT 0.54 / BAKU 0.90 / BAKU+VQ-BeT 0.90; Meta-World 0.65/0.13/0.79/0.78; DMC 0.66/0.59/0.70/0.70; real 30 tasks (150 runs) 0.37/0.56/0.86/0.91.
 - Table 2 long-horizon: LIBERO-10 MT-ACT 0.68 vs BAKU 0.86; real 5 tasks 0.64 vs 0.84.
Ablations (Table 3, one factor at a time; LIBERO-90 / Meta-World / DMC):
 - Trunk: MLP 0.81/0.78/0.68 vs transformer 0.90/0.79/0.70.
 - Model size (trunk+head): 4.4M 0.85/0.78/0.68; 10M 0.90/0.79/0.70; 31M 0.87/0.81/0.70; 114M 0.19/0.81/0.68 → 114M collapses on LIBERO-90 (suspected overfitting).
 - Action head: MLP 0.90/0.79/0.70; GMM 0.84/0.65/0.67; BeT 0.89/0.78/0.60; VQ-BeT 0.90/0.78/0.70; Diffusion 0.89/0.45/0.61. Real: VQ-BeT 0.91 vs MLP 0.86 (150 trials each).
 - Action chunking: without 0.76/0.78/0.74, with 0.90/0.79/0.70 (+14 pts on LIBERO manipulation; slight harm on locomotion).
 - Observation history: none 0.90/0.79/0.70; history with last-step loss 0.54/0.08/0.37; history with multi-step loss 0.90/0.82/0.68 → history gives no gain, and naive history is catastrophic.
 - Goal modality: text 0.90/0.79; goal image 0.88/0.81; intermediate goal image 0.91/0.80.
 - FiLM on vision encoder: without 0.87/0.79, with 0.90/0.79.
 - Appendix Table 8: separate per-view encoders 0.92 vs shared 0.90 (+15% params per view); separate modality tokens 0.90 vs concatenated vector 0.87.
 - Temporal ensembling + chunking: "important for precise and smooth motion" (qualitative).
Failure/limitations: struggles on precise real tasks (oven door, tea bottle in fridge door: 0–3/5); fixed object positions and fixed robot init in real eval → no robustness evidence; 5 trials per task; ResNet-18 trained from scratch-ish (LIBERO encoder) — no pretrained-encoder comparison; no augmentation study.
Conflicts: MLP (L1/MSE-type) head matching or beating diffusion in sim conflicts with DP paper and with ACT's CVAE ablation on human data; but in REAL human-teleop data the multimodal head (VQ-BeT) wins by 5 pts — consistent with ACT's claim that human data is multimodal. Diffusion head's 0.45 on Meta-World is likely under-tuned (2-layer transformer diffusion head). Model-size collapse at 114M agrees with low-data overfitting concerns (cf. DP-T needing heavy regularization).
Relevance: HIGH. A ~10M model trained ~6 h on an A4000-class GPU with 10–28 demos/task, wrist + scene cams, 10 Hz deployment — very close to our compute/data. Suggests: small transformer with chunking (~2 s at 10 Hz = 20 steps) + temporal ensembling + low-level min-jerk interpolation; current frame only; FiLM for adding a second language-selected object; multimodal head helps on real human data.
Decision impact:
 - Q01 action head: sim MLP ≈ multimodal heads (0.90 vs 0.84–0.90), real human data VQ-BeT 0.91 vs MLP 0.86 — supports a multimodal head for real teleop data, weakens diffusion-for-its-own-sake — confidence M (150 real trials, fixed positions)
 - Q06 chunking: chunk 10 vs 1: 0.90 vs 0.76 on LIBERO-90; real chunk 20 @10 Hz + exponential temporal ensembling — supports chunking + TE — confidence H (consistent with ACT)
 - Q07 history: no history 0.90 = multi-step-loss history 0.90; last-step-loss history 0.54 / 0.08 / 0.37 — supports current-frame-only — confidence H (3 benchmarks)
 - Q08 language: FiLM vision encoder 0.90 vs 0.87 without; text ≈ goal image — supports FiLM text conditioning — confidence M
 - Q10 smoothness: 10 Hz policy + temporal ensembling + 100 Hz minimum-jerk low-level controller yields smooth real motion — supports low-level interpolation between policy steps — confidence L (qualitative)
 - Q12 model size: 4.4M 0.85, 10M 0.90, 31M 0.87, 114M 0.19 on LIBERO-90 — supports ~10–30M policy in low-data; large from-scratch models overfit — confidence M
 - Q11 cameras: shared encoder across views costs only 2 pts vs separate (0.90 vs 0.92) at −15% params/view — supports shared encoder for scene+wrist on 8 GB — confidence L
