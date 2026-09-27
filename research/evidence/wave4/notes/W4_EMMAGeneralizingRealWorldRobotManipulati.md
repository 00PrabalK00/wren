# W4_EMMAGeneralizingRealWorldRobotManipulati — EMMA: Generalizing Real-World Robot Manipulation via Generative Visual Transfer (2025/26, arXiv 2509.22407)
Setup: Agilex CobotMagic (2 PiPER arms), 3 RealSense D435i (head + 2 wrist), 640×480. pi0 and pi0.5 post-trained. Tasks: Fold Clothes (50 real demos, real-to-real), Clean Desk and Throw Bottle (20 sim demos each in Isaac Sim → sim-to-real). Generated data at 1:1 ratio. DreamTransfer = depth-conditioned (ControlNet branch) multi-view video DiT, text-guided edits of foreground/background/lighting; trained on 50k AgiBot-World clips, 131 h on 4×H20. Eval: 4 unseen foreground-object appearances × 10 trials = 40 trials/setting; behavior score 0–5 + SR.
Claim: depth-conditioned, multi-view-consistent generative appearance transfer of demos (+ quality filter + hard-sample reweighting AdaMix) gives large zero-shot gains on unseen object appearances.
Evidence (Table 2, avg SR over 3 tasks, unseen appearances):
 - pi0: No aug 30%; Cosmos-Transfer1 50%; DreamTransfer (no filter) 65%; +FixMix (filter) 68.3%; +AdaMix 79.2%.
 - pi0.5: 43.3 / 63.3 / 73.3 / 75.0 / 82.5%.
 - Fold Clothes pi0: 10% → 65% (DreamTransfer) → 77.5% (AdaMix); pi0.5: 27.5 → 75 → 82.5.
 - Clean Desk pi0: 67.5 → 77.5 → 90; Throw Bottle pi0: 12.5 → 52.5 → 70.
 - Video quality: DreamTransfer multi-view matched pixels 3270 vs 2097 (Cosmos), Sq.Rel depth 0.54 vs 0.71.
Ablations:
 - Mix ratio (figure only, qualitative): gains peak at 50% generated; 75–90% plateau, 90% hurts Throw Bottle (fast, precise).
 - Quality filter: removes 5–8% of generated data; FixMix vs unfiltered +3.3 (pi0) / +1.7 (pi0.5) pts.
 - AdaMix λ (γ=1): λ=1 ≈ uniform; λ=10 best; 20/100 degrade (figure only).
 - Metric ablation (Throw Bottle): all three 70%; subsets 62.5 / 55 / 55%.
 - AdaMix execution: avg time 32.8 → 30.0 s; smoothness 2.0 → 1.9 rad/s²; joint over-limit 43.6 → 42.9 frames.
Failure/limitations: generator requires large GPU training (4×H20, 131 h) and multi-view depth; eval tests only unseen object appearances (not lighting/camera pose), 40 trials/setting; baselines are big VLAs fine-tuned on 20–50 demos with single appearance, so no-aug numbers are low by construction. Sim-to-real claim relies on Isaac Sim demos.
Conflicts: consistent with generative augmentation papers (RoboEngine, GreenAug, ROSIE-style): appearance diversity in training data is the lever for novel-object/background robustness. Also agrees with "don't go above ~50% synthetic" findings. Compared with classic photometric/crop augmentation it targets semantic appearance shifts that color jitter cannot cover.
Relevance: our "different-looking pumpkin" failure is exactly this setting (single-appearance real data, zero-shot new appearance). We have RealSense depth, so a depth-conditioned editing pipeline is plausible, but training DreamTransfer is out of our compute budget; cheaper paths: off-the-shelf image-editing / ControlNet-depth per frame (loses temporal consistency) or simply collecting demos with 3–5 pumpkin variants. Keep generated ratio ≤50%.
Decision impact:
 - Q05 augmentation: supports generative appearance transfer (pi0 avg SR 30 → 65–79% on unseen appearances); cap synthetic at ~50% — confidence M (real, 40 trials/setting, 3 tasks).
 - Q14 robustness: novel-object appearance is solved by data-side appearance diversity rather than model changes — M.
 - Q13 data: hard-sample reweighting adds +7.5–10.9 pts; filter bad synthetic samples — L.
