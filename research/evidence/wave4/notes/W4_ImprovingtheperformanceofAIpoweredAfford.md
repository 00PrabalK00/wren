# W4_ImprovingtheperformanceofAIpoweredAfford — Improving the performance of AI-powered Affordable Robotics for Assistive Tasks (2025, arXiv 2510.21771; CoRL 2025 workshop-style, high-school author)
Setup: LeRobot Moss arm (6 servos, SO-100-class, leader/follower teleop); 2 cameras (top-view smartphone, side-view laptop cam); 3 tasks (feeding 39 demos/18k frames, wiping 47/27k, fetching medicine 45/13.5k); ACT and "PACT" (ACT + phase token = frame index / max episode length), ± temporal ensembling (TE); embedding dims 32/64/128/256/512; runs on a laptop; "accuracy" metric, number of trials not stated (10 h testing total).
Claim: adding a normalized time/phase token to ACT disambiguates visually similar frames; TE smooths small models; PACT allows ~5× smaller model at similar accuracy.
Evidence (Table 1, accuracy %; column parsing of the extracted table partially ambiguous — ACT and PACT without TE only have values for dims 128/256/512, dims 32/64 "unstable without TE"):
 - Fetching: ACT (128/256/512) 50.0/69.9/79.9; PACT 83.3/86.6/93.3; ACT+TE (32→512) 9.9/16.6/63.2/73.3/76.6; PACT+TE 63.2/70.0/73.3/80.0/100.0.
 - Wiping: ACT 97.5/97.6/99.0; PACT 98.9/100/99.8; ACT+TE 59.6/88.1/91.2/98.3/99.8; PACT+TE 75.9/96.3/100/99.6/100.
 - Feeding: ACT 54.8/66.4/68.4; PACT+TE 76.1/85.2/90.8/87.1/88.1; (ACT+TE / PACT values interleaved in extraction: 67.2, 72.1, 73.1, 73.1, 87.6, 69.1, 76.5, 69.7).
Ablations: phase token → +10–30 pts on fetching/feeding at equal dim; TE makes dims 32/64 usable (jitter otherwise), TE slows robot motion; bigger embedding dim generally better, saturating ~128–256.
Failure/limitations: no trial counts, no error bars, no variance, single author; "accuracy" undefined; ACT dims 32–64 are far below ACT default 512 so size claims are about tiny models. Phase token = elapsed-time conditioning, which can break when a rollout runs slower/faster than demos or after recovery (not tested).
Conflicts: Time/phase conditioning helping mirrors χ0's "stage" signal and history-helps findings for visually ambiguous states; but time-index conditioning risks the timing-shortcut failure that history/copycat papers warn about.
Relevance: Same hardware class and demo counts (≈40–50 demos) on a laptop. Our pick-place pumpkin task has few visually ambiguous phases (gripper state + wrist cam disambiguate), so the phase token is low priority. The observation that ACT at d≤64 jitters and needs TE is a warning for aggressive downsizing.
Decision impact:
 - Q07 history/memory: weak support for a progress/phase signal to disambiguate similar frames — confidence L (no trial counts).
 - Q12 model size: ACT dim ≥128 needed; ≤64 unstable without TE — confidence L.
 - Q06/Q10 temporal ensembling: TE stabilizes small models but slows motion — confidence L.
