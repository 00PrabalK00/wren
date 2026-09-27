# W3_SPOCImitatingShortestPathsinSimulationEn — SPOC: Imitating Shortest Paths in Simulation Enables Effective Navigation and Manipulation in the Real World (2023/2024, arXiv 2312.02976, CVPR 2024)
Setup: Stretch RE1 (mobile base + telescoping arm), 2 RGB cameras (nav + manip), 20 discrete actions; trained purely in simulation (AI2-THOR/ProcTHOR, ~200k procedural houses, ~40k Objaverse objects) on ~90k shortest-path planner episodes per task; model: SigLIP ViT-B/16 image + text encoders, 3-layer transformer visual encoder (fuses both cams + goal + CLS), 3-layer causal transformer action decoder over up to 100 past steps; batch 224, 20k-50k iterations. Eval: ~195 sim episodes per task (CHORES: ObjNav, PickUp, Fetch, RoomVisit); real: 88 trials in 2 real homes, zero-shot.
Claim: behavior cloning of shortest-path experts works — beating RL — if the data are large and diverse and the policy uses strong pretrained encoders and long-context transformers; transfers sim->real with only data augmentation.
Evidence (avg success over 4 tasks, CHORES-S):
 - Single-task RL (EmbSigLIP) 31.2 vs single-task IL 50.0 vs multi-task IL 49.9 (no multi-task penalty); with GT detection 65.0. Large vocabulary (CHORES-L): 38.6 / 63.1 with GT detection.
 - Image encoder (Table 5, avg): CLIP-RN50 26.6; DINOv2 ViT-S/14 44.8; SigLIP ViT-B/16 49.9 (ObjNav 19.6 / 47.5 / 55.0).
 - Architecture (Table 4): TxEnc+GRU 43.6; nonTxEnc+TxDec 45.1; TxEnc+TxDec 49.9.
 - Context window (Table 6, avg): two shorter windows 27.8 and 39.9 (window sizes lost in extraction) vs 100 steps 49.9; Fetch 2.3 / 4.1 / 14.0 — longer context crucial for long-horizon, partially observed tasks.
 - Data scale (Table 7a ObjNav): 10k episodes 19.0 -> (intermediate) 39.0 -> 100k 57.0. Diversity (7b, same 100k episodes): 100 houses x 1000 eps 43.5 vs 10k houses x 10 eps 57.0 (+13.5). Exploration-style expert: 46.5 vs shortest-path 57.0 (no gain).
 - Real (88 trials): SPOC avg 39.5 (ObjNav 50.0, PickUp 46.7 [66.7 soft], Fetch 11.1 [33.3 soft], RoomVisit 50.0); with DETIC detector 56.1. Authors say train+test data augmentation was "critical" in sim and real (no ablation numbers).
Ablations: listed above (encoder, architecture, context, scale, diversity, expert type).
Failure/limitations: navigation-dominant, discrete coarse actions, heuristic grasping in real; sim-generated millions of frames — orders of magnitude beyond our data; real eval small per task.
Conflicts: SigLIP > DINOv2 here (language-conditioned multi-object search, semantics matter), while for precise manipulation some papers find DINOv2 better (e.g. Theia/ DINOv2-based policies) — task-dependent (semantic recognition vs geometry). Long-context benefit conflicts with copycat/causal-confusion results for short manipulation — here tasks are partially observable navigation, where memory is genuinely needed.
Relevance: moderate-low. Useful for Q03 (SigLIP/DINOv2 >> CLIP-RN50 for recognizing novel objects, relevant to "different-looking pumpkin") and Q13 (diversity of scenes beats more episodes in same scene: vary table/background/pumpkin across demos). Long history not needed for our fully observed single pick-place.
Decision impact:
 - Q03 vision encoder: SigLIP ViT-B 49.9 > DINOv2 ViT-S 44.8 >> CLIP-RN50 26.6 avg success — M (sim, large data, semantic tasks; DINOv2 is smaller ViT-S so size confounded).
 - Q13 data: same episode count spread over 100x more environments: 43.5 -> 57.0 — M (sim, controlled).
 - Q07 history: long context (100) >> short for long-horizon partially observable tasks (27.8 -> 49.9 avg) — L for our case (task type differs).
 - Q08 language: multi-task language-conditioned IL shows no penalty vs single-task (49.9 vs 50.0) — L/M.
