# W4_ASystematicStudyofDataModalitiesandStrat — A Systematic Study of Data Modalities and Strategies for Co-training Large Behavior Models for Robot Manipulation (2025/26, TRI; arXiv id not in text)
Setup: Bimanual Franka (TRI LBM stack), 4 RGB cams, EE-pose actions as relative trajectories, 16-step chunk (1.6 s, i.e. 10 Hz), execute 8 steps open loop. PaliGemma2-PT VLM + flow-matching "ActionFT" head conditioned on a SINGLE VL token. Target data TRI-Ramen 523 h / 403 tasks / 53k demos; + 5 co-training modalities (50M VL samples, OXE 1150 h, 2271 h human video). 89 policies, 58k sim rollouts (50/task, 13 seen + 8 unseen tasks, nominal + DS = lighting/texture/distractor/camera-param shift), 2835 real rollouts. 16 H100 x 64 h per phase. Inference latency 0.146 s (GPU unspecified).
Claim: co-training with diverse VL data and cross-embodiment robot data improves DS robustness / unseen tasks / language following; discrete action tokens (FAST, VQ-VAE, latent actions) give no significant benefit; explicit CoT conditioning does not help.
Evidence (mostly figure-only, with CLD significance tests):
 - Final combined model: 72.6% sim unseen-task success (+36.4% over no-co-training baseline); real language following 69.4% avg task completion (+45.3%).
 - Fine-tune to 3 unseen long-horizon dexterous tasks with 200 demos each (30 rollouts/task): FT Final 90.2% completion, +22.8% over FT baseline (robot-only pretrain), +42.9% over single-task from scratch. Baseline/scratch failures = precision (cap alignment, spatula, transparent cup).
 - No co-training modality changed in-distribution (seen-task) performance significantly; gains are on DS/unseen/language.
Ablations:
 - Robot-only training erodes VLM backbone (loses ability to generate language; worst on VLM benchmarks) → co-training with VL data preserves it.
 - FAST-token co-training: no gain, degrades unseen-task generalization (figure only). VQ-VAE tokens: marginal unseen gain, slightly worse under DS.
 - Latent actions from human video: help only in low target-robot-data regime; benefit vanishes with more robot data (Fig. 8, figure only). Authors suspect gains = extra compute.
 - Explicit CoT conditioning at inference: never beats implicit two-phase co-training; degrades with VLM annotations / latent-action CoT (error propagation).
 - Architecture (Fig. S1, figure only): single-token VL conditioning ≥ pi0.5-equivalent / piFAST-equivalent in-distribution and significantly better on DS/unseen; pi0-equivalent (timestep only at first layer) substantially worse in-distribution → inject flow timestep at every action-head layer.
 - Loss weight / batch ratio: too much co-training data hurts in-distribution; chosen 9:1 robot:co-train, CE weight w=0.02.
 - Deployment: chunk discontinuities caused jerky real motion → fixed with temporal ensembling = uniform average of the last 4 overlapping chunks, continuous inference.
Failure/limitations: huge compute/data regime (4000 h) irrelevant to 50-100-demo single-task training; most results in bar-chart figures; sim DS benchmark is appearance shift only; bimanual Franka.
Conflicts: FAST no-benefit contradicts pi0-FAST/pi0.5 reports of FAST co-training gains — difference is data scale (authors: FAST may need much bigger robot corpus). Jerky-chunk fix via averaging agrees with ACT temporal ensembling and disagrees with RTC-style claims that averaging is insufficient (here 146 ms latency so small shift).
Relevance: Low-medium. We won't co-train at this scale. Transferable bits: (1) fine-tuning a VLA only on robot data destroys VLM language ability — relevant if we rely on SmolVLA's language for a 2nd object; (2) chunk-boundary jerk is a known real-world issue fixed by averaging 4 overlapping chunks; (3) flow head timestep conditioning per layer matters.
Decision impact:
 - Q10 latency/smoothness: supports temporal ensembling (avg of last 4 overlapping chunks) to remove chunk-boundary jerk — confidence M (real deployment report, no numbers).
 - Q08 language: robot-only fine-tuning erodes VLM language grounding; keep some VL co-training or freeze backbone if language matters — confidence M (strong benchmark evidence, big-model regime).
 - Q01 action head: flow matching continuous head; discrete FAST/VQ token aux gives no gain — confidence M (large-scale, figures).
 - Q14 robustness: DS (lighting/texture/camera param) robustness improves via diverse VL + cross-embodiment co-training, not via in-domain tricks — confidence L for our regime (requires big data).
 - Q12 model size/pretraining: pretrained+co-trained model fine-tuned with 200 demos beats from-scratch single-task by 42.9% on dexterous tasks — confidence M.
