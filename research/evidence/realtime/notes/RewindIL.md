# RewindIL — Rewind-IL: Online Failure Detection and State Respawning for Imitation Learning (2026, arXiv 2604.16683)
Setup: real bimanual AgileX Piper (low-cost 6-DoF arms, parallel grippers) at 30 Hz; 6 tasks (Cup & Box, Pencil & Notebook, Box & Wrench, Drawers & Hammer, Toolbox & Knife, Folding Towel); base ACT trained on 50 expert demos/task (100k iters); 20 rollouts per condition; "Perturb" = human nudges objects / reopens drawers until a subtask fails. Sim: RoboCasa 3 tasks, 50 rollouts. Also flow-matching head variant of ACT.
Method: (1) TIDE (Temporal Inter-chunk Discrepancy Estimate): discrepancy among overlapping predictions of consecutive action chunks for the same future timestep (policy self-consistency; single sample, no batch), thresholded by split conformal prediction on successful rollouts. (2) Offline, a VLM picks recovery checkpoints in demos (completed grasps, subgoal transitions); frozen policy encoder stores their embeddings. Online, cosine similarity to checkpoint templates tracks the latest "peaked" (reached) checkpoint and snapshots the action there. (3) On alarm: replay the checkpoint action (move back), clear the policy's action queue / temporal ensembler, restart inference.
Evidence:
 - Detection (Table I, 6 ACT tasks): TIDE avg balanced accuracy 0.95 vs FAIL-Detect 0.83, Clustering-OOD 0.60, RND 0.59, Mahalanobis 0.58. FAIL-Detect over-triggers on Folding Towel (TNR 0.08) vs TIDE TNR 0.92.
 - Real success (Table II avg, no-perturb / perturb): ACT 66.7 / 18.3 → ACT+Rewind-IL 80.0 / 76.7 (+5 to +20 pp per task unperturbed; largest on Drawers & Hammer and Toolbox & Knife, +20). (A second "Average" row in the extraction reads 70.0/20.0 → 85.0/75.0; exact subset unclear.)
 - Sim RoboCasa: +15 pp on each of 3 tasks (e.g., Close Toaster Oven Door 55 → 70).
 - Flow-matching ACT: TIDE balanced acc 0.97–1.00 (avg 0.99); RND 0.96; FM + Rewind-IL +10 to +20 pp (90% on two tasks).
 - Overhead (Table V): TIDE 0.037 ms + cosine match 0.096 ms + bookkeeping 0.056 ms = 0.22 ms total (<1% of ACT inference).
Ablations: detection and respawn not separable (detection alone = episode termination baseline).
Failure/limitations: recovery = rewinding to a previously visited state; it cannot fix failures that need new behavior; checkpoint selection needs an offline VLM pass; 20 rollouts per cell.
Conflicts: disagrees with FAIL-Detect's ranking (here FAIL-Detect over-triggers on deformables); agrees with Sentinel/FIPER that action-consistency signals are informative, but achieves it with a SINGLE sample via overlap of successive chunks — much cheaper than STAC's batch.
Relevance to SO-101: the single most transferable Track-B paper: low-cost arm, ACT with 50 demos, 30 Hz, overhead 0.2 ms, no retraining. Directly applicable to "failed grasp → rewind to pre-grasp checkpoint and retry" and to object-moved disturbances.
Decision impact:
 - Add TIDE-style inter-chunk discrepancy monitor with conformal threshold — SUPPORTED — M/H (real, low-cost arm, 50 demos, cheap).
 - Recovery by rewind-to-checkpoint + re-query (clear queue) — SUPPORTED — M.
