# W3_WhatistheBetterCurriculumControllerShape — What is the Better Curriculum: Controller-Shaped Grasping Behavior for Contact Force-Sensitive Manipulation (2026, arXiv 2609.25887, CoRL 2026)
Setup: Real Piper 6-DoF arm + gripper teleoperated with an SO-101 LEADER arm; RealSense wrist cam + front RGB cam; dual MC-Tac tactile sensors (used only by a 25 Hz reflex controller, not by policy). Task: grasp/lift/place a 3.5 g fragile plastic cup. 30 demos per condition. Policies: ACT 18M (ResNet18, 15 Hz loop) and pi0.5 (2B+, LoRA, 10 Hz data, 20 Hz execution, 10-step synchronous chunks => ~1.7–1.8 Hz re-query). RTX 5090. 20 trials per row; 4 extra seeds x 20 trials for robustness. Recorded action for reflex data = FOLLOWER realized joint/gripper state (not leader command).
Claim: using a deterministic tactile reflex controller at collection time produces consistent, controller-shaped grasp demos; a tactile-free student learns them far better than best-effort manual demos; disturbance rejection still needs a runtime high-rate reflex.
Evidence:
 - ACT, 30 demos each (Table 1): reflex-data 95% stable (19/20), 0% drop; visually-screened manual (best 30 of 100) 15% stable, 30% drop (p=4.1e-7); manual + runtime arbiter 50% stable, 30% drop. Extra seeds: 95.0±4.1 / 16.3±4.8 / 48.8±2.5.
 - Contact-screened manual (top 30 of 100 by tactile metric, single run): 30% vs 95% (p=3.9e-5).
 - pi0.5 (Table 3): reflex 95% vs manual 5% vs manual+arbiter 55%; extra seeds 96.3±4.8 / 6.3±4.8 / 52.5±6.5. Unseen paper cup: 80% (8/10) vs 30% (3/10), p=0.07 n.s.
 - Disturbance during place (Table 5, pi0.5 reflex-data): policy-only retained 55% (11/20) vs policy+arbiter 100% (20/20); seeds 52.5±6.5 vs 98.8±2.5.
Ablations:
 - Gripper second-order dynamics (smoothness-shape) loss, lambda 0.1 (Table 4): teacher-near runs ACT 15->18/20, pi0.5 12->16/20; time to release 15.7->13.4 s (ACT), 28.1->21.7 s (pi0.5); but full-horizon teacher-near occupancy dropped 68.7->54.8% (ACT).
 - Naive tactile images as extra camera inputs: ACT severely degraded; pi0.5 no gain (appendix, no numbers).
Failure/limitations: one object family, one operator, collection order not randomized (reflex first), 20 trials, outcome labels by authors from video; the reflex vs manual comparison also changes the recorded action source (follower-realized vs leader-with-button gripper), so "consistency of demos" and "action label = realized follower state" are confounded.
Conflicts: Supports "demo consistency > demo count" findings; contrasts with the ACT recommendation to record LEADER joint positions as actions (force implicitly encoded by leader-follower gap) — here follower-realized states were used for the winning condition. Consistent with PAINT/RTC-style arguments that chunked policies cannot react within a chunk; a high-rate low-level reflex is needed for disturbances.
Relevance: Moderately high: same leader hardware (SO-101), same camera layout (RealSense wrist + front), ACT at 18M works on 30 demos when demos are consistent. For the pumpkin task: grasp consistency (e.g., fixed gripper close command/force level) matters more than more demos; a small deterministic gripper rule at runtime can fix drops. pi0.5 at ~1.7 Hz re-query shows large VLAs are too slow to react.
Decision impact:
 - Q13 data quality: consistent (controller-regulated) demos >> best-of-100 manual demos at equal count (ACT 95% vs 15–30%) — confidence M-H (real, significant, 2 backbones, but narrow task).
 - Q12 model size: ACT 18M matched pi0.5 2B (95% vs 95%) on this in-distribution task with 30 demos — confidence M.
 - Q10 latency/reactivity: chunked policies at low re-query rate can't reject disturbances (55% vs 100% with 25 Hz reflex) — confidence M.
 - Q09 aux objectives: second-order smoothness loss on gripper sharpens entry/release — confidence L.
 - Q02 action space: follower-realized state as action label worked (vs leader command) but confounded — confidence L.
