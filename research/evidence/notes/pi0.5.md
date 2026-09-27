# pi0.5 — π0.5: a Vision-Language-Action Model with Open-World Generalization (2025, arXiv 2504.16054)
Setup: π0 architecture (PaliGemma 2B-LM + SigLIP-400M, plus a 300M action expert with width 1024 / mlp 4096 / depth 18). Changes vs π0:
 - State goes in as DISCRETISED text tokens.
 - τ is injected via adaptive RMSNorm in every expert layer.
 - One model does both high-level subtask prediction (text) and low-level actions.
 - Chunk is 50 steps at 50 Hz, with 10 denoising steps.
Training is two-stage. Pretrain 280k steps with ALL actions as FAST discrete tokens (α=0, no expert). Then post-train 80k steps, adding a freshly initialised flow expert, with loss = CE(text+FAST) + 10·flow-MSE. FAST and flow action tokens cannot attend to each other. The VLM never attends to the expert.
Data sources:
 - MM: ~400 h of mobile manipulation in ~100 homes.
 - ME: static arms in many homes.
 - CE: lab cross-embodiment data + OXE.
 - HL: subtask + bounding-box annotations.
 - WD: captioning / VQA / detection.
 - VI: verbal-instruction demos, post-training only.
97.6% of stage-1 examples are not MM. Actions are target joint AND end-effector poses (a control-mode string in the prompt), normalised per dim to [−1,1] by the 1%/99% quantiles and zero-padded to 18–19 dims. Robots: two mobile bimanual platforms with 4 cams (front, back, 2 wrist). Low-level inference uses the wrist + front cams. PD tracking at 50 Hz.
Augmentation (appendix): RandomCrop 95%, then resize, Rotate ±5°, ColorJitter (brightness 0.3, contrast 0.4, saturation 0.5), applied to all images.
Eval: all in UNSEEN homes. Mock homes: 4 tasks × 10 trials = 40 per policy, interleaved, with two-sided t-tests. Real homes: 3 homes.
Claim: co-training on heterogeneous robot + web + high-level data lets a VLA do 10–15 min multi-stage cleaning in entirely new homes.
Evidence (almost all bar charts, so figure only):
 - Scaling training locations 3 → 12 → 22 → 53 → 82 → 104, with 40k post-training steps so every model sees the same number of unique samples. Task progress rises roughly monotonically. The 104-location model ≈ a control trained ON the test homes.
 - Without the co-training pretraining (MM-only), both "trained on test homes" and "104 locations" are "significantly worse". Figure only.
 - Language following on in-distribution vs unseen object categories also rises with #locations. In-distribution rises faster than OOD. Figure only.
 - π0.5 > π0-FAST+Flow (same hybrid recipe, robot data only) > π0 (flow only), even when π0 is trained to 300k steps. Language-follow rate: π0.5 slightly > π0-FAST+Flow >> π0 (Fig 15), which the authors attribute to discrete-token training.
Ablations:
 - Remove ME or CE → significant drop, larger when both are removed. The drop is concentrated in Items-in-Drawer and Dishes-in-Sink.
 - Remove WD → not significant on mock-home task progress, but significantly worse on OOD-object language following and on high-level inference.
 - High-level variants (Fig 13): full π0.5 HL > implicit-HL (HL data in training, no HL inference at run time) > human-oracle HL. No-HL-data, no-VI (VI is ~11% of HL examples) and no-WD are significantly worse. Zero-shot GPT-4 as HL is worst.
Failure/limitations: authors list unfamiliar drawer handles, cabinets physically hard to open, partial observability (arm occluding a spill), HL distracted (opening/closing a drawer repeatedly), only simple prompts, short context and no memory. Critical read:
 - No exact numbers are given anywhere, only bars with significance claims.
 - "New homes" still means the same robot, same task families, and ~400 h of in-domain-embodiment data from 100 homes. Generalisation comes from environment diversity, not from few demos.
 - None of the ablations touches the action-head design.
Conflicts:
 - Agrees with KnowledgeInsulation (same lab, same recipe) that discrete-token pretraining plus a late flow expert beats flow-only π0 on both speed and language.
 - Agrees with UMI and DataScalingLaws that the number of distinct environments drives OOD generalisation.
 - Web data does not help motor task progress here and only helps semantics for unseen objects. For a single-object task with no language, that source is mostly irrelevant.
Relevance:
 - The transferable pieces for a 10–50M SO-101 policy are narrow.
 - (a) Their exact augmentation recipe (95% random crop, ±5° rotation, strong colour jitter) is a cheap, proven default for lighting/camera robustness.
 - (b) Quantile (1/99%) action normalisation is robust to teleop outliers, which matters for our servo jitter spikes.
 - (c) The strongest robustness lever is scene/environment diversity in the demos, not model tricks. Varying lighting, background and object instances across our 50–100 demos should matter more than architecture.
 - (d) Subtask labels as auxiliary targets help even without HL inference ("implicit HL"). A cheap analogue for us is a phase label (reach/grasp/transport/place) as an auxiliary classification head. That transfer is my speculation, not tested at small scale.
Decision impact:
 - Q05 augmentation: supports random crop 95% + rotate ±5° + ColorJitter(0.3/0.4/0.5) as default — L/M (used, not ablated).
 - Q13 data: supports maximising distinct scenes/environments, with performance rising 3→104 locations to ≈ test-env-trained level. Diversity > same-env repetition — M (figure only, strong design, 40 trials/pt).
 - Q14 robustness: new-environment generalisation comes from diverse co-training data. Web data helps only for unseen object CATEGORIES, not task progress — M.
 - Q09 aux objectives: supports auxiliary subtask/phase prediction. Implicit-HL (training-only HL labels) is second best, above no-HL — L/M (large model, language labels).
 - Q01 action head: discrete-token pretraining + flow expert post-training > flow-only, but only relevant with a large backbone and huge data — L for us.
 - Q02 action space: absolute target joint/EE poses with per-dim 1–99% quantile normalisation — L (not ablated).
