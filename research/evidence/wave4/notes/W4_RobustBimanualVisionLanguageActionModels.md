# W4_RobustBimanualVisionLanguageActionModels — Robust Bimanual VLA Models via Embarrassingly Simple Modality Masking (M3) (2026, arXiv 2608.22419)
Setup: VLA-Adapter style query-based VLA (Prismatic, Qwen2.5-0.5B LLM, DINOv2+SigLIP vision, bridge-attention action expert, L1 regression of chunk, proprio as K/V), LoRA r64, 10k steps. RoboTwin 2.0: 10 bimanual tasks, 50 clean demos each, 100 eval scenes; Clean and Clean2Rand (train clean, test randomized background/lighting/distractors/table height). Real: Agilex Cobot, 3 long-horizon tasks (>800 steps), 50 demos each, 48 clean + 24 OOD (novel distractors) trials per task. Cams: egocentric (head) + 2 wrist.
Claim: training-only structured masking — always keep ego view, jointly drop both wrist views, drop language, lightly drop action queries (p=0.1, rescaled) — greatly improves success and robustness.
Evidence:
 - Clean avg: RDT 30.2, pi0 39.5, ACT 25.9, DP 25.5, Adapter 41.0, M3 62.7 (long-horizon 33.7→61.0; Handover Block 27→74).
 - Clean2Rand avg: RDT 8.8, pi0 12.9, ACT 2.9, DP 0.0, Adapter 3.7, M3 15.1 — every method collapses under background/lighting/distractor shift when trained on clean data (50 demos).
 - Real (3 tasks): clean 44.4 → 69.4; OOD distractors 12.5 → 61.1.
 - Transfer to OpenVLA-OFT: 32.2 → 53.5 (clean sim).
Ablations (avg over Place Phone Stand / Place Shoe / Handover Block; Adapter baseline 23.7):
 - Which view to mask: mask ego 37.0; mask one wrist 32.7; mask both wrists jointly 64.0.
 - Query-mask ratio: 0.0 23.7; 0.1 64.0; 0.3 56.0; 0.5 56.7; 0.7 54.0; 0.9 43.7.
 - Components: L only 29.0; V only 34.0; Q only 33.3; V+L 36.7; V+Q 60.3; V+L+Q 64.0.
 - Generic regularizers: token dropout 31.8; modality dropout (unstructured) 24.1; visual augmentation 22.3; region augmentation 23.0.
Failure/limitations: Block Rank Size (relational) ~0 in Clean2Rand for all; OOD robustness still low in sim (15.1%); real evaluation repeated same layouts 3 rounds; mechanism explanation mostly attention visualisation. Note baseline numbers here are very low for 50 demos (ACT 25.9).
Conflicts: Wrist-view dropout contradicts "always use all cams"; complements BFA++ (wrist important only in manipulation phase) and CLAIM that end-to-end fusion learns spurious cross-view correlations. Plain visual augmentation giving ~0 gain (22.3 vs 23.7) contrasts with augmentation-positive papers — here shift is random scene randomization and the bottleneck is fusion, not appearance.
Relevance: HIGH and cheap. Our setup = one scene cam + one wrist cam, ~50-100 demos, SmolVLA-like query/VLM model. Directly testable: during training randomly mask the wrist-cam tokens (keep scene cam), mask language occasionally, dropout a small fraction of action queries/chunk tokens. Zero inference cost. Evidence of large robustness gains to real novel distractors (12.5→61.1).
Decision impact:
 - Q11 cameras: keep scene cam as anchor, jointly mask wrist view during training: 23.7→64.0 (vs mask scene cam 37.0) — supports wrist cam + wrist-dropout — confidence M-H (sim 3-task ablation + real 216 trials).
 - Q14 robustness: real novel-distractor OOD 12.5→61.1 from training-only masking; sim Clean2Rand 3.7→15.1 — confidence M.
 - Q05 augmentation: generic visual/region augmentation gave no gain (22.3/23.0 vs 23.7) while structured modality masking gave +40 — structured input dropout > photometric aug for multi-view fusion — confidence M.
 - Q12/Q03: 0.5B VLA with DINOv2+SigLIP at 50 demos beats pi0/RDT after masking — small pretrained VLA sufficient — confidence L-M.
