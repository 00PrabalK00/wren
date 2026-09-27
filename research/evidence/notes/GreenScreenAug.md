# GreenScreenAug — Green Screen Augmentation Enables Scene Generalisation (2024, arXiv 2407.07868)
Setup: real only; leader-follower teleop (ALOHA-like) Franka + Robotiq, 3 RealSense D415 (upper wrist, lower wrist, shoulder), 240×320; 8 tasks × 50 demos per scene; ACT with ABSOLUTE joint positions; >850 demos, 8.2k eval episodes; test in 3 novel scenes (objects' relative poses kept) with 25 runs per cell (~112 per task-method).
Method: collect demos in front of green cloth; chroma-key mask; replace background with random textures (Rand), SD-generated rooms (Gen), or learned mask network (Mask).
Evidence (novel scenes): GreenAug-Rand > NoAug by ~65%, > standard CV aug (photometric/crop) by ~29%, > generative aug (CACTI/GenAug/ROSIE-style) by ~21%. Gen 2nd, generative aug 3rd; Mask worst (mask errors → OOD inputs). Texture randomness matters: solid colours 65%, Perlin 66%, MIL textures 87% (vs none 48%). Coverage proportional to success. Object generalization (trained on green cup): cups 95/83/80 (Rand/Gen/None), cans 38/46/40, cubes 0/32/52 — mixed; strong aug can confuse geometry. Works with RL on UR5 too.
Limitations: needs physical green screen during collection; doesn't solve different-geometry objects; lighting shifts not isolated (backgrounds changed, lighting somewhat).
Relevance: HIGH — same data regime (50 demos, leader-follower, ACT, absolute joints, RealSense). Cheap: green cloth behind/under the workspace while recording. Complements 3D branch. Generative segmentation from wrist views is unreliable → prefer chroma key.
Decision impact:
 - augmentation: background randomization via green screen (random high-entropy textures) + standard photometric aug — SUPPORTED — H (8.2k real evals).
 - generative/segmentation-based aug: lower priority — M.
