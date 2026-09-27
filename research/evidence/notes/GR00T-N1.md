# GR00T-N1 — GR00T N1: An Open Foundation Model for Generalist Humanoid Robots (2025, arXiv 2503.14734)
Setup: 2.2B total, of which the VLM is 1.34B: Eagle-2 = SmolLM2 LLM + SigLIP-2, 224² images, pixel-shuffle → 64 tokens per frame. Features come from the MIDDLE (12th) LLM layer, not the last. The action module ("System 1") is a DiT with AdaLN timestep conditioning. It alternates self-attention (over state + noised action tokens) with cross-attention to the VLM tokens (Flamingo/VIMA style). Embodiment-specific MLP state/action encoders and an action decoder. The action encoder MLP takes the timestep + noised action.
Flow matching: π0 Beta τ-schedule, chunk H=16, K=4 Euler steps ("work well across all embodiments"). Latency is 63.9 ms per 16-action chunk on an L40 in bf16.
Training: the LLM/text part is FROZEN in both pre- and post-training; the vision encoder and DiT are unfrozen. Pretraining: batch 16,384, 200k steps, LR 1e-4 cosine, weight decay 1e-5, ~50k H100-h. Data "pyramid":
 - GR-1 teleop (20 Hz) + OXE + AgiBot-Alpha (140k traj)
 - 780k DexMimicGen sim trajectories (≈6,500 h, generated in 11 h)
 - 827 h of video-model "neural trajectories" generated from 88 h of real data (~105k L40-h)
 - human egocentric video (Ego4D, EPIC etc.)
 Action-less video gets VQ-VAE latent-action (LAPA) labels or IDM pseudo-labels, treated as separate embodiments.
Post-training: batch 128 or 1024, 20k–60k steps. On a single A6000, tuning the adapters + DiT fits batch 200. Also tuning the vision encoder fits batch 16.
Benchmarks:
 - Sim: RoboCasa (24 tasks, Franka, 3 cams incl. wrist, relative EE actions); DexMG (9 bimanual tasks); GR-1 tabletop (24 tasks, 1 egocentric cam, joint-position actions). 30/100/300 demos per task, 100 trials, max over the last 5 checkpoints.
 - Real: GR-1 humanoid, 13 tasks across 4 categories, 15 min – 3 h of teleop per task, "10%" subsample vs full. 10 trials per task (machinery: 5), partial credit.
Claim: a VLM (frozen LLM) + cross-attention flow DiT, pretrained on real + sim + neural + human-video data, post-trains data-efficiently and beats from-scratch DP/BC-Transformer.
Evidence:
 - Sim @100 demos/task (Table 2), BC-Transformer / DP / GR00T:
   - RoboCasa 26.3 / 25.6 / 32.1
   - DexMG 53.9 / 56.1 / 66.5
   - GR-1 16.1 / 32.7 / 50.0
   - Avg 26.4 / 33.4 / 45.0
 - Sim data scaling (Table 4 averages), DP vs GR00T at 30 / 100 / 300 demos:
   - RoboCasa: DP 14.7(?) / 25.6 / 43.2 vs GR00T 17.4 / 32.1 / 49.6. The DP-30 value is split in the extraction; 14.7 is the orphan number.
   - DexMG: DP 23.7 / 46.9 / 68.4 vs GR00T 29.6 / 58.5 / 74.2. Table 2 lists DP DexMG@100 as 56.1, so the two tables are inconsistent.
   - GR-1: DP 21.3 / 32.7 / 40.4 vs GR00T 43.2 / 50.0 / 49.3. GR00T saturates from 100 to 300.
 - Real (Table 3/5), DP-10% / DP-full / GR00T-10% / GR00T-full:
   - Pick-place 3.0 / 36.0 / 35.0 / 82.0
   - Articulated 14.3 / 38.6 / 62.0 / 70.9
   - Industrial 6.7 / 61.0 / 31.0 / 70.0
   - Coordination 27.5 / 62.5 / 50.0 / 82.5
   - Avg 10.2 / 46.4 / 42.6 / 76.8
   - GR00T with 10% data is only 3.8 pts below DP with full data.
 - Seen vs unseen objects (pick-place), DP-10% / DP-full / GR00T-10% / GR00T-full: seen 2.0 / 42.0 / 36.0 / 92.0; unseen 4.0 / 30.0 / 34.0 / 72.0. Even the pretrained full-data model loses 20 pts on novel objects.
 - Pretrained zero-shot: bimanual handover 76.6% (11.5/15) and novel object to unseen container 73.3% (11/15).
