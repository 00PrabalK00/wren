# W3_AnchorDreamRepurposingVideoDiffusionforE — AnchorDream: Repurposing Video Diffusion for Embodiment-Aware Robot Data Synthesis (2025/2026, arXiv 2512.11797)
Setup: Data synthesis: perturb key states of seed demos (MimicGen/DemoGen-style, real: +-10 cm horizontal), render robot-only motion video from URDF, then a Cosmos-Predict2 2B video diffusion model (LoRA, 8xA100, 3 days) paints objects/scene conditioned on the robot render + language + global trajectory. Sim: RoboCasa 24 tasks x 50 human demos, BC-Transformer, 2 side cams + wrist, 50 rollouts/task. Real: PiPER single arm, 6 tasks x 50 demos, Diffusion Policy, third-person + wrist cam, 20 rollouts/task, 10x generated data. Generated video 128x128 (sim) / 180x320 (real).
Claim: robot-motion-anchored video generation turns 50 demos into many new-behaviour demos and roughly doubles real success.
Evidence:
 - RoboCasa avg: Human50 22.5% -> +AnchorDream300 30.7% -> oracle +MimicGen300 (sim execution) 33.3%. Per skill e.g. levers 36.0->54.7, knobs 10.0->21.0, pick&place 1.8->4.3.
 - Generated-only AnchorDream300 24.8% vs Human50 22.5% vs DreamGen10K (video+IDM) 20.6%.
 - Scaling generated data (7-task subset, figure): rises from ~16-24% at 0 to ~36% at 1000 (figure values, noisy at low counts).
 - Real PiPER (Table IV): avg 28 -> 63 (text says 60.0); CloseDrawer 30->75, OpenDrawer 0->25, PourToBowl 0->35, SweepCoffeeBeans 35->95, ToyToPlate 85->100, BookToShelf 20->45.
Ablations: no global trajectory conditioning 30.7 -> 26.6; shortened generation window (189->93 frames) 30.7 -> 28.1.
Failure/limitations: tabletop only. Critical read: gain is from new trajectories (object position diversity) + matching visuals, not tested under lighting/camera shift; needs URDF render + camera calibration + 2B video model fine-tuned on 8xA100 for 3 days — far outside an 8 GB laptop budget; real baseline DP on 50 demos is weak (28%), so doubling from a low base; table/text average mismatch (63 vs 60); 20 rollouts/task.
Conflicts: consistent with MimicGen/DemoGen (spatial diversity of demos is the bottleneck at 50 demos); unlike appearance-only generative augmentation (ROSIE, RoboEngine) it expands trajectories. DreamGen (IDM-labeled video) underperforms here.
Relevance: Confirms that with 50 demos the limiting factor is coverage of object positions; cheap alternative for us is collecting demos over a wider spatial spread or DemoGen-like point-cloud synthesis using RealSense depth. The method itself is not practical on our compute.
Decision impact:
 - Q05 augmentation (generative/synthetic demos): supports synthetic trajectory+visual demo expansion from 50 seeds — confidence M (real robot 6 tasks, but heavy compute; not reproducible on 8 GB).
 - Q13 data quantity/diversity: supports that position diversity beyond 50 demos gives large gains (28->63 real) — M.
