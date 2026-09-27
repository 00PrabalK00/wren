# pi0 — π0: A Vision-Language-Action Flow Model for General Robot Control (2024, arXiv 2410.24164)
Setup: PaliGemma-3B VLM (SigLIP + Gemma-2B: width 2048, depth 18, mlp 16384) plus a ~300M "action expert" trained from scratch (same depth 18, width 1024, mlp 4096), 3.3B total. The expert is a second set of transformer weights. It interacts with the VLM ONLY through shared self-attention, like a 2-expert MoE. Tokens: 2–3 images, language, state q (1 linear-projected token), and H=50 noisy action tokens. The attention mask is block-causal: [images+text] → [state] → [actions]. The prefix never attends to the robot tokens, which keeps the VLM close to its pretraining distribution and lets KV be cached. Action tokens are fully bidirectional among themselves. The flow-matching timestep τ is sampled from Beta((s−τ)/s; 1.5, 1) with s=0.999, which emphasises NOISY timesteps. τ is fused into each action token via an MLP (concat with a sinusoidal embedding). Inference uses 10 Euler steps. Pretraining: 10k h of data (903M timesteps from their own 7 robot configurations / 68 tasks, plus 9.1% OXE/DROID/Bridge), 700k steps. Datasets are weighted by n^0.43, and state/action are zero-padded to 18 dims. Post-training uses 1–100+ h per task. Control is 20 Hz (UR5e/Franka) or 50 Hz (the rest). Eval: 10 episodes per task per method with partial-credit rubrics. Baseline π0-small is 470M with no VLM init: DistilBERT text, an R26-S-32 ViT (not shared across cams), and a DiT expert with AdaLN-Zero that cross-attends to the encoder; it also uses 10 flow steps.
Claim: a VLM-initialised transformer plus a separate flow-matching action expert, pretrained on a large cross-embodiment mix and then post-trained on curated data, beats OpenVLA/Octo/ACT/DP on dexterous tasks and runs at up to 50 Hz with chunking.
Evidence (almost all results are bar charts, so figure only unless stated):
 - Inference latency (Table I, RTX 4090, 3 cameras): image encoders 14 ms, observation prefix forward 32 ms, 10× action-expert forward 27 ms, total on-board 73 ms (86 ms off-board over Wi-Fi). The 10 flow steps through a 300M expert cost about the same as ONE prefix pass.
 - Out-of-box (Fig 7, 5 tasks, 10 eps each): π0 (700k steps) is best on all tasks. π0-parity (160k steps) still beats all baselines. π0-small (470M, no VLM) beats OpenVLA (7B, no chunking) and Octo (93M diffusion). Figure only.
 - Fine-tuning new tasks with 1/5/10 h of data (Fig 11): π0 is generally best. The strongest prior baselines were ACT and DP trained from scratch, not the pretrained OpenVLA/Octo. On Tupperware, 5 h π0 ≈ baselines while 1 h π0 is "significantly better". Pretrained vs scratch π0 is "sometimes as much as 2×", with larger gains on tasks similar to the pretraining data. Figure only.
 - Complex multi-stage tasks (Fig 13): full recipe (pretrain + post-train) > scratch > out-of-box on all 7 tasks. Pretraining helps most on the hardest tasks. Figure only.
Ablations:
 - Temporal ensembling (Appendix D): "we tried temporal ensembling early on and found that it hurt policy performance". They execute chunks open-loop instead: 16 of 50 actions at 20 Hz (re-infer every 0.8 s) and 25 of 50 at 50 Hz (every 0.5 s). No number is given.
 - Separate expert weights vs a single Transfusion-style transformer: "led to an improvement in performance". No number.
 - VLM init vs none (π0 vs π0-small): large gains in language-following accuracy, and π0-small gains nothing from high-level VLM commands (Fig 9). This is confounded with size (3.3B vs 470M), which the authors admit.
 - The Beta timestep schedule is argued, not ablated. The authors reason that E[A|o] is hard for actions, unlike images, so they emphasise high-noise τ.
Failure/limitations: authors say pretraining-mix composition is not understood, not all tasks work reliably, and they cannot predict how much data a task needs. Critical read:
 - Every quantitative result is a bar chart with 10 trials and partial credit, so exact effect sizes are unreadable.
 - Architecture and data are confounded in every baseline comparison (OpenVLA/Octo use their public OXE checkpoints).
 - The action parameterisation (absolute vs delta joints) is not stated in this paper. The state is "a vector of joint angles".
 - There is no ablation of chunk length, number of flow steps, or expert size.
 - π0-small's baseline status shows a from-scratch 470M model is usable on 10k h of data. That says nothing about 50–100 demos.
Conflicts:
 - TE hurts here, which agrees with RTC and disagrees with ACT's +3.3%. Likely cause: π0 is a multimodal flow head, while ACT's CVAE is used near-deterministically (z=0).
 - OpenVLA-style discrete per-dim tokens are much worse on high-frequency data. FAST explains why: per-timestep binning gives tokens with near-zero marginal information.
 - SmolVLA later copies this expert design at 100M params with a frozen VLM and interleaved cross/self-attention. KnowledgeInsulation shows this π0 recipe (gradients from a freshly initialised expert into the VLM) degrades language following and converges ~7.5× slower than token training.
Relevance:
 - The design pattern "big shared encoder prefix, cached once; small bidirectional action transformer run K times" is the right shape for an 8 GB laptop. The expert's cost scales with its size × K, and π0 shows even 300M×10 steps ≈ 27 ms on a 4090.
 - A 10–50M expert would make K=10 nearly free. Our latency budget is dominated by the image encoder and prefix, so image resolution and the number of camera tokens matter more than flow steps.
 - Open-loop execution of about half the chunk (H=50, execute 16–25) is their default. At our 10 fps, H=50 would be 5 s, far longer than their 1–2.5 s. The time-equivalent is H≈10–20 at 10 Hz, or H≈30–50 at 30 Hz.
 - Nothing here on lighting, camera shift, or other robustness.
Decision impact:
 - Q01 action head: supports flow matching with a separate small action transformer (bidirectional over the chunk, block-causal from the observation) and 10 Euler steps — M (strong system results, but no head-vs-head ablation beyond Octo/OpenVLA confounds).
 - Q06 chunking: supports an H≈1–2.5 s chunk, executing ~30–50% open-loop before re-planning, and no temporal ensembling (TE "hurt") — M (stated, no numbers).
 - Q10 latency: supports KV-caching the observation prefix and keeping the expert small. 10 flow steps with a 300M expert cost 27 ms of 73 ms on a 4090 — H (measured table).
 - Q12 model size: a 470M from-scratch model is viable only with 10k h of data. The VLM-init advantage is confounded with size — L for our regime.
 - Q13 data: supports pretraining + small curated post-training set. Pretraining gains are largest for tasks similar to the pretraining data (up to ~2×) — M (figure only).
