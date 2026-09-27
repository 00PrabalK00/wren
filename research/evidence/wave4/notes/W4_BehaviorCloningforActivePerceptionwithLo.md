# W4_BehaviorCloningforActivePerceptionwithLo — Behavior Cloning for Active Perception with Low-Resolution Egocentric Vision (2026, arXiv 2605.14106)
Setup: Lynxmotion AL5D low-cost 6-DoF arm, Xbox-controller teleop, wrist RGB only at 64×64, 10 Hz. Toy task: plant placed left or right (partially visible), center it in view and close gripper. 4-layer CNN + LSTM over H=20 frame history, MSE on single-step joint targets, no chunking. 2–64 demos; 5 closed-loop trials per setting.
Claim: step-wise joint-delta targets beat absolute joint targets (lower test loss, fewer demos needed, smoother, interpolates to unseen placements); 64×64 wrist RGB suffices.
Evidence (Table I, MSE ×1e-3 test / success):
 - Delta: 2 demos 6.22 / 0/5; 4 demos 6.15 / 5/5; 8+ demos 5.5–6.1 / 5/5.
 - Absolute: 2 demos 157.5 / 0/5; 4 demos 189.1 / 0/5; 8 demos 93.3 / 5/5; 16: 30.5; 32: 16.6; 64: 12.8 (all 5/5).
 - Qualitative: absolute model overshoots then corrects; at intermediate (unseen) plant positions absolute model snaps to one of the two training configurations; delta model adapts.
Ablations: delta vs absolute only (above); demo count.
Failure/limitations: trivial 2-mode task, 5 trials, 10 Hz single-step (no chunks), metric MSE compares delta vs absolute in joint-position space on teacher-forced data; the gap closes by 8 demos in success. No contact/manipulation. Low-cost arm, but the absolute model has only 2 goal configurations so "memorize-a-pose" failure is expected.
Conflicts: contradicts ACT's (unquantified) claim that delta targets hurt; consistent with UMI/relative-action claims. Reconciliation: here actions are single-step and deltas are small, closed-loop corrections from visual servoing; ACT uses chunked absolute leader targets on a PID rig where drift accumulation from deltas matters. For chunked policies, "chunk-relative-to-current-state" deltas are the relevant variant, not tested here.
Relevance: same class of hardware (cheap position-controlled arm, wrist cam, 10 Hz). Supports trying delta (relative to current joint state) especially for viewpoint/position generalization, but evidence is weak for pick-and-place with chunking.
Decision impact:
 - Q02 action space: supports delta joint targets over absolute for low-data interpolation — confidence L (toy task, 5 trials, single-step).
 - Q13 data quantity: delta needed 4 demos vs absolute 8 for 5/5 on toy task — L.
 - Q11 cameras: low-res (64×64) wrist-only sufficient for visual-servo-type centering — L.
