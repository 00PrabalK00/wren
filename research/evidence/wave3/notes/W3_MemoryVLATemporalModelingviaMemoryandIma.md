# W3_MemoryVLATemporalModelingviaMemoryandIma — MemoryVLA++: Temporal Modeling via Memory and Imagination in VLA Models (2026, arXiv 2606.09827)
Setup: 7B VLM (perceptual + cognitive tokens) + memory bank with token-merge consolidation and gated fusion + frozen world model imagining future latents + ~300M diffusion action expert (DDIM 10 steps, CFG 1.5). Trained on 8 A100/H20. Real: Franka and WidowX with 3 fixed RealSense D435 (640x480 at 30 fps, downsampled to 224, frames kept on >=1 cm / 0.4 rad EE motion), Dual-ARX5 with a wrist cam. General tasks use 50–150 demos (15–25 trials), long-horizon tasks 200–300 demos (10–15 trials). Sim: LIBERO, SimplerEnv, Mikasa-Robo, CALVIN, LIBERO-Plus.
Claim: memory of past interactions + imagination of future latents improve VLAs on general, memory-dependent and dynamics-dependent tasks.
Evidence (Table VI, real): general manipulation avg OpenVLA 31 / pi0 72 / CogACT 76 / MemoryVLA 85. Memory-dependent tasks avg CogACT 57 -> MemoryVLA 83 (+26; e.g. Seq. Push Buttons +43). Imagination-dependent (conveyor, bag zip) avg pi0 49 / CogACT 49 / MemoryVLA 65 / MemoryVLA++ 77. OOD real robustness (background, distractors, lighting, objects, containers, occlusion) is figure-only; qualitatively "minor drops". LIBERO-Plus zero-shot 73.1% vs OpenVLA-OFT +5.2 pts (table garbled).
Ablations (Table VII/VIII):
 - Memory length small/default/large: SimplerEnv 67.7/71.9/67.7; LIBERO-Long-90 94.2/95.6/95.6; real Clean&Count 78/84/81. Both too little and too much memory hurt.
 - Gated vs additive fusion: 71.9 vs 67.7 (SimplerEnv); token-merge vs FIFO: 71.9 vs 66.7. Perceptual+cognitive memory 71.9 vs 63.5/64.6 for either alone.
 - Imagination: 1 denoise step 44.4 ~ 3 steps 44.6 ~ 5 steps 43.6; horizon 4/8/16: 43.4/43.8/44.4; frozen WM 44.4 vs updated 42.8.
Failure/limitations: model scale (7B + 300M) is ~10x beyond our GPU. Trial counts are small (10–25). The CogACT baseline differs from ours. The +9 on general tasks mixes memory with a stronger architecture.
Conflicts: contrasts with "history hurts in low data" (copycat) results. The difference is that the memory here is compressed, gated and retrieved on top of a large pretrained VLM with 50–300 demos, whereas copycat findings concern small from-scratch policies with raw stacked frames.
Relevance: low-medium. Architecture unusable on 8 GB. The transferable points are that memory length has a sweet spot and that general short tasks gained only modestly (+9) from memory.
Decision impact:
 - Q07 history: ~ compressed/gated memory gives +9 pts on short real tasks and +26 on memory tasks for a 7B VLA; optimal length is intermediate — confidence L-M (large model, small n)
 - Q09 auxiliary (future prediction): ~ frozen world-model imagination +12 on dynamics tasks; horizon/denoise steps barely matter (43.4–44.6) — confidence L
 - Q12 model size: ~ evidence only for 7B-scale models; not transferable to 8 GB — confidence L
