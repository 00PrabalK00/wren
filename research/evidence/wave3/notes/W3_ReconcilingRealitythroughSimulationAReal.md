# W3_ReconcilingRealitythroughSimulationAReal — Reconciling Reality through Simulation: A Real-to-Sim-to-Real Approach for Robust Manipulation (RialTo) (2024, RSS, arXiv 2403.03949)
Setup: Real Franka Panda, 6-DoF Cartesian EE position control, 3D point cloud from ONE calibrated depth camera. 6 tabletop tasks (book on shelf, plate on rack, mug on shelf, open drawer, open cabinet, open toaster) + in-the-wild scenes. Pipeline: scan scene (NeRFStudio/ARCode/Polycam) → digital twin GUI (~15 min active) → bring 15 real demos into sim ("inverse distillation") → PPO fine-tune with BC regularizer on privileged state with pose randomization → teacher–student distillation to point-cloud policy, co-trained with 15 real demos, with sim distractors. ≥10 real rollouts per condition. Three test levels: pose randomization, + visual distractors, + physical disturbances (moving objects/targets, closing drawers).
Claim: Real-to-sim-to-real RL fine-tuning robustifies small-data imitation policies to poses, distractors and disturbances far beyond what more demos achieve.
Evidence:
 - Across 6 tasks (Fig. 5, 15 demos): RialTo avg 91% (pose rand.), 77% (distractors), 75% (disturbances) vs BC 25%, 11%, 5%.
 - Book on shelf (Table I): BC 15 demos 10/0/0%; BC 50 demos 40/30/20%; RialTo (15 demos) 90/70/60%.
 - Real-to-sim asset vs Objaverse-diverse drawers: real target drawer 90% vs 10%.
Ablations:
 - Distractor training in sim (mug on shelf, Table II): pose rand. 60 → 100%; with distractors 30 → 70%.
 - Co-training the distilled policy with 15 real demos vs sim-only: 3.5x (book) and 2x (plate) success under disturbances; equal on easy tasks. Starting from real or sim demos: similar.
 - PPO from scratch (no demos): 0% on 3/5 tasks, exploits simulator bugs.
Failure/limitations: ≥10 trials only (big error bars, ±15%); needs depth camera, scanning, articulation specification, reward functions, GPU sim + RL; point-cloud policies; per-scene specialization (not general).
Conflicts: Agrees that clean-data BC collapses under distractors/disturbances (consistent with SID, CFNBC, CRAFT) and that 3x more demos helps only modestly (book 10→40%). Contrasts with generative-augmentation approaches: here robustness comes from state-space exploration (recovery behaviours) + distractor randomization rather than image-level augmentation.
Relevance: Our RealSense provides depth, and SO-101 has MuJoCo/Isaac models, so a digital twin of the pumpkin/tray scene is feasible but a big engineering investment. Cheaper transferable lessons: (1) train with distractors present (30→70%); (2) BC gains from more demos alone are modest; recovery/disturbance data is what gives closed-loop robustness.
Decision impact:
 - Q13 data: BC 15→50 demos lifts book task only 10→40% (pose), 0→30% (distractors), while sim-RL-augmented 15 demos reach 90/70% — supports "diversity/recovery coverage beats raw count" — confidence M (real, but ≥10 trials).
 - Q14 robustness: BC (15 demos, point cloud) drops 25% → 11% with distractors → 5% with disturbances; distractor training 30→70% — supports distractor randomization during training — confidence M.
 - Q05 augmentation (synthetic demos via sim): digital-twin RL-generated data + real co-training gives large robustness gains — confidence M (engineering-heavy).
 - Q04 3D: point-cloud BC is itself not robust to distractors (11%) — 3D input alone does not solve distractors — confidence L.
