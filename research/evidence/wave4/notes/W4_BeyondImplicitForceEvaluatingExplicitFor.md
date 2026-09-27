# W4_BeyondImplicitForceEvaluatingExplicitFor — Beyond Implicit Force: Evaluating Explicit Force-Torque Proxies in Action Chunking with Transformers (2025/26, arXiv id not in text)
Setup: ALOHA Solo (ViperX-300s follower, WidowX-250s leader), 3 cams (high BEV, low side, wrist), 50 Hz joint-space control, 4 real contact tasks (Board Wipe, Plug Insert, Soft Bottle Press, Foam Stop), SE(2) randomized start poses; #demos per task NOT stated; ACT hidden 512, ff 3200, chunk 100 (=2 s), batch 16, lr 2e-5, KL β 10, 8000 epochs; torque τ = k_t·motor current, concatenated with joint states before the shared joint embedding (14-D in). Inference on RTX 4090. Trials: Bottle 10 per stiffness mode, Plug 10, Wipe 20, Foam 10 per mode (force-profile only).
Claim: ACT's contact competence depends on the leader–follower tracking gap (targets = leader positions); predicting follower states (ACT-o) removes it and collapses contact tasks; motor-current torque as an input restores and exceeds it.
Evidence (Table IV; Base ACT / ACT+τ / ACT-o / ACT-o+τ):
 - Board Wipe (n=20): 60 / 90 / 15 / 95 %.
 - Soft Bottle overall: 50 / 70 / 25 / 75 (Low-stiff 100/60/50/80; High-stiff 0/80/0/70) — Base ACT collapses to the low-stiffness mode.
 - Plug Insert (n=10): 1-step 20/40/0/10; 1-or-2 attempts 30/70/0/50.
 - Foam Stop: all stop at roughly correct height; +τ variants match demo effort equilibrium better (figure only).
Ablations:
 - Target leader → follower (removes implicit force cue): Wipe 60→15, Bottle 50→25, Plug 30→0. Stated: "hesitant/stalled" behavior; follower-state targets alone ≈ worse ACT.
 - Add torque input to base ACT: Wipe 60→90, Bottle 50→70, Plug 30→70.
 - Add torque to ACT-o: Wipe 15→95, Bottle 25→75, Plug 0→50.
 - Injection: concatenating raw effort with joint state before the projection "works best" (stated, no comparison numbers).
Failure/limitations: joint-current proxies are low-bandwidth, not tactile; low-data only. Critical read: 10–20 trials per cell, 1 robot, demo count unreported, no seeds/std; tasks are chosen to be force-critical (vision-ambiguous) so gains may not carry to pick-and-place; torque inputs could also hurt under changed payload/gravity (not tested); risk of proprioception copycat not examined.
Conflicts: confirms ACT paper's claim that leader targets implicitly encode force; supports absolute LEADER joint targets over "achieved follower state" targets. Contrasts with policies trained on observation-state targets (some LeRobot datasets log follower state as action) — those lose the cue.
Relevance: SO-101 is exactly leader/follower position-controlled, and Feetech STS3215 servos expose present current/load registers, so a τ proxy is essentially free to log. For pumpkin pick-and-place (low contact) the benefit is probably small, but ensure actions = leader joint positions (not follower). Adding effort to state is a cheap option for grasp-success detection (pumpkin slip). No effect on latency.
Decision impact:
 - Q02 action space: supports absolute LEADER joint targets over follower-state targets (60→15, 50→25, 30→0 when switched) — confidence M (real robot, few trials, contact tasks).
 - Q09 auxiliary objectives / extra inputs: supports adding motor-current effort as proprioceptive input for contact phases (+30–40 pts) — L for our pick-place (tasks are force-critical).
 - Q12 model size: ~ ACT hidden 512 works on real contact tasks — L.
 - Q06 chunking: ~ chunk 100 @ 50 Hz (2 s) used successfully, not ablated — L.
