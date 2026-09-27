# HiPolicy — Hierarchical Multi-Frequency Action Chunking for Policy Learning (2026, arXiv 2604.06067)
Setup: plug-in for DP (2D) and DP3 (3D). Jointly predicts action chunks at M=3 temporal frequencies (coarse→fine), each conditioned on history observations sampled at the matching frequency, with cross-frequency attention fusion; chunk Lc=8, history Lh=3. Entropy-guided execution: N=100 parallel samples → per-step Gaussian entropy; thresholds pick which frequency level's chunk to execute (low entropy → coarse/fast progress; high entropy → fine high-frequency actions). Sim: RoboTwin 1.0/2.0 (100 scripted demos/task, 100 eval episodes). Real: Franka + Robotiq, DROID-style 3 ZED cams, 8 tasks, 10 trials each, control at fixed 15 Hz.
Claim: multi-frequency chunks capture long-horizon/non-Markovian structure AND fine closed-loop control; entropy decides how much to commit.
Evidence:
 - Sim: relative +62% (vs DP) and +44% (vs DP3) on RoboTwin (Table 1).
 - Real (Table 5): DP 60% vs HiPolicy 85% avg SR; steps 129 vs 111 (14% faster).
 - Entropy-guided execution (Table 3, 8 tasks): DP 24% SR /133 steps; HiPolicy w/o EG 45%/139; HiPolicy 41%/100 → 25% faster at −4 pts SR.
 - Sampling cost (Table 4): N 1→100 adds only 2.0 ms and ~+100 MB GPU memory because condition features are computed once; SR saturates ~N=100.
Ablations (Table 2, RoboTwin 1.0): conditioning only on high-frequency obs hurts most (e.g., Block hammer beat 67 → 0; Block handover 100 → 61); w/o fusion −6%; w/o hierarchy big drop. Entropy thresholds (Table E.2): more high-freq execution 47% / 143 steps; default 45% / 108; more low-freq 37% / 75 → threshold trades success vs speed.
Failure/limitations: 10 real trials/task; entropy threshold hand-tuned; DP baseline "running at 15 Hz" fails on non-Markovian pauses.
Conflicts: entropy/uncertainty from multi-sampling is useful here as an execution-horizon selector, while Knowing-When-to-Stop (W3) found multi-sample truncation caused stop-go pauses on a real robot (18.3%) and BCP (W3) found uncertainty triggers marginal and costly. Difference: here sampling is cheap because only the small head is resampled (2 ms).
Relevance to SO-101: high feasibility (DP-scale, 2 ms sampling overhead). Suggests an uncertainty-gated execution horizon for our small policy: commit longer in transit, re-plan often around grasp. Evidence is one paper with modest real trials.
Decision impact:
 - Uncertainty (sample spread) as a re-plan / horizon trigger for a small diffusion/flow head — PROMISING — L/M.
 - Condition on multi-rate history rather than only latest frames — L/M.
