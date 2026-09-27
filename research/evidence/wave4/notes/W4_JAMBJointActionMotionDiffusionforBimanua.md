# W4_JAMBJointActionMotionDiffusionforBimanua — JAMB: Joint Action–Motion Diffusion for Bimanual Manipulation (2026, arXiv 2609.25322)
Setup: RoboTwin 2.0 sim, 16 bimanual tasks (8 sync, 8 seq), 100 demos/task, 3 seeds x 50 rollouts. Real: 2 xArm, one fixed ZED Mini stereo cam (overhead), VR teleop, 3 tasks, 50 demos/task, 30 trials/method/task. Policy: single RGB view (obs horizon 1) + proprio; DINOv2 patch tokens (17x23=391) fused with patch-aligned noisy future 3D track tokens; 4-block DiT (hidden 1024); action horizon 16, track horizon 16; 10 DDIM steps; 4D RoPE anchored at 3D patch positions (depth from FoundationStereo). Track labels from CoTracker3 + stereo depth in real.
Claim: jointly denoising actions AND future 3D point tracks (not just auxiliary or conditioning) improves bimanual success and OOD visual generalization.
Evidence:
 - Sim avg: Sync — DP 45.8, DP3 58.1, DICP (future visual) 57.5, GAP (future geometry aux) 45.3, ATM (2D tracks → action) 63.2, JAMB 85.2. Seq — DP 39.0, DP3 51.9, DICP 61.5, GAP 51.1, ATM 40.8, JAMB 81.6. Overall JAMB 83.4 (+23.9 over best baseline).
 - Real (50 demos, 30 trials): DP3 35.6, GAP 64.4, JAMB 85.6 avg; Store Block 23.3/73.3/83.3; Stack Basin 76.7/86.7/93.3; Place Duck Box 6.7/33.3/80.0.
 - Easy→Hard (unseen textures + clutter, no fine-tune, 8 tasks): DP3 1.7, DICP 3.9, GAP 4.3, ATM 0.0, JAMB 17.9 — everything collapses, JAMB least.
Ablations (8 sim tasks, avg / sync / seq):
 - Action-only 61.4 / 57.5 / 65.3
 - Track regression aux (shared attention, predicts clean tracks) 73.9 / 68.4 / 79.3  ← +12.5 from future-motion supervision alone
 - Track-conditioned action diffusion (predict tracks then condition) 76.3 / 72.8 / 79.8
 - w/o 4D RoPE 74.1 / 65.7 / 82.5
 - Full joint denoising 81.7 / 74.3 / 89.0
 - Track accuracy ADE/FDE (mm): full 7.6/10.0; track-cond 9.9/12.5; regression 11.1/14.8; no RoPE 13.2/17.2 — better tracks ↔ better success.
 - Future representation for Easy→Hard: 2D tracks 9.3, endpoint 3D geometry 10.3, 3D tracks full horizon 17.9.
Failure/limitations: single camera; fixed grid of queries; real supervision depends on tracker + stereo depth quality. Critical: OOD Hard setting success still very low (17.9%) so "better generalization" is relative; real baselines only DP3 and GAP (no RGB DP / ACT in real); bimanual.
Conflicts: Aux future-motion prediction helping (+12.5) agrees with HumanEgo (object motion aux +17.5) and contrasts TRI co-training (discrete latent actions no gain) — difference: dense metric future motion of the scene in low-data single-task, vs discrete tokens in large multi-task regime. DP3 > DP in sim (58 vs 46) supports point-cloud/depth input, but DP3 is weak in real (35.6), consistent with reports that raw real point clouds are noisy.
Relevance: Medium-high. Recipe fits our setup: fixed RealSense (real depth, no stereo net needed) + DINOv2 patches + small DiT, 50 demos, 30-trial real evaluation. Adding a future 3D track head (labels offline from CoTracker + RealSense depth) is a cheap training-only aux that gave large gains; at inference it costs extra tokens (391 track tokens) — heavier than plain aux regression, and 10 DDIM steps.
Decision impact:
 - Q09 aux: future 3D point-track prediction +12.5 (as aux regression) to +20.3 (joint denoising) over action-only (61.4→81.7) — confidence M-H (sim 8 tasks x 150 rollouts + real 30 trials).
 - Q04 3D: depth used as positional grounding (4D RoPE) +7.6 pts; DP3 point cloud > RGB DP in sim but weak in real (35.6%) — supports depth as positional/aux signal over raw point-cloud encoder — confidence M.
 - Q14 robustness: unseen texture+clutter still collapses all methods (≤17.9%) — future-motion modelling helps but does not solve appearance shift — confidence M.
 - Q03 encoder: DINOv2 patch features used successfully with 50 real demos — confidence L.
