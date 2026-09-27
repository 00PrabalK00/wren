# W4_MoEACTScalingMultiTaskBimanualManipulati — MoE-ACT: Scaling Multi-Task Bimanual Manipulation with Sparse Task-Conditioned MoE Transformers (2026, arXiv 2603.15265)
Setup: RoboTwin 2.0 Easy, 16 bimanual tasks, 50 demos/task (800 total), one multi-task policy, 50 trials/task; chunk 50; 2xA800. Real: AIRBOT MMK2, 3 RealSense D435i (head + 2 wrist), 2 tasks x 50 demos, 30 trials/task, inference on RTX 3050. MoE-ACT = ACT + sparse MoE FFNs in encoder (sim 64 experts top-4; real 6 experts top-2; router input = proprio + task emb + mean image token) + task FiLM on decoder queries + multi-scale cross-attention; CVAE + L1 kept. 983M total / 195M active params.
Claim: sparse task-routed experts + FiLM task conditioning fix multi-task interference in ACT; beats pi0 with far fewer active params.
Evidence:
 - Sim avg: ACT (84M, task-emb) 44.6; DP (97M) 46.3; RDT (1.23B) 49.0; BAKU (9M) 45.0; pi0 (3.24B) 56.9; MoE-ACT 62.0.
 - Real (30 trials): ACT 43.3/26.7 (avg 35.0); BAKU 56.7/36.7 (46.7); MoE-ACT 66.7/53.3 (60.0) on Handover bottle / Cubes into box.
Ablations (sim avg): full 62.0; w/o multi-scale cross-attn 58.8; w/o FiLM 53.1; w/o both 50.1; dense Scaled ACT 0.9B 48.5 (vs 84M ACT 44.6 → dense scaling gives only +3.9). Experts: 8 → 55.1, 16 → 56.4, 32 → 56.4, 64 → 62.0.
Failure/limitations: small cubes → grasp alignment errors; failures when initial object positions shifted a lot (limited placement diversity in 50 demos). Critical: multi-task only (single-task ACT not reported), sim Easy setting (no appearance shift), 2 real tasks.
Conflicts: Supports FiLM task conditioning (consistent with BAKU/RT-1 style) for language/multi-task; supports "bigger dense model doesn't help in low data" (0.9B dense ACT ≈ 84M ACT). pi0 (3.24B) best baseline in sim, consistent with pretrained VLAs helping multi-task, but small specialized models can surpass it.
Relevance: Low-medium: only matters when we add a second object/instruction. Then FiLM conditioning of the decoder on a task embedding is the cheap high-value piece (+8.9 pts); MoE unnecessary for 2 tasks. Confirms ACT-sized models (~100-200M active) run fine on laptop GPUs (RTX 3050 inference).
Decision impact:
 - Q08 language/multi-task: task-conditioned FiLM in decoder +8.9 pts (53.1→62.0) over token-only conditioning — confidence M (sim 16 tasks x 50 trials).
 - Q12 model size: dense ACT scaled 84M→0.9B only 44.6→48.5; 195M-active MoE beats 3.24B pi0 (62.0 vs 56.9) with 50 demos/task — supports small models in low data — confidence M.
 - Q13 data: failures from insufficient placement diversity at 50 demos/task — confidence L.
