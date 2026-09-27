# W3_VisuomotorControlinMultiObjectScenesUsin — Visuomotor Control in Multi-Object Scenes Using Object-Aware Representations (2023, arXiv 2205.06333)
Setup: PyBullet planar pushing (cylinder EE, 8 blocks, push target block to a rod), Implicit BC policy, 1k–10k scripted episodes, 200 eval configs x 4 seeds. Frozen self-supervised encoders (Slot Attention K=16, autoencoder, MoCo) trained on same interaction videos; features concatenated to RGB. Real: 1080 human pushing demos, but ONLY offline action-prediction MSE (no real rollouts).
Claim: object-aware (Slot Attention) self-supervised features improve sample efficiency of BC in multi-object scenes over object-agnostic SSL (MoCo, AE) and raw RGB.
Evidence:
 - Object localization PCK (1 block mean): MoCo 61.5, AE 49.0, Slot 95.8; 4 blocks: 22.9 / 21.2 / 95.1; 8 blocks: 16.0 / 13.8 / 51.8 (Slot fails on same-colour blocks, ~15–23).
 - IBC success (mean over 4 seeds) at 1000/2000/3000/10000 episodes: RGB 36.9/78.9/88.8/95.1; RGB+GT segmentation 78.5/93.5/94.8/95.4; AE 46.0/61.3/83.5/85.8; RGB+AE 49.0/76.9/66.5/92.6; Slot 57.1/86.0/92.4/95.0; RGB+Slot 53.3/87.8/92.6/95.0.
 - MoCo features + IBC did not converge (contrastive features focus on the moving arm, miss the goal rod).
 - Real action-prediction MSE (RGB / Slot / Slot+RGB) at 55 demos (0.0625): 2.35/2.07/2.03; 110: 2.01/1.93/1.87; 220: 1.78/1.67/1.64; 440: 1.57/1.55/1.54; 880: 1.41/1.46/1.41.
Ablations: number of slots — performance improves up to K=16, drastic drop at K=20 (figure only). Object prior (Slot) vs same-loss AE: Slot better at every data size.
Failure/limitations: sim-only closed-loop results; real = offline MSE only; needs known approx. number of objects; slot swapping for similar-looking objects; 1000 "low-data" episodes is 10x our regime; gains vanish by 3k–10k episodes.
Conflicts: consistent with VIMA / ToolFlowNet notes that explicit object masks (GT seg: 36.9 -> 78.5 at 1k eps) are a large prior in low data; contrastive (MoCo) features failing matches reports that global-pooled contrastive embeddings lose spatial info needed for control (vs R3M/DINO patch features).
Relevance: low-moderate. Our scene has 1–2 objects (pumpkin, tray), so the multi-object binding issue is small; the transferable signal is that object masks as extra input channels substantially help low-data BC and that global-pooled contrastive encoders are poor for control. No evidence on lighting/camera shift.
Decision impact:
 - Q03 vision encoder: weakens global-pooled contrastive (MoCo) frozen features for control (failed to converge); object-aware dense features help at low data — confidence L (sim pushing).
 - Q14 robustness / inputs: supports adding object segmentation masks (RGB 36.9 -> 78.5 with GT seg at 1k episodes; gain disappears at 10k) — confidence L.
 - Q13 data: benefit of representation priors shrinks with data (all ~95% at 10k eps) — confidence M (4 seeds, 200 evals, but sim).
