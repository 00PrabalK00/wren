# W3_LDA1BScalingLatentDynamicsActionModelvia — LDA-1B: Scaling Latent Dynamics Action Model via Universal Embodied Data Ingestion (2026, arXiv 2602.12215)
Setup: 1.6B-param foundation model: frozen Qwen3-VL conditioning + frozen DINO encoder; MM-DiT jointly flow-matches action chunks (delta wrist pose + gripper/finger keypoints, 10 Hz) and FUTURE DINO features (3 Hz); task embedding selects policy / forward dynamics / inverse dynamics / visual forecasting so actionless human video and low-quality data contribute. Pretrain EI-30k (30k h human+robot, real+sim), 48 H800, 4,608 GPU-h. Sim: RoboCasa-GR1 24 tasks, 1,000 traj/task, 51 trials/task. Real: Galbot G1 gripper and dexterous hands, Unitree G1; single egocentric head camera; 100 teleop traj/task (50–80% expert, rest with pauses/retries); 10 trials per task.
Claim: co-training policy with latent (DINO-space) dynamics/forecasting lets a 1B model scale on heterogeneous, mixed-quality data and outperform π0.5 / GR00T.
Evidence:
 - RoboCasa-GR1 (Table II): GR00T-N1.6 (3B) 47.6; GR00T-EI10k (1B, same data) 51.3; LDA-1B 55.4.
 - Real gripper, few-shot new embodiment: pick&place 80–90%; Clean Rubbish 35% vs GR00T/π0.5 0% (figure values, 10 trials).
 - Real dexterous: Pull Nail 80% (π0.5 "largely fails"), Flip Bread 90% vs π0.5 10%.
 - Generalization pick&place (Table III, 10 trials): novel object π0.5 26.7 / GR00T 40.0 / LDA 60.0; unseen background 20.0 / 40.0 / 60.0; OOD start position 6.7 / 20.0 / 40.0.
Ablations:
 - Future-state target: VAE pixel latents vs DINO latents (same arch): 20.0 → 55.4 (UWM-MMDiT vs LDA-1B). UWM 0.1B → 1B: 14.2 → 19.3 only.
 - MM-DiT → plain DiT: 55.4 → 48.9; 1B → 0.5B: 55.4 → 50.7.
 - Objectives (offline L1 action error on held-out AgiBot, figure only): policy-only degrades when low-quality data is added; policy+forecasting+dynamics keeps improving, even with 10k h actionless video.
 - Mixed-quality fine-tuning (Table IV): place pen (63 high-quality traj → +37 low): π0.5 60 → 40, LDA 70 → 80; remove lid (66 → +34 low): π0.5 50 → 40, LDA 50 → 60.
Failure/limitations: frozen DINO features and egocentric-only views may limit new viewpoints; enormous pretraining; real results 10 trials/cell, mostly figures; baselines fine-tuned only on filtered expert subset (by design).
Conflicts: agrees with aux-future-prediction papers (Seer, UVA, PAD) that a dynamics/forecast objective helps; adds that the latent space matters (DINO ≫ VAE). Contradicts the naive "more demos always help": for plain BC (π0.5), adding 34–37 imperfect demos HURT by 10–20 pts.
Relevance: model is 1.6B → not trainable on 8 GB; but two transferable lessons at our scale: (1) auxiliary prediction of future frozen-DINO features (cheap: no pixel decoder) is the better aux target vs pixel/VAE; (2) our teleop demos with pauses/retries hurt plain BC — filter them or add a dynamics objective.
Decision impact:
 - Q09 auxiliary objectives: supports future-latent (DINO-feature) forecasting + dynamics co-training; DINO target ≫ VAE target (20.0 → 55.4) — confidence M (sim, 51 trials×24 tasks, but 1B scale).
 - Q13 data quality: imperfect demos hurt plain BC (π0.5 −10 to −20 pts) unless a dynamics objective absorbs them (+10) — confidence L/M (10 trials, 2 tasks).
 - Q12 model size: 0.5B → 1B: 50.7 → 55.4 (with 30k h pretraining) — confidence L (irrelevant regime for 8 GB).
 - Q14 robustness: large latent-dynamics pretraining: unseen bg 60 vs π0.5 20; OOD position 40 vs 6.7 — confidence L (10 trials).
 - Q03 vision encoder: frozen DINO as state/target representation works at scale — confidence L.
