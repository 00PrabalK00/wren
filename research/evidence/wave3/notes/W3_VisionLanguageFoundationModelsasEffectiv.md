# W3_VisionLanguageFoundationModelsasEffectiv — Vision-Language Foundation Models as Effective Robot Imitators (RoboFlamingo) (2023, arXiv 2311.01378)
Setup: CALVIN sim only (Franka, static + gripper cams, 34 tasks, 5-instruction chains, 1000 chains eval), trained on language-annotated ~24k-step subset per split; OpenFlamingo backbones 3B–9B total (≈1B trainable: resampler + gated cross-attn + policy head; LLM frozen); per-frame VLM + LSTM policy head over history; relative EE pose (MSE) + gripper (BCE); 8x A100, 13–26 h per epoch. No real robot.
Claim: lightly fine-tuning an open VLM with a separate history-aware policy head gives SOTA language-conditioned imitation on CALVIN.
Evidence (Table 1, avg completed chain length): ABCD→D: RoboFlamingo 4.09 vs HULC 3.06 (full data) / 2.90 (lang), RT-1 re-impl 2.45, MCIL 0.40. ABC→D (unseen env): 2.48 vs RT-1 0.90, HULC 0.67. Enriched GPT-4 instructions: 1.85 (2.12 with frozen embedding layer) vs HULC 1.82.
Ablations:
 - Frozen robotics encoders (Table 7, ABCD→D): R3M frozen 0.10, Voltron frozen 0.11, Voltron fine-tuned 2.08, RoboFlamingo 4.09; ABC→D Voltron frozen 0.03 vs fine-tuned 1.00.
 - No VL pretraining / no VL fine-tuning (only head): "large margin" drop (figure only, qualitative).
 - Full-model fine-tuning (3B trainable) vs partial (1B): 0.50 vs 4.09 (Table 8) — full fine-tune collapses.
 - Policy head / history: MLP w/o history worst < MLP w/ history in VLM < GPT ≈ LSTM head (figure only, qualitative).
 - Model size, full data: M-3B-IFT 4.09 best vs M-9B 3.97, L-9B 2.79 (Table 2) — size not decisive; with 10% language data (Table 3): M-3B 0.05, M-3B-IFT 0.13, G-4B 0.48, G-4B-IFT 0.55, M-9B 0.83 → bigger VLM more data-efficient.
 - Open-loop action sequence without retraining degrades; retraining with jump-step data alleviates (figure only).
 - Co-training with COCO/VQA: robot perf 4.09 → 3.76 (ABCD→D), preserves VL ability (COCO/VQA collapse after plain fine-tune: VQA 43.86 → ... fine-tuned model loses captioning).
Failure/limitations: sim only; enormous compute (8xA100); per-step prediction (no chunking); relative EE actions.
Conflicts: model-size result (bigger VLM better at low data) contradicts small-model-in-low-data findings (e.g., PolarNet single-task small better; SeedPolicy) — but here "low data" is still ~2.4k annotated steps across 34 tasks and the extra params are pretrained, not scratch. Frozen R3M/Voltron failing agrees with TOTO (frozen generic features weak).
Relevance: low-moderate. Not deployable on 8 GB/latency budget. Transferable: (1) frozen off-the-shelf robot representations (R3M, Voltron) are nearly useless without fine-tuning; (2) full fine-tuning of a large pretrained model can collapse — partial/PEFT fine-tuning safer (relevant to how we fine-tune SmolVLA/any VLM); (3) history helps on CALVIN.
Decision impact:
 - Q03 vision encoder: weakens frozen robotics encoders (R3M 0.10, Voltron 0.11 vs Voltron fine-tuned 2.08 avg len) — confidence M (sim, big gap).
 - Q12 model size: pretrained capacity helps at low data (10% data: 3B 0.05–0.13 vs 9B 0.83) but full fine-tune of 3B collapses (0.50 vs 4.09) — confidence L (sim, not our scale).
 - Q07 history: supports history via policy head (LSTM/GPT) over single frame — confidence L (figure only).
 - Q08 language: frozen word embeddings improve paraphrase robustness (1.85 → 2.12) — confidence L.
