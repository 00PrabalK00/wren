# W4_3DCAVLALeveragingDepthand3DContexttoGene — 3D-CAVLA: Leveraging Depth and 3D Context to Generalize Vision Language Action Models for Unseen Tasks (2025, arXiv 2505.05800)
Setup: OpenVLA-OFT (~7B, LoRA, action chunking, L1 regression) fine-tuned with (i) GPT-5.2 chain-of-thought rewritten instructions, (ii) ~1M-param PointNet-style encoder on back-projected depth point cloud (one per camera), (iii) task-aware ROI pooling (NER + Molmo + SAMURAI/SAM2 masks, disabled for 30% of train samples). LIBERO: 50 demos/task, 50 trials/task; LIBERO-Unseen: 10 new compositional tasks x 50 trials. Real: Franka, 10 pick-place tasks (5 YCB-like objects, 2 target regions), 50 demos/task, wrist + third-person cam, 5 random 7/3 seen/unseen splits x 10 trials/task. 1x A100, batch 8. Rollout 4.3 Hz (4.4 Hz without depth).
Claim: adding depth point-cloud features + CoT text + ROI pooling to a VLA mainly improves generalization to unseen task compositions.
Evidence:
 - LIBERO avg (wrist+3rd+state): 3D-CAVLA 98.1 vs OpenVLA-OFT 97.1 vs pi0 94.2 vs MDT 76.1 (margins small, near ceiling).
 - LIBERO third-person only: 3D-CAVLA 82.6 vs Diffusion Transformer 82.4, OpenVLA 76.5, DP 72.4, Octo 75.1.
 - LIBERO-Unseen avg: DP 27.0, OFT 36.4, ECoT* 40.6, 3D-CAVLA 45.2.
 - Real (Table V, 10 trials/task): Seen DP 84.2 / OFT 88.6 / 3DC 90.0; Similar (compounded instruction) 46.0 / 54.4 / 60.0; Unseen 21.8 / 30.2 / 38.0.
 - Training convergence: 3K vs 10K epochs for OFT (attributed to TA-ROI).
Ablations (Table IV, Seen / Unseen): full 98.1/45.2; w/o CoT 97.4/42.4; w/o Depth 97.0/41.0; w/o TA-ROI 98.2/41.4. Depth removal = largest drop but only ~1.1 pts in-distribution, ~4 pts on unseen. Authors also state (Fig. 4 caption) SE(3) waypoint actions outperformed velocities on the real robot — no numbers.
Failure/limitations: authors: policy reverts to trajectories of seen tasks (overfitting to small fine-tune set); robot oscillates near grasp point without closing (low image variation near contact); wrong Molmo masks mislead policy. Critical read: all ablations are sim-only (LIBERO), single seed, differences 1–4 pts on 50 trials/task; real ablation of depth is absent; the "real-world" gain mixes three components; 7B backbone on A100 at 4.3 Hz — nowhere near our 8 GB budget. Depth has no lighting/camera-shift test.
Conflicts: consistent with other depth-add papers (GeoVLA, iDP3-type) that 3D helps most in clutter/spatial generalization, but effect size here is small in-distribution; agrees with our prior that frozen external modules (detectors/segmenters) add brittle failure modes.
Relevance: Low-to-moderate. The idea of a tiny (~1M) PointNet branch on RealSense point cloud concatenated as a token next to RGB features is cheap and adaptable to a small policy; the evidence it helps is sim-only and small. ROI-mask pooling with a frozen segmenter could help against background/lighting shift but introduces dependence on Molmo/SAM (heavy for 8 GB, though run once per episode).
Decision impact:
 - Q04 3D/depth: supports adding a light point-cloud branch alongside RGB — confidence L (sim ablation, -1.1 seen / -4.2 unseen without depth, no real ablation)
 - Q08 language: supports LLM-expanded step-wise instructions for compositional generalization — confidence L (sim, +2.8 unseen)
 - Q14 robustness: object-mask/ROI pooling helps unseen-task generalization, not in-distribution — confidence L
 - Q02 action space: EE SE(3) waypoints better than velocities on real Franka — confidence L (stated only, no numbers)
 - Q12 model size: not usable at our budget (7B, 4.3 Hz on A100) — confidence M
