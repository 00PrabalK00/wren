# W3_AhaRobotALowCostOpenSourceBimanualMobile — AhaRobot: A Low-Cost Open-Source Bimanual Mobile Manipulator for Embodied AI (2025/26, arXiv 2503.10070)
Setup: $1,000 bimanual mobile manipulator using the SAME Feetech STS3215 servos as SO-101 (1:345 gearbox), SCARA-like horizontal arms + lifting rails, ESP32 PID at 66 Hz; 3 webcams (pan-tilt head + 2 wrist) 640×360 @30 Hz; onboard RTX 4060. Teleop via webcam-tracked 26-faced marker handle + pedals (Cartesian → IK → absolute joint commands). IL: ACT and π0 on 6 real tasks, 18-D state + 3 images; 50 demos (box transfer, can pressing, pen insertion), 80 (floor pick), 200 (table cleaning, pan sweeping); 10 trials per task, stage-wise success.
Claim: hardware-control co-design (dual-motor anti-backlash, dithering stiction compensation, trapezoidal profiling) makes cheap servos precise (0.72 mm repeatability) and the collected data trains ACT/π0 well.
Evidence:
 - Repeatability 0.72 mm (dial indicator). Dithering enabled: tracks 2-encoder-step increments; disabled: fails to follow (figure only). Backlash compensation removes oscillation at square-wave reversals (figure only).
 - Handle: 26-faced reduces rotation tracking error ~80% vs 6-faced (5.391° baseline; Table 3).
 - Teleop (Table 4): RoboPilot 100% success, 30% faster than leader-follower and SpaceMouse; SpaceMouse 44.4% on task 1; leader-follower hit wrist singularities (roll-pitch-roll).
 - IL (Table 5, stage success /10; assignment of ACT vs π0 columns inferred from text): Box Transfer 10/10→10/10; Pen Insertion 10/10, 6/10, 6/10; Floor-to-table pick 8/10, 7/10, 7/10; Can pressing 10/10, 6/10; Table cleaning 9/10, 7/10, 7/10; Pan sweeping 8/10, 6/10, 5/10.
 - RoboPilot vs VR (Quest Pro) data, same count: 73% vs 70% average (Table 6).
Ablations:
 - Base velocity vs position action: velocity control learned from pedal data with spikes → policy fails to move; position (displacement from start) → smooth reliable motion (figure 18, qualitative).
 - Authors attribute robustness to teleop noise to "absolute joint commands".
Failure/limitations (stated): π0 early termination on can pressing (no temporal memory); action chunking + long π0 inference caused command discontinuities that knocked over tools in cleaning/sweeping. Critical: 10 trials, no baselines on the IL side; no ablation of the backlash/dithering fixes on POLICY success, only on tracking.
Conflicts: Supports ACT-style absolute position targets (vs delta/velocity) on cheap position-controlled servos; consistent with SmolVLA/π0 users reporting chunk-boundary jerks with slow inference.
Relevance: HIGH on hardware: SO-101 uses STS3215 with the same backlash/stiction; a trapezoidal/C1 reference filter on commanded targets and stiction dithering are cheap controller-level fixes that can reduce jitter independent of the policy. Directly echoes our "jerky at chunk boundaries with slow async inference" failure with π0. 50 demos sufficed for simple spatial pick-place (10/10).
Decision impact:
 - Q02 action space: velocity targets failed (spiky teleop data), absolute position targets smooth; authors credit absolute joint commands for noise tolerance — supports absolute position over velocity — confidence M (qualitative, same servo family)
 - Q10 latency/smoothness: π0 long inference + chunking → discontinuities knocking over tools; trapezoidal C1 profiling of targets reduces oscillation — supports low-level target smoothing + faster inference — confidence M (qualitative)
 - Q13 data: 50 demos → 10/10 simple pick-place with ACT; RoboPilot ≈ VR data quality (73 vs 70%) — supports ~50 demos adequate for simple pick-place — confidence L (10 trials)
