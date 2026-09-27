# W3_AdaptationofGeneralistRobotPolicieswithM — Adaptation of Generalist Robot Policies with Minimal Data (MiDAS) (2026, arXiv n/a in text)
Setup: base policy π0.5 (VLA, flow-matching head). Stage I: LoRA on VLM + full action head BC on K=1 demo; Stage II: frozen base + lightweight residual actor-critic, sparse-reward online RL (offline warmup, success-balanced replay, PA-RL best-of-N extraction). Sim: LIBERO-Long (10 tasks), RoboCasa-365; 3 seeds. Real: bimanual YAM, 2 pick-place tasks, 1 demo, 15 rollouts, 5–6 h autonomous interaction with (presumably human) reset + reward.
Claim: one demonstration + value-based residual RL on a pretrained VLA can reach reliable success; BC alone gives only coarse behavior.
Evidence:
 - Zero-shot π0.5 = 0% on every sim task; Stage-I-free RL stays at 0%.
 - K=1 BC baselines: flow policy on pretrained ResNet features nonzero on only 3/10 LIBERO-Long tasks; privileged-state flow policy 0%.
 - Real (Table 3, 15 rollouts): block sorting BC(1 demo) 40% → MiDAS 67%; knife+donut 27% → 80%.
 - Table 2 (action-cloud distance to base samples): Filtered-BC 0.112, DSRL 0.024, MiDAS 4.54 → RL leaves base-policy support.
 - Per-task Table 1 sim numbers: not reliably extractable from text (table split); text states MiDAS recovers strong policies on all tasks; Filtered BC and DSRL inconsistent when warm-start < 20%.
Ablations:
 - Representation for residual RL (Fig. 3, figure only): ResNet from scratch collapses; frozen DINO works but converges slower; π0.5 backbone features fastest; π0.5 fine-tuned on 1 vs 50 demos give similar representation quality on 2/3 tasks.
 - Generalization (Fig. 7 / Table 4, LIBERO-PRO perturbations): color/texture and language-paraphrase shifts mostly retained (attributed to frozen VLM); object position swap → 0% for both BC and RL; shape change OK only if grasp affordance same; category change fails. Broader demos or a reset curriculum approach the robustness of a 50-demo policy (appendix, figure only).
Failure/limitations: RL needs reward + resets + hours of robot time; real eval 15 rollouts; tasks plausibly in π0.5 pretraining distribution (authors admit); per-task sim numbers only as mean±std in split table. Large VLA — not runnable on 8 GB.
Conflicts: consistent with the view that pretrained VLA/foundation features give appearance robustness while positional/affordance generalization requires coverage in demos (cf. data-scaling studies: diversity of object placements matters more than count).
Relevance: Mostly outside our pipeline (online RL, big VLA). Useful takeaways: (a) appearance robustness came from a frozen large pretrained backbone, not from demos; (b) state shifts (object positions/swaps) are NOT fixed by pretraining → our 50–100 demos must cover the pumpkin/tray position range; (c) from-scratch ResNet features are much worse than frozen DINO for low-data adaptation.
Decision impact:
 - Q03 vision encoder: scratch ResNet collapses, frozen DINO works (slower), action-pretrained VLA features best — supports pretrained (frozen) encoders over scratch in low data — confidence L (RL setting, figure only)
 - Q13 data: 1-demo BC gives coarse behavior only (real 27–40%); object swap → 0%; broader demo coverage restores robustness — supports spreading demos over positions — confidence L
 - Q14 robustness: color/texture/paraphrase shifts retained via frozen VLM, positional/affordance shifts not — supports frozen pretrained features for appearance shift — confidence L
