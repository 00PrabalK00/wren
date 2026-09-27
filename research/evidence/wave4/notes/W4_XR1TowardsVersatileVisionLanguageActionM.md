# W4_XR1TowardsVersatileVisionLanguageActionM — XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations (2026, ICML; arXiv id not in text)
Setup: VLA with Unified Vision-Motion Codes (dual-branch VQ-VAE jointly encoding future visual dynamics + action chunks; Ego4D + robot data), 3 stages: UVMC learning → UVMC-guided pretraining on large cross-embodiment XR-D dataset → task post-training. Full model (π0-scale) and XR-1-Light (230M trainable). >14,000 real rollouts, 6 embodiments, 120 tasks, 20 rollouts per task. Few-shot: 15 new tasks × 20 demos on unseen Tien Kung 2.0.
Claim: joint vision-motion discrete latent codes as an auxiliary target improve VLA multi-task learning, cross-embodiment transfer and OOD generalization.
Evidence:
 - Dual-Arm UR-5e 20 tasks: XR-1 > π0.5/π0/RDT/UniVLA/GR00T-N1.5 (e.g., FindTapeBasket 85% vs π0 50%); per-task tables in appendix.
 - OOD (Dual-Arm Franka, π0 vs XR-1): novel rubbish 15→65, novel dustpan 50→60, dynamic distractors 5→55, background 30→55, illumination 15→30, static distractors 10→30.
Ablations (6 DUR tasks, avg success, 20 rollouts each):
 - XR-1-Light 230M: no UVMC stages 42.5 → with UVMC (trained on downstream data) 57.5 (+15).
 - Full XR-1: no Stage 1/2 28.3; UVMC w/o KL/alignment 48.3; motion-only codes 35.0; vision-only codes 50.0; full on downstream data 66.7.
 - Stage-1 pretraining data 1/10/50/100%: 29.2/38.3/53.3/65.0; + full XR-D stage-2: 81.6.
 - Ego4D in UVMC (10% data): 32.5 → 38.3.
 - Few-shot 20 demos/task, unseen robot: XR-1 multi-task beats single-task ACT and DP (figure; readable numbers e.g. 77/57/53/44/35 not attributable reliably).
Failure/limitations: huge data/compute; illumination remains weak (30%). Critical read: interesting that the large full model WITHOUT pretraining (28.3) is worse than the 230M Light model without it (42.5) — capacity hurts when data is only downstream; π0 baseline via JAX; OOD test only vs π0.
Conflicts: vision-only codes (future visual dynamics) help more than motion-only (50.0 vs 35.0) — supports future-prediction auxiliaries (world-model style). Lighting stays hard even for large pretrained VLAs (π0 15%, XR-1 30%) — consistent with ReShoot (no lighting gain) and our SmolVLA observation.
Relevance: we cannot pretrain on XR-D. Transferable lessons: (1) with only downstream data a 230M model beats the big one (42.5 vs 28.3) → small models for 50–100 demos; (2) an auxiliary future-visual-dynamics target helps even on downstream-only data (+15 for Light); (3) lighting robustness must be engineered (data/aug), not expected from pretraining.
Decision impact:
 - Q09 auxiliary objectives: supports joint future-vision + action latent auxiliary (Light 42.5→57.5; vision-only codes 50.0 > motion-only 35.0) — M (20 rollouts × 6 tasks).
 - Q12 model size: without pretraining, 230M Light 42.5% > full large model 28.3% on downstream data only — M.
 - Q14 robustness: illumination change still 15% (π0) / 30% (XR-1); distractors 5→55 — M.
 - Q13 data quantity (pretraining scale): 1%→100% stage-1 data 29.2→65.0 — L for us (no access).
