# W3_WhatDoWeLearnfromaLargeScaleStudyofPreTr — What Do We Learn from a Large-Scale Study of Pre-Trained Visual Representations in Sim and Real Environments? (2023/24, arXiv 2310.02219, ICRA 2024)
Setup: 5 PVRs (R3M ResNet50 23M, CLIP ViT-B 86M, MVP ViT-L 307M, VC-1 Base ViT-B 86M, VC-1 Large ViT-L 307M); real TriFinger push cube (BC), Franka reach-to-goal-image (30 teleop demos), pick up bottle (30 demos), open drawer (150 demos) with one RealSense D435 RGB (424x240) + proprio, MLP BC policy outputting joint angles; Stretch ImageNav (RL in sim → real). 3 seeds, 10 real eval episodes each; 348 experiments, 110 h of robot time. Aug = 20% color jitter + 8 px random shift.
Claim: sim PVR rankings are predictive of real rankings (SRCC > 0.5 for all variations); augmentation and fine-tuning benefits transfer to real.
Evidence (Table I, frozen, real avg over 5 tasks): R3M 56, CLIP 47, MVP 53, VC-1 Base 69, VC-1 Large 63. Best per task differs (MVP on TriFinger; R3M and VC-1 Base on Franka; VC-1 Large on ImageNav, real 90 vs 20–60).
Ablations (Table IV, real success; Push / Reach / Pick bottle / Open drawer; averages computed by me from the per-task values because the extracted average column is garbled):
 - VC-1 Base frozen, no aug: 37 / 97 / 83 / 67 (≈71)
 - VC-1 Base frozen + aug: 35 / 40 / 83 / 70 (≈57)
 - VC-1 Base fine-tuned, no aug: 37 / 33 / 63 / 53 (≈46.5)
 - VC-1 Base fine-tuned + aug: 37 / 93 / 90 / 73 (≈73.3) ← best overall (authors agree)
 - VC-1 Large: frozen 38/87/43/57 (≈56); frozen+aug 38/37/60/63 (≈49.5); FT 34/57/90/43 (≈56); FT+aug 31/87/50/67 (≈58.8)
 → Fine-tuning WITHOUT augmentation hurt (71→46.5 for Base); fine-tuning WITH augmentation was best; ViT-B beat ViT-L in every configuration with 30–150 demos.
 - Sim-to-real transfer of these policies failed for almost all manipulation tasks (Reach/Pick real 0 across all variants; Table V), except ImageNav.
Failure/limitations: 10 eval episodes x 3 seeds per cell, high variance (e.g., Reach 97→40 with frozen+aug is suspicious); simple MLP single-step BC head; single camera; no OOD (lighting/camera) tests; tasks are easy (reach, pick bottle).
Conflicts: Agrees with CAGE that frozen pretrained ViTs work at ~50 demos, and adds that FT is only safe together with augmentation (matches "fine-tuning overfits in low data" folklore and Octo/OpenVLA fine-tune recipes that use aug). Model size result (Base > Large) agrees with VC-1 paper and with our small-data regime; contrasts with CAGE's use of DINOv2-L (but CAGE uses LoRA, not full FT). No encoder dominates across tasks — conflicts with claims of a single best PVR.
Relevance: For 50–100 SO-101 demos on an 8 GB GPU: prefer a ViT-B-sized (or smaller) pretrained encoder; if fine-tuning it, always use color jitter + random shift; frozen is a safe fallback. Evidence is in-distribution only.
Decision impact:
 - Q03 vision encoder: fine-tune + aug best (VC-1 B ≈73 real avg), full FT without aug worst (≈46.5); frozen is a decent default (≈71) — confidence M (real robot, 3 seeds, but 10 episodes and noisy)
 - Q12 model size: ViT-B (86M) > ViT-L (307M) in all 4 configurations at 30–150 demos (73 vs 59 best-vs-best) — confidence M
 - Q05 augmentation: color jitter + shift needed when fine-tuning the encoder (46.5 → 73) — confidence M
 - Q03 vision encoder: no single PVR best across tasks; CLIP weakest on real manipulation (47 avg) — confidence L-M
