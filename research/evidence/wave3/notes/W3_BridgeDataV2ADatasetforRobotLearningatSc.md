# W3_BridgeDataV2ADatasetforRobotLearningatSc — BridgeData V2: A Dataset for Robot Learning at Scale (2023, arXiv 2308.12952)
Setup: WidowX 250 low-cost 6-DoF arm; 60,096 trajectories (50,365 VR-teleop demos + 9,731 scripted pick-place), 13 skills, 24 environments, 100+ objects; cameras: fixed over-shoulder RGB-D, 2 randomized RGB, wrist RGB, 640×480, 5 Hz. Policies trained on over-shoulder view only at 128×128 (RT-1 320×256); action = 6D delta EE pose + discrete gripper. Methods: GCBC (ResNet-34), D-GCBC (DDPM), ACT, CRL (offline RL), LCBC (ResNet-34 + FiLM, MUSE text), RT-1. 10 trials per task (20 in scaling study).
Claim: a large diverse dataset on a cheap arm yields policies that generalize to new objects/environments/labs; performance scales with model size, data size and skill diversity.
Evidence:
 - Seen tasks (Table 2, averages over 8 tasks × 10 trials): GCBC 0.49, D-GCBC 0.49, ACT 0.41, CRL 0.42, LCBC 0.23, RT-1 0.49.
 - Unseen objects/environments (Table 3): nonzero success for most methods; language-conditioned methods struggle with unseen object names; RT-1 ≫ LCBC (per-cell numbers are garbled in extraction; GCBC avg appears as 0.60).
 - Cross-institution zero-shot (Table 4, avg Lab1 → Lab2, differences in camera placement, lighting, object instances): GCBC 0.30 → 0.13, D-GCBC 0.23 → 0.13, ACT 0.03 → 0.10, CRL 0.13 → 0.20, LCBC 0.13 → 0.03, RT-1 0.47 → 0.40.
Ablations (Figure 5, figure only, qualitative): larger image encoder strictly better on spoon task (small models fail to rotate gripper); more data (stratified subsampling) improves seen and unseen; 13 skills vs 3 skills at matched size (27k vs 28k traj) → significantly better on an unseen pick-place task.
Qualitative: D-GCBC, ACT, RT-1 reproduce demo pauses; D-GCBC (no history, no chunking) shows jerky mode-oscillation; chunking/history avoid it.
Failure/limitations: 10 trials per cell → ±15 pts noise; methods not tuned; ACT performed poorly here (5 Hz data, delta EE, 60k multi-task data — far outside ACT's design regime). Tasks low-precision.
Conflicts: ACT is weak here (0.41 seen, 0.03 cross-lab) vs strong in ALOHA single-task 50-demo settings — regime difference (multi-task goal-conditioned, 5 Hz, delta EE). The "diffusion without chunking is jerky" observation agrees with Diffusion Policy/ACT reasoning that chunking or history is needed to commit to a mode.
Relevance: low-moderate. Cheap arm like SO-101; cross-lab camera/lighting shift drops most small policies by ~50% relative, only large RT-1 with history holds up. Skill diversity at fixed size helps generalization, but our regime is 50–100 single-task demos.
Decision impact:
 - Q14 robustness: camera placement + lighting + object instance shift halves small-policy success (GCBC 0.30 → 0.13) while RT-1 0.47 → 0.40 — supports expecting large drops under camera shift for small scratch-ish models — confidence M (10 trials).
 - Q01 action head: diffusion without chunking/history oscillates between modes (qualitative) — supports pairing expressive heads with chunking — confidence L.
 - Q13 data: skill diversity at matched size (27k vs 28k) improves unseen pick-place; more data helps — supports diverse data — confidence L (figure only, large-data regime).
 - Q12 model size: bigger encoder strictly better at 50k-demo scale — confidence L (figure only; different data regime).
