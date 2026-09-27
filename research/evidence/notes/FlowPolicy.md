# FlowPolicy — FlowPolicy: Enabling Fast and Robust 3D Flow-based Policy via Consistency Flow Matching for Robot Manipulation (2024, arXiv 2412.04987, AAAI 2025)
Setup: SIM ONLY. DP3 architecture (single-view depth → point cloud, FPS to 512 (Adroit) / 1024 (Metaworld) pts, lightweight MLP encoder, 64-D condition incl. robot state; obs horizon 2) with the diffusion head replaced by two-segment Consistency Flow Matching (velocity-consistency loss, EMA target, no distillation), ONE-step inference. 37 tasks (Adroit 3, Metaworld 34), 10 SCRIPTED expert demos per task, 3 seeds, 20 episodes every 200 epochs, reported = mean of top-5 success rates (optimistic protocol inherited from DP3). 3,000 epochs, RTX 2080 Ti.
Claim: one-step consistency flow matching on 3D input matches/exceeds DP3 (10 NFE) success at ~7× lower latency, without a teacher.
Evidence:
 - Success (Table 2, average over 37 tasks): DP (2D, 10 NFE) 35.2±5.3; AdaFlow 35.6±6.1; Consistency Policy (2D) 50.1±4.7; DP3 (10 NFE) 68.7±4.7; Simple DP3 67.4±5.0; FlowPolicy (1 NFE) 70.0±4.7.
 - Per group FlowPolicy vs DP3: Hammer 100 vs 100; Door 58 vs 56; Pen 53 vs 46; MW Easy 90.2 vs 87.3; Medium 47.5 vs 44.5; Hard 37.2 vs 32.7; Very Hard 36.6 vs 39.4.
 - Latency (Table 1, per step, 2080 Ti): FlowPolicy 19.9 ms avg vs DP3 145.7 ms vs Simple DP3 63.0 ms. FlowPolicy latency ≈ 20 ms regardless of task.
Ablations:
 - # demos (Fig. 5, 1/10/20/50 demos, 4 tasks): figure only, qualitative: FlowPolicy ≥ DP3 on non-hard tasks at few demos; both improve with more demos on Pick-Place; DP3 saturates/declines on Coffee Pull while FlowPolicy keeps improving.
 - Learning curves (Fig. 4): figure only, qualitative: FlowPolicy more stable across training than DP3/Simple DP3.
 - NO ablation of number of flow steps, segment count, or 1-step vs multi-step flow; no plain (non-consistency) flow-matching baseline; no regression baseline.
Failure/limitations: none stated by authors. Critical read: sim-only, scripted (unimodal) demos, top-5-checkpoint metric with 20 episodes (noisy, optimistic); +1.3 pts average over DP3 is within std; DP (2D) far lower mainly because of 2D vs 3D input and DP3's evaluation protocol, not the head. Very Hard group is worse than DP3 (36.6 vs 39.4). The latency gain vs DP3 at 10 NFE is only ~7× even though NFE drops 10×, because encoder/overhead remains; ~20 ms on a 2080 Ti is also about what a regression head would cost.
Conflicts: consistent with ConsistencyPolicy (1-step ≈ multi-step quality) but achieves it without a teacher. No evidence here about multimodality — scripted Metaworld demos are near-unimodal, so it cannot distinguish flow from regression.
Relevance: Shows a DP3-style point-cloud policy with a 1-step flow head runs ~20 ms on an older GPU — fits 8 GB laptop easily; relevant if we go RealSense depth (Q04). Weak evidence for head choice on human multimodal demos; zero real-robot or robustness evidence.
Decision impact:
 - Q01 action head: 1-step consistency flow matching ≈ 10-step diffusion (70.0 vs 68.7 avg, 37 sim tasks, 10 scripted demos) — supports few-step flow — confidence L/M (sim, scripted, optimistic metric).
 - Q10 latency: 19.9 ms vs 145.7 ms (DP3 10-step) on 2080 Ti — supports 1-step heads — confidence M.
 - Q04 3D: 3D baselines (DP3 68.7) >> 2D DP (35.2) on same 10 demos — supports point clouds in sim — confidence L/M (DP3's protocol, cameras 84x84).
