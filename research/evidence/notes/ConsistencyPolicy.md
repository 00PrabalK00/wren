# ConsistencyPolicy — Consistency Policy: Accelerated Visuomotor Policies via Consistency Distillation (2024, arXiv 2405.07503, RSS)
Setup: Distil a Diffusion Policy teacher (EDM, 1D-conv UNet, Heun solver, pseudo-Huber loss) into a student via CTM-local consistency objective + DSM loss (warm-started from teacher). Same DP I/O: 2 obs frames (wrist + over-shoulder images + EE pose), action chunk of 16 × 10-D (pos + 6D rot + gripper). Sim: Robomimic Lift/Can/Square/ToolHang (image, 200 proficient-human demos each), Push-T state (200), Kitchen state (566 human); 200 rollouts, best checkpoint. Real: Franka + 2 Zed Mini (wrist + shoulder), 180 VR demos (stated "for our task"), policy waypoints at 15 Hz; Trash Clean Up (10 trials), Plug Insertion (20 trials, 256x256 images), Mobile Microwave on Kinova (10 trials, static start). Inference on a LAPTOP RTX 3070 Ti 8 GB.
Claim: 1–3-step consistency-distilled policy keeps Diffusion Policy success with ~10× lower latency, enabling laptop-GPU inference.
Evidence:
 - Sim (Table I; DDPM NFE 27* / DDIM NFE 9* / CP-1 / CP-3; *optimistic ParaDiGMS-adjusted): Lift 1.00 all; Can .97/.82/.98/.95; Square .93/.85/.92/.96; ToolHang .79/.14/.70/.77; Push-T .87/.78/.82/.84. Note DDIM-15 collapses on ToolHang (.14) — few-step DDIM is NOT safe on hard precise tasks.
 - Kitchen (Table II) p4: DDPM .98, DDIM .93, CP-1 .93, CP-3 .94.
 - Sim latency (Table III, P5000): DDPM-100 110 ms, DDIM-15 11 ms, CP-1 1 ms, CP-3 2 ms.
 - Real (Table IV, DDIM-15 vs CP-1): Trash 0.8±.13 vs 0.8±.13 (192 ms vs 21 ms); Plug insertion 0.6±.11 vs 0.7±.10 (198 vs 22 ms); Microwave 0.5±.16 vs 0.4±.15. DDPM-100 on the 3070 Ti ≈ 1.5 s per forward pass (unusable).
 - Latency breakdown (Table XI, 3070 Ti): image encoder 6 ms both; network 179 ms (DDIM) vs 13.5 ms (CP); total 192 vs 21 ms.
Ablations:
 - Consistency objective (Square): Consistency Distillation .88, CTM .91, CTM-local .92 (CTM >40% slower to train).
 - Initial sample variance (Square): N(0,1)→ low-variance N(0,1/T²): 1-step .90→.91, 3-step .92→.96.
 - Chaining at discretized vs continuous subdivisions: Square .96 vs .94, ToolHang .77 vs .72.
 - Teacher quality .92/.88/.84 → student .92/.92/.88 (robust to teacher).
 - Dropout on s→0 generations enabled .92 vs disabled .86.
 - Consistency Training without teacher (CT Policy): Lift .91 vs 1.0, Square .55 vs .92 → teacher distillation essential.
Failure/limitations: authors: loses some multimodality (ODE-based EDM teacher and CP favour one side on Push-T); slightly less stable training; needs teacher + longer training (Microwave under-trained); CP-1 weaker on long-horizon later stages. Critical read: real trials are 10–20 per task with SE ≈ ±0.1–0.16, so "equal" means "not distinguishable"; 180 demos (> our 50–100); DDPM/DDIM baselines use ParaDiGMS-optimistic NFE. Two-stage training doubles engineering effort; flow matching with few Euler steps (FlowPolicy/StreamingFlow, π0-style) gives similar speed without distillation.
Conflicts: agrees with VQ-BeT/FlowPolicy that multi-step diffusion is the latency bottleneck; CP claims only ~equal success, unlike FlowPolicy's claims of improvement. DDIM-15 ToolHang .14 vs DDPM .79 contrasts with Diffusion Policy's claim that DDIM ~10–16 steps is fine for real tasks — the gap shows few-step DDIM can fail silently on precision tasks.
Relevance: Highly relevant — same 8 GB laptop-GPU class as our RTX 5060. Shows (a) a DP-sized UNet with 1 step runs in ~21 ms total on 3070 Ti including 2 cameras; (b) image encoder cost is small (6 ms) — the 2 s SmolVLA latency is the backbone/steps, not the cameras. Multimodality loss matters little for pumpkin→tray.
Decision impact:
 - Q01 action head: diffusion quality preserved at 1–3 steps via distillation (real: 0.8=0.8, 0.7 vs 0.6) — supports "generative head with few steps" — confidence M (10–20 trials).
 - Q01 action head: consistency distillation adds a teacher stage; loses some multimodality — weakens CP vs simpler flow matching — confidence L/M.
 - Q10 latency: 21 ms vs 192 ms (DDIM-15) vs ~1.5 s (DDPM-100) on 8 GB laptop 3070 Ti — confidence H for latency numbers.
 - Q10 steps-vs-quality: DDIM-15 ToolHang .14 vs DDPM .79; CP-3 .77 — naive step-cutting can collapse precision — confidence M.
