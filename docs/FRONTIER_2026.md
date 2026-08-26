# ARC-AGI-2 2026 Frontier — What Matters for Our Prize Strategy

Snapshot: 2026-08-26

This document separates **three different frontiers** that must never be conflated:

1. **public-code Kaggle baseline frontier** — directly inspectable/copyable notebooks;
2. **live private competition frontier** — best scores currently achieved by competing teams under the real no-internet Kaggle rerun;
3. **hosted/verified model-agent frontier** — much stronger systems that may use APIs, external sandboxes or much larger budgets and are not directly competition-valid.

That distinction materially changes our prize strategy.

## 1. Public-code Kaggle baseline frontier

The public-code snapshot moved materially again. Public notebook evidence now includes:

- `Failed in AIMO`: **Best/Public Score 33.89, Version 1**; successful **26m11s** run on **L4 x4**, Apache-2.0 notebook, 3 inputs and **44 output files**;
- `ARC Baseline Rebuild`: **Best Score 31.81, Version 73**; later versions are lower;
- `ARC2 vanilla exact`: **31.39** source snapshot; our controlled reproduction scored **29.72**;
- `ARC 2026 NVARC TRM Evidence Cost V1`: **31.11**;
- `ARC 2026 NVARC TRM Aggressive Cost Order`: **31.11**;
- `ARC2 champion E48`: **29.86**;
- `ARC-AGI-2 Public Frontier Perfpatch Evidence Lab`: **29.03**;
- `ARC AGI2 Minimal Augmentation Specialist`: **28.89**.

Therefore **33.89 is the strongest public-notebook score currently verified in our audit**. N1 remains our controlled reproduction anchor because a stronger public score is not automatically a better scientific baseline.

A related public clone, `Failed in AIMO on Docker-v169-v03`, exposes `qwen3_4b_bfloat16-v02-01-01`, `flash-attn-2.8.2` and an Unsloth notebook dependency, but scores only **29.86**. This supports treating the 33.89 source as part of the broad Qwen/NVARC-style public family while leaving the exact cause of the 33.89 gain unresolved.

The 44 output files make this notebook more interesting as an **artifact-audit target** than as another leaderboard reproduction. See `docs/M1_PUBLIC_3389_AUDIT.md`.

These public notebooks are useful because their code/resources can be inspected. **They are not the live competition frontier.** A gain from our N1 anchor to 35–40% would still be meaningful engineering/scientific progress, but it is not reasonable to treat 35–40% as a likely prize-contending target given the live leaderboard below.

Sources captured/re-verified 2026-08-26:
- https://www.kaggle.com/code/koushikrudra/failed-in-aimo
- https://www.kaggle.com/code/konstantinboyko/failed-in-aimo-on-docker-v169-v03/comments
- https://www.kaggle.com/code/yusuketogashi/arc-baseline-rebuild/output
- https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/code

### P33 consequence

`Failed in AIMO` is assigned internal label **P33**.

P33 does **not** trigger an automatic competition run. The +2.08pp over the previous 31.81 public best and +4.17pp over our N1 score are insufficient reasons by themselves to spend user-side execution or leaderboard quota while live leaders remain ~70%+.

P33 is worth inspecting because its 44 outputs may expose candidate pools, per-task traces, selector evidence, coverage/runtime telemetry or other artifacts that can answer M1 evidence buckets B/C/D without another run.

## 2. Live competition frontier — major strategy reset

Fresh ARC Prize public updates on 2026-08-25 report:

- **nvbanana: 72.08%** — high score in the latest evidence currently frozen here;
- **rabbithole: 70.42%** — second place in that evidence, after a reported jump from 50.42% over the weekend.

ARC Prize President Greg Kamradt publicly noted that nvbanana appeared to have the competition locked around 72% before rabbithole's +20 percentage-point jump and suggested multiple teams may eventually reach the 85% threshold.

These are live competition scores under the ARC Prize 2026 Kaggle regime, not merely public notebook reproductions. The exact current **8th-place score is not established in this repository yet** and must not be guessed.

Sources captured 2026-08-25:
- ARC Prize public post mirror: https://ngntipkolamrenang.twstalker.com/arcprize
- Greg Kamradt public post mirror: https://instalker.org/GregKamradt
- Kaggle leaderboard: https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/leaderboard

### Consequence

Correct interpretation:

> **33.89% is the current public-notebook frontier we can inspect, while ~72% is the latest live competition frontier in our evidence.**

That gap is still enormous. Incremental notebook tuning alone is unlikely to be enough for a Progress Prize unless the live field changes unexpectedly.

## 3. Competition constraints and hidden rerun

The Kaggle competition reruns submitted notebooks on **240 unseen tasks**. The majority have one test input, with a minority requiring multiple outputs. Each test output is scored independently and either exact attempt can earn that output's point.

