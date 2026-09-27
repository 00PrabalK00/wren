# W4_PipetteAnEmbodiedSimulationPlatformBench — Pipette: An Embodied Simulation Platform, Benchmark, and Success-Verified Simulation Augmentation Framework for Wet-Lab Robotics (2026, arXiv 2606.12936)
Setup: Isaac Sim/Isaac Lab, 12 wet-lab tasks (4 sample/culture, 4 lid/hatch, 4 precision placement), 3 arm embodiments; 30 keyboard-teleop demos per task (DLS IK → joint targets); 3 RGB views (top, main, wrist) at 400×400, joint-target actions + gripper (8-D), 10 Hz; ACT, SmolVLA, π0 via LeRobot. Augmentation = replay each demo in simulation under perturbed lighting, camera pose, execution speed and joint-action noise, re-render all views, keep only replays passing the task success checker. Number of augmented episodes, eval trial counts and perturbation magnitudes are in a separate supplement (not available). Sim-only.
Claim: success-verified, physically re-simulated augmentation of 30 demos substantially improves VLA policies in a wet-lab benchmark.
Evidence (Table 2, category averages Unenh → Enh):
 - Sample/culture: ACT 59.5→69.3; SmolVLA 36.3→90.0; π0 41.8→53.3.
 - Hatch/lid: ACT 79.3→83.5; SmolVLA 63.0→83.5; π0 65.8→68.0.
 - Placement/relocation: ACT 42.3→24.3 (worse); SmolVLA 22.0→42.0; π0 4.3→11.0.
 - Overall (abstract): SmolVLA 40.4→71.8, π0 37.3→44.1; 26/36 policy–task combos improve.
 - Task-level (Table 3) highlights: SmolVLA remove petri dish 0→92, close centrifuge lid 6→83; ACT balance placement 58→3, pipette rack 67→5 (large degradations), ACT remove dish 0→9 only.
Ablations: none isolating which perturbation (light / camera / speed / action noise) helps; no count-matched comparison (more raw demos vs augmented replays).
Failure/limitations: sim-only; augmentation replays the same trajectories (no new state coverage beyond action noise) — perturbations of action/speed can corrupt precise contact behavior, hurting ACT on placement; trial counts unknown; unaugmented baselines had no image augmentation reported, so gain vs simple image aug unknown.
Conflicts: SmolVLA gains far more than π0 and ACT from the same augmented data — consistent with W4_LightsCamera (SmolVLA benefits strongly from appearance-diverse data) and contrasts with the intuition that bigger π0 is more data-efficient. ACT's degradation under trajectory perturbations echoes findings that noisy/perturbed demos hurt precise BC (data quality > quantity).
Relevance: We have no simulator of our scene, so the direct method isn't available; the transferable lessons: (a) with 30 demos, SmolVLA benefits massively from appearance+camera-pose variation (supports camera/lighting augmentation or re-rendered data), (b) injecting action/speed noise into demos can destroy precision placement for ACT — keep placement demos clean, (c) success-filter any synthetic data.
Decision impact:
 - Q05 augmentation: simulated lighting+camera-pose+speed+action replay aug: SmolVLA 40.4→71.8, π0 37.3→44.1; ACT mixed (placement 42.3→24.3) — L/M (sim-only, perturbations not isolated)
 - Q13 data: 30 demos/task insufficient for precision placement across all models (π0 ≤17%, SmolVLA ≤60%); perturbed trajectories can hurt precise tasks — L
 - Q12 model size: SmolVLA (~0.45B) ≥ π0 (3B) with 30 demos (71.8 vs 44.1 augmented) — L (sim)
