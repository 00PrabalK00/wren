# RCNF — RC-NF: Robot-Conditioned Normalizing Flow for Real-Time Anomaly Detection in Robotic Manipulation (2026, arXiv 2603.11106, Fudan)
Setup: monitor trained only on successful demos: SAM2 tracks task-object masks (first-frame box prompt; in real world from Gemini 2.5 Pro), grid-sampled into point sets; conditional normalizing flow whose affine coupling layers (RCPQNet) are conditioned on robot proprioception (joints, gripper, pose) and a task-prompt encoding; anomaly score = NLL, threshold with α=0.05 (FAIL-Detect style). Benchmark LIBERO-Anomaly-10 (gripper open, gripper slippage, spatial misalignment). Real: Franka FR3 with wrist + third-person RealSense D435, pi0 as policy; RC-NF uses only the third-person view.
Claim: an object-point + robot-state density monitor detects anomalies within 100 ms and triggers state-level rollback (homing) or task-level replanning.
Evidence:
 - LIBERO-Anomaly-10 (Table 1): RC-NF best across all three anomaly types, ≈ +8% AUC and +10% AP over best baseline; baselines = Sentinel-style VLM monitors (GPT-5, Gemini 2.5 Pro, Claude 4.5 queried at 1 Hz in parallel) and FAIL-Detect.
 - Real: response latency < 100 ms. Qualitative: ball moved from gripper to table → score rises → homing procedure → score normal → control returned to pi0 which re-targets the ball; without RC-NF pi0 keeps moving toward the old position.
 - Ablation (Table 2): removing positional-residual branch → avg AUC ≈ 0.89 (moderate drop).
Failure/limitations: needs SAM2 tracking (GPU cost) and a detector prompt; real-world results are demonstrations/case studies, not success-rate tables; "homing" is a crude recovery.
Conflicts: agrees with FIPER/FAIL-Detect (density on successful data) but monitors explicit object motion instead of policy embeddings; reports VLM monitors as too slow (multi-second).
Relevance to SO-101: exactly our disturbance case (object moved / grasp failed). A cheaper version for us: track the pumpkin with a lightweight detector/segmenter on the RealSense view + gripper state, flag "gripper closed but object not lifted" or "object jumped" → re-query policy / rewind. SAM2 on 8 GB alongside the policy is possible only in small variants (not tested here).
Decision impact:
 - Object-state + robot-state consistency monitor (<100 ms) as re-plan/rollback trigger — SUPPORTED — L/M (benchmark strong; real evidence qualitative).