Ablations:
 - Neural-trajectory co-training (1:1 ratio with real): RoboCasa +4.2 / +8.8 / +6.8 at 30/100/300 demos; real +5.8 avg over 8 tasks (10% data, 100 neural traj per task, IDM labels). LAPA ≥ IDM at 30 demos; IDM pulls ahead at 100–300.
 - Middle-layer (12th) vs final-layer LLM features: "faster inference and higher success". No numbers.
 - K=4 denoising steps chosen empirically. No sweep reported.
Failure/limitations: authors cite short-horizon tabletop only, synthetic data physics/diversity limits, and the need for a stronger VLM. Critical read:
 - The real benchmark is on the SAME GR-1 embodiment that dominates pretraining, so the "data efficiency" is partly in-embodiment pretraining.
 - The DP baseline was trained from scratch with no pretrained vision encoder mentioned. DP-10% "immobile during the initial frames" suggests a weak baseline setup (idle-frame issue).
 - 10 trials/task with partial credit.
 - The "10%" regime is not given in demo counts.
 - Post-training on right-hand-only data erased the pretrained handover skill: catastrophic narrowing.
Conflicts:
 - Freezing the LLM works here (unlike KnowledgeInsulation's 0% for a fully frozen backbone) because the vision encoder is fine-tuned and features come from a middle layer. This is consistent with SmolVLA (keeps the first 16 layers) and VLA-Adapter (mid/all-layer features beat last-layer).
 - The short chunk (16) and only 4 flow steps contrast with π0 (50 / 10), and both work. This suggests the step count can be low for smooth teleop data.
 - The DP-vs-pretrained-VLA gap at low data agrees with π0 (pretraining helps most at small data). It disagrees with SO101-Benchmark, where ACT ≈ SmolVLA, likely because GR00T's pretraining includes the same embodiment.
Relevance:
 - GR00T's action module is the closest published template for our small policy: frozen or lightly-tuned perception tokens → small DiT with alternating self-attention (state + action tokens) and cross-attention (vision tokens), H=16, K=4 Euler steps, AdaLN τ.
 - That DiT is itself small relative to the VLM, so a 10–50M version is natural.
 - Practical 8 GB notes: tuning the vision encoder cuts max batch from 200 to 16 on a 48 GB A6000. On 8 GB we must freeze most of the encoder, use a small encoder, or use gradient accumulation / LoRA.
 - 64 tokens per 224² frame via pixel shuffle is a good token budget.
 - The novel-object drop (92 → 72) warns that object-appearance shift (our different pumpkin) remains the hard case even with big pretraining.
Decision impact:
 - Q01 action head: supports a flow-matching DiT with cross-attention to vision tokens + self-attention over [state, action] tokens and AdaLN τ. Beats DP from scratch by +11.6 avg sim @100 demos and +30.4 real full-data — M (confounded by pretraining).
 - Q06 chunking: H=16 with K=4 steps works across embodiments at 20 Hz (~0.8 s chunks) — L/M (not ablated).
 - Q10 latency: 63.9 ms per chunk for 2.2B on an L40 with K=4. Fewer flow steps is a valid latency lever — M.
 - Q03 vision: supports a frozen language part + FINE-TUNED vision encoder + middle-layer features (claimed better and faster) — L/M (no numbers).
 - Q12 model size: ~1–2B pretrained beats small from-scratch DP/BC-T by a big margin at 30–100 demos. GR-1 plateaus 50.0 → 49.3 at 100 → 300 demos — M.
 - Q13 data: 10% data + pretraining ≈ full data from scratch (42.6 vs 46.4). Synthetic neural trajectories add +4–9 pts sim and +5.8 real — M.
 - Q14 robustness: unseen objects −20 pts (92 → 72) even for the full-data pretrained model — M.
 - Q05 augmentation: generative video "neural trajectories" as data augmentation give +5.8 real at low data but cost ~105k L40-h at scale — L for us (compute).
