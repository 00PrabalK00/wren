# ACT — Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware (2023, arXiv 2304.13705)
Setup: ALOHA bimanual (2×6DoF+gripper, 14-D), 4 RGB cams 480×640, 50 Hz; 6 real + 2 sim tasks; 50 demos/task (100 for velcro); ~80M params, ResNet18 per cam (ImageNet init, trained end to end), transformer enc/dec, trained from scratch per task, ~5 h on 2080Ti, ~10 ms inference.
Claim: action chunking + CVAE + temporal ensembling lets a from-scratch transformer learn fine bimanual skills from ~50 demos.
Evidence: real success: Slide Ziploc 88%, Slot Battery 96%, Open Cup 84%, Thread Velcro 20%, Prep Tape 64%, Put On Shoe 92%; prior methods (BC-ConvMLP, BeT, RT-1, VINN) ≈0% final on real. Sim transfer cube 90/50 (scripted/human) vs BeT 51/13.
Ablations:
 - Chunk size k (50 Hz, no TE, 4 sim settings): 1% at k=1 → 44% at k=100, slight dip at k=200/400 (near open-loop). Chunking also lifts BC-ConvMLP and VINN → general effect.
 - Temporal ensembling: +3.3% for ACT, +4% BC-ConvMLP, hurts VINN.
 - CVAE vs plain L1 regression of the chunk: scripted data no difference; HUMAN data 35.3% → 2% without CVAE. "CVAE crucial when learning from human data" (multimodal/noisy demos).
 - L1 loss > L2 for precision (stated, no table).
 - Delta joint targets DEGRADED performance vs absolute target joint positions (stated in method, no numbers).
 - Actions = LEADER joint positions (not follower): force implicitly encoded via leader–follower gap through PID.
 - User study: teleop at 5 Hz vs 50 Hz → 62% slower completion; high frequency matters for fine skills.
Failure modes: Thread Velcro drops ~half per stage — low-contrast black tie on black background, small in image → perception-limited, not control-limited. Compounding errors, pauses (non-Markovian) cured by chunking.
Conflicts: (a) delta vs absolute — contradicts ActionSpaceStudy 2026 (delta better). Note ACT's claim is un-quantified and for a PID position-controlled leader/follower rig identical to SO-101; the 2026 study defines delta relative to current state per chunk; need to see its details. (b) Plain L1 chunk regression collapses on human data here, yet OpenVLA-OFT reports L1 regression works — difference: OFT uses a large pretrained VLM backbone + more data; ACT ablation is from-scratch small model on multimodal human sim data (only 2 sim tasks, no real ablation).
Relevance to us: SO-101 is the same leader/follower PID paradigm; 50 demos per task is our regime; our data is human teleop (multimodal) → a plain regression head is RISKY; keep a generative element (CVAE latent or flow). Our recording at 10 Hz is 5× lower than ACT's 50 Hz; the chunking curve is in steps, so k should be expressed in seconds (k=100@50Hz = 2 s).
Decision impact:
 - action_head: plain L1 regression — WEAKENED (human data multimodality) — confidence M (sim-only ablation, 2 tasks).
 - action_space: delta — CONFLICT; absolute leader targets proven on identical hardware paradigm — confidence M.
 - chunking: chunk ≈1–2 s, closed-loop re-query + ensembling — SUPPORTED — H.
 - control_rate: higher rate helps fine skills — SUPPORTED (record at 30 Hz not 10) — M.