The notebook must run self-contained, offline, under the Kaggle compute/runtime limits. This makes the 70%+ live scores especially important: they demonstrate that very high ARC-AGI-2 performance is already achievable **inside the competition sandbox**, not only through online frontier APIs.

Sources:
- https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/data
- https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/leaderboard

## 4. Hosted / verified frontier — capability, not direct Kaggle recipe

Modern hosted systems remain useful scientific references but must be kept separate from competition-valid scores.

Examples include:

- frontier model/harness results above 80% ARC-AGI-2;
- Confluence Labs program-synthesis/refinement reports near 98% public evaluation with Gemini + external sandboxes;
- Johan Land's **Modality-Driven Search with Holistic Trace Judging**: 72.9% ARC-AGI-2 semi-private and 76.1% public evaluation, using multiple frontier models, long-horizon search, code execution, visual reasoning and holistic trace judging.

These methods prove strong capability and expose useful mechanisms, but their published forms depend on resources/API access that do not fit the Kaggle no-internet rerun.

Sources:
- https://arcprize.org/leaderboard/community
- https://arxiv.org/abs/2606.31543
- https://github.com/beetree/ARC-AGI

## 5. Important 2026 scientific correction: refinement can collapse diversity

Our earlier design pressure emphasized iterative refinement because 2025 was the “year of the refinement loop” and hosted systems showed large gains from repeated program repair.

Johan Land's 2026 work adds an important counterexample: the paper reports that **prescriptive prompting templates and iterative refinement systematically reduced hypothesis diversity and degraded performance** in his setting. His strongest solver instead generated diverse candidates independently across **text, image and code** modalities, then used a holistic judge to compare full reasoning traces. The work argues that the correct answer is often a minority hypothesis rather than the modal/majority answer.

This does **not** mean refinement is bad in general. It means our M2/M3 thesis must become more precise:

> generate/refine candidates without collapsing useful hypothesis diversity, and measure whether selection preserves unique exact hypotheses.

“Iterative refinement” by itself is therefore neither a sufficient design prescription nor a novelty claim.

Source:
- https://arxiv.org/abs/2606.31543

## 6. Open-weight / hardware reality

Large open-weight ARC-capable models can exceed our controlled baseline but may not fit 4xL4 directly. The current preferred feasibility probe is Nemotron 3.5 Lightning NVFP4, pinned to a specific upstream revision for reproducibility. Vendor documentation indicates a W4A16 fallback path on non-native FP4 hardware, while the BF16 TP4 profile floor is 20 GB/GPU on four Ampere-or-newer GPUs. The target L4 x4 satisfies the nominal BF16 profile floor; bare-vLLM Kaggle compatibility and throughput still require measurement.

The live 70%+ competition scores prove that **a competition-fit route exists**. We should therefore focus less on asking whether 4xL4 is enough in principle and more on discovering what efficient representation/search/adaptation/selection stack makes such performance possible.

Public details of the current leaders' complete methods are not yet available here. Community speculation about particular NVIDIA/Nemotron resources or harnesses is **not treated as evidence** until sourced from the teams or reproducible artifacts.

## 7. Revised prize strategy

Low-value direction:
- optimize toward 35–40% and mistake that for a prize target;
- spend runs reproducing every public notebook update for score alone;
- stack correlated public notebooks without unique exact coverage;
- blindly imitate hosted API systems that cannot fit the competition;
- assume more refinement iterations necessarily improve reasoning;
- infer leader methods from forum speculation.

High-value direction:
- use N1 as a controlled open anchor, not the target frontier;
- mine P33's public artifacts before considering a reproduction;
- obtain candidate-pool, selector and runtime evidence;
- identify which failure class creates the largest exact-score loss;
- preserve genuinely diverse hypotheses under the two-attempt budget;
- investigate efficient competition-fit mechanisms that can produce **large**, not incremental, generalization gains;
- test high-information public routes such as the ARC-post-trained Lightning/NVARC path under bounded compute;
- keep Paper Prize evidence rigorous even if leaderboard competitiveness remains distant.

## 8. M1 consequence

M1 should still finish rather than restart around every public score change:

1. N1 competition evidence is **complete** at 29.72 and remains our reproducible open anchor;
2. candidate-pool / selector / runtime / provenance instrumentation remains high priority;
3. P33 is **inspect-only first** because its 44 outputs may provide this evidence without another Kaggle run;
4. N2 stays conditional because another correlated Qwen-family leaderboard number does not close the live-frontier gap;
5. the Lightning/NVARC L4 feasibility smoke remains the next user-side GPU gate because it probes a materially different ARC-post-trained open-weight path;
6. before M2, hypotheses must be ranked by **potential step-change leverage**, not just likelihood of +1–2 points;
7. we must keep searching for public evidence from current 70%+ teams as it appears;
8. exact current top-8 threshold remains an open fact to retrieve, not something to estimate casually.

The scientific/Paper Prize path remains valuable even if current Progress Prize odds are low. A strong, reproducible mechanism can still be important even before it reaches the 70% live frontier.
