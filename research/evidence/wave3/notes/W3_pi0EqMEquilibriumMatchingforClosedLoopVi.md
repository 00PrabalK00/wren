# W3_pi0EqMEquilibriumMatchingforClosedLoopVi — π0-EqM: Equilibrium Matching for Closed-Loop Vision-Language-Action Control (2026, arXiv 2605.23128)
Setup: Sim only. π0 VLA with its flow-matching action expert replaced by a time-free Equilibrium Matching decoder (Nesterov solver, residual-based adaptive stopping, half-chunk warm start from previous prediction). RoboTwin 2.0, 19 tasks, 500 demos/task (100 clean + 400 domain-randomized); LIBERO 4 suites. Matched 300 solver steps(!) per decode; receding horizon executing only the first action. Trials per task not stated.
Claim: a time-free EqM action decoder beats π0's flow matching under matched compute and makes inference depth a controllable policy variable.
Evidence: RoboTwin avg 40.4 → 50.2 (12 tasks up, 5 down, 2 tied; e.g. pick dual bottles 26→66, place cans plasticbox 32→65, put bottles dustbin 42→72; place dual shoes 54→45, stack bowls three 68→60). LIBERO avg 94.15 → 94.35 (LIBERO-10 85.2→87.0; Goal 95.8→94.8).
Ablations: threshold scans on 2 tasks: best residual threshold is task dependent (place dual shoes peaks at τ≈1.0; click bell best at strictest τ) — "stationarity–executability gap": lowest residual ≠ best execution (figure only). Authors state they did NOT isolate EqM objective vs stopping rule vs warm start.
Failure/limitations: sim-only, VLA-scale (π0 ~3B), 300 iterations per decode is far heavier than π0's 10 flow steps — latency not reported; no real robot; gains on LIBERO are within noise.
Conflicts: none direct; relates to RTC/warm-start ideas (reuse previous chunk to initialize next decode) which are motivated by chunk-boundary continuity.
Relevance: Low. Not usable on an 8 GB laptop at our latency targets. The only transferable idea: warm-starting the next chunk's generative decode from the previous chunk's remaining half (improves temporal coherence), which is also available in flow-matching via RTC-style inpainting.
Decision impact:
 - Q01 action head: EqM > flow matching on RoboTwin (40.4→50.2, sim, VLA-scale, 300 steps) — L
 - Q10 latency/smoothness: warm-start from previous chunk as coherence mechanism; not isolated — L
