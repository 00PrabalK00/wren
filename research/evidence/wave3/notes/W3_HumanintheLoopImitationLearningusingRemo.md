# W3_HumanintheLoopImitationLearningusingRemo — Human-in-the-Loop Imitation Learning using Remote Teleoperation (IWR) (2020, arXiv 2012.06733)
Setup: Sim only (robosuite/MuJoCo Sawyer, OSC control), 2 tasks: Threading (1 operator) and Coffee Machine (3 operators); LOW-DIM state observations (object poses), no images. Start from 30 full demos + base policy; 3 rounds of intervention collection, each adding interventions ≈33% of initial samples; Full-Demos baseline gets an equal number of human-annotated samples. Policy: 2-layer LSTM (hidden 100), seq length 10, BC. Eval: 50 rollouts per checkpoint, max over checkpoints, 3 seeds.
Claim: human interventions on a running policy, trained with IWR (balanced 50/50 sampling of intervention vs on-policy samples), beat an equal budget of extra full demos and HG-DAgger.
Evidence (final success %):
 - Threading (Table I): Base 58.0; Full Demos 76.7; HG-DAgger 75.3; IWR-no-balance 74.7; IWR 87.3. Round1/Round2: HG 57.3/62.7, IWR-NB 76.0/72.0, IWR 84.0/90.7.
 - Coffee, 3 operators (Table II): Base 52.0; Full Demos 64.9; HG-DAgger 69.6; IWR 87.5.
 - Cross-dataset (Tables III/IV): IWR training on HG-DAgger's collected data gets 87.3 (Threading) / 85.6 (Coffee) → gain is from the weighting, not only the collection.
Ablations: balancing removed (IWR-NB) → 87.3 → 74.7; discarding on-policy samples (HG-DAgger) → 75.3. One large round vs 3 iterative rounds: no difference on Threading, ~7% lower on Coffee (more bottlenecks → iterative better).
Failure/limitations: sim only, low-dim state (no vision), max-over-checkpoints reporting inflates numbers; std up to ±10–16 with 3 seeds; operator skill variance.
Conflicts: consistent with DAgger-style / recovery-data literature (RaC, HG-DAgger) that correction data near bottlenecks is more sample-efficient than more full demos; contrasts with the common "just collect more demos" practice at equal human effort.
Relevance: moderate for Q13. For SO-101 with leader/follower teleop we can do interventions cheaply (operator takes over with the leader arm when the policy fails at grasp/place). Suggests: after ~30–50 demos, spend the next budget on interventions at the grasp and tray-place bottlenecks, and upweight intervention samples ~50/50 in the loader.
Decision impact:
 - Q13 data: supports intervention/correction data over equal amount of full demos (Threading 87.3 vs 76.7; Coffee 87.5 vs 64.9) with 50/50 balanced sampling — confidence M (sim, low-dim, but consistent over 3 operators).
