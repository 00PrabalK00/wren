# W3_CACTIAFrameworkforScalableMultiTaskMulti — CACTI: A Framework for Scalable Multi-Task Multi-Scene Visual Imitation Learning (2022, arXiv 2212.05711)
Setup: Real Franka, toy kitchen, 10 single-stage tasks, joint-position control (8-D) at 12.5 Hz, single camera. Data: 5 kinesthetic demos/task, each REPLAYED 20× while a human re-arranges distractors (→100 traj/task with identical actions), then Stable-Diffusion in-painting adds object/scene variations. Policy: frozen visual embedding (R3M ResNet-50 out-of-domain, or MoCo in-domain) + task-name text embedding → MLP, Gaussian head, MSE BC, single-step (no chunking). Sim: 18 kitchen tasks × 10/50/100 layouts, RL experts, 50 episodes per task-layout (45k episodes). Real trial counts not stated in text.
Claim: cheap diversity multiplication (replay + generative in-painting) + frozen pretrained embeddings lets a small MLP learn a multi-task, distractor-robust policy.
Evidence:
 - Real: ≈30% average success over 10 tasks with shuffled/novel distractors (figure only). End-to-end pixel RL in sim: 0%.
 - Sim Table 1 (success %, train / heldout layouts):
   Sim-10: state 81.2/14.1, out-of-domain R3M 51.3/9.5, in-domain MoCo 88.7/18.8
   Sim-50: state 83.3/31.6, R3M 64.7/30.4, MoCo 72.1/30.2
   Sim-100: state 91.3/47.2, R3M 62.0/33.1, MoCo 75.9/38.4
Ablations:
 - Layout diversity in training 10 → 100: held-out success R3M 9.5 → 33.1, MoCo 18.8 → 38.4 (diversity drives generalization, not count per layout).
 - In-painting augmentation vs only random crop + color jitter (real, same action data): ~15–20% absolute success gain for in-painting variants (figure only).
 - Frozen out-of-domain R3M ≈ frozen in-domain MoCo ≈ fine-tuned (real, figure only); fine-tuned MoCo WITHOUT in-painting aug cannot match frozen + aug. In sim, in-domain MoCo > R3M (visual domain gap).
Failure/limitations: absolute real performance low (~30%); single-step MSE MLP; kinesthetic replay means no action diversity (same 5 trajectories); no lighting/camera shift test; trial counts unreported; real results figure only.
Conflicts: supports generative scene augmentation (ROSIE, GreenAug, etc.). The frozen-vs-finetuned parity contradicts Diffusion Policy / iDP3 findings that fine-tuned encoders win in-distribution — likely because CACTI's policy is weak overall (~30%) and the benchmark is distractor-robustness, where a frozen encoder avoids overfitting to 5 source demos.
Relevance: our failure modes (new-looking pumpkin, lighting) are appearance shifts; in-painting the target/background in recorded frames is directly applicable offline and costs GPU time only (can be done on the 8 GB laptop with SD-inpaint at 512px, slowly). Replay-with-rearranged-distractors trick needs a physically repeatable arm — SO-101 backlash makes open-loop replay imprecise but fine for distractor variation.
Decision impact:
 - Q05 augmentation: supports generative in-painting (semantic) augmentation over crop+color-jitter only (~+15–20 abs, real) — confidence L/M (figure only, ~30% base, unknown trials).
 - Q13 data diversity: supports scene/layout diversity over repeated count (heldout 9.5 → 33.1 with 10 → 100 layouts) — confidence M (sim, large effect).
 - Q03 vision encoder: ~ frozen pretrained R3M competitive with fine-tuned in real distractor setting — confidence L (figure only, weak policy).
 - Q14 robustness (distractors): supports augmentation for distractor robustness — confidence L.
