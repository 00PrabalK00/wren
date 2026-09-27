# W3_TowardsSynergisticGeneralizedandEfficien — Towards Synergistic, Generalized, and Efficient Dual-System for Robotic Manipulation (RoboDual) (2024, arXiv 2410.08001)
Setup: Generalist = OpenVLA (Prismatic-7B) LoRA-tuned to output 8-step discretized action chunks (~4 Hz, 3.9 Hz alone). Specialist = 20M-trainable-param DiT diffusion policy (frozen DINO ViT for RGB; small 6-layer ViTs for depth/tactile; perceiver resampler 8 queries/input; proprio via AdaLN; cross-attn to generalist action+task latents; generalist's discrete actions concatenated with noisy actions), chunk ks=8, DDIM 5 steps (x0-prediction), CFG 3 on generalist latents/proprio, temporal aggregation w_i = exp(−0.1·i). Latency-aware training: specialist sees observations leading the generalist output by random offset τ ∈ [0, kg]. Real: ALOHA-style arm (7-DoF actions), ONE third-view RGB 192×256, 20 Hz non-blocking controller, 20–120 demos/task, 15 runs per task. Sim: CALVIN ABC→D.
Claim: slow VLA generalist + fast lightweight diffusion specialist beats either alone in success, generalization, data efficiency and control rate.
Evidence:
 - CALVIN ABC→D avg len: generalist-only 3.27 → RoboDual 3.66; free-form GPT-4 instructions: RoboDual 3.47 vs LCB 1.78, RoboFlamingo 0.40.
 - Real generalization (Table 3, 15 runs): position / distractor / unseen background / novel object → avg
   ACT 46.7/26.7/0/13.3 → 21.7; DP 53.3/40.0/26.7/40.0 → 40.0; Octo 20.0/60.0/6.7/6.7 → 23.4; OpenVLA 26.7/73.3/20.0/46.7 → 41.7; RoboDual single-task 93.3/80.0/60.0/46.7 → 70.0; multi-task 86.7/73.3/53.3/60.0 → 68.3.
 - Data efficiency, real "put block into bowl" (Table 4b): 5 demos ACT 0 / DP 20.0 / RoboDual 73.3; 10 demos 6.7 / 20.0 / 80.0; 100 demos 46.7 / 53.3 / 93.3.
 - CALVIN data efficiency: 5% data RoboDual 3.59 vs RoboFlamingo 1.35.
 - Latency: specialist 0.035 s/inference → 15 Hz on A5000 Ada; OpenVLA 3.9 Hz causes jitter/pauses and failure to fine-adjust before grasping.
 - Training: specialist ~1 h on 8×A100 adds +0.25 len (3.27 → 3.52) vs 1,400 GPU-h generalist.
Ablations (CALVIN, figure values): removing generalist discrete-action conditioning −0.8 len (as stated); removing task latents −0.14; adding depth/tactile/gripper-camera to the specialist each improve (figure only, range ~3.52–3.66); cross-attention ≥ in-context > FiLM conditioning (small differences).
Failure/limitations: assumes constant inference times (fixed generalist:specialist ratio); generalist outputs discrete actions only; 15 trials per cell; single camera real. Baselines ACT/DP are from scratch; ACT at 0% unseen background is typical of unaugmented from-scratch policies.
Conflicts: Supports "small specialist + big prior" hierarchy (like HiRT, Hi Robot). Notable: DP > ACT on every generalization axis and at low data (5–10 demos: DP 20 vs ACT 0–6.7) — contrasts with ACT's claims of 50-demo efficiency; here ACT with 100 demos only 46.7.
Relevance: HIGH conceptually for our latency problem (SmolVLA 2 s on laptop): split into a slow semantic model and a ~20M fast diffusion specialist at 15 Hz with 5 DDIM steps + temporal aggregation; latency-aware training (random offset between slow-model output and current observation) is a directly usable trick for async inference. But generalist = 7B OpenVLA won't fit 8 GB; a smaller generalist (or none) needed. Specialist recipe (frozen DINO + resampler + small DiT, chunk 8, DDIM 5, exp temporal aggregation) fits our budget.
Decision impact:
 - Q10 latency/async: supports fast small specialist + latency-aware (random-delay) training + exponential temporal aggregation; 3.9 Hz VLA → jitter/pauses — confidence M (real, 15 runs; mechanism ablation not isolated).
 - Q12 model size: 20M-param diffusion specialist sufficient for control when guided; from-scratch 5-demo regime DP 20% vs guided 73% — confidence M.
 - Q14 robustness: VLA-guided specialist 70 avg vs DP 40 vs ACT 21.7 on position/distractor/background/novel object — confidence M (15 runs/cell).
 - Q01 action head: DP > ACT at 5/10/100 demos (20/20/53.3 vs 0/6.7/46.7) and on all generalization axes — confidence M (single real task for data sweep).
 - Q06 chunking: chunk 8 with exp temporal aggregation (m=0.1), DDIM 5 steps as working config (no ablation) — confidence L.
 - Q03 vision encoder: frozen DINO in the specialist works when conditioned on VLA latents — confidence L.
 - Q11 cameras: adding gripper camera to specialist improves CALVIN (figure only) — confidence L.
