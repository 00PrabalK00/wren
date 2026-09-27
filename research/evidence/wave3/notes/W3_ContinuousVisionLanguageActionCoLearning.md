# W3_ContinuousVisionLanguageActionCoLearning — Continuous Vision-Language-Action Co-Learning with Semantic-Physical Alignment for Behavioral Cloning (CCoL) (AAAI 2026, arXiv n/a in text)
Setup: ACT-like CVAE chunk policy + NeuralODE latent proprio dynamics (MCC) + bidirectional language–vision cross-attention (CSA) + latent discontinuity penalty. ViT image encoder (ViT-S 22M / ViT-B 86M in Franka Kitchen), RoBERTa text. Sim: ALOHA MuJoCo (cube transfer, bimanual insertion; scripted and human demos, AWE settings), RLBench 4 tasks (3 seeds), Franka Kitchen (MPI settings). Real: Franka + RealSense D435i, 3 tasks, 50 kinesthetic demos each, 15 trials under shifted conditions. Train 5.3 h RTX 4090; inference 15 ms per chunk.
Claim: continuous latent dynamics + stepwise language anchoring reduce compounding error and jerk vs ACT/AWE/diffusion.
Evidence:
 - ALOHA MuJoCo (success %, cube transfer scripted/human; insertion scripted/human): DP 54/4, 74/0; ACT 86/50, 32/20; AWE 99/71, 57/30; DIC 95.9/78.1, 83.2/30.2; CCoL 99/82, 87/36.
 - RLBench avg: ACT 52.8, AWE 60.3, CCoL 68.0, HDP 66.6, 3DDiff (3D) 78.8, CCoL3D 84.9 — 3D-token variants beat 2D by ~17 pts.
 - Real: no baseline comparison; CCoL e.g. 86.7% on cubes placement (figure only for others).
Ablations (ALOHA, cube scripted/human; insertion scripted/human): full 99/82/87/36; w/o MCC 99/74/72/34; w/o CSA 99/73/74/35; w/o discontinuity penalty 99/78/76/32; CSA replaced by avg pooling 98/72/70/28; TCN encoder w/o MCC 92/58/54/20. Smoothness: vs w/o MCC, velocity fluctuations −30.8%, acceleration fluctuations −32.7%. Coarser ODE solver step (2.0) better/steadier than 0.5.
Failure/limitations: real-world has no baselines; ALOHA sim uses a single task per model with a language string that carries no information (single-task) → "language alignment" gains on ALOHA are really architectural. Human-demo insertion only 36%.
Conflicts: DP extremely weak on human ALOHA data here (0–4%) whereas other papers find DP strong — likely untuned hyperparameters from the AWE protocol; ACT human-data numbers (50/20) consistent with ACT paper order of magnitude.
Relevance: low-moderate. Confirms: on human (multimodal, noisy) sim demos, CVAE-chunk models beat DP-as-configured; latent smoothing losses reduce jerk; 3D tokens add a lot on RLBench.
Decision impact:
 - Q01 action head: CVAE-chunk family (ACT/AWE/CCoL) ≫ DP in ALOHA sim human data (ACT 50 vs DP 4 on cube transfer) — weak support for CVAE chunk head, baseline tuning suspect — confidence L.
 - Q10 smoothness: latent-ODE + discontinuity penalty cuts acceleration fluctuation 32.7% and raises success (insertion scripted 72 → 87) — supports explicit smoothness regularization — confidence L (sim).
 - Q04 3D: RLBench 2D CCoL 68.0 vs CCoL3D 84.9; 3DDiff 78.8 — supports 3D tokens from RGB-D — confidence L-M (sim, multi-view RLBench).
