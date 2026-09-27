# FLOWER — FLOWER: Democratizing Generalist Robot Policies with Efficient Vision-Language-Action Flow Policies (CoRL 2025, arXiv 2509.04996)
Setup: Florence-2-L with the decoder removed (encoder only; "intermediate fusion") feeds an 18-layer, 1024-d rectified-flow transformer through cross-attention. It uses action-space Global-AdaLN (shared modulation weights plus per-action-type signals and per-layer LoRA) and per-action-type encoders/decoders. 947M params. Inference VRAM is 1.85 GB, with 4 flow steps (8 for bimanual). Pretraining: an "OXE-soup" of 8 datasets (~250k trajectories, 75% Droid / Google / Bridge; 74% delta-EEF, 26% joint), chunk 20, single static image, 360k steps in 48 h on 4×H100 (~200 GPU-h). Fine-tunes: CALVIN up to 40k steps (4 GPUs × batch 8, "6 h"), LIBERO 30k steps. Real: Franka kitchen, 20 tasks, 417 kinesthetic-teach trajectories (45 min total, ~21 per task), 2 static cams, joint-state actions at 6 Hz, 5 trials per task. Generalization tests with 3 trials per cell.
Claim: pruning the VLM and giving capacity to a strong flow head gives a <1B VLA competitive with 3–7B VLAs, at ~1% of their pretraining compute.
Evidence:
 - CALVIN ABC 4.53 (SoTA at the time), ABCD 4.67, D 4.35. LIBERO avg (S/O/G/L) 96.9, with Long 94.9. LIBERO-90 94.7. SIMPLER Bridge 40.0 (OpenVLA 1.0, Octo 16). SIMPLER Google 31.9 (RT-1X 42.4).
 - Real kitchen multi-task: FLOWER 61% vs OpenVLA 31%, CrossFormer 22%, Octo 10%.
 - Real generalization (FLOWER vs OpenVLA): novel object 33.3 vs 10.0. Flashlight-only lighting 50.0 vs 25.0. Background distractors 69.5 vs 41.7. New compositions 51.1 vs 16.7.
 - Inference on an RTX 4090 (bf16, chunk 50):
   - DP (0.26B): 130.7 Hz, 0.341 s, 517 MB
   - OpenVLA: 6.1 Hz, 0.164 s, 14.6 GB
   - π0: 288 Hz, 0.104 s, 6.7 GB
   - FLOWER with late fusion: 287 Hz, 0.055 s, 2.2 GB
   - FLOWER: 311 Hz, 0.052 s, 1.85 GB
 - Aloha sim (50 demos/task, 500 evals): FLOWER beats ACT on Insertion "by a considerable margin" and is comparable on Transfer. DP solves neither. Numbers are figure only.
Ablations (3 seeds, ≤100k steps):
 - Fusion (Florence: CALVIN-ABC success / LIBERO-Long): early 57.1 / 33.4, intermediate 89.5 / 93.4, late 71.2 / 61.8. SmolVLM: early 25.8 / 44.5, intermediate 72.1 / 70.7, late 66.3 / 69.2. The text says late = 73%; the table says 61.8.
 - SmolVLM layer pruning (C-ABC / L-Long): full 66.3 / 69.2, drop 20% 68.6 / 71.8, drop 30% 72.1 / 70.7, drop 50% 66.4 / 62.5.
 - Florence (detection/grounding-pretrained) > SmolVLM (general VLM) as the backbone.
 - CALVIN-ABC Avg. len. My reconstruction of Table 3 from split text, so treat the mapping as M confidence:
   - FLOWER 4.44
   - standard AdaLN 4.43 (Global-AdaLN saves 20% params at no cost)
   - L1 head instead of flow 3.33
   - constant LR 4.40
   - FROZEN VLM 2.65
   - small Florence 4.26
   - no VLM 3.42
   - discrete tokens 1.12
   - small head (384-d, 6 layers) 2.60
 - Pretraining type (Aloha joint-space): droid-joint-only pretraining is best "by a considerable margin". Cross-action-space pretraining is WORSE than training from scratch.
Failure/limitations: authors cite iterative sampling, only 3 action spaces tested, weak SIMPLER-Google, and ~1B params that may still be heavy for real-time use; 8 of 10 benchmarks are sim. Failure modes: ~1 cm positioning misses at workspace boundaries (they suspect normalization), loops before completion, excess force. Critical read:
 - Only 5 trials per real task and 3 per generalization cell.
 - Baseline fine-tunes were constrained (OpenVLA at batch 1).
 - The 6 Hz real data means huge chunks in time.
Conflicts:
 - Frozen VLM is very bad here (2.65 vs 4.44), which conflicts with SmolVLA's frozen VLM (works with robot pretraining) and VLA-Adapter's frozen variant (86.4). Resolution: FLOWER prunes the decoder and relies on fine-tuning the encoder, while SmolVLA/VLA-Adapter keep the LLM layers and add a query interface.
 - Flow > L1 agrees with SmolVLA and disagrees with VLA-Adapter/OFT.
 - "Cross-embodiment pretraining worse than scratch on joint-space Aloha" agrees with X-VLA (naive heterogeneous pretraining −14.6) and with SmolVLA's in-embodiment pretraining gain: pretraining only helps when the action space matches.
Relevance: FLOWER is released with weights, runs in <2 GB, and takes ~52 ms per chunk on a 4090, so it would run on our laptop. But its evidence says the VLM must be fine-tuned, and full fine-tuning of 947M with AdamW is ~15 GB of states. That means 8 GB needs LoRA or 8-bit optimizers, which is untested. Pretraining is mostly delta-EEF; our SO-101 is joint-space, and FLOWER's own Aloha result shows mismatched pretraining can be worse than scratch. The real lighting/distractor/novel-object tests are the only real robustness numbers in this batch, though with tiny trial counts.
Decision impact:
 - Q01 action head: supports flow over L1 (4.44 vs 3.33) and over discrete tokens (1.12) — M.
 - Q03 vision: supports a grounding/detection-pretrained VLM (Florence-2) using intermediate features; fine-tune rather than freeze (2.65 vs 4.44) — M.
 - Q12 model size: supports a high-capacity action head (small head 2.60) over a large LLM; prune 30–50% of VLM layers — M.
 - Q13 pretraining: cross-embodiment pretraining can hurt when the action space differs; joint-space pretraining helps joint-space tasks — M (sim Aloha, figure only).
 - Q10 latency: 4-step flow at 52 ms / 1.85 GB on a 4090 — M/H (clean measurement).
 - Q14 robustness: VLA beats OpenVLA under flashlight lighting (50 vs 25) and background distractors (69.5 vs 41.7) — L (3 trials per cell).
