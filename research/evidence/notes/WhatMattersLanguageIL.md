# WhatMattersLanguageIL — What Matters in Language Conditioned Robotic Imitation Learning over Unstructured Data (HULC) (2022, arXiv 2204.06252)
Setup: sim only, CALVIN benchmark (Franka Panda, 34 subtasks, 7-DoF actions), static + gripper RGB cameras; ~6 h of teleoperated undirected PLAY data per environment, only 1% language-annotated (rest trained with goal-image relabeling). Eval: 1000 chains of up to 5 instructions; ablations on env D, 3 seeds. Model 47.1M trainable params (MCIL-style conv encoders, 2-block multimodal transformer posterior, categorical latent plan 32×32, discretized logistic mixture action head + gripper CE). Language encoder frozen: paraphrase-MiniLM-L3-v2 (384-d sentence embedding). Aug: random shift 0–4 px gripper, 0–10 px static.
Claim: hierarchical global latent plan (static cam) + local policy in gripper frame with delta actions, discrete latents, contrastive video-language alignment, and a sentence-similarity language encoder give SOTA on CALVIN.
Evidence (Fig. 3 table, env D, 5-chain success / avg. seq. length; everything else fixed = full HULC):
 - Full HULC: 1-task 82.7%, 5-chain 28.3%, avg len 2.64. MCIL (absolute actions): 34.4%, 0.08%, 0.41. MCIL + delta actions: 76.4%, 9.3%, 1.82. GCBC + delta: 64.7%, 1.3%, 1.11.
 - Multi-env A,B,C,D→D: 88.9% / 38.3% / 3.06 (more data → better). Zero-shot A,B,C→D (unseen env): 41.8% / 1.1% / 0.67 — generalization to a new scene is very poor.
Ablations (avg len; 5-chain %):
 - Language encoder (frozen): MiniLM-L3 SBERT 2.64 > Distilroberta-SBERT 2.50 > CLIP text+ResNet50 2.42 > MPNet-SBERT 2.24 > Distilroberta (MLM) 2.21 > BERT 2.03 > MPNet (MLM) 1.92. Sentence-similarity fine-tuned encoders beat raw MLM encoders; bigger (768-d) not better than tiny 384-d MiniLM.
 - Vision-language alignment loss: none 2.29 (21.8%); MIA matching 2.29; regression (BC-Z style) 2.45; CLIP-style contrastive 2.64 (28.3%) → auxiliary alignment helps +0.35 avg len.
 - No image augmentation (random shift): 2.64 → 1.99 (5-chain 28.3 → 15.4%) — largest single ablation among HULC components.
 - Adding 7-DoF proprioceptive input: 2.64 → 2.20 (5-chain 18.1%); authors attribute to causal confusion — agent relies on initial robot pose instead of language.
 - No local (gripper-frame) policy: 2.24; no transformer posterior (GRU): 2.45 (and 106M vs 5.9M params in posterior); continuous Gaussian latent instead of discrete: 2.39; no KL balancing 2.33; KL β 0.1 (over-regularized, ignores plans): 2.10; gripper as mixture instead of log loss: 2.45.
 - Delta vs absolute actions (MCIL): 0.41 → 1.82.
Failure/limitations: sim only; play data (hours), not 50–100 task demos; the huge gap on unseen environment (0.67) shows language grounding doesn't transfer across scenes; small differences (e.g. 2.45 vs 2.64) across only 3 seeds; language model not fine-tuned.
Conflicts: agrees with BAKU (FiLM/MiniLM text encoder sufficient; goal modality matters little in single-scene multi-task) and RT-1 (USE embedding + FiLM). Proprio hurting agrees with robomimic's "extra proprio overfits", but disagrees with ACT/DP which use proprio successfully — the difference: CALVIN resets to a neutral pose and task must be inferred from language, so proprio→task shortcut is harmful there; in single-task pick-place proprio is not a task cue. CLIP encoder ~ equal (sim domain gap).
Relevance: For a 2-object SO-101 "which object" instruction, the grounding problem is exactly CALVIN's colored-block problem: instructions differ by one word. Use a small frozen sentence-embedding encoder (MiniLM-class, 384-d) + FiLM/token conditioning; consider a contrastive/alignment aux loss only if the policy ignores the instruction. Keep random-shift aug. Delta actions (gripper/relative) strongly help in this regime. Note HULC doesn't test low-demo regime.
Decision impact:
 - Q08 language: supports small frozen sentence-similarity encoder (MiniLM-L3 SBERT) over BERT/MPNet/CLIP-text — confidence M (sim, 3 seeds, but consistent ordering).
 - Q08 language: supports a contrastive vision-language alignment aux loss when instructions differ by a word (avg len 2.29→2.64) — confidence L/M.
 - Q09 aux objectives: supports CLIP-style contrastive alignment as a cheap aux loss — confidence L (language-grounding specific).
 - Q05 augmentation: supports random shift (1.99→2.64; 5-chain 15.4→28.3%) — confidence M/H.
 - Q02 action space: supports delta/relative actions (MCIL 0.41→1.82 avg len) — confidence M.
 - proprio / Q07-style causal confusion: weakens feeding proprio when it can shortcut task identity (2.64→2.20) — confidence M.
 - Q14 generalization: unseen environment 0.67 vs 3.06 seen — language policies trained on few scenes do not transfer — confidence M.
