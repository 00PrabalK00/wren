# W3_AxisGuideGroundingRobotActionCoordinateS — AxisGuide: Grounding Robot Action Coordinate System in RGB Observations for Robust Visuomotor Manipulation (2026, arXiv 2606.06761)
Setup: LIBERO sim (256×256) + real UR5e/RG2, one front RGB cam (+ optional wrist cam). Actions = relative EEF pose (6D + gripper) in base frame. Policies: Diffusion Policy (single task) and SmolVLA (multi-task, trained FULLY incl. backbone for fairness). Method: using camera intrinsics/extrinsics + EEF pose, render 2D projections of unit base-frame +x/+y/+z directions anchored at the EEF, concatenated as extra input channels. Real: 30 rollouts per task (3 tasks); position-generalization: 120 demos Pick Up (Pear), 84 rollouts at unseen positions. Sim: 75 rollouts (25×3 seeds); position test 400 demos, 210 rollouts.
Claim: BC memorizes image→numeric-action mappings; making the action frame visible in pixels improves generalization to unseen object positions.
Evidence:
 - Unseen object positions: sim SmolVLA 52.38 → 65.71; real DP 30.12 → 50.00 (84 rollouts). TraceVLA-style cue 51.90, AimBot cue 52.38 (no gain).
 - Sim single-view DP (Table I): Pick&Place Bowl 69.33 (KYC 73.33) → 82.67; Drawer 86.67 (89.33) → 93.33; Stove 92.00 (96.00) → 100.
 - Real single-view (Table II, 30 rollouts): Grape 83.33 (KYC 86.67) → 93.33; Flip Pot 36.65 → 50.00; Close Pot 33.33 → 40.00 (KYC values for these two are 40.00 / 23.33 but column assignment is garbled in extraction).
 - Real multi-view front+wrist: Grape 93.39 → 96.66; Flip Pot 73.33 → 93.33; Close Pot 36.66 → 53.33.
 - Sim multi-view: Pick&Place Bowl 74.7 → 88.0; Put Both 78.8 → 86.7. Multi-task SmolVLA LIBERO: gains in all 4 suites; +7.5 over fully-trained SmolVLA on LIBERO-Object (figure only for other numbers).
Ablations:
 - Wrist camera (implicit, same DP, real): single-view → multi-view DP baseline: Grape 83.33 → 93.39, Flip Pot 36.65 → 73.33, Close Pot 33.33 → 36.66. Wrist cam is the single biggest lever in their table.
 - Cue design (sim Bowl, 75 rollouts): baseline 74.67; overlay+EEF 84.00; concat+center 80.00; concat+EEF unnormalized 85.30; concat+EEF normalized 88.00.
 - Calibration noise at test: extrinsic 3 cm / 6° and intrinsic 10% focal / 10 px → 61.4–65.2 vs 65.7 clean, still > 52.4 baseline.
Failure/limitations: needs camera calibration; failures remain in contact/grasp phase; small scale. Critical read: 30 real trials per cell; gains on unseen positions are interpolation between training clusters, not extrapolation; no lighting/appearance shift tested; with a moved camera the cue would be re-rendered from new extrinsics — potentially helpful for camera shift but NOT tested (only noise injection).
Conflicts: agrees with "SmolVLA drifts toward training-like configurations" (our observed failure). Complements KYC/camera-conditioning; beats it here. Poor spatial generalization of DP on sparse object placements matches data-diversity papers (placement coverage matters more than count).
Relevance: SO-101 has known URDF → EEF pose via FK is available; scene RealSense can be calibrated once (ArUco/hand-eye). Cheap extra channels, no architecture change. But SO-101 backlash makes FK EEF pose noisy (~mm–cm) — their calibration-noise test suggests tolerance to 1–3 cm. Our action space is joint-space; the idea still applies if we render EEF-anchored axis cues. Wrist-cam gain is directly relevant.
Decision impact:
 - Q11 cameras: supports adding wrist cam to front cam (real DP: Flip Pot 36.65 → 73.33) — confidence M (30 trials, UR5e).
 - Q14 robustness (object position): supports explicit action-frame cues for unseen positions (real 30.1 → 50.0) — confidence M (one task, 84 trials).
 - Q02 action space: ~ EEF-relative actions are hard to ground from pixels without a visual frame reference; weak hint that frame-grounding matters for delta EEF — confidence L.
 - Q12/Q03 (SmolVLA): full fine-tune of SmolVLA backbone used as the stronger baseline vs frozen-VLM action-expert-only — confidence L (figure only).
