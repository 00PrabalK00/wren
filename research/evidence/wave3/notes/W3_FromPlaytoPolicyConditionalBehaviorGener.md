# W3_FromPlaytoPolicyConditionalBehaviorGener — From Play to Policy: Conditional Behavior Generation from Uncurated Robot Data (C-BeT) (2022, arXiv 2210.10047)
Setup: Sim: CARLA (200 demos, 2 routes), multimodal BlockPush (1,000 scripted demos), Franka Relay Kitchen (566 human VR demos). Real: Franka + toy kitchen, 4.5 h / 460 sequences / 45,287 frames of unscripted play via Vive VR; 2 side RGB cams; action = 7 joint-angle deltas in [-1,1] + binary gripper. Images -> per-camera ImageNet ResNet18 fine-tuned with BYOL on the play frames, then FROZEN 512-d embeddings; proprio (sin,cos) repeated to 1036-d. GPT-style transformer over observation history + goal (future observation) tokens; BeT head = k-means bin classification + continuous offset. Real trials 5-20 per task.
Claim: Combining BeT's multimodal discretized action head with future-observation goal conditioning learns task policies from uncurated play data without labels.
Evidence:
 - Sim (Table 2; CARLA/BlockPush out of 1, Kitchen out of 4): GCBC 0.04/0.06/0.74; WGCSL 0.02/0.10/1.17; Play-LMP 0.0/0.02/0.04; RIL 0.59/0.07/0.39; C-IBC 0.65/0.01/0.13; GTI 0.74/0.04/1.61; GoFAR 0.72/0.04/1.24; BeT (uncond.) 0.31/0.34/1.77; C-BeT unimodal 0.62/0.35/2.74; C-BeT multimodal 0.98/0.90/2.80.
 - Real single-task (Table 4, knobs/oven/microwave/pot, cumulative): GoFAR 0/10,0/5,0/5,0/5 = 0/25; BeT 5/20,6/10,1/10,0/10 = 12/50; unimodal C-BeT 1/20,8/10,4/10,0/10 = 13/50; multimodal C-BeT 3/20,9/10,7/10,5/10 = 24/50.
 - Real long-horizon 2-task goals (Table 5, avg tasks/run): BeT 0.47, unimodal 0.37, multimodal 1.1.
 - Future-observation conditioning ~= human labels (Table 3): 0.98/0.90/2.80 vs 1.0/0.89/2.75.
Ablations:
 - Multimodal (k-means bin + offset) -> unimodal regression head: BlockPush 0.90 -> 0.35, CARLA 0.98 -> 0.62; real 24/50 -> 13/50, pot 5/10 -> 0/10; but oven (simple, unimodal data) 9/10 vs 8/10 — no difference.
 - Generalization: unseen conditioning demos keep ~67% of single-task perf (16/50); 2 distractors -> ~67% of original; >=4 distractors -> 0 success.
Failure/limitations: Knob task fails because frozen BYOL representation cannot resolve the small knob state (nearest-neighbor check ~ chance) — perception bottleneck from frozen, self-supervised features on small data. Few real trials (5-20). Old baselines; no diffusion/flow comparison.
Conflicts: Agrees with ACT's CVAE ablation and Diffusion Policy that unimodal regression collapses on multimodal human data; here the difference is large when data is play (highly multimodal) and vanishes on simple single-mode tasks — consistent with the view that for single-task, consistent teleop demos the head matters less. Distractor collapse at >=4 objects consistent with frozen global-embedding policies being brittle to clutter.
Relevance: Our data is single-task-ish (pumpkin -> tray) human teleop at 50-100 demos: modest multimodality; the paper suggests a multimodal head is cheap insurance and matters most when demonstrations vary in strategy. Frozen generic SSL features failed on small visual details -> fine-tune or use strong pretrained encoder. Distractor sensitivity is a warning for global-pooled embeddings.
Decision impact:
 - Q01 action head: multimodal discretized head 24/50 vs unimodal 13/50 real; BlockPush 0.90 vs 0.35 — weakens plain unimodal regression on human data; no gain on unimodal oven task — confidence M (old baselines, few trials)
 - Q03 vision encoder: frozen BYOL-finetuned ResNet18 embeddings cannot resolve knob state -> knob 3/20 — weakens frozen global embeddings for small details — confidence L
 - Q14 robustness: 2 distractors -> ~67% of perf; >=4 distractors -> 0 — confidence L
 - Q13 data: 4.5 h uncurated play can yield policies without labels; future-obs conditioning ~= labels — confidence L
