# W4_LatentPolicySteeringAnEfficientandFlexib — Latent Policy Steering: An Efficient and Flexible Framework for Cross-Embodiment Transfer (2025/26, CMU; arXiv id not in text)
Setup: Dreamer-style image world model (33M) pretrained with optical-flow conditioning on ~55 h / 15K episodes from 9 non-Franka embodiments incl. human play; fine-tuned with robot actions on 50 target (Franka) demos; at inference sample B candidate chunks from base policy (DP B=400, π0.5 B=16), roll out in WM latent space, pick by value function trained to stay near data. Robomimic 4 tasks (3 seeds × 150 eps) + real Franka 4 tasks (wrist + fixed side cam, joystick teleop, 50 demos, 20 trials each at pre-selected positions). All policies chunk 16. RTX 3090; WM scoring of 400 plans ≈ +100 ms.
Claim: test-time steering with a cross-embodiment-pretrained WM improves any base policy in the 50-demo regime.
Evidence:
 - Robomimic avg: DP (550K params, scratch) 57.2, LPS-DP-scratch 60.9, HPT (12.6M) 45.4, π0.5 (3.6B, LoRA) 60.9, LPS-DP 66.7, LPS-π0.5 66.0. Square: DP 40.5 vs π0.5 30.7 vs LPS-DP 53.4. Transport: DP 26.4, π0.5 25.1, LPS-DP 35.3.
 - Real (successes/20; DP / LPS-DP-scratch / π0.5 / LPS-DP / LPS-π0.5): radish-in-pot 12/13/20/18/20; sweep 5/7/10/11/12; scoop 13/15/16/18/20; fold towel 7/7/9/13/12. Avg 46.2 / 52.5 / 68.8 / 75.0 / 80.0.
Ablations (Can, 50 demos):
 - Pretrained WM vs scratch WM: 88.0 vs 81.0 (largest effect).
 - Value fn from expert states only with binary reward: 79.5 vs DP 77.8 (marginal); off-data states without shift penalty: 76.5 (worse than base).
 - Demo scaling 50–300: LPS-DP@50 > DP@100; gain shrinks at 200–300 (figure).
 - Horizon 4/8/12/16: LPS > DP; horizon 24: LPS worse (noisy shift penalty) (figure).
Failure/limitations: compute at inference (+100 ms for DP; π0.5 limited to 16 samples by memory); requires multi-embodiment pretraining data; authors concede large VLAs outperform on simple common-object pick-and-place.
Conflicts: In sim, a 550K-param DP from scratch ≈ 3.6B π0.5 fine-tuned with 50 demos (57.2 vs 60.9), but in real π0.5 is much better (68.8 vs 46.2) — real-world pretraining matters for real deployment. Consistent with "pretraining helps most in low data".
Relevance: 50-demo regime exactly ours. Best-of-N sampling + learned WM/value is an option to boost a small DP/flow policy, but adds latency and a WM training pipeline; lower priority than robustness fixes. Real π0.5 > DP gap (69 vs 46 at 50 demos) is evidence that pretrained VLAs help in real low-data settings — but π0.5 does not fit our 8 GB inference budget comfortably.
Decision impact:
 - Q09 auxiliary objectives / world models: supports WM-based test-time steering (+29 pts real for DP, +11 for π0.5) — M (20 trials/task, 4 tasks).
 - Q12 model size: sim DP 550K ≈ π0.5 3.6B (57 vs 61), real π0.5 69 vs DP 46 at 50 demos — M (pretraining, not size per se).
 - Q13 data quantity: LPS@50 demos > DP@100; gains vanish by 200–300 demos — L (sim Can only).
 - Q06 chunking: horizon 16 fine, 24 hurts LPS — L.
