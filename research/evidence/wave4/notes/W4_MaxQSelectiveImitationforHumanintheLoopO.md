# W4_MaxQSelectiveImitationforHumanintheLoopO — Max-Q Selective Imitation for Human-in-the-Loop Online Robot Learning with Monte Carlo Q-Chunk Critics (2026, arXiv id not in text)
Setup: HIL online RL; chunk-level MC-return critic ensemble; actor imitates the higher-Q of {policy chunk, buffer chunk}; ACT or flow actor. Sim: Peg Insertion, Square. Real: Franka-class arm, wrist camera, USB pick-and-insert under fixed dual LED lighting, 20 demos + autonomous rollouts + human interventions. Trial counts per success estimate not stated.
Claim: MC Q-chunk critic + hard max-Q selective imitation absorbs interventions and self-improves ~10× faster than HIL-SERL.
Evidence: Real USB (time to peak / success): HIL-SERL 5.0 h / 100%; plain MCBC 1.0 h / 96%; ACT QChunk-MCBC 0.5 h / 99%; Flow QChunk-MCBC 0.8 h / 96%; EXPO 2.4 h / 30%; E2HiL 3.7 h / ~90%. Sim: Q-chunk variants ≥96% within ~0.5 h (Square Flow 96% at 0.60 h).
Ablations: NONE reported — section lists ablations they "recommend (and plan to report)".
Failure/limitations: critic-quality dependent; MC variance; chunk horizon task-dependent. Critical read: no ablations, unclear trial counts; plain intervention-BC (MCBC) already gets 96% in 1 h, so most of the benefit is from human interventions themselves, not the RL machinery.
Conflicts: consistent with HIL/DAgger literature that corrective interventions are the most sample-efficient data; contrasts with HIL-SERL's TD approach (slower).
Relevance: For SO-101 the lightweight takeaway is: after an initial 50-demo policy, collect human intervention/correction segments with the leader arm and BC on them (MCBC-style ≈ 96% in 1 h on a real insertion task). The RL part needs reward/reset infrastructure we lack.
Decision impact:
 - Q13 data quality/recovery: supports collecting intervention/correction data on top of 20 demos (plain intervention BC 96% in 1 h real) — L (no ablations, single task).
 - Q01 action head: ~ ACT and flow actors both work in chunk-critic HIL — L.
