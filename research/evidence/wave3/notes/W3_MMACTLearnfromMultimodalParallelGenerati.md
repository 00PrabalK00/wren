# W3_MMACTLearnfromMultimodalParallelGenerati — MM-ACT: Learn from Multimodal Parallel Generation to Act (2025/26, arXiv; github HHYHRHY/MM-ACT)
Setup: unified discrete-token VLA initialized from MMaDA (masked-diffusion LLM, ~8B class); text (sub-task plan), future image (next frame after chunk) and action tokens decoded by block-level masked parallel decoding; action chunk 8 decoded in ONE forward pass. LIBERO (official data, per-suite models ~11k steps), RoboTwin 2.0 Agilex Piper 8 tasks (500 domain-randomized expert episodes/task, eval in unseen settings), real Franka FR3 with wrist D435 + third-person D435i, 100 teleop demos/task, 3 tasks, 20 trials. Actions: EE delta pose (LIBERO, Franka), absolute EE pose (RoboTwin). Batch 128.
Claim: co-training action with text planning and future-image prediction from a shared context improves action generation (+9.25 pts OOD in RoboTwin) with fast one-step action decoding.
Evidence:
 - LIBERO avg: MM-ACT 95.0 vanilla / 96.3 with text planning on Long (88.0 -> 93.0); pi0 94.2, OpenVLA-OFT 95.4, UniVLA 95.5.
 - RoboTwin 8 unseen tasks avg: pi0 48.13, OpenVLA-OFT 23.13, MM-ACT vanilla 43.13, +text 46.5, +image 48.75, +text&image 52.38.
 - Real Franka (20 trials): press button pi0 75 / OFT 70 / MM-ACT 80; stack 70/50/70; sort 65/56/66; avg 70.0 / 58.6 / 72.0.
Ablations:
 - Action decoding: one-step PD cs=8: 43.13 (0.22 s); re-mask 6 steps cs=8: 42.38 (1.06 s); one-step cs=16: 43.75 (0.23 s); re-mask cs=16: 56.75 (1.06 s). Iterative refinement only helps for longer chunks, at ~5x latency.
 - Robot state in image-context: +image 48.75 -> 51.50 with state; in text-context 46.50 -> 43.50 (state hurts there).
 - Text planning accuracy drops 81.5 -> 68.7 after joint action training (text overfits fast).
Failure/limitations: huge backbone (training GPU not stated in main text; 0.22 s/chunk), multi-task sim with 500 demos/task, real gain over pi0 is +2 pts avg on 20 trials (noise). Aux-image gain measured in sim only with scripted demos.
Conflicts: aux future-image prediction gain (+5.6 sim) is consistent with SpatialVAM/other world-model co-training notes; real advantage over pi0 negligible.
Relevance: low — model too large for 8 GB laptop inference; the transferable points are (i) future-frame prediction as auxiliary target gives a few pts, (ii) iterative decoding costs ~5x latency for little gain at short chunks.
Decision impact:
 - Q09 aux objectives: supports future-image co-training (+5.62 sim, +9.25 with text) — confidence L (sim, 500 demos, big model).
 - Q01 action head: discrete masked-token one-step decoding competitive (real 72 vs pi0 70) — confidence L.
 - Q10 latency: one-step vs 6-step re-mask 0.22 s vs 1.06 s with equal SR at chunk 8 — confidence L.
