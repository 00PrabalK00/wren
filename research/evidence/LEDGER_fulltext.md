# Evidence ledger — one line per (paper, decision). Direction: + supports / - against / ~ conditional
ACT | action_head | plain L1 chunk regression collapses on human demos (35.3%→2%, sim) | - regression, + generative/latent | M
ACT | action_space | delta joint targets degraded vs absolute leader targets (no numbers) | - delta | M
ACT | chunking | k=1→1%, k=100 (2 s @50Hz)→44%; TE +3.3% | + chunk ~1-2 s + TE | H
ACT | control_rate | 5 Hz vs 50 Hz teleop: 62% slower | + higher rate | M
DiffusionPolicy | vision | frozen pretrained 0.40-0.70 vs finetuned 0.92-0.98 vs scratch R18 0.94 | - frozen, + finetune low LR | H(in-dist)
DiffusionPolicy | action_space | position (absolute) > velocity for DP | - delta/velocity | M/H
DiffusionPolicy | action_head | diffusion beats GMM/IBC/BET, +46.9% | + generative | H
DiffusionPolicy | chunking | execute 8 of 16 @10Hz optimal; latency tolerant ≤4 steps | + | H
BAKU | model_size | 4-31M equal; 114M severely worse on LIBERO-90 (50 demos/task) | - large from-scratch, + ~10-30M | M/H
BAKU | action_head | sim: MLP>=multimodal; real: VQ-BeT 91% vs MLP 86% | ~ multimodal for real human data | M
BAKU | history | no gain over current obs; last-step-loss history hurts | - history | M
BAKU | language | FiLM vision >= unconditioned | + FiLM | M
BAKU | chunking | LIBERO -14% without | + | H
OFT | action_head | L1≈diffusion only with 7B VLM on filtered LIBERO; authors credit capacity | ~ L1 only with big pretrained backbone | M/H
OFT | language | no FiLM → language following at chance (33%) with wrist cams | + FiLM essential | H
OFT | action_space | absolute joint targets on ALOHA (leader/follower) succeed | + absolute | M
OFT | from_scratch | DP from scratch ≥ RDT-1B on folding/scooping with 20-45 demos | + small from scratch viable | M
DP3 | 3d_input | real 40 demos: DP3 85±11 vs image DP 35±25 vs depth-image DP 20±12 | + point cloud | M/H
DP3 | robustness | color-free input generalizes to new colors (1 trial/cond, anecdotal) | + color-free geometry | L/M
DP3 | encoder_size | tiny MLP point encoder > PointNeXt/PointTransformer | + small encoder | M
iDP3 | 3d_input | OOD (new obj/view/scene): image DP(finetuned R3M+jitter) 0-3/10 vs iDP3 9/10 | + 3D for OOD | M/H
iDP3 | vision | in-dist: finetuned R3M image DP ≥ iDP3; frozen R3M worse | + finetune, - frozen | M
iDP3 | augmentation | color jitter did not rescue image policy in new scene | - aug alone | M
iDP3 | 3d_setup | camera-frame clouds, no calibration; 4096 pts; conv pyramid encoder | + | M
RTC | execution | TE fails (invalid averages; protective stops at +100ms); RTC robust to +200ms | + inpainting async, - blending/TE | H
RTC | action_head | RTC requires flow/diffusion head | + flow | H
RTC | chunking | shorter execution horizon better when continuity handled | + frequent re-query | M/H
Legato | execution | training-time continuation ~10% smoother/faster than RTC; stops mode switching | + flow + Legato | M
ActionSpaceStudy | action_space | chunk-wise delta > step-wise (~10%); chunk-wise delta ≥ absolute (sometimes marginal); joint > task in fixed embodiment | + chunk-wise delta joint | M/H
ActionSpaceStudy | chunking | absolute likes long exec horizon; delta shorter | ~ | M
RESOLVED | action_space | ACT/DP negative results were vs step-wise delta/velocity; not in conflict with chunk-wise delta | | 
SPA | vision | frozen, 268 tasks: SPA > MAE > ... ; DINOv2 < MoCoV3/MAE; CLIP-style poor | - DINOv2/SigLIP as frozen, + SPA/MAE init | M
GreenScreenAug | augmentation | novel scenes: +65% vs none, +29% vs CV aug, +21% vs generative (ACT, 50 demos, 8.2k evals) | + green screen random textures | H
GreenScreenAug | augmentation | texture entropy matters (48→87%) | + high-entropy textures | M
RoboEngine | augmentation | 6 new scenes: +210% vs no gen-aug (colorjitter already on); textures/ImageNet bg strong & fast | + bg replacement | M/H
SO101-Benchmark | evaluation | ACT 33.75 ≈ SmolVLA 32.5 < Wall-X 51 < π0.5 56; execution failures dominate; recovery ACT 6.5%, SmolVLA 3.2% | + recovery demos, + grasp robustness | M
CopycatAgents | Q07 history | BC-OH (H=2) lower held-out loss than H=1 but copies prev action; TCA+IB: Walker2d 592→1296, Hopper 293→1086 (MuJoCo, state-based) | + current obs only / no past-action input; + IB if history used | M
CopycatAgents | Q07 history | RNN history worse than frame stacking (Ant −311 vs 1750); dropout-on-history poor | - RNN / dropout fixes | L
CopycatAgents | eval/checkpoint | test loss BC-OH < BC-SO and Ours > BC-OH, yet reward ordering opposite in several envs | - val loss as selection criterion | M
BeT | Q01 action_head | Kitchen (566 human demos) ≥2 tasks: MLP-MSE 0 vs BeT .93; CARLA MSE collapses to 1 mode (0/0.98 L/R) | - MSE regression on multimodal data | M
BeT | Q01 action_head | GPT-MDN (GMM head) rel. perf 0.30/0.83/0.86; no-offset 0.78 in 9-D Kitchen | - GMM head, - pure discretization, + bin+offset | L/M
BeT | Q07 history | no-history rel. 0.65 CARLA / 0.95 / 0.88 | + short history (sim, no chunking) | L/M
BeT | Q10 latency | 2.8 ms/action BeT vs 52 ms IBC vs 0.5 ms MLP | + single-pass heads | M
robomimic | Q07 history | BC-RNN vs BC (image, no chunking): Square PH 82.0 vs 62.0, Tool Hang PH 67.3 vs 20.0, Transport MH 42.0 vs 18.7; seq len 10≈30≈50 | + temporal context when NOT chunking; ~ when chunking | M
robomimic | Q13 data | MH 300 demos < PH 200 demos; adding 100 worse demos hurts BC (Square 58.7→46.7); Lift/Can 75–100% with 20% data | + quality over quantity | M/H
robomimic | Q05 augmentation | real Can: 73.3% with pixel-shift vs 26.7% without; sim −35–47% rel | + random shift/crop | H
robomimic | Q11 cameras | real Can: 73.3% with wrist vs 43.3% without; sim Transport −43% rel | + wrist cam | H
robomimic | Q01 action head | no-GMM (deterministic) −58% rel on MH Transport low-dim; smaller gap for BC-RNN | + multimodal head for multi-operator data | M
robomimic | eval/checkpoint | lowest-val-loss or last checkpoint 10–100% rel worse than best checkpoint | - val loss for checkpoint selection | H
robomimic | Q03 vision | shallow conv vs ResNet-18: −25–62% rel; LR 1e-3 vs 1e-4: −35–63% (image) | + ResNet-18-class encoder, low LR | M
robomimic | proprio/obs space | +EEF vel or +joint pos/vel: −49–88% rel (low-dim), −2–29% (image) | - extra proprio features | M
VQ-BeT | Q01 action_head | real Stretch single-phase VQ-BeT 47/50 ≈ DP-T 45/50 >> MLP-BC 29/50; two-phase 19/30 vs 11/30 vs 7/30 | + VQ tokens / generative, - MLP regression | L/M
VQ-BeT | Q06 chunking | receding-horizon open-loop "fails completely" on low-cost robot (OOD within 3 steps); chunking hurt VQ-BeT | - long open-loop chunks on cheap arms | M
VQ-BeT | Q10 latency | single pass 18 ms vs DP-T 573 ms GPU closed-loop (15 vs 100 ms sim @10 DDIM steps) | + single-pass head | M/H
WhatMattersLanguageIL | Q08 language | frozen MiniLM-L3 SBERT 2.64 avg len > Distilroberta-SBERT 2.50 > CLIP 2.42 > MPNet-SBERT 2.24 > BERT 2.03 > MPNet 1.92 (CALVIN D) | + small sentence-embedding encoder | M
WhatMattersLanguageIL | Q08 language | CLIP-style contrastive video-language loss 2.64 vs none 2.29 vs regression 2.45 | + contrastive alignment aux loss | L/M
WhatMattersLanguageIL | Q05 augmentation | no random shift: avg len 2.64→1.99, 5-chain 28.3→15.4% | + random shift | M/H
WhatMattersLanguageIL | Q02 action space | MCIL absolute 0.41 vs delta 1.82 avg len | + delta/relative actions | M
WhatMattersLanguageIL | proprio | adding proprio 2.64→2.20 (causal confusion with initial pose) | - proprio when it can cue task | M
WhatMattersLanguageIL | Q14 generalization | unseen env zero-shot avg len 0.67 vs 3.06 in-distribution | - expecting scene transfer | M
ImplicitBC | Q01 action_head | real xArm (95-502 human demos, 60 trials): EBM 85/88/83/48% vs MSE 35/55/7/20%; 1mm insertion 83 vs 7 | - single-step MSE regression | M/H
ImplicitBC | Q01 action_head | DFO inference fails beyond ~5-D actions; Langevin needs grad penalty; others (BeT, DP) find IBC unstable | - EBM head for 6-DoF chunks | M
ImplicitBC | Q01 action_head | sim pixels pushing: MDN 10% vs MSE 87% vs EBM 100% | - GMM/MDN head | L/M
ImplicitBC | Q10 latency | EBM 7.2 ms vs MSE 3.5 ms (2-D action, 2080Ti) | ~ | L
RT-1 | Q08 language | USE embedding → identity-init FiLM in ImageNet EfficientNet; RT-1 97/76 seen/unseen vs Gato late-fusion 65/52 (same data) | + frozen sentence enc + zero-init FiLM early fusion | M
RT-1 | Q07 history | w/o 6-frame history: seen 97→82, unseen 76→62, distractors 83→50 (single-step, 3 Hz, 130k demos) | + history only for non-chunked/big-data; ~ for us | M
RT-1 | Q01 action head | Gaussian continuous vs 256-bin discrete: seen 97→68, unseen 76→43 | + multimodal/discrete head | M/H
RT-1 | Q03 vision | no ImageNet pretraining: unseen 76→43, backgrounds 59→41 | + pretrained encoder | M/H
RT-1 | Q13 data | 75% tasks@97% data ≈ 51% data; ≤50 ep/task: unseen 14%, backgrounds 41 | + diversity > quantity | M/H
RT-1 | Q10 latency | TokenLearner 2.4× speed-up, token caching 1.7×; AR actions 36 vs 15 ms no gain | + token reduction, - AR action decoding | M
RT-1 | eval/checkpoint | real-to-sim (RetinaGAN) success ordering directionally matches real; used for checkpoint selection | ~ proxy eval needed, not loss | L
ConsistencyPolicy | Q01 action_head | real Franka 180 demos: CP-1 0.8/0.7/0.4 vs DDIM-15 0.8/0.6/0.5 (10-20 trials); sim ToolHang CP-3 .77 vs DDPM .79 | + few-step generative head | M
ConsistencyPolicy | Q10 latency | laptop 3070Ti 8GB: CP 21 ms (enc 6 + net 13.5) vs DDIM-15 192 ms vs DDPM-100 ~1.5 s | + 1-3 step head on 8GB laptop | H
ConsistencyPolicy | Q10 steps_vs_quality | DDIM-15 ToolHang .14 vs DDPM-100 .79 vs CP-3 .77; low-var init +.04 | - naive step reduction on precise tasks | M
ConsistencyPolicy | Q01 action_head | CP/EDM lose multimodality (Push-T one side); CT w/o teacher Square .55 vs .92 | - distillation complexity; ~ multimodality | L/M
FlowPolicy | Q01 action_head | 37 sim tasks, 10 scripted demos: 1-step consistency-FM 70.0 vs DP3 10-step 68.7 vs SimpleDP3 67.4 | + 1-step flow (no distillation) | L/M
FlowPolicy | Q10 latency | 19.9 ms vs DP3 145.7 ms vs SimpleDP3 63.0 ms (2080Ti) | + 1-step head | M
FlowPolicy | Q04 3d_input | 2D DP 35.2 / CP 50.1 vs 3D DP3 68.7 / FlowPolicy 70.0 (sim, 10 demos) | + point cloud (sim) | L/M
MDT | Q09 aux objectives | masked future-frame reconstruction (v=3, mask .75): MT-ACT 2.80→4.03, MDT 3.34→4.41 CALVIN ABCD; LIBERO avg 68.5→70.0 (MGF), 74.3 (MGF+CLA) | + train-only masked foresight loss | M
MDT | Q09 aux objectives | full reconstruction (mask 1.0) 63.7 vs 67.5 LIBERO-Spatial; v=9 worse than v=3 | - full-frame / long-horizon pixel prediction | L/M
MDT | Q09 aux objectives | LIBERO-Long 5 demos ≈0.14→0.18 (aux, scratch), ≈0.29 with action-free pretraining; 20 demos ≈0.52→0.53 (figure) | ~ aux gain small at ≤20 demos from scratch | L/M
MDT | Q08 language | frozen CLIP text token + CLA: LIBERO (2% labels) avg 68.5→73.1 | + frozen text token; + contrastive alignment for sparse labels | M
MDT | Q07 history | no history, chunk 10: SOTA CALVIN 4.52 | + current obs only | M
MDT | eval/checkpoint | MT-ACT kept improving after val loss rose → authors used last epoch | - val loss for ACT-style ckpt selection | L
StreamingFlowPolicy | Q01 action_head | same velocity field trained w/o noise (regression) vs flow-matching: Can 12.4 vs 95.6, Push-T 72.1 vs 91.7 | - regression, + flow matching | M
StreamingFlowPolicy | Q01 action_head | SFP ≈ DP-100: Square 78.0 vs 77.2, Can 98.4 vs 94.0, Push-T img 83.9 vs 87.0; stabilization k=0 → Square 53.2 | + flow w/ stabilizing target | M
StreamingFlowPolicy | Q10 latency | per-action 3.5-8.8 ms vs DP-100 40-127 ms, DDIM-10 4.4-10.4 ms; chunk starts at last action (no boundary jump), smoother real motion (video only) | + streaming/continuity-aware flow | M
StreamingFlowPolicy | Q06 chunking | exec chunk peak 8 (3/4 envs) or 6 of Tpred 16 | + exec ~half of predicted | M
FLARE | Q09 aux objectives | future-latent cosine alignment (t+16, λ=.2): RoboCasa 61.9→70.1, GR1 44.0→55.0; generic frozen SigLIP2 target 43.9→50.9; frozen target (no EMA) still > baseline | + latent future-embedding aux loss | M
FLARE | Q09 aux objectives | UWM (joint future VAE-latent + action diffusion, 5× steps) 60.8/29.5 vs FLARE 70.1/55.0 | - pixel/latent video co-generation | M
FLARE | Q09 aux objectives | post-training 100 traj/task: +10 pts RoboCasa; real GR-1 +14 pts avg (figure/text) | + at ~100 demos/task (w/ pretrained encoder) | L/M
FLARE | Q13 data | novel objects: 10 demos 42.5 → 80.0 with 150 human ego videos/object (alignment loss only on videos) | + action-free video co-training | L/M
R3M | Q03 vision | frozen RN50, in-dist only: sim ~62% (+>10 pts vs CLIP/MoCo, +>20 vs scratch); real 20 demos 56% vs CLIP 24% | ~ R3M (in-dist only), + pretrained>scratch | M
R3M | Q14 robustness | no OOD test at all; views trained separately | ~ (no evidence) | L
VC-1 | Q03 vision | E2E fine-tune ViT-L on few-shot IL collapses: MW 88.8→22.7, Adroit 59.3→15.9, DMC 66.9→6.7 | - fine-tuning LARGE encoder on small data | H
VC-1 | Q03 vision | real Franka: frozen 70% vs E2E (enc LR 1e-5) 67.5% vs MAE-adapt-on-demo-frames 85% | + in-domain MAE adaptation, ~ low-LR fine-tune | M
VC-1 | Q03 vision | frozen VC-1 < frozen R3M on Adroit/MW/DMC (59/89/67 vs 73/96/81); no universal PVR | - VC-1 as pick | M
VC-1 | Q13 data | pretraining diversity > size (+Nav/+ImageNet +1.5–3.6; +800K frames +0.1) | + diverse pretraining | M
Theia | Q03 vision | spatial tokens 78.9 vs CLS 50.0; Theia-B 79.8 vs MVP-L 77.4, R3M 76.5, VC-1-L 69.6 (frozen) | + spatial tokens, + distilled small ViT | H/M
Theia | Q03 vision | real: frozen 0% on long-horizon microwave; drawer frozen→FT Theia 85→100, R3M 0→55, VC-1 0→45, but DINOv2-L 35→20 | + fine-tune (except DINOv2-L) | M
Theia | Q12 model size | 22–86M distilled encoder beats 300–630M VFMs on real WidowX | + small encoder | M
UnbiasedLookPVR | Q03 vision | real 50 demos, fine-tuned MAE ViT-B: ImageNet 41 / Kinetics 44 / DoH 38 vs Ego4D 28 / RoboNet 30 / VC-1 33 / MVP 25; Soup+DoH 60 | + ImageNet-style diverse init, - Ego4D/robot PVRs | M/H
UnbiasedLookPVR | Q03 vision | ViT-B from scratch = 0% on all 3 real tasks | + pretrained init mandatory | H
UnbiasedLookPVR | Q14 robustness | policy dropout 0.2: perturbed-stacking 10→24%, smoother real motion; hurts in sim | + dropout | M
UnbiasedLookPVR | evaluation | sim vs real PVR performance R²=0.32 | - trust sim encoder rankings | M/H
WhatMakesPVRsRobust | Q03 vision | frozen, 9k sim evals: manipulation PVRs (R3M/MVP/VIP) best in-dist but best one ranks 7/15 OOD; DINO/MoCo-v3/sup-ViT better OOD | + ImageNet SSL ViT, - R3M/MVP/VIP for OOD | M
WhatMakesPVRsRobust | Q14 robustness | emergent segmentation (Jaccard) predicts OOD among ViTs; drop w/ distractors 37% vs 85%; real ALOHA lighting+pos shift MoCo-v3 4/10 vs MVP 0/10 | + high-segmentation ViT (DINO-style) | M
WhatMakesPVRsRobust | Q03 vision | DINOv2-S/14 worse in- and OOD than DINO v1 (frozen) | - plain frozen DINOv2 | L/M
RoboMP-DINOv2 | Q05 augmentation | unseen object colors: masked-region color rand + mask prompts 72.5 vs DP-DINOv2 full-image rand 19.1; aug-only masked vs full 0.11 vs 0.01 | + object-region randomization via offline masks | M
RoboMP-DINOv2 | Q03 vision | fine-tuned DINOv2-B DP: spatial-OOD 50.7 → clutter 41.0; RoboMP 60.7/59.7 | ~ fine-tuned DINOv2 fragile | M
RoboMP-DINOv2 | Q04 3D | hard object-centric 3D filtering: obstacle task 3–7% vs full-scene 80–83% | - segmented-only point clouds | M
RESOLVED | Q03 vision | frozen-vs-FT tension: FT wins in-dist when encoder small/low-LR/aug (DP, Theia, Dasari); FT collapses only for ViT-L+MLP+tiny data (VC-1); OOD robustness depends on pretraining recipe (DINO/MoCo/ImageNet ViT > R3M/MVP/VC-1), not frozen-vs-FT; no 2D encoder survives camera/scene shift like 3D (iDP3) | |
DiffusionTransformerPolicy | Q01 action_head | real Franka 50 demos/task, same backbone: discretized 256-bin 19.3% vs MLP diffusion head 34.8% vs DiT denoiser 46.9%; ManiSkill2 30.2/58.6/65.8 | - per-dim discrete tokens, + continuous diffusion w/ strong denoiser | M
DiffusionTransformerPolicy | Q06 chunking | pred length 2→32: 40.8→65.8; exec 1 vs 16 steps: 61.6 vs 58.0 | + long prediction, short execution | M
DiffusionTransformerPolicy | Q07 history | 2 obs 65.8 vs 1 obs 61.6 (chunk 32); 3 obs 35.4 | ~ 1-2 frames | L/M
DiffusionTransformerPolicy | Q10 latency | DDPM 100 steps on 334M model, no latency reported | - (unknown; likely too slow for 8GB) | L
SmolVLA | action_head | LIBERO flow 80.25 vs L1 75.25 (long 53 vs 38), frozen VLM | + flow | M
SmolVLA | chunking | re-query every 1/10/30/50 steps: 80.3/82.8/70.8/51.8; chunk 10 best (84.0) | + short exec horizon, chunk 10-50 | M/H
SmolVLA | execution | async 9.7s vs sync 13.75s/task, 19 vs 9 cubes/min; success 78.3->73.3 (sorting 70->50), no continuity handling | + async queue, - async without boundary fix | M
SmolVLA | model_size | 0.24/0.45/2.25B LIBERO 82.75/87.3/88.75; skip VLM top half ok | + ~0.45B frozen VLM | M
SmolVLA | data | SO-100 real: single-task no-PT 40 < ACT 48.3; multi-task 51.7; +community PT 78.3 | + in-embodiment pretraining + multi-task | M
SmolVLA | robustness | only OOD positions tested (SO-101 ACT 40 vs SmolVLA 50) | ~ no evidence | L
ReactVLA | latency | real: 38.6 ms (5-step iMF) vs SmolVLA 82.2 ms; stack 90 vs 75%; LIBERO 88.0 @18.3 ms vs SmolVLA 87.3 @74.1 ms | + few-step mean flow; our 2 s SmolVLA latency is a deployment bug | M
ReactVLA | action_head | mean flow + Pseudo-Huber; MSE unstable with JVP; AttnRes 88.0 vs 28.7 | + iMF head | L/M
BidirectionalDecoding | execution | EMA/TE under noise 1.5: 18.4 vs vanilla 29.5; BID 31.7; BID +32% rel sim, +46% with EMA; 2x latency (13->26 ms) | + coherence-based sample selection, - naive TE | M
BidirectionalDecoding | chunking | open-loop chunk collapses with noise (64->13) vs closed-loop (49->30); longer context hurts, longer horizon helps | + long pred horizon, frequent re-query | M
BidirectionalDecoding | history | Push-T: extending obs context beyond few steps degrades | - long obs history | L/M
TinyVLA | model_size | real 5 tasks x100 demos: TinyVLA-S 0.4B 23.3 < DP 35.3 < B 77.4 < H 1.3B 94.0 (OpenVLA 68.3) | - <0.5B VLA from own VLM, + ~1B | M
TinyVLA | action_head | inside VLA: diffusion 94 vs ACT head ~13 vs MLP 0 | + diffusion (baseline integration suspect) | L/M
TinyVLA | robustness | view shift 12/16 vs DP 0/16; low light 3/6 vs 0/6; background 10/12 vs 0/12 (1-2 trials/cell) | + pretrained VLM backbone | L
VLA-Adapter | vision | LIBERO-Long bridge: last-layer raw 85.8 < query 90.2 < all-layer raw 90.6 < all query 92.6 < both 95.0; frozen VLM 86.4 vs SmolVLA 77.0 | + multi-layer VLM features + query tokens | M
VLA-Adapter | action_head | L1 one-pass 95.0 vs DiT 91.6 (LIBERO-Long) | + L1 when conditioning rich (conflicts SmolVLA/FLOWER/ACT) | M
VLA-Adapter | model_size | 0.5B no robot PT = 7B OFT (97.3 vs 97.1 LIBERO); 7B backbone +0.2 | + 0.5B VLM | M
VLA-Adapter | latency | 36.5 ms / 219 Hz (8-step chunk) vs OFT 112 ms; train VRAM 24.7 GB @batch 8 (not 8 GB) | + single-pass head; - full FT on 8 GB | M
FLOWER | action_head | CALVIN-ABC len: flow 4.44 vs L1 3.33 vs discrete 1.12 | + flow | M
FLOWER | vision | intermediate fusion 93.4 vs late 61.8 vs early 33.4 (LIBERO-Long); frozen VLM 2.65 vs 4.44; Florence-2 > SmolVLM | + fine-tuned grounding VLM, intermediate features | M
FLOWER | pretraining | Aloha joint-space: cross-action-space PT worse than scratch; droid-joint PT best | - mismatched-action PT | M
FLOWER | latency | RTX 4090: 52 ms/chunk, 1.85 GB (pi0 104 ms/6.7 GB, DP 341 ms/0.5 GB) | + 4-step flow VLA fits laptop inference | M/H
FLOWER | robustness | real: flashlight 50 vs OpenVLA 25; distractors 69.5 vs 41.7; novel obj 33 vs 10 (3 trials/cell) | + VLA semantics help | L
X-VLA | data | PEFT 9M params LIBERO 92.8 @50 demos -> 91.1 @10 demos/task | + fine-tune pretrained VLA in low data | M
X-VLA | pretraining | naive heterogeneous PT: 39.6 -> 25.0 (-14.6); fixed by action alignment + soft prompts -> 73.8 | - naive cross-embodiment PT | M
X-VLA | cameras | wrist view to separate vision encoder, not VLM: 50/47.9 -> 64.6 | + separate wrist encoder | M
X-VLA | model_size | LoRA 9M ~= pi0 full FT (LIBERO-Long 84.2 vs 85.2; WidowX 54.2 vs 55.7) | + ~0.9B + LoRA (8 GB-friendly, inferred) | M
Seer-PIDM | Q09 aux objectives | CALVIN ABC→D from scratch: BC 3.31 → +future-image loss 3.41 → +inverse dynamics on foresight 3.64 | + future prediction; + predictive inverse dynamics coupling | M
Seer-PIDM | Q13 data/pretraining | real 100 demos/task: scratch 60.0 → DROID-pretrained 78.4 SR; OXE (other robots) 53.3→56.7 | + same-embodiment pretraining only | M
Seer-PIDM | Q14 robustness | scratch vs pretrained: background change 6.7 vs 33.3; strong light 46.7 vs 66.7; distractor bowls 33.3 vs 60.0 | - from-scratch 100-demo robustness | M
Seer-PIDM | Q12 model size | OpenVLA-7B full FT at 100 demos 16.7% vs Seer 65M-trainable 60–78% | + small trainable (~65M) with frozen encoders | L/M
Seer-PIDM | Q07 history | uses 7–10-frame history but no ablation | ~ no evidence | L
GenAug | augmentation | real CLIPort/suction, 10 demos: unseen env 38→80%, unseen place obj 8→54%, unseen pick obj 10→46% (offline affordance metric); random-bg baseline competitive for env, not for objects | ~ generative object re-texture (only for object appearance); + cheap random bg for scene | L
GenAug | robustness | object appearance hardest even with aug: pick 45% vs env 85% | + physical object variety in data | M
DemoGen | data diversity | spatial success region ≈ union of demonstrated placements; no extrapolation; DP3 sim 25→400 demos 3→98%, fixed positions 100% | + spread demos over placement grid covering eval region | H
DemoGen | recovery data | disturbance resistance needs disturbance demos: 40.4 → 92.3 normalized (ADR) | + recovery/disturbance demos | M
DemoGen | demo count | 100→150 demos +37 pts, 150→200 +6 pts (precise peg, 40×40 cm) | + ~100–150 demos to cover workspace, diminishing after | M
DemoGen | augmentation | 1 real demo → synthetic point-cloud demos: real 11.0 → 74.6% avg (8 tasks); sim 1-src DemoGen 88 vs 25 real 91; saturates (visual mismatch) | + optional synthetic spatial demos for 3D branch | M
DemoGen | 3D | spatial gen at 100 demos: DP3 49, DP+DINOv2 61, DP+CLIP 53, DP scratch 22, R3M 9 | + 3D / pretrained encoders | M
DemoGen | vision | DINOv2/CLIP init ≫ scratch ResNet ≫ R3M for spatial generalization | + pretrained init (not R3M) | M
RoboAgent-MT-ACT | augmentation | SAM+inpaint semantic aug: ≈+30% rel L1, +100% rel L2 (bg/distractors), +400% rel L3 (new objects); new kitchen 25% vs 0 w/o aug | + scene & object augmentation for OOD | M
RoboAgent-MT-ACT | chunking | chunk 20 (4 s @5 Hz) best; 10 −5%; 40 >−20% | + moderate chunk | M
RoboAgent-MT-ACT | language | FiLM vs concat: −5–10% without FiLM | + FiLM | M
RoboAgent-MT-ACT | data (new task) | add task with 50 demos ×4 aug + 10% replay of old data, no significant forgetting | + small new-task set + replay | L
RoboAgent-MT-ACT | co-training | universal (all activities) < single-activity policy on most tasks (negative transfer) | - indiscriminate unrelated-task mixing | L
DataScalingLaws | data diversity | 32 env-object pairs × 50 demos → 85–92.5% success in unseen envs+objects (4 tasks); per-env demo fraction 50% ≈ 100% | + many conditions, few demos each | H
DataScalingLaws | demo count | plateau at 400–800 total demos (16 env × 64 obj); ~50 demos per env-object pair; ≤100 total unstable | ~ 100–150 demos gives partial OOD only | M
DataScalingLaws | object diversity | 8 training objects → >0.8 on unseen objects; object gen easier than env gen | + 4–8 different pumpkins | H
DataScalingLaws | vision | fine-tuned DINOv2 ViT-L 0.90, LoRA 0.72, frozen 0.00, scratch 0.03; ViT-S/B/L 0.66/0.81/0.90 | + pretrained + full fine-tune; - frozen | H
DataScalingLaws | model size | diffusion U-Net small/base/large 0.88/0.90/0.83 | + small action head | M
DataScalingLaws | evaluation | val action MSE unreliable (LoRA lower MSE but 0.72 vs 0.90 score) | - MSE for model selection | M
DataScalingLaws | protocol | randomize initial gripper pose + object pose each demo; standardize strategy/speed across operators | + randomized starts, consistent strategy | M
MobileALOHA | co-training | 50/50 co-train with 825 same-embodiment off-task demos: whole-task +45/+20/+80/+95/+80 pts on 5 of 7 tasks, 0 on 2 | + co-train with public SO-100/101 data | M/H
MobileALOHA | co-training | 35 co-trained demos 70% > 50 plain 50%; mix 30/50/70% → 95/95/90; pre-train-then-FT no gain | + co-train (not pretrain), ratio insensitive | M
MobileALOHA | action head | ACT 95 vs DP 65 (co-trained, Wipe Wine, 50 demos) | + CVAE/light head in low data | L/M
MobileALOHA | compute | ACT collection+inference on 8 GB RTX 3070 Ti laptop, 50 Hz | + small ACT-class model fits our GPU | H
MobileALOHA | robustness | co-training helps extrapolation: 5th chair 89 vs 0 | + co-training as regularizer | L/M
ALOHA-Unleashed | data quality | duration filtering (2164 eps): all 30%, shortest-50% 55%, shortest-25% 40% | ~ mild filtering, keep corrected mistakes | L/M
ALOHA-Unleashed | recovery data | retries emerge when in data; unseen states (face-down shirt, flipped shoe) never recovered | + explicit recovery / odd-state demos | M
ALOHA-Unleashed | demo count | ShirtMessy 0/20/70/70% at 25/50/75/100% (2164→8658 demos); ShirtEasy saturates at 25–50% | + narrow init first, widen with more data | M
ALOHA-Unleashed | action head | diffusion 70 vs L1 25 (ShirtMessy, 150M); authors: ACT easier in low data | + generative head; data-dependent | M
UMI | data diversity | in-the-wild 1400 demos/30 envs: 71.7% unseen envs; narrow-domain data + same ViT-L: 0% | + vary scene conditions in collection | H
UMI | action space | relative-to-chunk-start 20/20, step delta 16/20, absolute 5/20 (calibration bias) | + chunk-wise relative | M
UMI | latency | latency matching 105/120 vs 69/120 without; jitter removed; 0.5× exec speed smoother | + measure & compensate latency | M/H
UMI | cameras | wrist fisheye 20/20 vs 69°-FoV crop 11/20 | + wide-FoV wrist cam | M
UMI | vision | CLIP ViT-B fine-tuned 14/20 vs scratch ResNet-34 0/10 | + pretrained fine-tuned | M
3DDiffuserActor | Q04 3d_input | RLBench same model: 3D tokens 81.3 vs 2D pooled 47.0; single front RGB-D 78.4 | + 3D (RGB features lifted to 3D) | H(sim)/L(real)
3DDiffuserActor | Q04 fusion | CALVIN ABC→D: pooled point embedding (DP3) 0.31 vs tokenized lifted CLIP features 3.35; rel-attn 81.3 vs abs 71.3 | + lift pretrained 2D feats to 3D + relative attention | M
3DDiffuserActor | Q04 depth_noise | trained clean; 3D noise σ²=0.01 → 72.4 (−6), σ²=0.03 → 50.1 (−28) | ~ needs moderate-quality depth / noise aug | M
3DDiffuserActor | Q01 action_head | Act3D (regression/classification, similar tokens) 65.3 vs diffusion 78.4 single-view | + diffusion | M
3DDiffuserActor | Q10 latency | 600 ms per 6-pose trajectory on 2080 Ti (DP3 581 ms) | - many-step diffusion on laptop | M
Hyper-DP3 | Q04 3d_input | Piper + single D455 stereo, 50 demos, joint actions: HDP3 73/47/20% vs DP3 53/33/7% (15 trials) | + point-cloud policy works with stereo depth on low-cost arm | M
Hyper-DP3 | Q12 model_size | 2.52M params ≈ DP3 255.8M (5000-ep: 58.2 vs 59.3); RoboTwin 63.2 vs 55.2 | + tiny decoder (MLP-Mixer) | M/H
Hyper-DP3 | Q01 action_head | 2 DDIM steps ≈ 10 steps (58.2 vs 58.0); 1 step 53.0; DP3 also 59.3@2 vs 59.9@10 | + diffusion with 2 steps | M/H
Hyper-DP3 | Q10 latency | 4.5 ms (2 steps, 2.5M) vs DP3 51.4 ms vs DP 460 ms | + few-step small 3D policy | H
PointVLA | Q04 fusion | scratch conv point encoder → zero-init linear → additive into 5 late action-expert blocks; VLM 2D-only | + side-branch injection preserving pretrained 2D | M
PointVLA | Q04 3d_input | table height 3→52 mm: 2D VLAs 0/5, PointVLA 5/5; photo-vs-real 0/3 vs 3/3 | + 3D for geometry/height shift | L/M
PointVLA | Q04 rgb_concat | RoboTwin: DP3+RGB < DP3 in 12/13 tasks @20 demos (mean 15.6 vs 23.6) | - naive RGB concat into point cloud | M
PointVLA | Q04 encoder | pretrained 3D encoders hindered learning (no numbers) | + small scratch point encoder | L
EquivariantDP | Q04 3d_input | same DP: voxel 46.3 vs RGB 42.0 @100 demos (+4); equivariance bigger factor | ~ 3D alone modest in sim | M
EquivariantDP | Q04 equivariance | SO(2)-equi +21.9 pts @100 demos; real 80–95% vs voxel-DP 0–60% (20–60 demos, 20 trials) | + equivariant/rot-aug 3D (needs EE actions + calibration) | M/H
EquivariantDP | Q05 augmentation | rot-aug CNN 53.3 vs equi 63.9 vs plain 46.3 (voxel, 100 demos) | + SO(2) rotation aug recovers ~half | M
EquivariantDP | Q02 action_space | absolute EE > relative EE: DP 42.0 vs 33.3, EquiDiff 63.9 vs 48.8 @100 demos | + absolute pose | M
LBM-CarefulExamination | Q13 data | finetuned LBM with 15% task data beats single-task 100% (real SetBreakfastTable); 3–5× less data overall | + pretrain→finetune on own task | H
LBM-CarefulExamination | Q14 robustness | sig. better than single-task in 3/16 sim tasks nominal → 10/16 under lighting/camera/texture shift | + pretrained+finetuned for OOD | H
LBM-CarefulExamination | Q13 data_quality | unfiltered idle starts → policy never moves (89/200 rollouts); trim until 5 cm/15° motion | + trim low-motion prefixes | M
LBM-CarefulExamination | Q13 data_quantity | single-task sim SR 13.5–19.5% @49 demos, 50% @196, 68.5% @490 | ~ 50 demos is low for single-task | M
LBM-CarefulExamination | evaluation | effects only visible with 50 real / 200 sim rollouts + stats; normalization bugs dominate arch changes | + ≥50 trials per condition | H
LBM-CarefulExamination | Q08 language | non-finetuned LBM with small CLIP text encoder executes wrong task in ambiguous scenes | - small frozen text encoder w/o finetune | M
RoboVLMs-WhatMatters | Q03 backbone | VL-pretrained KosMos P.H. ABC→D 4.25 vs no-VL 0.56; PaliGemma-3B 3.82 > Qwen-VL-9B 0.30 | + strong VL pretraining over size | H
RoboVLMs-WhatMatters | Q01 action_head | continuous 4.09 vs discrete bins 0.55 (KosMos); flow 3.68 ≈ MSE+BCE 3.57 (ABC→D) | + continuous; FM≈MSE | H
RoboVLMs-WhatMatters | Q07 history | policy-head history 4.49 > interleaved 4.12 > one-step 4.09 (KosMos, window 16) | + history via separate policy head | M
RoboVLMs-WhatMatters | Q06 execution | unseen scenes: execute full chunk 3.68 > ensemble 3.14 > first action 2.45 | + full-chunk execution | M/H
RoboVLMs-WhatMatters | Q12 model_size | Flamingo 0.1x data: 3B 0.13, 9B 0.83; but 2–3B KosMos/PaliGemma beat 9B VLMs | ~ pretraining quality > size | M
RoboVLMs-WhatMatters | Q13 cross_embodiment | OXE co-train ≈ no gain; same-robot other-task data > OXE; OXE pretrain → few-shot +17.2% SR | + in-domain data first | M
RoboVLMs-WhatMatters | Q14 moe | π0-style action expert: unseen +0.12–0.16 Avg.Len, seen −0.26–0.58 | ~ action expert trades fit for generalization | M
Dita | Q01 action_head | CALVIN scratch: in-context DiT 2.38 vs UNet1D head 1.80 vs MLP head 1.68 vs single-token chunk 0.84; ManiSkill2 discrete 30.2 vs diffusion 58.6/65.8 | + continuous diffusion, - discrete bins | M
Dita | Q10 steps_vs_quality | DDIM steps 100/50/20/10/5/2 → Pick-Coke var 76.4/79.1/85.5/85.3/82.7/70.4; Move-Near var 52.1/66.0/73.0/69.5/63.5/51.6 | + ~10 steps; - 2 steps w/o distillation | M
Dita | Q10 latency | 334M VLA run at 3 Hz on A100 server | - mid-size VLA on 8GB laptop | L/M
Dita | Q11 cameras | LIBERO +wrist cam 82.4 → 92.3 avg (LONG 63.8 → 83.6) | + wrist camera | M
Dita | Q14 robustness | LoRA (11M trainable) fails under bg/clutter/lighting variance; full FT + ColorJitter 20% | + full fine-tune with aug | L
VideoPredictionPolicy | Q09 aux objectives | predictive VDM features 4.33 vs VAE 2.58 / VC-1 1.23 / Voltron 1.54 CALVIN ABC→D (same head) | + future-predictive representations | M
VideoPredictionPolicy | Q09 aux objectives | w/o SVD pretrain + w/o internet video 1.63 vs 4.33; requires 1.5B video model, 8×A100 days | - impractical at 8 GB (use FLARE/MDT-style loss instead) | H
VideoPredictionPolicy | Q11 cameras | static-only 3.58 vs static+wrist 4.33 | + wrist cam | M
VideoPredictionPolicy | Q14 robustness | real Panda unseen objects/backgrounds: VPP 0.73 vs DP 0.25 vs GR-1 0.38 | + predictive pretrained features for shift | M
VideoPredictionPolicy | Q10 latency | TVP 1-step ≈140 ms on 4090 (7–10 Hz w/ chunk 10); no Video Former ≈450 ms | ~ heavy encoders cost latency | M
Octo | Q01 action head | Octo-Small WidowX 40 trials: diffusion 83 vs MSE 35 (hedging, slow) vs discrete-256 18 (misses grasps) | + diffusion over MSE/discrete at small scale | M
Octo | Q03 vision | ~100 demos from scratch: ResNet beats ViT/patch transformer; big transformer overfits; ViT wins only on 800k-traj pretraining (83 vs ResNet-50 70) | + ResNet/CNN for small-data from scratch | M
Octo | Q06 chunking | chunking helps coherence; ALOHA best = chunk 64 exec 12 receding horizon; temporal ensemble no benefit | + chunk + receding horizon, ~ temporal ensemble | L/M
Octo | Q07 history | 2 frames helps zero-shot, diminishing beyond; proprio input "generally worse" (causal confusion) in pretraining | ~ short history, caution proprio | L/M
Octo | Q11 cameras | FT often better with 3rd-person only than 3rd+wrist (only 27% pretrain data has wrist) | - relying on OXE-pretrained generalist for wrist view | M
Octo | Q12 model size | zero-shot 10M<27M<93M; ~100-demo fine-tune avg Octo 72 vs 28M scratch 20 vs VC-1 15 | + pretrained 27–93M init; - big from-scratch transformer | M
Octo | Q13 data | pretrain mix: 25 datasets 83 vs 11 datasets 60 vs Bridge-only 43 | + diversity of pretraining data | M
Octo | Q14 robustness | zero-shot in-dist 85, novel objects 80, novel env 40, novel skill 5 | ~ pretraining helps objects not environments | M
HPT | Q03 vision | frozen ResNet-18 + pretrained 12.6M trunk 70.0 vs VC-1 53.3 / R3M 50.0 / Voltron 46.7 / scratch 43.3 (Sweep, ~100 demos) | + frozen small CNN + policy-level pretraining over vision-only pretraining | L/M
HPT | Q07 history/proprio | scratch no-proprio 26.7 vs with proprio 43.3; pretrain w/o proprio 63.3 vs with 70.0 | + include current proprio | M
HPT | Q12 model size | HPT-XL (227M) 76.7 vs HPT-B (12.6M) 70.0 finetuned | ~ small trunk sufficient, modest gain from size | L
HPT | Q13 data | cross-embodiment pretrain +27 pts over scratch at ~100 demos (43.3→70.0) | + pretrained trunk for 100-demo regime | L/M
HPT | Q10 latency | HPT-Base 47 Hz, HPT-XL 19 Hz on RTX 3070 | + small trunk real-time on laptop GPU | H
OpenVLA | Q01 action head | 7B discrete-token works (Bridge 70.6) but DP from scratch smoother/more precise and competitive on narrow single-instruction fine-tunes | - discrete tokens for small single-task policy | M
OpenVLA | Q03 vision | LoRA-era FT: frozen vision 47.0 vs full FT 69.7 vs last-layer 30.3 (7B, Franka 33 rollouts) | + fine-tune encoder when adapting a big pretrained VLA | M
OpenVLA | Q08 language | OXE pretraining helps mainly multi-object language-grounded fine-tunes; DP wins narrow tasks | ~ language/VLA only needed for multi-object tasks | M
OpenVLA | Q10 latency | int8 at 1.2 Hz on 5 Hz task: 58.1 vs bf16 71.3 (same token accuracy) | + keep inference rate >= control rate | M
OpenVLA | Q12 model size | fine-tuned 7B needs 60 GB (LoRA); int4 inference 7 GB at ~3 Hz; DP from scratch competitive on narrow tasks | - 7B VLA for 8 GB single-task | M
RDT-1B | Q01 action head | diffusion vs regression (1.2B pretrained): unseen object 50 vs 12.5, instruction 100 vs 12.5 (8 trials) | + diffusion over regression | M
RDT-1B | Q12 model size | 166M vs 1.2B: unseen object 37.5 vs 50, scene 62.5 vs 62.5, instruction 25 vs 100 | ~ size matters mainly for language | L/M
RDT-1B | Q13 data | no-pretrain 1.2B: unseen object 0 vs 50, unseen scene 25 vs 62.5 | + pretraining for OOD objects/scenes | M
RDT-1B | Q07 history | 2-frame image history; proprio history excluded to avoid shortcut fixed motions (design, not ablated) | ~ no proprio history | L
RDT-1B | Q11 cameras | 10% independent modality masking to avoid over-reliance on exterior vs wrist (not ablated) | + modality dropout | L
RDT-1B | Q05 augmentation | color jitter + image corruption + proprio noise 40 dB SNR used against fine-tune overfitting; lighting diversity collected (not ablated) | + photometric + proprio-noise aug | L
RDT-1B | Q06 chunking | Ta=64 with DPM-Solver++ 5 steps: 6 chunks/s, 381 actions/s on RTX 4090 (not ablated) | ~ long chunk + fast solver | L
CogACT | Q01 action head | SIMPLER avg: DiT-B 89M 62.5 vs MLP-7L 89M 52.5; DiT-S 13M 58.5 > MLP 89M | + transformer diffusion head over MLP head | M
CogACT | Q06 chunking | future steps 0/3/15/31 → avg 42.8/55.5/62.5/51.2 | + chunk ~16 (1–3 s), - very long chunks | M
CogACT | Q10 latency/smoothness | 2-step chunk exec 50.7 vs temporal ensemble 58.9 vs adaptive (cos-sim weighted) ensemble 62.5 | + overlapping-chunk similarity-weighted ensembling | M
CogACT | Q12 model size | action module 13M/89M/308M → 58.5/62.5/64.8 (log-linear, 7B backbone fixed) | ~ bigger head helps modestly | L/M
CogACT | Q14 robustness | real Realman 71.2 seen → 58.4 unseen table+distractors; unseen colors 87.5, shapes 81.3, categories 25.0 (OpenVLA 6.3 avg) | ~ VLM backbone helps color/shape shift | L/M
pi0 | Q01 action_head | 3.3B VLM + 300M flow expert (bidirectional over H=50, block-causal from obs, 10 Euler steps) beats OpenVLA/Octo/ACT/DP (figure only) | + flow with separate small action transformer | M
pi0 | Q06 chunking | H=50, execute 16 @20Hz / 25 @50Hz open-loop; temporal ensembling "hurt" (no number) | + ~1-2.5 s chunk, execute ~half, no TE | M
pi0 | Q10 latency | RTX 4090: img enc 14 + prefix 32 + 10x expert 27 = 73 ms; KV-cache prefix | + cache obs prefix, small expert makes K steps cheap | H
pi0 | Q12 model_size | pi0-small 470M from scratch viable only with 10k h; VLM-init gain confounded with size | ~ | L
pi0 | Q13 data | pretrain+finetune up to ~2x vs scratch, largest on tasks similar to pretraining (figure only) | + pretraining + curated post-train | M
pi0.5 | Q05 augmentation | recipe: RandomCrop 95% + Rotate ±5° + ColorJitter(b0.3,c0.4,s0.5) on all images (not ablated) | + crop/rotate/strong color jitter default | L/M
pi0.5 | Q13 data | 3->104 training locations: monotone gain, 104 ≈ model trained on test homes (40 trials/pt, figure only) | + maximize scene diversity over repetitions | M
pi0.5 | Q14 robustness | web data only matters for unseen object CATEGORIES (lang follow), not task progress; ME/CE removal significant drop | + diverse data for new env; ~ web data for single task | M
pi0.5 | Q09 aux objectives | implicit-HL (subtask labels in training only) 2nd best > no-HL (significant) | + auxiliary subtask/phase prediction | L/M
pi0.5 | Q01 action_head | FAST-token pretrain + flow post-train > pi0 flow-only even at 300k steps (figure) | ~ large-backbone only | L
pi0.5 | Q02 action_space | absolute target joint/EE poses, per-dim 1–99% quantile norm to [-1,1] (not ablated) | ~ absolute + quantile norm | L
FAST | Q01 action_head | naive per-step binning makes no progress at 20/50 Hz; FAST ≈ diffusion pi0 on small data (<50 h) | - naive discrete tokens; ~ FAST vs flow | H
FAST | Q10 latency | pi0-FAST ~750 ms vs diffusion pi0 <100 ms per 1 s chunk (4090) | + continuous flow head over autoregressive tokens | H
FAST | Q13 data | idle all-zero frames filtered; stationary starts caused hovering (temp 0.7 workaround) | + trim idle frames | M
FAST | Q11 cameras | DROID: random 1-of-2 external cams in training, no calibration -> works from unseen viewpoints (44 trials, partial credit) | + multi-view randomization for camera shift | L/M
FAST | Q06 chunking | 1 s chunks all rates; DROID 15 @15 Hz, execute 8–15 (not ablated) | ~ | L
KnowledgeInsulation | Q03 vision | frozen PaliGemma backbone + trained expert = 0% (drawer, shirt fold) | - fully frozen generic backbone for precise tasks; + fine-tune with protected gradients | M
KnowledgeInsulation | Q01 action_head | flow-only pi0 needs 7.5x steps; KI DROID 0.55 vs pi0 0.49 vs FAST 0.45; LIBERO-Long 85.8 < OFT 94.5 | + flow at inference + aux discrete objective | M (L at 10-50M)
KnowledgeInsulation | Q09 aux objectives | aux token objective FAST > naive stride-5 > naive dense > none; heads must be mutually masked (HybridVLA hurt) | + auxiliary action objective with stop-grad from flow head | M
KnowledgeInsulation | Q10 latency | expert ~10 Hz vs AR 1.3 Hz; pi0-FAST 2x wall-clock per task | + small continuous expert | M/H
KnowledgeInsulation | Q08 language | gradients from fresh expert erode language following; stop-grad or VLM co-training restores | ~ only if multi-task language | M
GR00T-N1 | Q01 action_head | cross-attn flow DiT (H=16, K=4) vs DP @100 demos sim avg 45.0 vs 33.4; real full 76.8 vs 46.4 | + flow DiT, cross-attn to vision tokens | M
GR00T-N1 | Q06 chunking | H=16 @20 Hz with K=4 Euler steps across all embodiments (not ablated) | + ~0.8 s chunk, few flow steps | L/M
GR00T-N1 | Q10 latency | 2.2B, 16-action chunk 63.9 ms on L40 bf16 with K=4 | + reduce flow steps to ~4 | M
GR00T-N1 | Q03 vision | frozen LLM + unfrozen vision encoder + middle-layer (12th) features "better and faster" (no numbers) | + fine-tune vision, mid-layer features | L/M
GR00T-N1 | Q12 model_size | GR-1 sim 30/100/300 demos: GR00T 43.2/50.0/49.3 vs DP 21.3/32.7/40.4 | + pretrained large at low data (confounded by same embodiment) | M
GR00T-N1 | Q13 data | 10% data GR00T 42.6 ≈ full-data DP 46.4; neural traj +4.2/+8.8/+6.8 sim, +5.8 real | + pretraining; + synthetic data | M
GR00T-N1 | Q14 robustness | pick-place seen 92 vs unseen objects 72 (full data); DP 42 vs 30 | - object-appearance shift remains hard | M
GR00T-N1 | Q05 augmentation | video-generated neural trajectories +5.8 real at 10% data, ~105k L40-h to make 827 h | ~ too costly for us | L
CONFLICT | 3d_input | iDP3/DP3 (camera-frame full-scene clouds robust OOD) vs CAGE/RISE (full-scene cloud 0.13 new background, 0 all shifts) & GROOT (only segmented object-centric 3D robust) — likely: robustness needs object-centric/cropped clouds; iDP3 scenes may have had less background clutter change | ~ object-centric 3D | OPEN
CONFLICT | vision | frozen DINOv2+LoRA with spatial tokens (CAGE) robust 0.87/0.80/0.80 vs DP ResNet-scratch 0/0/0.27; fine-tune WITHOUT aug worst, fine-tune WITH jitter+shift best (encoder study) | + pretrained, spatial tokens, aug mandatory | M
EVIDENCE | lighting | E-VLA: SmolVLA (frozen VLM) on SO100 trained at 200 lux → 65%@75lux, 30%@40, 0%@30; adding low-light demos 30→80% @40 lux; enhancement preprocessing barely helps | + collect across lighting | M/H
