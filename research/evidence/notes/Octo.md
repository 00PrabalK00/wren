# Octo — Octo: An Open-Source Generalist Robot Policy (2024, arXiv 2405.12213)
Setup: "transformer-first" policy pretrained on 800k OXE trajectories (25 curated datasets, delta-EEF only, diverse ones up-weighted 2x). Tokenizers: shallow CNN stem -> 16x16 patches (256 tokens 3rd-person @256x256, 64 tokens wrist @128x128), frozen t5-base (111M) for language (16 tokens), goal images optional. Block-wise masked transformer + readout tokens -> diffusion head (3-layer MLP, hidden 256, residual+LN, DDPM cosine, 20 steps). History = 2 frames. Sizes: Tiny 10M, Small 27M (12L, D=384, 6 heads), Base 93M (12L, D=768). Base pretrain: 300k steps, batch 2048, TPU v4-128, 14 h. Fine-tune recipe (identical for all 6 targets): ~100 demos, full-model FT, 50k steps, cosine LR + warmup, <5 h on one A5000 24 GB. Aug: random crop+resize, color jitter (no crop on wrist). Eval: 10 trials/task zero-shot; 20 trials/finetune domain (10 for bimanual); ablations 40 trials on WidowX.
Claim: a flexibly tokenized, diffusion-headed transformer pretrained on OXE is a good initialization that fine-tunes with ~100 demos to new robots, sensors and action spaces, beating from-scratch and VC-1.
Evidence:
 - Fine-tuning (Table I, ~100 demos, 20 trials each; ResNet+Transformer scratch 28M / VC-1 ViT-B+MLP(MSE) / Octo): Berkeley Insertion (new F/T obs) 10/5/70; Stanford Coffee 45/0/75; CMU Baking 25/30/50; Berkeley Pick-Up (new joint-position action space, wrist cam + proprio) 0/0/60; Berkeley Coke (new robot ViperX, 3rd+wrist, 5 Hz) 20/10/100; Berkeley Bimanual ALOHA (new 14-D joint action head) 20/50/80; Average 20/15/72.
 - Zero-shot (Fig. 5): Octo +29% avg over RT-1-X (35M); "similar" to RT-2-X (55B) on WidowX and RT-1 robot (bars figure only). Goal-image conditioning +25% over language on WidowX.
 - Zero-shot generalization (Table VII, Octo-Small, WidowX, 20 trials/row): in-distribution 85%, novel objects 80%, novel environment 40%, novel skill 5%.
 - Bimanual best config: chunk 64 trained, execute 12 with receding horizon (same for baselines).
Ablations (Table VI, Octo-Small, WidowX, 40 trials, 2 lang + 2 goal tasks; avg):
 - Full recipe 83%.
 - Data: RT-X 11-dataset mix → 60%; Bridge-only (single robot) → 43%.
 - Head: discretized 256-bin CE → 18% ("decisive but imprecise, misses grasps"); MSE/L2 → 35% ("hedging", slow, fails to rotate gripper); diffusion 83%.
 - Encoder: ResNet-50 + transformer → 70% (vs ViT-style 83%) on full mix; BUT ResNet beats their ViT when training from scratch on ~100 demos (App. E; big from-scratch transformer "overfit quickly").
 - Model scale (Fig. 6, 10 trials, one lang task per robot): Tiny 10M < Small 27M < Base 93M zero-shot (figure only); Base more robust to initial scene config, fewer premature grasps.
 - History: 1 extra frame helps zero-shot; "significantly diminishing gains" beyond 2 frames.
 - Chunking helps coherence; temporal ensembling gave no benefit over receding-horizon execution.
 - Patch 16x16 > 32x32, especially for grasping/fine tasks (4x tokens).
 - Proprio input: "generally worse" in pretraining — hypothesized causal confusion (states strongly correlate with next actions).
 - Gripper: absolute (open=1/closed=0) chosen over relative/toggle; relative gave slightly higher grasp success but less retrying after failed grasp.
 - Frozen vs FT: full FT beat freezing subsets. Language: frozen T5-base best; T5-large or FT'ing T5 no gain.
 - ImageNet-pretrained ResNet: no benefit zero-shot (confounded with ResNet underperformance).
 - Data loading: large shuffle buffer (500k frames, <=100 steps per traj) crucial; small buffer hurt significantly.
Failure/limitations: Authors: poor use of wrist camera — fine-tuning was often BETTER with 3rd-person only than 3rd+wrist (only 27% of pretraining data has wrist cams); language weaker than goal images (56% of data has language); novel skills fail. Critical read: 10–20 trials per cell, per-task scale figure uses 10 trials; ablations only on WidowX in-distribution tasks; from-scratch baseline is one fixed 28M ResNet+transformer, not a tuned DP/ACT; the "Octo" finetune numbers use per-setup cameras that differ by task. RDT-1B and OpenVLA later report Octo fine-tunes near 0% on their harder tasks (CogACT Realman 4.9%, RDT handover 0%) — Octo's value is task/data-regime dependent.
Conflicts: MSE-head collapse agrees with ACT (L1 without CVAE bad) and disagrees with OpenVLA-OFT (L1 fine at 7B) — capacity + data cleaning explain it. "Proprio hurts" agrees with copycat/causal-confusion papers and RDT (drops proprio history) but conflicts with HPT (proprio pretraining +6.7 pts, no-proprio from scratch much worse 26.7 vs 43.3). The difference: Octo's pretraining data is heterogeneous delta-EEF where state→action shortcuts are strong; HPT uses per-embodiment stems. Wrist-cam weakness is a pretraining-data artifact, not a general finding (ACT/ALOHA and OFT show wrist cams help).
Relevance: Octo-Small (27M) is the most realistic generalist checkpoint for an 8 GB GPU: the paper fine-tunes Base (93M) on a 24 GB A5000 in ~5 h; Small at 27M should fit 8 GB with modest batch (my inference, not reported). But it is JAX-only (PyTorch ports exist in the community, not in this paper), pretrained only on delta-EEF, weak with wrist cams, and its zero-shot novel-environment drop (85→40%) shows it will not by itself fix our lighting/camera-shift failures. New action spaces (joint position) work by adding a new head (Pick-Up 60% vs 0% scratch; ALOHA joint 80%), relevant to SO-101 absolute joint targets. Diffusion head is small (MLP 256) and 20 steps — cheap latency.
Decision impact:
 - Q01 action head: supports diffusion over MSE and discrete-256-bin at small scale (83 vs 35 vs 18) — confidence M (40 trials, one robot, but mechanism consistent with ACT/DP).
 - Q03 vision encoder: at ~100 demos from scratch, ResNet beats a ViT/patch-transformer; large transformers only pay off with huge data — confidence M.
 - Q06 chunking: supports chunking + receding horizon (chunk 64 / exec 12 on ALOHA); temporal ensembling no benefit — confidence L/M (qualitative statement).
 - Q07 history: 2 frames enough; proprio input can cause causal confusion — confidence L/M (qualitative, pretraining only).
 - Q11 cameras: Octo's pretrained model underuses wrist cam; don't expect OXE-pretrained generalists to help wrist-view — confidence M.
 - Q12 model size: zero-shot improves 10M→27M→93M, but from-scratch large transformer overfits on 100 demos — confidence M.
 - Q13 data diversity: pretraining mix breadth matters (83 vs 60 vs 43) — confidence M (for pretraining, not fine-tune).
 - Q14 robustness: pretraining helps novel objects (80%) but novel environment drops to 40% — confidence M.
