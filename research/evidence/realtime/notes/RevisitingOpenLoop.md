# RevisitingOpenLoop — Revisiting Open-Loop Execution in Robotics: Toward Reactive, Higher-Performing Policies (Zeng, Agarwal, Bati, Lee, Ancha, Tedrake; MIT, Aug 2026, arXiv 2608.15938)
Setup: Diffusion-Policy-style chunked policies; sweeps of observation context T_o and execution horizon T_exec. Sim: FurnitureSim OneLeg (200 and 1000 scripted non-Markovian demos), PushT-D (160 human), GearInsertion (200), Kitchen (581). Real: bimanual SinglePillDispense (516 demos, 1.34 h) and SlipIntoBaggie (540 demos, 5.24 h), 20 trials per cell with 95% CIs.
Claim: long open-loop execution mainly helps SHORT-CONTEXT policies imitate non-Markovian demonstrations (pauses, history-dependent behaviour); compounding-error mitigation matters less; with long enough context, closed-loop (T_exec 1–2) is optimal.
Evidence:
 - Real (Table 1, SR at T_exec 2/4/8): SinglePill T_o=2: 50/60/75; T_o=8: 90/80/60; T_o=12: 75/70/60. SlipIntoBaggie T_o=2: 60/40/80; T_o=8: 85/70/55; T_o=12: 75/65/65. Optimal horizon moves from 8 (short context) to 2 (context 8), and absolute SR rises.
 - FurnitureSim OneLeg 1000 demos: best long-context (T_o 12–20), T_exec<4 policy 93.2% vs best short-context (T_o=2, T_exec=6) 90.6%; at 200 demos the benefit is smaller (figure).
 - With sufficient context, T_exec=1 optimal or near-optimal in PushT-D, GearInsertion, Kitchen (figure).
 - Too long context (T_o=12) degrades in both real tasks — sample complexity.
Ablations: non-Markovianity vs compounding error controlled experiments (Sec. 4) — non-Markovianity has the larger effect (figures).
Failure/limitations: data scales 160–1000+ demos, much larger than ours; optimal context–data trade-off left open. Critical read: the gain from long context appears data-hungry (grows with 1000 vs 200 demos).
Conflicts: agrees with WhyDoesActionChunking (chunking's value = predicting from past obs / non-Markovian demos) and with DEHP/SmolVLA that short execution helps when the policy can stay coherent; conflicts with BID/Copycat/RevisitingOpenLoop's own T_o=12 result that long history often overfits at small data.
Relevance: moderate: with 50–150 demos we should NOT expect long-context to pay off; keep short context + chunking, and fix coherence via prefix conditioning rather than via long history. The real table is a clean illustration that the best execution horizon is policy-dependent (swings of 20–35 pts).
Decision impact:
 - Q06 execution horizon: optimal T_exec depends on context length; with 2-frame context, longer execution (8) was best on real tasks — M (20 trials, 500+ demos).
 - Q07 history: longer context enables reactive short-horizon control only with large data; T_o=12 hurt — L/M for our data scale.
