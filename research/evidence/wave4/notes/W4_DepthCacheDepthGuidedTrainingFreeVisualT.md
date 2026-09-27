# W4_DepthCacheDepthGuidedTrainingFreeVisualT — DepthCache: Depth-Guided Training-Free Visual Token Merging for VLA Model Inference (2026, arXiv id not in text)
Setup: training-free token merging for large VLAs (π0.5 3.3B, OpenVLA 7B, GR00T 2.2B); depth maps split image into K=3 depth clusters, near-field kept, far merged progressively over W=5 frames; LIBERO 4 suites ×100 eps; real PIPER 6-DoF arm, 2 RealSense D435 (static + wrist), 3 core tasks ×20 trials + 2 extended ×15; RTX 4090.
Claim: depth-guided spatially/temporally differentiated token merging gives 1.07–1.33× speedup with <1% success loss, unlike pruning (FastV −20.3% on π0.5) or uniform merging (ToSA −24.1%).
Evidence: Real π0.5: baseline 55/60 @191 ms vs DepthCache 52/60 @143 ms (1.33×). Pick&Place 20→20, Stack 18→17, Drawer 17→15. Sorting time 28.6→22.1 s (success 15/15→13/15). Perturbation recovery (cube pushed 2–3 cm): 11/15 → 12/15, 17.4→13.7 s.
Ablations: LIBERO π0.5: remove depth partitioning −18.2%, remove progressive merge −16.6% (uniform merge ratio hurts most on Object/Long suites).
Failure/limitations: only up to 1.33×; our 2 s SmolVLA latency would still be >1 s. Critical read: real success actually drops slightly (−3/60), within noise; latency benefit to reactivity shown on 15 trials only.
Conflicts: consistent with other token-pruning papers that uniform pruning destroys spatial detail; supports "near-field workspace matters, background compressible" (cf. foveation/AFP).
Relevance: marginal. We plan a small policy where token compression is unnecessary. Minor point: lower latency → faster perturbation recovery (weak evidence for Q10). Depth used only as a compute prior, not as policy input.
Decision impact:
 - Q10 latency: ~ 1.33× faster VLA inference improves recovery time 21% but not success materially; token tricks don't close a 2 s gap → prefer small model — L.
 - Q04 depth: ~ depth useful as a cheap attention/compute prior (near-field emphasis), not as input — L.
