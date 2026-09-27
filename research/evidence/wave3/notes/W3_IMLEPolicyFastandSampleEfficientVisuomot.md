# W3_IMLEPolicyFastandSampleEfficientVisuomot — IMLE Policy: Fast and Sample Efficient Visuomotor Policy Learning via Implicit Maximum Likelihood Estimation (2025, arXiv 2502.12371)
Setup: 8 sim tasks (Robomimic PH Lift/Can/Square/ToolHang/Transport, Push-T, UR3 BlockPush, Franka Kitchen) + 2 real tasks (real Push-T; shoe racking, pick/place 2 shoes, either first), real robot arm with wrist cam + side/front scene cam; real data 35 demos, trained on 35 and 17-demo subsets; 20 real trials per method per setting. Same 1D-UNet as Diffusion Policy (timestep embedding removed), noise vector used as latent; Tp=16, Ta=8, To=2; eps=0.03, 20 samples per datapoint; real training fixed 12 h; inference measured on RTX 3090. Sim: 3 seeds x 50 inits, max / mean-of-last-3 checkpoints.
Claim: a single-step generator trained with conditional rejection-sampling IMLE captures multimodal action chunks from fewer demos than DP (100-step DDPM) or 1-step flow matching, at ~110 Hz.
Evidence (Table II, max/last-3 avg; IMLE / IMLE-no-consistency / DP / FM-1step):
 - Push-T full: 0.59/0.54, 0.56/0.53, 0.57/0.52, 0.36/0.34. Push-T 20 demos: 0.10/0.07, 0.05/0.03, 0.03/0.03, 0.012/0.00.
 - UR3 BlockPush full: 0.82/0.73, 0.90/0.77, 0.74/0.73, 0.87/0.81; 20 demos: 0.11/0.09, 0.07/0.04, 0.10/0.06, 0.09/0.05.
 - Kitchen (18 demos): 0.34/0.32, 0.34/0.31, 0.26/0.21, 0.21/0.14.
 - Robomimic full: all methods within ~0.05 (e.g. Square .82/.86/.84/.82; ToolHang .81/.74/.84/.78). 20 demos: Can .50/.44/.47/.48, Square .18/.11/.16/.16, ToolHang .03/.02/.00/.02, Transport .28/.27/.27/.26.
 - Push-T data-size sweep (Fig 5, figure): reward 0.5 reached with <29% data (IMLE), ~43% (DP), >80% (FM 1-step) — basis of the "38% less data" headline.
 - Real (Fig 7, figure only, qualitative): IMLE best on both tasks at 17 demos by "significant margin"; competitive at 35 demos.
 - Inference speed (Table III, 2 images, RTX 3090): IMLE 111 Hz, IMLE w/o consistency 123 Hz, DP (100 DDPM steps) 1.8 Hz, FM 1-step 110 Hz.
Ablations:
 - Temporal consistency (pick candidate closest to previous chunk's unexecuted tail, random reset every C=10): helps on highly multimodal Push-T (0.10 vs 0.05 at 20 demos) and real tasks (figure); on UR3 full it is slightly worse (0.82 vs 0.90).
 - eps and samples-per-condition sweeps (Fig 6): stable over eps 0–0.2 and 0–100 samples (figure only).
 - 1-step FM mode-averages (qualitative Fig 1/2); DP biases to majority mode with little data.
Failure/limitations: authors: capturing all modes makes it sensitive to demo quality (bad demos get reproduced); mode switching between chunks requires the consistency hack, which can lock in bad plans; not consistently better than DP at full data. Critical read: differences in sim at 20 demos are mostly within a few points (3 seeds, 50 inits) — the big win is only Push-T/Kitchen; real results are figure-only with 20 trials; no robustness (lighting/object/camera) tests; DP baseline uses 100 DDPM steps with no DDIM — an unfairly slow latency comparison (DDIM 10-step DP would be ~10x faster); FM baseline was only 1 step, not the usual 10.
Conflicts: agrees with ACT's finding that plain unimodal regression fails on multimodal human data; contrasts with papers reporting 1-step/few-step flow matching as adequate (e.g. pi0 uses 10 steps) — here FM was restricted to 1 step, which is the cause of its mode averaging. Consistency selection is a cheap alternative to temporal ensembling/RTC for chunk-boundary jerk.
Relevance: very relevant to us: 17–35 demos, wrist + scene cam, real multimodal pick-place, single forward pass (UNet ~DP size fits 8 GB easily). A drop-in head for a small LeRobot-style policy; the "pick sample closest to previous chunk tail" trick directly addresses our chunk-boundary jerk. But evidence of superiority over DP/flow is weak outside low-data multimodal tasks; a single-object pumpkin pick-place is low-multimodality where all heads tie.
Decision impact:
 - Q01 action head: supports single-step generative head (IMLE) over 1-step FM / DDPM-DP in low data; heads tie on low-multimodality tasks — confidence M (real results figure-only, small sim deltas).
 - Q10 latency/smoothness: supports 1-step generation (111 Hz vs 1.8 Hz DDPM) and chunk selection by consistency with previous chunk tail to avoid mode-switch jerk — confidence M.
 - Q13 data: headline "38% less data" on Push-T sim sweep; with 17 real demos learns multimodal shoe racking — confidence L-M (figure only).
 - Q06 chunking: Tp=16, Ta=8, To=2 worked; no sweep — confidence L.
