# W3_Ag2ManipLearningNovelManipulationSkillsw — Ag2Manip: Learning Novel Manipulation Skills with Agent-Agnostic Visual and Action Representations (2024, arXiv 2404.17521)
Setup: visual encoder = ResNet50 pretrained on Epic-Kitchens with humans/robots masked out ("agent-agnostic", time-contrastive like R3M/VIP), 24 h on A100. Main use: reward shaping for RL with an agent proxy in IsaacGym (24 tasks, FrankaKitchen/ManiSkill/PartManip, 3 cams × 3 seeds). Real: Franka FR3 + single Kinect Azure camera, 4 tasks (PushDrawer, CloseCabinet, PickBag, MoveBasket), 20 demos per task, advantage-weighted regression using embedding-distance-to-goal weights, 10 trials per task.
Claim: masking the agent out of human video pretraining gives embodiment-agnostic features that improve RL skill discovery and few-shot real imitation.
Evidence (real, Table III, successes/10; column order reconstructed from split text, totals match the paper's 50%→77.5% claim):
 - ResNet50 (ImageNet): 1,5,1,1 → 8/40 = 20%
 - CLIP: 2,3,0,0 → 25%... (10/40)
 - R3M: 4,5,4,3 → 16/40 = 40%
 - VIP: 6,6,2,6 → 20/40 = 50%
 - Ag2Manip: 7,8,8,8 → 31/40 = 77.5%
 Sim: "325% increase" over baselines for RL without demos (Table I, 9 runs per task).
Ablations: sim-only ablations of visual vs action representation (both needed); not relevant to BC design.
Failure/limitations: 10 trials per task; imitation method is AWR with representation-derived weights, so the encoder affects both features AND sample weighting — not a clean encoder comparison; unclear whether encoders were frozen (text suggests used as fixed representations); single camera; tasks are coarse (push/close/move).
Conflicts: Ordering ImageNet ResNet < CLIP < R3M < VIP agrees with early manipulation-pretraining papers (R3M/VIP) but contradicts later large studies (e.g., Dasari et al., Burns et al.) finding ImageNet/DINO competitive with or better than R3M/VIP when fine-tuned — difference likely frozen features + 20 demos + AWR.
Relevance: weak; 20 demos real regime is close to ours, but the method (goal-image AWR, frozen ResNet50) is not what we would build. Only mild evidence that frozen generic CLIP/ImageNet ResNet50 features are poor for low-data real BC.
Decision impact:
 - Q03 vision encoder: frozen ImageNet ResNet50 20% / CLIP 25% vs manipulation-pretrained R3M 40%, VIP 50%, Ag2Manip 77.5% (20 demos, 40 trials) — weakens frozen generic ImageNet/CLIP features — confidence L (AWR confound, 10 trials/task)
