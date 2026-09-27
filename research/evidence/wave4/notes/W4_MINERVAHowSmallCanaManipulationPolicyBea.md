# W4_MINERVAHowSmallCanaManipulationPolicyBea — MINERVA: How Small Can a Manipulation Policy Be and Still Solve LIBERO? (2026, arXiv 2609.03715)
Setup: SIM ONLY (LIBERO 4 suites, 40 tasks pooled, lerobot/libero 1,693 demos ≈42/task; LIBERO-90 extension; LIBERO-Plus robustness audit). Agent-view + wrist cams 256² → 144² → random crop 128² (center crop at eval); from-scratch depthwise-separable CNN + spatial-softmax keypoints, FiLM by 40-way task-ID embedding (no language), 2-step obs history, 8-D proprio; flow-matching DiT head with MLP token mixer (or one-pass L1 regression), chunk H=16; aux progress head (training only); distillation from larger teacher for mid sizes. 0.09M–9.66M params. 90–120k steps, bs 128, AdamW 1e-4, ≈2 h on RTX 5080 laptop/GH200. Eval 2,000 rollouts (50/task), fixed seed; key ablations × 3 training seeds.
Claim: standard LIBERO needs only ~0.5–1M params; only chunk length and vision capacity survive the ±1-pt seed band; flow matching ≈ L1 regression; TE with replan-every-step is the best execution strategy.
Evidence:
 - Table I avg SR: 0.54M 95.05 (L1 head 95.75); 0.99M 96.75; 4.89M 97.15; 9.66M 97.45; π0.5 LeRobot (4.1B, 400 rollouts) 97.50. Collapse: 0.24M 88.6, 0.09M 68.3 (Long suite fails first: 73.0 at 0.24M).
 - Seed band: baseline 1M, 3 seeds: 95.63 ± 1.08 (range 94.60–96.75; Long alone 87.6–92.8).
 - Inference (Table III, per chunk, RTX 5080 laptop GPU / 8 CPU threads): 0.54M flow 8.2 / 8.9 ms; 0.54M L1 2.2 / 5.1 ms; 9.66M 11.1 / 17.8 ms; SmolVLA (450M) 118 ms / 1,010 ms, 0.97 GB; π0.5 196 ms / 12,781 ms, 9.36 GB VRAM.
 - LIBERO-Plus (Table IV; 0.54M / 0.99M / 4.89M): baseline 96.7/96.7/99.2; new objects 69.7/62.1/95.5; sensor noise 68.5/60.0/73.8; robot init 57.1/60.3/63.5; layout 50.0/51.8/58.9; camera 11.5/18.5/34.6; background 9.3/4.7/7.0; LIGHT 1.1/2.2/6.5; avg 46.7/46.0/55.7.
Ablations (1M, 3 seeds unless noted):
 - chunk 16 → 8: −3.16 (goal suite breaks: dithers between modes); 16 → 32: −2.20 (long suite breaks: can't react at subgoal boundaries).
 - vision 0.49M → 0.13M at same total: −1.41 (Long −4.6); single-run dev: moving params from attention head into CNN → Long 80.8 → 91.0. "Shrink the action head, not the eyes."
 - flow matching → L1 regression: +0.34 (within band); regression 3.8× faster on GPU.
 - AdaLN→concat −0.40, →FiLM −0.10, no distillation +0.10, self-attn head +0.05 (all n=1, noise).
 - Obs history 1 → 2 steps at 7M: +6 Goal, +4 Long (single run).
 - Execution (0.54M, 25 eps/task): executing 1–2 actions per replan > 4 > 8 for every method; TE 96.3 > BID 95.0 > plain chunking 94.1 > RTC soft inpainting 91.8.
 - Initial-noise temperature 0.85: +0.2 to +2.25 on sub-1M flow models; nothing at ≥1M.
 - Distillation at 5M: +1.85 (single run).
 - Task-ID permutation: 96.75 → 6.5% (task ID selects memorized task).
Failure/limitations: sim only, single evaluation seed, LIBERO is memorization; photometric robustness ≈0 at all scales (scratch CNN), camera shift 11–35%; authors suggest photometric augmentation as the fix (untested). No real robot.
Conflicts: Flow ≈ L1 contradicts ACT's finding that plain L1 collapses on human data (2% vs 35%) and generative-head advocates; LIBERO demos are human teleop yet L1 matches — suggests at small capacity + chunking + TE, multimodality is manageable; but LIBERO scenes are fixed. TE > RTC here (sync, no latency) while χ0 found chunk-wise smoothing > TE and RTC on a real robot with latency — difference: MINERVA replans every step with ~5 ms latency, so TE has no stale-action problem. History helps (+4–6) contrary to copycat warnings — sim, no proprio noise.
Relevance: HIGH for our compute constraints. A ~1–10M from-scratch CNN policy runs in ms on CPU/8 GB GPU, eliminating our 2 s latency and allowing replan-every-step + TE (which removes chunk-boundary jerks). BUT the LIBERO-Plus audit shows exactly our failure modes (light 1–7%, background 5–9%, camera 12–35%) are catastrophic for a scratch CNN — a small policy must be paired with a pretrained/robust vision encoder and/or heavy photometric + geometric augmentation. Chunk 16 at LIBERO's 20 Hz ≈ 0.8 s.
Decision impact:
 - Q01 action head: L1 regression ≈ flow matching (+0.34, 3 seeds) and 3.8× faster — confidence M (sim, large seeds/rollouts).
 - Q06 chunking: predict ~16 (≈0.8 s), execute 1–2 steps + TE; chunk 8 and 32 both worse — confidence M.
 - Q10 latency: tiny policy enables replan-every-step at 2–9 ms (vs SmolVLA 118 ms GPU/1 s CPU) — confidence H for the latency numbers.
 - Q12 model size: ~1M saturates standard LIBERO; 5M buys robustness (new objects 62→96) — supports small (1–10M) but capacity helps generalization — confidence M.
 - Q03 vision encoder: scratch CNN → near-zero lighting robustness (≤6.5%) and poor camera robustness — weakens scratch encoder for our shift problems — confidence M.
 - Q05 augmentation: random crop alone insufficient for photometric shift — supports adding photometric aug — confidence M.
 - Q07 history: 2-step history +4–6 pts (single run) — confidence L.
 - Q08 language: for a closed task set a task-ID embedding replaces language at no cost — confidence M.
