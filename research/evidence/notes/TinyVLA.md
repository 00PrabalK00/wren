# TinyVLA — TinyVLA: Towards Fast, Data-Efficient Vision-Language-Action Models for Robotic Manipulation (RA-L 2025, arXiv 2409.12514)
Setup: the authors train their own small VLMs (Pythia LLM with the LLaVA pipeline and data): S 422M, B 740M, H 1.3B total. For robot data, the VLM gets LoRA on Q/K/V (~5% of params) and a full-trained DDPM Diffusion Policy head, conditioned on adaptive-pooled VLM features + proprio through a 3-layer MLP. Trainable params: 101M / 138M / 143M. NO robot-data pretraining. Actions are 7-D EEF (xyz, rpy, gripper). Real single-arm Franka: 5 tasks × 100 demos, 2 side ZED cams (no wrist cam), 20 trials per task × 3 checkpoints. Bimanual UR5: 3 tasks, 2 wrist + 1 top RealSense D435i, 10 trials. Sim: Meta-World 50 tasks × 50 demos. Latency measured on an A6000.
Claim: a small VLM + diffusion head, with no robot pretraining, beats OpenVLA at 20× lower latency and generalizes better than DP.
Evidence:
 - Real Franka multi-task avg (PlaceTennis / FlipMug / StackCubes / CloseDrawer / OpenBox):
   - DP (111M, FiLM language): 16.7 / 30 / 3.3 / 73.3 / 53.3, avg 35.3
   - MDT (230M): avg 18.0
   - OpenVLA (7.2B, OXE-pretrained, LoRA): 83.3 / 51.7 / 40 / 85 / 81.7, avg 68.3
   - TinyVLA-S: avg 23.3 (BELOW DP)
   - TinyVLA-B: avg 77.4
   - TinyVLA-H: 90 / 98.3 / 98.3 / 96.7 / 86.7, avg 94.0
 - Bimanual (PlaceBread / StackCubes / PlaceTennisBag): DP 40.3 / 31.3 / 43. OpenVLA 0 / 0 / 0. TinyVLA-H 76.7 / 36.7 / 30. The text says avg 44.5 vs 38.2, but the table gives 47.8 (internal inconsistency).
 - Meta-World avg: TinyVLA-H 31.6 vs DP 10.5.
 - Latency (A6000, per action prediction): OpenVLA-7B 292 ms → OpenVLA-1B backbone 140 ms, TinyVLA-1B 14 ms.
 - Generalization (tiny trial counts, DP / OpenVLA / TinyVLA):
   - camera view ±15/±30°, 16 trials/task: A 0/3/12, B 0/0/6, C 0/1/7
   - background: 0/12, 9/12, 10/12
   - lighting: L1 0/6, 3/6, 4/6; L2 0/6, 1/6, 3/6
   - distractor L1/L2: TinyVLA 3/6 and 2/6 (the paper claims it "manages both" levels)
   - novel object: 1/6, 2/6, 4/6
   - appearance: 0/6, 2/6, 3/6
   - spatial OOD: 0/16, 13/16, 12/16 and 0/10, 4/10, 3/10
Ablations:
 - Head (TinyVLA-H, 5 tasks): MLP 0 on all tasks. ACT head 13.3 / 8.3 / 8.3 / 13.3 / 23.3. Diffusion 90 / 98.3 / 98.3 / 96.7 / 86.7.
 - VLM size failure analysis (6 trials × 4 tasks): the 0.4B model misreads instructions (3 failures). 1.3B and 3B (PaliGemma) reduce positioning and target errors.
Failure/limitations:
 - Generalization tests use 1–2 trials per condition, so they are anecdotal.
 - The DP baseline (multi-task with FiLM language, no wrist cam) is weak: StackCubes 3.3%.
 - An ACT head at 8–23% inside a VLA is implausibly low compared with standalone ACT results, which suggests an untuned integration.
 - The VLM is the authors' own Pythia-based model (not a standard checkpoint).
 - TinyVLA-S (0.4B) loses to DP, so the "small" claim only holds at 1.3B.
 - Only 2 external cams on the Franka.
Conflicts:
 - Head ranking (diffusion >> ACT/MLP) conflicts with VLA-Adapter/OFT (L1 ≥ DiT). Likely cause: TinyVLA pools VLM features into a single vector through an MLP, so a deterministic head sees a weak condition, and a small per-task setting is not what OFT tested.
 - DP's view and lighting fragility agrees with our observed SmolVLA/ACT-style brittleness, and with GreenScreenAug/RoboEngine that pretrained semantics alone do not fix it. The trial counts here are too small to weigh against those.
 - FLOWER calls this "late fusion" and shows late fusion < intermediate fusion.
Relevance: this is 100 demos per task, close to our regime. The robustness hints (camera shift, lighting) favour a pretrained VLM backbone over a from-scratch ResNet DP, but the evidence is thin. Feasibility: 1.3B with LoRA plus 143M trainable is borderline on 8 GB (bf16 weights ~2.6 GB plus activations for 2 images; untested). The 0.4B version that fits easily performed poorly. It uses a DDPM head (slow sampling; the 14 ms number is per action prediction on an A6000).
Decision impact:
 - Q12 model size: weakens very small VLAs (0.4B TinyVLA-S 23.3 < DP 35.3). The benefit appeared at ≥0.74B in THIS family — M (5 tasks × 20 trials × 3 ckpts).
 - Q01 action head: supports a diffusion head over MLP/ACT on pooled VLM features — L/M (baseline integration questionable).
 - Q14 robustness: pretrained-VLM backbone more robust to view (12/16 vs 0/16), lighting, and background than scratch DP — L (1–2 trials per cell).
 - Q03 vision: LoRA-adapted VLM vision > ImageNet-ResNet DP in multi-task language setting — L/M.
