# BAKU — An Efficient Transformer for Multi-Task Policy Learning (2024, arXiv 2406.07539)
Setup: sim LIBERO-90 (50 demos/task, 128×128, 3rd-person + wrist), Meta-World (35 demos), DMC; real xArm7 kitchen 30 tasks, 520 demos total (~17/task), 4 cams incl. gripper cam, 128×128, EE-pose actions, collected at 30 Hz, deployed at 10 Hz. Model ~10M params total (encoders 2.1M, transformer trunk 6.5M, head 1.4M); FiLM-conditioned ResNet-18 (LIBERO's), shared across cameras; 6-layer MiniLM text encoder (pretrained); MLP head predicting a concatenated action chunk (10 steps) + temporal smoothing; current obs only.
Claim: simple modular transformer (encoders → trunk → head) beats RT-1/MT-ACT by 18% sim (36% LIBERO), 86% real (91% with VQ-BeT head) vs strongest baseline 56%.
Ablations (one factor at a time, Table 3 + text):
 - Trunk: transformer > MLP (−9% LIBERO-90 with MLP).
 - Model size 4.4M / 10M / 31M ≈ same; 114M SEVERELY underperforms on LIBERO-90 (overfitting suspected).
 - Action head: in sim MLP ≥ GMM, BeT, VQ-BeT, diffusion; on REAL robot VQ-BeT head 91% vs MLP 86% (+5%) — multimodal head helps with real human data.
 - Chunking: LIBERO-90 −14% without it; Meta-World no change; DMC locomotion +4% without.
 - Observation history: last-step-loss history degrades a lot; multi-step loss recovers (+47%) but still NO gain over no-history → use current obs only.
 - Goal modality text vs goal image vs intermediate image ≈ same.
 - FiLM on vision encoder ≥ unconditioned.
Failure/limitations: struggled on precise real tasks (oven door, bottle in fridge) — data sharing across tasks of varied difficulty may hurt precise skills. Real eval used FIXED object positions (5 runs/task) → weak test of spatial/appearance generalization.
Conflicts: plain MLP head fine in sim but loses on real human data (agrees with ACT CVAE ablation: real/human data needs multimodal head). Model-size result argues against my ~100M plan at ~50–100 demos.
Relevance: closest published analog to our data regime (tens of demos/task, wrist + scene cams, 10 Hz deploy). Tiny models (≈10–30M trainable) suffice; transformer trunk; FiLM for language; no history.
Decision impact:
 - model_size: ~10–30M trainable, avoid ≥100M from scratch — SUPPORTED — M/H (sim ablation).
 - action_head: multimodal (VQ/latent/flow) over plain MLP for real human data — SUPPORTED — M (one real comparison, +5%).
 - history: current obs only — SUPPORTED — M.
 - language: FiLM-conditioned vision — SUPPORTED — M.
 - chunking: yes for manipulation — SUPPORTED — H.
