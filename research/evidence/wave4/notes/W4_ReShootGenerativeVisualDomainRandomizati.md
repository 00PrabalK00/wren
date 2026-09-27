# W4_ReShootGenerativeVisualDomainRandomizati — ReShoot: Generative Visual Domain Randomization of Recorded Robot Demonstrations for Visuomotor Policy Learning (2026, arXiv id not in text)
Setup: VLM (qwen) captions scene and edits one attribute (object color 37%, material 28%, background 23%, shape/robot/added object rare); Wan2.2-T2V-A14B + ControlNet on HED edge maps re-renders BOTH third-person and wrist videos; FlashVSR super-res; actions/proprio copied verbatim; training batches 50/50 recorded/re-rendered. Policy: OpenVLA-OFT (7B, full FT, its own image aug). Sim: LIBERO 1,693 recorded + 1,000 re-rendered eps; LIBERO-Plus sample 2,395 eps (McNemar tests). Real: Robot A AgileX PiPER (overhead + wrist cam), 43 demos red cube → +43 blue re-renders, 20–21 trials; Robot B FAIRINO FR5 (third-person + wrist), 4 tasks, 100 demos all black objects → +700 recolored, 10 trials/task.
Claim: re-rendering recorded demos with a structure-conditioned video model gives domain-randomization-like robustness without new data collection and without hurting in-distribution success.
Evidence:
 - LIBERO (Rec / Mix / Gen-only): 96.9 / 96.5 / 77.0.
 - LIBERO-Plus: Rec 82.3 → Mix 85.5 (+3.2, p<0.001); Gen-only 64.3. By dimension (Mix−Rec): camera viewpoint +22.5 (n=102), sensor noise +12.1, background texture +7.1, layout +0.7, robot init 0.0, LIGHTING −2.2 (n=400), language −11.1.
 - Real A: red cube (in-dist) 14/20 Rec vs 10/20 +ReShoot (p=0.34, not significant but a drop); blue cube w/ red distractor 0/21 → 9/21 (p=0.004).
 - Real B: black objects 21/40 vs 23/40; novel colors 0/40 → 19/40 (p<0.001).
Ablations:
 - Gen-only vs Mix: re-rendered alone loses 18–20 pts (needs recorded anchor half).
 - Edge-map correlation recorded vs re-rendered 0.80 (third-person) / 0.70 (wrist); pixel difference 81 / 47 on 0–255.
 - NO comparison vs simple color jitter / random-conv augmentation (authors argue it is a narrower regime) — key missing baseline.
Failure/limitations: contours drift (edge conditioning only); instruction rewrite can mismatch video; lighting edits don't change rendered illumination. Critical read: in-distribution real drop 70→50% on Robot A; 10–21 trials; color-shift test is exactly the attribute edited; a hue-jitter baseline might recover much of the color gain cheaply; 14B video model generation is far beyond 8 GB (offline cloud).
Conflicts: agrees with every paper that a single appearance change (color) zeroes a narrowly trained policy (0/40, 0/21) — even a 7B pretrained VLA. Lighting robustness NOT improved by generative edits — lighting must come from real lighting variation or photometric aug. Camera-view gain +22.5 echoes that appearance randomization regularizes toward structure (cf. InfiNoVA, CLASS).
Relevance: our "different-looking pumpkin" failure is exactly this color/appearance shift: expect ~0% without appearance diversity. Cheapest path for us: (1) collect with 2–3 different pumpkins/colors, (2) strong hue/color jitter + background randomization, (3) generative re-render only if budget permits (needs large GPU offline). Lighting needs separate handling.
Decision impact:
 - Q05 augmentation: supports generative re-rendering of both views for appearance shift (0→43–48% on novel colors real) — M; weak for lighting (−2.2) — M.
 - Q14 robustness: single object-color change → 0% for recorded-only OpenVLA-OFT on 2 robots — H (consistent across platforms).
 - Q13 data diversity: appearance diversity matters more than count; re-rendered-only data insufficient (Gen 77 vs Rec 96.9) — M.
 - Q12 model size: 7B VLA pretraining does not confer color invariance — M.
