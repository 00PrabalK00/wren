# W4_TheCurseofPrecisionADataScalingLawforHig — The Curse of Precision: A Data Scaling Law for High-Precision Robotic Manipulation (2026, arXiv 2607.23108, ICRA'26)
Setup: ManiSkill3 sim, Franka; Diffusion Policy (ResNet-18 + 1D U-Net, 100 DDPM steps), two 256×256 RGB-D cams (static + wrist) + proprio, delta-EE actions; scripted/motion-planned experts (Peg Insertion clearance 4–10 mm; Stack Cuboid base half-side 4–10 mm) and RL expert (Roll Ball, target radius 35–200 mm); success-only trajectory pools; N ∈ ~{200, 500, 1000, 2000}; single training run per (N,P), ~20 A100-h each; top-3 of periodic evals × 100 episodes. >100 runs total. Heavy domain randomization (object pose/size, hole size/position).
Claim: failure rate follows a power law in N at fixed precision, and the N needed for a fixed success rate grows super-exponentially as tolerance P approaches a system-specific limit c: log N ∝ 1/(P − c); c depends on sensors, expert quality and task randomization.
Evidence:
 - SR law slopes a in log(1−SR)=a·logN+b (Table I): Peg 4 mm −0.19 → 10 mm −0.72; Stack 4 mm −0.06 → 10 mm −0.26; Roll Ball 35 mm −0.07 → 200 mm −0.50. Tighter tolerance → much flatter data scaling. R² 0.84–0.99.
 - Precision law (Table II): single c per task fits all target SRs (R² ≥ 0.968): Peg c=2.35 mm, Stack c=2.75 mm, Roll Ball c=20.3 mm.
Ablations (Peg, Table III, limit precision c; lower = better):
 - Baseline (static+wrist cam, conservative expert with corrective re-alignment moves, high randomization): 2.35 mm.
 - Remove wrist camera: 3.85 mm (worse).
 - "Aggressive" single-shot expert (only 50% raw success, filtered to successes, no hesitant corrections): 1.27 mm (much better) → unambiguous demos beat cautious multi-attempt demos.
 - Low randomization (only XY position): 1.00 mm.
 - Model capacity (Roll Ball, Fig. 4): U-Net base width 64 → no scaling trend (R² 0.22); width 256 → clean law (R² 0.99) (figure only).
Failure/limitations: sim-only; scripted experts (not human); single seed per point; data sizes ≥200 (above our regime); success measured with privileged checks.
Conflicts: Complements "Data Scaling Laws in IL" (Lin et al.: diversity > count for generalization) — here in closed-world precision, count matters but with sharply diminishing returns near c; system changes (wrist cam, cleaner demos) shift the limit. Agrees with ACT/Robomimic findings that demo quality/consistency (not just success) matters and with the "pauses/hesitations cause non-Markovian ambiguity" discussion.
Relevance: Our pumpkin-into-tray task is low precision (cm tolerance), so we are likely far from c and 50–100 demos may suffice; but SO-101 backlash raises effective c. Practical lessons: keep wrist camera; teleoperate decisively (avoid hesitation/re-alignment wiggles; drop ambiguous demos even if successful); limit unnecessary scene variation if precision matters; test on looser-tolerance variants to diagnose whether failures are data-limited.
Decision impact:
 - Q13 data quality/quantity: unambiguous direct demos lower achievable precision limit 2.35→1.27 mm vs cautious corrective demos; data need grows super-exponentially near limit — M (sim, scripted, large N)
 - Q11 cameras: removing wrist cam worsens precision limit 2.35→3.85 mm — M
 - Q12 model size: too-small denoiser (width 64) shows no data scaling on dynamic task; width 256 does — L (figure only)
 - Q14/diversity: higher randomization raises c (1.00 → 2.35 mm) — L
