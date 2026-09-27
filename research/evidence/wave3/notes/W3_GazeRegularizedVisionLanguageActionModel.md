# W3_GazeRegularizedVisionLanguageActionModel — Gaze-Regularized Vision-Language-Action Models for Robotic Manipulation (2025, arXiv id not in text)
Setup: π0 (primary) and OpenVLA fine-tuned on LIBERO (4 suites) and ALOHA-Sim (transfer cube, peg insertion), 3 seeds; synthetic gaze heatmaps from a pretrained gaze-prediction model, temporally aggregated over ±T frames, converted to patch distributions; KL loss between language→visual-token attention and gaze distribution, weight λ. Real robot: 3 tasks (cube→plate, cup→container, multiple cups), robot/demos/trial counts not specified in text.
Claim: a training-only KL regularizer aligning VLA attention with (predicted) human gaze improves success, convergence speed and robustness to lighting/noise with no inference cost.
Evidence:
 - LIBERO-Spatial (π0): 85.9% → 95.5%. LIBERO average +8.8 pts at 30k steps (+4.5 at 10k); LIBERO-10 +11.8. ALOHA-Sim avg +4.4 (transfer cube +5.0?; peg insertion small; table fragments garbled).
 - OpenVLA LIBERO: Spatial 76.0→82.2, Object 79.5→86.1, Goal 72.5→76.8, 10 45.9→51.5, avg 68.5→74.2.
 - Real (base → gaze, at 20k / 40k steps): cube→plate 4/32 → 6/44%; cup→container 24/64 → 28/72%; multiple cups 5/30 → 5/40%.
 - Perturbations (LIBERO, simulated): lighting Spatial 77.2 → 89.1; camera noise Spatial 82.1→91.3, Object 85.8→93.5, Goal 79.6→88.9.
Ablations: λ=0.001 → 90.8% avg; λ=0.01 → 82.2% (≈ baseline); λ=10 → 41.6% (catastrophic). Synthetic vs real eye-tracking gaze overlap: 68.6% top-32 IoU, 82.3% top-64.
Failure/limitations: Critical read: baseline π0 at 85.9% on LIBERO-Spatial is well below published π0 numbers (~96%), suggesting an under-trained baseline — gains may shrink at convergence; real-world trial counts and setup not reported; very sensitive to λ (one order of magnitude flips gain to nothing). Only applies to transformer attention over visual tokens.
Conflicts: consistent with other "attention/object-centric focus" papers (e.g. FocusVLA, masking distractors) that focusing on task-relevant regions improves robustness to lighting/noise; contrasts with papers showing augmentation alone gives similar robustness — not compared here.
Relevance: low-moderate. We could apply a similar weak auxiliary attention prior in a small transformer policy (e.g., toward pumpkin/tray masks from a detector rather than gaze) to target our lighting/appearance failures, but evidence is VLA/sim-heavy and the regularizer is fragile.
Decision impact:
 - Q09 auxiliary objectives: weak attention-alignment prior (λ≈1e-3) +4–10 pts sim, +8–12 pts real at 40k steps; strong prior destroys performance — confidence L (under-trained baselines, unreported real protocol).
 - Q14 robustness: gap widens under simulated lighting (+11.9) and noise (+9) — confidence L (sim perturbations only).
