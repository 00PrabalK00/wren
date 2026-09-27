# RTC — Real-Time Execution of Action Chunking Flow Policies (NeurIPS 2025, arXiv 2506.07339)
Setup: sim Kinetix 12 dynamic tasks (force control, action noise), 4-layer MLP-Mixer flow policy H=8, 2048 rollouts/point; real: π0.5 (H=50, 50 Hz, 5 denoise steps, 76–97 ms), bimanual 6-DoF, 6 tasks × 10 trials × 4 methods × 3 latency levels = 480 episodes (28 h).
Method: inference-time only; next chunk generated while executing current; first d (delay) actions frozen, overlapping rest inpainted with guidance (ΠGDM) + SOFT exponentially-decaying mask over all H−s overlapping steps; guidance-weight clipping needed for few denoise steps. Only for diffusion/flow heads.
Evidence:
 - Sim: temporal ensembling (TE) poor "across the board, even at d=0" — averaging valid multimodal actions gives invalid actions. RTC > BID (BID uses ~2.3× latency with batch sampling), gap grows with delay. Soft masking > hard masking, esp. small d. RTC benefits monotonically from shorter execution horizons (more closed-loop).
 - Real: RTC best throughput at all delays; fully robust to +100/+200 ms injected latency; synchronous degrades linearly; TE (sparse & dense) could NOT run at +100/+200 ms — oscillations triggered the robot's protective stop. RTC completes tasks faster even excluding pauses; big gain on precision task (light candle) and bed making.
Limitations: extra compute (guidance backprop); requires diffusion/flow policy; dynamic locomotion not tested on real.
Conflicts/implications for our code: my current eval_real blending (linear fade old→new chunk) is a TE-like average — RTC shows averaging can yield invalid/oscillating actions with multimodal policies and gets worse with latency. Proper fix = inpainting-based continuation (RTC) or training-time continuation (Legato) — both need a flow/diffusion head.
Relevance: SO-101 is position-controlled like their real setup; our inference delay at 10 Hz with ~0.1–0.3 s latency is d≈1–3 steps — small d is exactly where soft masking matters.
Decision impact:
 - action_head: choose FLOW matching (enables RTC/Legato) — SUPPORTED — H.
 - execution: async + RTC-style soft-masked inpainting instead of blending/TE — SUPPORTED — H (large real study).
 - temporal ensembling: AVOID with multimodal heads — SUPPORTED — H (conflicts with ACT's +3.3%, which was a unimodal-ish CVAE with z=0 and synchronous per-step queries).
