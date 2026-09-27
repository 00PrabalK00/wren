# W4_InContextVLAEndowingVisionLanguageAction — In-Context VLA (VLA-Talker): Endowing VLA Models with Language via In-Context Post-Training and Agentic Tool Use (2026, arXiv 2608.05738)
Setup: OpenVLA-OFT backbone (7B, parallel decoding + chunking), single third-person RGB (no wrist cam). Tools at keyframes (initial, gripper open/close change, periodic): GroundingDINO detector, DepthAnything monocular relative depth, gripper projected via known intrinsics/extrinsics, Qwen2.5-VL-7B fallback. Evidence rendered as diverse paraphrased <spatial> text injected into prompt; loss on action tokens only; then GRPO with sparse success reward. Sim: LIBERO (50 demos/task), RoboCasa-GR1 (24 tasks), SimplerEnv WidowX. Real: 8 tasks on AgiBot humanoid — numbers only in the (truncated) appendix, not available.
Claim: VLAs should consume grounded, tool-derived spatial evidence as context rather than generate CoT; generative CoT hurts low-level control and costs 4.6× latency.
Evidence:
 - LIBERO avg: VLA-Talker 97.4 vs backbone OpenVLA-OFT 90.4. RoboCasa-GR1 avg (24 tasks) 59.5 (best). SimplerEnv avg 72.4 vs Gen-CoT 54.7.
 - Supervision scheme (matched evidence, LIBERO): generate+supervise text 81.5 (4.6× latency, 359 ms vs 78 ms); inject+supervise text 89.7; inject+action-only 97.4 (73 ms).
 - Demo efficiency (LIBERO avg, 5/10/25/50 demos): BC 50.6/63.1/77.4/90.4; Gen-CoT 48.2/59.7/74.3/87.6; VLA-Talker 71.4/84.6/92.8/97.4.
 - Unseen objects / + distractors (held-out split): BC 54.8 / 47.6; Gen-CoT 52.1 / 44.9; VLA-Talker 85.1 / 80.3.
Ablations:
 - Training stages: SFT in-context only 95.6; GRPO without SFT 87.8 (below backbone 90.4, unstable); full 97.4.
 - Keyframe gating (figure): initial-only ~lower; adding gripper-change frames gives most of the gain, then saturates; every-step injection no better.
Failure/limitations: sim-dominant; real results not in extracted text; relies on simulator-known camera extrinsics for gripper projection; huge tool stack (GroundingDINO + DepthAnything + 7B VLM) — heavy for an 8 GB laptop. The "unseen object" gains come from open-vocabulary detection resolving identity, i.e. an object-centric perception front-end.
Conflicts: agrees with other evidence that textual CoT hurts/slows low-level control and that explicit object localization (object-centric cues) improves distractor/novel-object robustness (ControlVLA, GSL). BC baseline at 50 demos = 90.4 on LIBERO; at 5 demos BC 50.6.
Relevance: the transferable idea for SO-101 is cheap: feed the policy explicit object/gripper locations (detector centroid + RealSense depth) as extra conditioning, refreshed at keyframes, rather than asking the network to infer it; skip CoT. Full stack too heavy for our latency budget.
Decision impact:
 - Q14 robustness: explicit detector-based object localization as input → unseen objects 54.8 → 85.1, distractors 47.6 → 80.3 (sim) — confidence L/M (sim only, held-out split details thin).
 - Q08 language: do not generate CoT; paraphrase-diverse conditioning text; generative CoT −16 pts and 4.6× latency — M.
 - Q13 data quantity: explicit spatial evidence gives ~2× data efficiency (25 demos 92.8 > BC 50 demos 90.4) — L.
 - Q10 latency: CoT generation 359 ms vs 73–78 ms injection — M.
