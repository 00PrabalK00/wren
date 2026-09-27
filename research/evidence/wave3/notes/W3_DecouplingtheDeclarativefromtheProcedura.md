# W3_DecouplingtheDeclarativefromtheProcedura — Decoupling the Declarative from the Procedural in Vision-Language-Action Models (w2VLA) (2026, arXiv id not in text)
Setup: REAL SO-101 leader/follower + LeRobot, single top-down ZED2i (left RGB only, no depth), center-crop 256x256; 4 scenarios x 2 (skill, object) pairs, 16 demos per pair (32 per scenario); eval 6 rollouts per (skill, object) combination with varied poses; granular 3-point score (right object / right skill / task complete). w2VLA: frozen MetaCLIP2 ViT-L/16 two-tower VLM + frozen VFM; 55.17M trainable; FiLM-conditioned causal transformer over 8-step proprio history; 4-layer MLP head, L1 loss, joint targets, execution horizon 10; trained 15k steps bs 32 on one RTX 4090. Baselines: OTTER (frozen VLM, 67M trainable), pi0.5 (frozen PaliGemma, 693M trainable action expert, chunk 50).
Claim: sequentially modulating proprio tokens with a "where" (text-image localization heatmap from frozen CLIP) then a "what" (skill) signal, plus 50% VFM patch dropout, decouples object identity from skill and allows zero-shot skill transfer to other/unseen objects.
Evidence (Table 1, avg score %): Seen pairs: OTTER 93.8, pi0.5 95.8, w2VLA 95.1 (all comparable). Skill transfer: OTTER 30.6, pi0.5 38.2, w2VLA 91.7. Baselines pick the right object but execute the skill paired with that object in training (spurious skill-object correlation).
 - Robustness: +3-5 unseen distractors -> w2VLA drops 16.6 (seen) / 13.9 (transfer) pts; object-interaction rate 100 -> 66.7%; failures were imprecise grasps (picking mid-air), not wrong object — CLIP heatmaps stayed precise.
 - Unseen objects (cans, toothpaste, fruit): score -8.3 pts; task completion -16.7 due to geometry differences.
Ablations (Scenario 2, seen / transfer %):
 - Heatmap-only (no visual modulation): 66.7 / 52.8 -> imprecise manipulation.
 - + VFM visual modulation: 100 / 58.3 -> precise but spurious skill-object correlation.
 - + 50% random VFM patch masking: 100 / 94.4.
 - Module order where->what 100/94.4 vs what->where 100/55.6.
Failure/limitations: very small eval (6 rollouts per combination), simple primitive skills, minimal pose variation; objects of similar geometry; no lighting/camera shift tests; 16 demos per pair.
Conflicts: pi0.5 (frozen VLM, action expert tuned) matches in-distribution but fails compositional transfer — consistent with the view that big pretrained VLAs overfit spurious correlations in low-data fine-tuning. Heavy patch dropout on dense visual features as a regularizer is an unusual but strong result (58 -> 94 on transfer).
Relevance: HIGH — same robot (SO-101), same regime (tens of demos per task, LeRobot, single consumer GPU, 55M trainable params). Directly relevant to our planned "second object with language": a frozen CLIP text-image localization heatmap as a FiLM "where" signal gives language-grounded object selection and robustness to distractors/unseen objects. In-domain results show small models (55M trainable over frozen encoders) match pi0.5 on SO-101.
Decision impact:
 - Q08 language conditioning: supports FiLM conditioning on frozen text-image localization heatmap (where) + separate skill signal over token-concat; transfer 91.7 vs 30.6-38.2 — M (real SO-101, but 6 rollouts/combination)
 - Q03 vision encoder: supports frozen pretrained VLM/VFM backbones (MetaCLIP2) with small trainable head in low-data — M
 - Q05 augmentation: supports 50% random patch masking of visual tokens to kill spurious correlations (transfer 58.3 -> 94.4) — L/M (one scenario)
 - Q12 model size: 55M trainable matches pi0.5 (693M trainable) in-domain on SO-101 (95.1 vs 95.8) — M
 - Q14 robustness: distractors cost ~14-17 pts, unseen objects ~8 pts with CLIP localization — L/M
