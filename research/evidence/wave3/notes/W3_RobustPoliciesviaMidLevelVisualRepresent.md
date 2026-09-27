# W3_RobustPoliciesviaMidLevelVisualRepresent — Robust Policies via Mid-Level Visual Representations: An Experimental Study in Manipulation and Navigation (2020, arXiv 2011.06698)
Setup: RL (not imitation). Manipulation in RLBench sim (Franka, Reach, Pick+Place), single camera 64×64 RGB for scratch vs frozen ResNet-50 mid-level encoders (surface normals, depth, segmentation, denoising, …; Taskonomy, fine-tuned offline on sim images) giving 16×16×8 features; EE delta XYZ + gripper actions. Test on held-out table/floor/background colors and unseen objects. Navigation: Gibson sim → real TurtleBot, 594 real runs in 2 unseen buildings.
Claim: frozen, asynchronously trained mid-level visual features give invariances that generalize better and learn faster than learning from pixels or domain randomization.
Evidence:
 - Pick+Place (texture/color shift test): mid-level ~100% train/100% test; scratch+domain randomization train 100%→70% (DR makes learning harder), test 4%→20%; unseen-color test mid-level 100% vs DR-pixels 20%.
 - Unseen objects Pick+Place: state-based agent 2% train / 0% test; surface-normals agent 96% train / 90% unseen objects / 88% unseen green objects.
 - Sim-to-real navigation: scratch SPL 0.319, completion 0.4 (≈ blind); mid-level SPL 0.608, completion 0.7.
Ablations: better mid-level objective performance ↔ better downstream (figure only); feature ranking task-dependent but stable across sim/real (Spearman 0.77).
Failure/limitations: RL not BC; low-res sim; manipulation robustness only in sim with flat-color texture swaps; 2020-era features (pre-DINOv2/CLIP) and fine-tuned on the sim domain.
Conflicts: Consistent with later BC findings that frozen pretrained features beat scratch under visual shift (VGA LoRA vs full-FT; RoboTwin scratch ACT/DP collapse). Contrasts with papers showing end-to-end fine-tuned ImageNet ResNets do best in-distribution — the distinction is in- vs out-of-distribution evaluation.
Relevance: Supports using a frozen (or lightly adapted) pretrained encoder for our lighting/appearance shifts, and warns that trying to learn invariance purely from augmented/randomized data with a scratch encoder can make training harder. Geometry-like features (normals/depth) generalized to unseen objects — weakly supports adding depth-ish cues.
Decision impact:
 - Q03 vision encoder: frozen pretrained features > scratch pixels under texture/color shift (100% vs 20% test) — confidence L/M (RL, sim, old features).
 - Q05 augmentation: domain randomization with scratch encoder degrades training (100→70%) and still generalizes poorly (20%) — confidence L.
 - Q14 robustness: frozen mid-level features generalize to unseen objects (90%) and sim→real (0.4→0.7 completion) — confidence L/M.
