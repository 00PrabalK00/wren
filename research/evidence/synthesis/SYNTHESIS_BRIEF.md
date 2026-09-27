# Brief for the final synthesis

You are the final synthesizer of a large literature review. Your output decides how the user builds their own small, robust, real-time robot policy. Be rigorous, adjudicate conflicts explicitly, and state confidence honestly. Never invent numbers: every number you cite must come from a note, ledger line, card or report in this directory tree, and you should cite the source file.

## Read first (in this order)
1. synthesis/CONTEXT.md — the user's setup, data, failures, constraints, and the known conflicts you must adjudicate.
2. synthesis/STATS.md — size of the evidence base.
3. realtime/TRACK_A_REPORT.md and realtime/TRACK_B_REPORT.md — real-time execution + decision architecture (the user also asked for this topic explicitly).
4. fulltext/PROGRESS.md — running conclusions from the first deep reads.
5. synthesis/ledger_by_decision/*.md — every full-text finding grouped by decision (Q01…Q14). This is your main evidence table; each line points to a paper short name.
6. For every decision, open the underlying notes for the strongest and the conflicting evidence (synthesis/NOTES_INDEX.md maps short names to note paths in fulltext/notes, wave3/notes, wave4/notes, realtime/notes). Prefer: real robot > sim; controlled ablations; more trials; low-cost arms (SO-100/101, Koch, Piper, AgileX); 20–150 demos; 8 GB-class compute. fulltext/notes are the most carefully written.
7. synthesis/cards_by_decision/*.md — ~4,800 abstract-level claims from screening all 7,162 papers. Use them to check breadth/consensus and to spot missed evidence, but weight them far below full-text notes.

## Deliverables (write both files)
### synthesis/FINAL_REPORT.md
1. Executive summary (≤1 page): the recommended policy and why, top 10 findings, what changed vs. the user's first naive plan (frozen DINOv2 + L1 + ~100M params + blending) and vs. SmolVLA.
2. Per-decision verdicts Q01–Q14. For each: verdict; evidence table (paper | setting | key number | direction | weight); explicit adjudication of every conflict listed in CONTEXT.md (explain WHY results differ: data regime, latency, model size, sim vs real, metric); confidence H/M/L; what cheap ablation would resolve residual doubt on our robot.
3. The architecture spec: exact components (encoder + init + fine-tune scheme + resolution + token handling; per-camera handling incl. wrist vs scene and any regularization/masking; optional depth/object-centric branch and when to add it; language path for the 2nd object; trunk size; action head type, steps, chunk length in seconds and steps for 10 and 30 fps; action representation; proprio handling; auxiliary losses), with parameter counts and expected latency on an RTX 5060 8 GB, and why each choice.
4. Training recipe: augmentations (with the hue caveat), normalization, optimizer/LR per module, steps, checkpoint selection (not by val loss), EMA, noise on proprio, etc.
5. Data-collection protocol for the SO-101 (how many demos, pumpkins, lighting/background/camera variations, recovery/intervention demos, operator consistency, fps, idle trimming, gripper timing, green screen or segmentation-based background replacement).
6. Real-time execution + decision architecture (merge Track A/B): executor, async/continuity method, re-query cadence, monitors, rewind/retry, latency budget, profiling steps.
7. Evaluation protocol: conditions (in-dist, lighting, new pumpkin, camera shift, distractors, placements), trials per condition, failure taxonomy, recovery rate, statistics.
8. Build plan: staged roadmap with the ablation order (what to build and test first for maximum information), including baselines (ACT, the current SmolVLA fixed for latency) and go/no-go criteria.
9. Risks, unknowns and where the literature is thin or contradictory for our exact setting.
10. Appendix: key references table (short name, title line, venue/year if known, why it matters).

### synthesis/EXECUTIVE_SUMMARY.md
≤2 pages, plain language, for the user: the design, the data plan, the real-time plan, and the first 3 things to build.

## Our code (for integration context only; do not modify)
/home/zuci/So101/server.py (Episode Studio: recording UI, policy test panel), /home/zuci/So101/teleop_runner.py (100 Hz control loop + LeRobot recording), /home/zuci/So101/eval_real.py (async inference runner with blending), dataset at /home/zuci/ripple-research/data/lerobot/so101_pumpkin_v1.
