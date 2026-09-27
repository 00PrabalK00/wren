# W3_SeeSelectivelyActAdaptivelyDualLevelStru — See Selectively, Act Adaptively: Dual-Level Structural Decomposition for Bimanual Robot Manipulation (2026, arXiv 2606.13279)
Setup: pi0.5 backbone fine-tuned with LoRA (30k steps, bs 16, chunk H=50, 3 cams 224x224: external + 2 wrist). Adds View-Selective Router (sigmoid weight per wrist view, from external view + language/state) and interaction-aware MoE (coordinated vs per-arm LoRA experts with view/action masks), routers supervised by KNN-propagated labels from 10% hand-annotated episodes. Sim: RoboTwin 2.0, 6 bimanual tasks, 50 demos/task (Easy), eval Easy + Hard (randomized clutter/visuals), 100 rollouts. Real: 3 six-stage bimanual tasks, 40 demos/task, 10 trials; Hard = unseen object instances + 4 distractors.
Claim: re-weighting wrist views by task-stage relevance and routing action generation by interaction mode improves bimanual success and robustness over a monolithic VLA.
Evidence (Table I, avg success Easy / Hard, 50 demos, 100 rollouts):
 - From-scratch/small: ACT 35.3 / 0.2; DP 24.3 / 0.0; RDT 32.3 / 7.5; TwinVLA 35.3 / 4.5; InterACT 47.5 / 4.7; DIF 58.0 / 0.8.
 - pi0.5 variants: baseline 61.5 / 22.3; LoRA 2x 61.7 / 21.0; VSR only 67.8 / 40.7; IAMoE only 74.5 / 44.8; no view masks 72.8 / 42.3; full 81.2 / 58.0.
 - Real Easy full-task success R1–R3: baseline 40/60/30 vs ours 90/100/80. Real Hard (unseen objects + distractors): baseline 10/20/10 vs ours 40/60/60.
Ablations: view router alone +18.4 pts Hard (S2 blocks-ranking: +23 Easy, +37 Hard); removing expert view masks on S3–S6: 84.8 -> 76.5 Easy, 56.3 -> 38.0 Hard; extra LoRA capacity gives nothing (41.3 vs 41.9 overall).
Failure/limitations: needs frame-level router labels (10% of episodes hand-annotated); bimanual-specific; 10 real trials; everything built on a 3B VLA.
Conflicts: Small from-scratch policies (ACT, DP) collapse to ~0% under visual randomization with 50 clean demos — same pattern as SeedPolicy entry (ACT 1.74, DP ~1%) — while pretrained pi0.5 retains 22%. Suggests visual robustness comes from pretraining/data, not architecture, unless structural priors (view gating) are added.
Relevance: Moderate. Single-arm SO-101 has one wrist cam, so IAMoE is irrelevant; but the view-router result says "down-weighting an irrelevant/distracting camera by task phase" helps robustness under distractors (+18 pts Hard). A cheap analogue: modality/view dropout during training so the policy does not depend on one view. Strong warning: ACT/DP trained on 50 clean demos are near 0% under visual shift.
Decision impact:
 - Q14 robustness: small scratch policies (ACT 35.3 -> 0.2, DP 24.3 -> 0.0) collapse under visual randomization with 50 clean demos; pretrained VLA 61.5 -> 22.3 — confidence M-H (sim, 100 rollouts, agrees with other RoboTwin papers).
 - Q11 cameras: learned per-phase wrist-view gating improves Hard success 22.3 -> 40.7 (alone) and helps with distractors in real — confidence M.
 - Q12 model size: capacity (LoRA 2x) is not the bottleneck; structure is — confidence L-M.
 - Q03 vision encoder: pretrained VLA backbone keeps nonzero Hard success where scratch ResNet policies fail — confidence M.
