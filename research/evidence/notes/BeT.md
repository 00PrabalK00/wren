# BeT — Behavior Transformers: Cloning k modes with one stone (2022, arXiv 2206.11251)
Setup: SIM ONLY. Point-mass toys (200 demos), CARLA driving (100 scripted-PID demos + noise, RGB 224x224 via FROZEN ImageNet ResNet-18), multimodal Block-push (XArm, 1,000 scripted demos, state obs), Franka Kitchen (566 HUMAN VR demos, 9-D action, state obs, goal dims zeroed). Single-step actions (no chunking), history context h=2–10. MinGPT trunk, 1e4–1e6 params (Kitchen: 6 layers, 6 heads, width 120; k=64 bins; Block-push k=24; CARLA k=32). RTX 3080; Block-push trains <1 h. Eval: 100 rollouts CARLA, 1,000 Block-push/Kitchen.
Claim: k-means action binning (categorical head) + per-bin continuous residual offset on a transformer captures multimodal behaviour that MSE-BC averages away.
Evidence (Table 1, same data per env):
 - CARLA success: RBC(MLP+MSE) 0.98, 1-NN 0.99, LWR 1.0, VAE 0, NormFlow 0.03, IBC 0.25, BeT 0.98 (easy env: regression is fine when only success is counted).
 - Block-push (Reach1/Reach2/Push1/Push2): RBC 0.67/0/0/0; IBC 0.98/0.04/0.01/0; LWR 0.50/0.06/0/0; BeT 1/0.99/0.96/0.71.
 - Kitchen, human data (≥1/2/3/4 tasks): RBC 0/0/0/0; 1-NN .90/.72/.44/.17; LWR 1/.83/.52/.21; VAE 1/0/0/0; IBC .99/.87/.61/.24; BeT .99/.93/.71/.44.
 - Mode coverage (Table 2): CARLA left/right RBC 0/0.98 (collapses to one mode), BeT 0.34/0.64 (demos 0.5/0.5); Kitchen task-sequence entropy RBC 0, IBC 2.41, BeT 2.47, demos 2.96.
 - Latency: BeT 2.8 ms/action vs IBC 52 ms vs MLP 0.5 ms (Kitchen); training BeT <1 h vs IBC ~14 h (Block-push).
Ablations (Table 3, performance relative to full BeT, CARLA/Block-push/Kitchen):
 - no offsets (bin centre only) → 0.94/0.95/0.78 (largest loss in highest-dim action space; discretization alone loses fidelity).
 - no binning (k=1 ⇒ regression-like) → 0.94/0.25/0.68.
 - no history → 0.65/0.95/0.88.
 - MLP trunk 0.90/0/0.05; Temporal conv 0.72/0.01/0.26; LSTM 0.03/0.03/0.04.
 - GPT-MDN (Gaussian mixture head) → 0.30/0.83/0.86; uniform quantization → 0.90/0.96/0.90.
 - k sweep: figure only, qualitative: trade-off; k=1 clearly worse.
Failure/limitations: authors: shares BC OOD failure; primary Block-push failure = not noticing block not fully in target; IBC overfits (needs early stopping). Critical read: entirely simulation, state-based except CARLA; no action chunking; large datasets (566–1000 demos) — far from 50–100; baselines (RBC MLP) are not action-chunked transformers; "no binning" ablation mixes regression + transformer so it is the cleanest regression-vs-multimodal comparison here; k-means on single-step actions will not scale to chunks (VQ-BeT addresses that).
Conflicts: agrees with ACT (L1 w/o CVAE collapses on human data) and Diffusion Policy (MSE/LSTM-GMM weaker on multimodal data). Much of the Kitchen gap is MLP-vs-transformer as well as head (MLP trunk → 0.05). Diffusion Policy later reports BeT beaten by DP on real tasks and that BeT struggles with action chunks — BeT's advantage is mode coverage at low latency, not precision.
Relevance: Pumpkin→tray pick-place from ONE start pose has mild multimodality (approach path, grasp point, human hesitations) — nothing like Block-push's 4 combinatorial modes; so BeT's big wins are on a regime we are not in. But the latency numbers (ms-scale) and the 1e6-param models show a discrete/categorical head is cheap on an 8 GB laptop. The GPT-MDN (GMM head) result (0.30 on CARLA) is evidence against a simple GMM head.
Decision impact:
 - Q01 action head: plain MSE regression — WEAKENED on multimodal/human data (Kitchen RBC 0 vs BeT .99; mode collapse) — confidence M (sim, MLP baseline confounds trunk).
 - Q01 action head: GMM/MDN head — WEAKENED (GPT-MDN 0.30/0.83/0.86 relative) — confidence L/M.
 - Q01 action head: discrete bins + continuous offset — SUPPORTED over pure discretization (no-offset 0.78 in 9-D) — confidence M.
 - Q07 history: short history helps (no-history 0.65 CARLA) — confidence L/M (sim, no chunking; ACT/DP find less need).
 - Q10 latency: categorical head is single-pass, 2.8 ms vs IBC 52 ms — confidence M.
