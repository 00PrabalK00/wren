# W3_REBOOTFromFailuretoRecoveryADatasetandBe — REBOOT: From Failure to Recovery – A Dataset and Benchmark for Precision Assembly (2026, arXiv id not in text)
Setup: Trossen WidowX AI bimanual leader/follower (2×6DoF + gripper, 14-D), LeRobot fork; 4 RGB-D cams 480×640 (overhead, low-angle, 2 wrist); 30 Hz; actions = absolute target joint positions from leader arms. 18 precision connector tasks (9 install / 9 remove, clearance 0–2.73 mm); per task 60 expert demos + 60 recovery demos (2,160 total). Object start varied within 3–6 cm radius; goal fixed. Policies benchmarked: ACT, Diffusion Policy, π0-FAST (15 rollouts/task/policy, 810 total). Model sizes/compute not reported.
Claim: a dataset where half the episodes are teleoperated failure-then-recovery, allocated per phase in proportion to observed policy failures, plus phase-level evaluation, exposes failure structure that binary success hides.
Evidence (expert-only-trained policies; no result yet for training WITH recovery data):
 - Install mean success 16% vs remove 56% (aggregated over 3 policies).
 - Align(place)+Engage(place) = 54% of all install failures; Transport = 8%.
 - Engage-phase failure by symmetry: continuous 14%, C1 19%, C2 22%.
 - ACT vs DP similar overall failure; ACT fails Align on M12 install (6/15 vs 7/15 in text, ambiguous), DP stalls Engage on RJ45 (5/15 vs 4/15). π0-FAST highest success on both install and remove (per-policy totals figure only).
Ablations: none. The paper does not train on recovery data or compare expert-only vs expert+recovery; it proposes the uses (train only on corrective segment, cut failure segment, mix) as future work.
Failure/limitations: authors: fixed lighting/cameras/objects (no visual robustness), no F/T or audio, right-arm bias, untrimmed trailing static segments (trimming tool released). Critical read: 60 demos/task with 3–6 cm randomisation, and 16% install success for all three families — sub-mm insertion is beyond ACT/DP/π0-FAST in this data regime. Numbers in the per-policy comparison are tiny (15 rollouts) and differences of 1/15 are noise.
Conflicts: consistent with RaC / HG-DAgger-style evidence that recovery data targets where policies actually fail; cites [20] that IL policies copy demo pauses and stall at uncertain states (same finding as SeedPolicy note: trim pauses).
Relevance: moderately relevant as a protocol for SO-101 (same LeRobot leader/follower paradigm, same absolute-joint action space at 30 Hz). Recipe to borrow: train on ~50 clean demos, roll out ~20 times, log the failing phase, then teleop recoveries reproducing those failure states (start recording at object init). Pumpkin→tray is loose-tolerance, so per their data the Engage/Align(place) failures should matter less than grasp alignment. No evidence on whether this beats simply more expert demos.
Decision impact:
 - Q13 data quality: supports adding failure-calibrated recovery demos (phase-targeted) — confidence L (no training result, only rationale + failure stats).
 - Q13 data quality: trim trailing static/idle segments — confidence L (authors' own caution + cited finding).
 - Q01 action head: ACT ≈ DP overall on precision assembly with 60 demos, π0-FAST best — confidence L (15 rollouts, figure mostly).
 - Q02 action space: absolute leader joint targets at 30 Hz used on LeRobot leader/follower rig — confirms common practice, no comparison — L.
