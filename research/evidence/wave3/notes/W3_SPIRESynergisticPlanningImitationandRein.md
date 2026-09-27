# W3_SPIRESynergisticPlanningImitationandRein — SPIRE: Synergistic Planning, Imitation, and Reinforcement for Long-Horizon Manipulation (2024, CoRL 2024; arXiv id not in text)
Setup: simulation only (robosuite/MimicGen-style tasks: Square, Coffee, Three Piece, Tool Hang, Broad variants; 9 tasks); TAMP plans free-space motion, human teleops only "handoff" contact segments; 200 demos/task for BC (also 10/50); RL = DrQ-v2 fine-tune with BC warmstart (init or residual) + KL penalty to BC; 50 rollouts, best of 5 seeds.
Claim: TAMP-gating + BC warmstart + KL-constrained sparse-reward RL fine-tuning gives 87.8% avg success vs 52.9% TAMP-gated BC and 37.6% TAMP-gated RL, 5.8× fewer demos, episodes 59% the length of BC.
Evidence: Tool Hang BC 10% → SPIRE 94% (RL alone 0%). 7 tasks: SPIRE needs 150 demos total to reach ≥80% vs BC >870. KL-penalty ablation: Three Piece 84% → 17.6%, Tool Hang 74% → 0% without it (5-seed means).
Ablations: KL penalty critical (above); curriculum: sequential lower variance, permissive better top-1 (figure only).
Failure/limitations: sim-only, needs fast simulator for RL, full-state TAMP, Markovian policies only. Critical read: nothing transfers to a real SO-101 without a simulator of the pumpkin task; best-of-5-seeds reporting inflates numbers.
Conflicts: agrees with RL-fine-tune-of-BC literature (residual RL, PA-RL) that BC anchoring is necessary for sparse-reward RL.
Relevance: low. We have no simulator; the one transferable point is that a BC policy trained on few demos is mostly a good exploration prior, and demo-count requirements drop a lot if a later correction stage (RL or human corrections) exists.
Decision impact:
 - Q13 data quantity: with a post-BC improvement stage 10–50 demos suffice where BC alone needs ~125+/task — confidence L (sim, RL, not applicable to our pipeline).
