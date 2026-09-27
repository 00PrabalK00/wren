# W3_SoftVTBenchADeformationAwareVisuoTactile — SoftVTBench: A Deformation-Aware Visuo-Tactile Dataset and Benchmark for Deformable-Object Manipulation (2026, arXiv id not in text)
Setup: simulated (FEM) visuo-tactile benchmark, 4 suites x 10 tasks x 1,000 demos at 20 Hz; policies Diffusion Policy, pi0.5, FastWAM with vision-only vs visuo-tactile input; OOD = 9 held-out conditions (illumination, object mass, Young's modulus).
Low relevance: tactile/deformable sim benchmark; no tactile sensor on SO-101. Only tangential datapoints: pooled OOD (illumination+physics) TSR drops for vision-only DP 8.2/4.6 pts, pi0.5 5.8/1.6, FastWAM 7.6/9.2 (Object-Soft/Spatial-Soft); figure-only note that DP "degrades strongly at the illumination extremes" on Object-Soft; success-only metrics hide 0.7-24% of successes that over-compress objects (relevant only if our pumpkin were soft).
Decision impact:
 - Q14 robustness: illumination extremes degrade vision-only Diffusion Policy strongly (figure only) — L
