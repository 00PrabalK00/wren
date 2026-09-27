# HybridFlow — A 2-NFE Generative Policy for Real-Time Robotic Manipulation (Dong et al., 2026, arXiv 2602.13718v2)
Setup: one MeanFlow-trained network used twice: Global Jump (average velocity, full interval) → parameter-free ReNoise interpolation to a nonzero time (α=0.15) → Local Refine (instantaneous velocity at that time). No distillation. Sim: image RoboMimic Can/Lift/Square/Transport, 3 cams, ViT encoder, 100 episodes/task; baselines DDIM, ReFlow, ShortCut, OFP, OneDP, DMPO, STEP. Real: UMI-style setup, 224² fisheye RGB + state, DINOv3-base fine-tuned, ~300 demos/task; 5 settings (pick-place ID, unseen-colour OOD, eyepatch folding: 80 trials each; car transport 63 trials; whack-a-mole 6 rounds); ALL policies on one Jetson AGX Thor.
Evidence:
 - Sim: plain 1-step MeanFlow 78% avg; uniform MeanFlow iteration 78/72/60% at 2/4/16 NFE (more steps HURT); HybridFlow 95% (reused noise) / 95.5% (fresh noise). No-ReNoise variant 24%. Square: HybridFlow 98 vs STEP-2 96, OneDP 84, DMPO 83; Transport 82 vs STEP-2 86, DDIM-16 88.
 - Real (Table I, task score %; T_inf): MeanFlow-1 (~10 ms) 0/0/0/0/0; DDIM-2 (~19 ms) 0/0/2.5/0/0; ReFlow-2 (~19 ms) 10.0/7.5/5.0/2.3/0.0; DDIM-16 (~152 ms) 63.8/47.5/51.3/47.7/0.0; HybridFlow-2 (~19 ms) 86.3/68.8/66.3/60.7/68.3 (PP-ID/Pink OOD/Eyepatch/Whack-a-mole/Car transport). Counts: PP-ID 69/80 vs DDIM-16 51/80.
 - VLA transfer (StarVLA action expert): LIBERO avg ReFlow-4 97.1 → HybridFlow-2 97.7; RoboTwin 88.3 → 89.3.
 - Camera path latency ~95 ms on Thor, ~62 ms on RTX 5090 (excluded from T_inf).
Ablations: time sampling logit-normal 78% vs uniform 70% for MeanFlow; ReNoise α sweep: best 0.15–0.20, >0.25 degrades.
Failure/limitations: refinement ratio tuned empirically; single lab; 300 demos per task (more than ours).
Conflicts: STRONG CONFLICT with MP1/ReactVLA-style claims that 1-step MeanFlow suffices: here plain MeanFlow scores 0/80 on real tasks despite 78% sim — sim success of 1-step generators does not guarantee real-robot validity. Also: 2-step DDIM (0%) and 2-step ReFlow (≤10%) collapse on the real robot; 16-step DDIM works. Agrees with ConsistencyPolicy/HCP that naive step-cutting fails.
Relevance: high as a caution: if we cut SmolVLA's 10 flow steps to 1–2 without distillation/refinement, expect collapse; test step counts on the real robot, not offline MSE. Note latencies on Thor: 19 ms (2 NFE) vs 152 ms (16 NFE) for a DP-sized head.
Decision impact:
 - Q10 fast generator: naive few-step sampling (DDIM-2, ReFlow-2, 1-step MeanFlow) fails on real robots (0–10%) while a 2-NFE jump+refine keeps 60–86% — M/H (80 trials/setting, controlled).
 - Q10: evaluate step reductions on hardware; sim/offline success is not predictive — M.
