# W3_SnapFlowOneStepActionGenerationforFlowMa — SnapFlow: One-Step Action Generation for Flow-Matching VLAs via Progressive Self-Distillation (2026, arXiv id not in extracted text)
Setup: SIM only. π0.5 (3B) on LIBERO 4 suites (40 tasks, 10 episodes/task = 400) and SmolVLA (~0.5B) evaluated OFFLINE only (PushT held-out MSE). Self-distillation: VLM frozen, action expert + zero-init target-time MLP trained 30k steps (bs 4, bf16, grad checkpointing; π0.5 ~40 GB, SmolVLA ~18 GB peak VRAM) mixing FM loss (α=0.5) with a consistency loss (λ=0.1) whose target is the model's own 2-step Euler shortcut velocity. Latency on A800. Chunk 50, n_act default 10.
Claim: 1-NFE generation matches/exceeds the 10-step teacher at ~3.3–3.6x lower end-to-end latency, no architecture change.
Evidence:
 - π0.5 LIBERO avg success: 10-step 97.75%; naïve 1-step 96.75%; SnapFlow 1-step 98.75% (spatial 97/96/99, object 100/99/100, goal 96/98/99, long 89/95/91 — base/naïve/SF).
 - Latency (Table 7, A800): π0.5 E2E 274.0 ms @10 steps → 81.2 ms @1 step (denoise 80% → 28%); SmolVLA 178 ms @10 steps → 50 ms @1 step (denoise 79% → 24%).
 - SmolVLA offline (PushT): MSE −8.3%, P90 −11.4%, CosSim +6.9% vs 10-step. No closed-loop SmolVLA results.
 - Offline MSE of the pretrained model increases monotonically with step count (+30.7% from 1→10 steps), yet 10-step still wins closed-loop over naïve 1-step → offline MSE is an imperfect proxy.
Ablations:
 - Execution horizon n_act on libero_10 (Table 9, success base/SF): 1 → 77/72; 3 → 88/87; 5 → 90/93; 10 → 89/91; 20 → 97/92. Re-planning every step hurts both (resampled noise + observation jitter); baseline best at 20 of 50.
 - α ∈ {0,0.3,0.7,1.0}, λ ∈ {0.01,1.0}: training stable (no numbers for success given in text).
Failure/limitations: no real robot; SmolVLA only offline; 10 episodes/task — authors note a 50-pt swing on one libero_10 task, so suite differences of 1–2 pts are noise; LeRobot eval issue may share initial states at bs=1 (authors' footnote).
Conflicts: agrees with consistency-policy / one-step diffusion literature (Consistency Policy, OneDP) that few-step generation loses little. The n_act result (n_act=1 worst) agrees with ACT/DP evidence that per-step re-sampling of a generative head causes jitter/mode switching; opposite of "always replan as often as possible". 
Relevance: Directly addresses our ~2 s SmolVLA latency: on an A800, 79% of SmolVLA E2E latency is the 10-step denoising; 1-step distillation cut it 178→50 ms. If the same proportion holds on the RTX 5060 laptop, distillation (or simply testing fewer steps first) could remove most of the denoising cost, but the VLM prefix remains. Training fits ~18 GB for SmolVLA — too much for 8 GB without further tricks (LoRA/smaller batch), so it may need a cloud GPU.
Decision impact:
 - Q10 latency: 1-step flow distillation cuts SmolVLA E2E 178→50 ms (3.56x) and π0.5 274→81 ms with no loss in LIBERO success (98.75 vs 97.75) — confidence M (sim/offline, A800 timing)
 - Q01 action head: flow matching can be run at 1 NFE after self-distillation without quality loss — confidence M (sim)
 - Q06 chunking: executing 1 step per replan is worst (77/72%); 5–20 of 50 best — confidence M (sim libero_10, 100 eps per point)
