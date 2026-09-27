# W3_LanguageConditionedImitationLearningWith — Language-Conditioned Imitation Learning with Base Skill Priors under Unstructured Data (SPIL) (2023/24, arXiv 2305.19075)
Setup: CALVIN sim (Franka, static + gripper RGB cams, play data, 34 tasks, 1000 five-task chains, 3 seeds); HULC-based model with a VAE latent "skill" space = action sequences of Nh=5 steps, plus base-skill priors (translation / rotation / grasp, heuristically labeled from delta-EE magnitudes). Real: zero-shot sim→real, 10 tasks, 10 rollouts each from identical starting positions, static + gripper RGB.
Claim: predicting latent skills (5-step action chunks) regularized by base-skill priors improves zero-shot generalization to an unseen environment.
Evidence (Table I, ABC→D avg length): MCIL 0.31, HULC 0.67, SPIL 1.71 (1-task success 41.8 → 74.2%). Single env D→D: HULC 2.64 vs SPIL 2.67 (no gain in-distribution). For reference, pretrained-foundation-model methods: 3D Diffuser Actor 3.27, GR-1 3.06. Real zero-shot (Table II): HULC 3% vs SPIL 33% avg (10 tasks x 10 rollouts).
Ablations: w/o base skills avg len 1.05 (vs 1.71); Nh=4 1.58, Nh=6 1.65 vs 5 → 1.71 (flat); loss-weight changes 1.62/1.63.
Failure/limitations: critical read: real test is 10 rollouts/task from a single fixed start, zero-shot sim2real with weak absolute numbers; gain is only for environment shift; the skill-prior labeling uses hand-tuned "magic weights". Language here is CALVIN templated instructions; no language ablation.
Conflicts: matches the broader finding that predicting short action sequences (chunks/skills) helps over single-step actions (ACT, DP); skill length within 4–6 barely matters.
Relevance: low. Hierarchical skill priors are not something we'd build for a single pick-place; the only takeaway is chunk/skill-level prediction and structured latent priors helping under environment shift.
Decision impact:
 - Q14 robustness: latent skill priors improved unseen-env CALVIN 0.67→1.71 but not in-distribution (2.64 vs 2.67) — confidence L (sim, weak baseline).
 - Q06 chunking: skill length 4/5/6 → 1.58/1.71/1.65, insensitive — confidence L.
