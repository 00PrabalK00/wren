# W4_ExploringPoseGuidedImitationLearningforR — Exploring Pose-Guided Imitation Learning for Robotic Precise Insertion (2025/26, arXiv id not in text)
Setup: Cobot Mobile ALOHA (agilex, passive compliance, no F/T), one Orbbec Dabai RGB-D front camera, 30 Hz; 6 real insertion tasks (clearance down to 0.01 mm); 7–10 demos/task with target object FIXED during collection; observation = relative SE(3) pose source→target from 6D pose tracker (FoundationPose-style), action = future relative pose trajectory; DP backbone; RTX 4060 (8 GB) for everything; 10 trials per task per method.
Claim: object-centric relative-pose observations let DP learn precise insertion from ~10 demos and generalize to pose variation; gated RGB-D fusion compensates for pose-estimation noise.
Evidence (ID avg / OOD avg over 6 tasks, 10 trials each): ACT (50 demos) 1.7 / 0; RISE point-cloud (50 demos) 3.3 / 0; SPOT (10 demos) 71.7 / 61.7; PoseDP 81.7 / 76.7; RPDP 91.7 / 78.3. USB-C task: PoseDP 30/30 vs RPDP 100/80.
Ablations:
 - Pose encoder MLP → disentangled rot/trans: ID 71.7→81.7, OOD 61.7→76.7.
 - Adding RGB-D by naive concat: ID 81.7→68.3 (image features dominate low-dim pose; hurts tasks 1–5, helps USB 30→60).
 - Gated residual fusion: 91.7 ID / 78.3 OOD; still slight drop on tasks 1–5 vs pose-only ("visual features may cause overfitting").
 - Data quality: same task trained on noisier demo set → 100% vs 60%.
 - Runtime on RTX 4060: PoseDP 70 ms, RPDP 140 ms.
Failure/limitations: needs reliable 6D pose tracking of known rigid object models; occlusion breaks tracking; target fixed in demos. Critical read: ACT/RISE baselines obviously not tuned for sub-mm insertion (0–10%), so the comparison mainly shows pixels→actions can't do sub-mm from 50 demos; 10 trials per cell.
Conflicts: agrees with object-centric/pose-based papers (SPOT, PRISM-DP) that compact object state is extremely data-efficient; contrasts with end-to-end pixel policies which need more data but don't need object models.
Relevance: our pumpkin is not a rigid known CAD model and pick-and-place tolerance is loose, so pose-tracking pipelines are overkill; but the lesson "high-dim image features can dominate low-dim state when concatenated" and "demo noise 100→60%" are relevant. Runtime shows DP at 70 ms on an 8 GB-class RTX 4060.
Decision impact:
 - Q04 3D/depth: ~ object-pose (from RGB-D tracker) >> raw RGB/point cloud for precision with 10 demos; RISE point cloud 3.3% — L (insertion, not pick-place).
 - Q13 data quality: supports demo consistency; noisy set 60% vs clean 100% — L (single task).
 - Q12 model size/compute: DP pose-only 70 ms on RTX 4060 — L.
