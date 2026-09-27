# W3_FurnitureVLALearningLongHorizonBimanualF — FurnitureVLA: Learning Long-Horizon Bimanual Furniture Assembly with Vision-Language-Action Model (2026, arXiv 2607.01212)
Setup: two Kinova Gen3 7-DoF arms; cameras: front D435, rear D435, wrists; green screen. Sim (IsaacGym/FurnitureBench): 3 IKEA items (LACK 650 steps, KALLAX 850, IVAR 1550 steps ~155 s at ~10 Hz), 500 motion-planned demos/furniture, one multi-furniture model, 100 rollouts each. Real: IVAR chair, 100 VR-teleop demos, 15 rollouts. Model: pi0.5 fine-tuned (flow matching, chunk H=50, absolute EE pose actions 14-D + progress scalar), 40k steps on 8x L40S, inference on 1 L40S. Parts randomized only within 3 cm / 5 deg.
Claim: fine-tuning pi0.5 on language-grounded subtasks with a jointly predicted continuous progress signal (auto subtask switching; boundaries at post-retreat states) fixes long-horizon drift; temporal ensembling, execution horizon, rear camera and resolution matter for precision.
Evidence:
 - Table I (sim success) LACK/KALLAX/IVAR/avg: pi0.5 zero-shot 0/0/0/0; pi0.5 monolithic FT 0.91/0.11/0.41/0.48; FurnitureVLA 0.98/0.85/0.56/0.80.
 - Real IVAR (15 rollouts): full-assembly SR after S1..S7 = 0.80, 0.73, 0.60, 0.53, 0.47, 0.47, 0.40; per-subtask (reset to intermediate state) 0.80, 0.80, 0.73, 0.80, 0.67, 0.87, 0.80. Failures accumulate rather than one catastrophic subtask; S3-S4 hurt by left arm far from camera (low visual detail).
Ablations (sim, Table II, avg LACK/KALLAX/IVAR; default = lambda -0.1, full cameras, 448 px):
 - Temporal ensembling (weights exp(lambda*i)): none 0.65 (0.76/0.83/0.36); lambda -0.25 0.75; -0.1 0.80 (best, ~70% weight on newest chunk); 0.0 (uniform) 0.62; +0.1 0.77; +0.25 0.75.
 - Execution horizon of the 50-step chunk: 5 steps 0.60 (0.92/0.43/0.44); 10 steps 0.74 (0.98/0.67/0.56); 25 steps 0.67 (0.75/0.85/0.41) — best horizon is task dependent (heavy KALLAX parts favor 25).
 - Viewpoint: front+rear+wrist 0.80; rear replaced by front-view depth 0.50 (0.69/0.45/0.48); without rear 0.47 (0.45/0.57/0.34).
 - Resolution: 224 px 0.60; 300 px 0.72; 448 px 0.80.
 - Demo count (Table III): 25% (125 demos) 0.50; 50% 0.68; 100% (500) 0.80. Discrete (per-subtask constant) progress 0.00 everywhere (model never advances).
Failure/limitations: authors: fixed base; magnets instead of screws. Critical read: 3.3B VLA on 8x L40S — irrelevant compute for us; real eval 15 rollouts, one task; tiny initial randomization (3 cm/5 deg); depth ablation replaces the rear RGB camera with front depth, so it mostly measures losing the rear view (depth ~= no rear camera), not depth vs RGB fairly; TE lambda=0 vs 0.1 non-monotonic (0.62 vs 0.77) suggests noise of several points.
Conflicts: agrees with ACT (temporal ensembling helps) but finds UNIFORM averaging worse than no ensembling on average (0.62 vs 0.65) — recency-weighted ensembling is what helps; pi0 papers argue against TE for dynamic tasks; our data is a slow pick-place, so moderate recency weighting is consistent. Execution horizon sweet spot (10 of 50) matches Diffusion Policy/Bidirectional decoding reports of intermediate horizons.
Relevance: medium. Directly usable: recency-weighted temporal ensembling (lambda ~ -0.1) or execute ~20% of chunk; extra camera views to cover occlusions help more than depth; higher resolution helps precision (but costs latency on 8 GB). Demo scaling shows diminishing returns 50%->100%. Subtask decomposition + progress head is overkill for single pick-place, but a continuous progress head is a cheap aux target.
Decision impact:
 - Q06 chunking/TE: supports recency-weighted temporal ensembling (avg 0.65 -> 0.80) and executing ~10 of 50 predicted steps (0.74 vs 0.60 at 5); uniform TE 0.62 — M (100 rollouts x 3 tasks, sim).
 - Q10 smoothness: recency-weighted TE is the smoothing mechanism that helped; supports blending over hard chunk switching — L/M.
 - Q11 cameras: extra (rear) view +0.33 avg over without it — M (sim).
 - Q04 depth: front depth in place of rear RGB 0.50 vs 0.80 — weakens naive depth-as-extra-image for a VLA — L (confounded).
 - Q13 data: 125 -> 250 -> 500 demos: 0.50 -> 0.68 -> 0.80, diminishing returns — L/M (sim motion-planner demos).
 - Q09 aux: continuous progress head enables stage switching; discrete progress fails (0.00) — L.
