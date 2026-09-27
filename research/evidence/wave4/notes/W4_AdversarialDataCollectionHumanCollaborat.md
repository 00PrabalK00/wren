# W4_AdversarialDataCollectionHumanCollaborat — Adversarial Data Collection: Human-Collaborative Perturbations for Efficient and Robust Robotic Imitation Learning (2025, arXiv 2503.11646)
Setup: AgiBot G1 (dual-arm humanoid upper body, AR teleop), pi0 fine-tuned from AgiBot-World checkpoint, default 3 cams (head + 2 wrist). One composite task "grasp [fruit] place into [plate]" (kiwi-place held out). Traditional: 120 episodes / 90k frames; ADC: 80 episodes / 96k frames (episodes = scene resets; ADC episodes contain many mid-episode perturbations). 10 real trials per condition. Also ACT on ALOHA (cup-on-plate) — qualitative only.
Claim: a second human perturbing object positions / instructions mid-episode during teleop yields denser, recovery-rich data; 20% of ADC data beats 100% conventional data.
Evidence (pi0, 10 trials each):
 - Static env, avg SR by table height: Var1 Trad 0.47 vs ADC 1.0; Var2 0.30 vs 1.0; Var3 (extreme) 0.13 vs 0.72. Traditional = 0.0 on every "varied positions" cell (object sampled across whole workspace) at all heights; ADC 1.0 at Var1/2.
 - Dynamic visual perturbation (object/container moved before grasp): Trad 0.0 vs ADC 0.88 avg.
 - Linguistic perturbation mid-task: Trad 0.0 everywhere; ADC 1.0/1.0 before grasp, 0.6/0.7 during grasp, 1.0/1.0 after grasp.
 - Camera masked (zeros): right-wrist masked Trad 0/0 vs ADC 0.6/0.5; head masked 0/0 vs 0.7/0.4; avg 0.0 vs 0.55.
 - Data efficiency (Table VI, avg static+dynamic): 100% Trad 0.24; 20% ADC 0.65; 50% ADC 0.74; 100% ADC 0.89.
 - Cost: 25 s vs 40 s collection per episode (+label 10 vs 15 s); per-frame cost ~equal (46.7 vs 45.8 ms/frame); 2 operators.
Ablations: data fraction (above). No ablation separating visual vs linguistic perturbation, or ADC vs simply "more diverse initial positions" (confound: traditional data has objects near table center only, so its 0.0 on varied positions is a coverage failure, not evidence that mid-episode perturbation per se is needed).
Failure/limitations: 10 trials per cell, one task family, single robot; baseline's collapse is largely out-of-distribution positions. ACT/ALOHA result only qualitative: ADC data caused oscillatory grasping with varied heights — authors blame small-model capacity for high state coverage/low action consistency (anecdotal). Novel tablecloth generalization only qualitative (figure).
Conflicts: agrees with Data Scaling Laws / diversity-over-count findings (coverage of positions matters more than count). The ACT-oscillation remark hints small models may struggle with very diverse/inconsistent data (cf. "action consistency" arguments in data-quality papers), a caveat for us since we will run small models.
Relevance: very cheap to adopt for SO-101 — a second person nudges the pumpkin/tray mid-demo, moves them across the workspace, occasionally occludes; teleoperator recovers. Produces recovery data and view diversity on wrist cam. Masked-camera result suggests multi-cam redundancy is learned only if data has occlusions. Caveat: our model is small; keep perturbations moderate so action consistency stays high.
Decision impact:
 - Q13 data quality/diversity: supports in-episode perturbation + recovery demos + full-workspace position coverage over more static demos — confidence M (pi0 real, huge effect, but 10 trials, confounded with position coverage).
 - Q14 robustness: supports data-side robustness (moved objects, dynamic changes) — M.
 - Q11 cameras: data with occlusions makes policy robust to one camera dropping (0.0 → 0.55) — L.
 - Q12 model size: qualitative warning that small ACT oscillates on highly diverse ADC data — L.
