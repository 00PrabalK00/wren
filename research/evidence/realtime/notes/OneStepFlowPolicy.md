# OneStepFlowPolicy (OFP) — One-Step Flow Policy: Self-Distillation for Fast Visuomotor Policies (Li, Sun, Chen, Mar 2026, arXiv 2603.12480)
Setup: from-scratch (no teacher) one-step flow policy: flow-matching anchor + self-consistency loss across time intervals (few-step capability) + self-guided regularisation (sharpen toward high-density modes; drives 1-step quality) + warm start from the previous action chunk (shorter transport). No JVPs. 56 sim tasks (Adroit, DexArt, Meta-World; 2D image and 3D point cloud), 3 seeds; transfer into π0.5 on RoboTwin 2.0 (NFE=1 vs 10). No real robot.
Evidence:
 - 2D image avg (Table 1): OFP NFE=1 68.3 vs DP 100-step 64.2, DP 10-step 60.9, FM Policy 100-step 67.2.
 - 3D point cloud (Table 2): OFP NFE=1 +8% over DP3-100 avg and +19.7% over 3D FM Policy-100.
 - Latency: OFP 17.58 ms/chunk vs DP3-100 3225.67 ms and FM-100 1865.72 ms (~183×/106×); slightly slower than OneDP and MP1 due to warm start.
 - Few-step (Table 3, 4 DexArt tasks avg): OneDP-1 62.5; CP-1 60.7, CP-4 64.2; OFP-1 64.5, OFP-4 66.2.
 - Data scaling (DexArt Faucet): OFP 32.7% (20 demos) → 51.0% (150); MP1 degrades sharply at 20 demos and drops after 100 demos; MP1 training showed loss spikes (JVP sensitivity).
 - π0.5 RoboTwin (Fig. 5): 1-step OFP surpasses the 10-step original (numbers figure-only).
Ablations: self-consistency needed for few-step; self-guided regularisation drives 1-step gains; warm start helps (qualitative in text).
Failure/limitations: sim only; mostly state/point-cloud; multimodality preservation not stress-tested. Critical read: 100-step baselines are straw-men for latency; the relevant comparison (10-step flow) is only ~4–7 pts lower and ~10× slower.
Conflicts: disagrees with MP1 on MeanFlow stability at low data; agrees with SnapFlow/SeFA that 1-step flow can match or beat 10-step. Warm-start from previous chunk = the same continuity lever as RTC/StreamingDP.
Relevance: moderate: if our head latency ever matters, a 1–4-step self-distilled flow head is trainable from scratch on 20–150 demos without a teacher; for SmolVLA, prefill dominates instead.
Decision impact:
 - Q10 fast generator: teacher-free 1-step flow ≥ 10–100-step baselines in sim — M (56 tasks, no real).
 - Q01 head: avoid JVP-based MeanFlow at very low data (instability) — L/M.
