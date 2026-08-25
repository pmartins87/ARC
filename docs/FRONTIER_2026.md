# ARC-AGI-2 2026 Frontier — What Matters for Our Prize Strategy

Snapshot: 2026-08-25

This document now separates **three different frontiers** that must never be conflated:

1. **public-code Kaggle baseline frontier** — directly inspectable/copyable notebooks;
2. **live private competition frontier** — best scores currently achieved by competing teams under the real no-internet Kaggle rerun;
3. **hosted/verified model-agent frontier** — much stronger systems that may use APIs, external sandboxes or much larger budgets and are not directly competition-valid.

That distinction materially changes our prize strategy.

## 1. Public-code Kaggle baseline frontier

At the 2026-08-24/25 public Code snapshot, directly inspectable notebooks include roughly:

- `ARC2 vanilla exact`: **31.39**;
- `ARC 2026 NVARC TRM Evidence Cost V1`: **31.11**;
- `ARC 2026 NVARC TRM Aggressive Cost Order`: **31.11**;
- `ARC2 champion E48`: **29.86**;
- `ARC-AGI-2 Public Frontier Perfpatch Evidence Lab`: **29.03**;
- `ARC AGI2 Minimal Augmentation Specialist`: **28.89**.

These are valuable because their code/resources can be inspected and reproduced. **They are not the current live competition frontier.**

N1 (`ARC2 vanilla exact`) remains useful as our first open, reproducible anchor. A gain from ~31% to 35–40% would still be meaningful engineering/scientific progress relative to that open anchor, but it is no longer reasonable to describe 35–40% as a likely prize-contending target given the live leaderboard below.

Source:
- https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/code

## 2. Live competition frontier — major strategy reset

Fresh ARC Prize public updates on 2026-08-25 report:

- **nvbanana: 72.08%** — current high score;
- **rabbithole: 70.42%** — current second place, after a reported jump from 50.42% over the weekend.

ARC Prize President Greg Kamradt publicly noted that nvbanana appeared to have the competition locked around 72% before rabbithole's +20 percentage-point jump and suggested multiple teams may eventually reach the 85% threshold.

These are live competition scores under the ARC Prize 2026 Kaggle regime, not merely public notebook reproductions. The exact current **8th-place score is not established in this repository yet** and must not be guessed.

Sources captured 2026-08-25:
- ARC Prize public post mirror: https://ngntipkolamrenang.twstalker.com/arcprize
- Greg Kamradt public post mirror: https://instalker.org/GregKamradt
- Kaggle leaderboard: https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/leaderboard

### Consequence

Our earlier mental model that the competition frontier was around 31% was too optimistic about how close a public notebook baseline is to a prize position.

Correct interpretation:

> **31.39% is the open/public-code baseline frontier we can reproduce, while ~72% is the current live competition frontier.**

That gap is enormous and means incremental notebook tuning alone is unlikely to be enough for a Progress Prize unless the live field changes unexpectedly.

## 3. Competition constraints and hidden rerun

The Kaggle competition reruns submitted notebooks on **240 unseen tasks**. The majority have one test input, with a small number requiring two outputs. The public leaderboard is calculated from approximately half the hidden test data and final standings from the other half.

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

Large open-weight ARC-capable models can exceed our public-code anchor but may not fit 4xL4 directly. Earlier audits already showed examples whose official checkpoints need substantially more aggregate VRAM than Kaggle supplies.

The live 70%+ competition scores prove, however, that **a competition-fit route exists**. We should therefore focus less on asking whether 4xL4 is enough in principle and more on discovering what efficient representation/search/adaptation/selection stack makes such performance possible.

Public details of the current leaders' complete methods are not yet available here. Community speculation about particular NVIDIA/Nemotron resources or harnesses is **not treated as evidence** until sourced from the teams or reproducible artifacts.

## 7. Revised prize strategy

Low-value direction:
- optimize toward 35–40% and mistake that for a prize target;
- stack correlated public notebooks without unique exact coverage;
- blindly imitate hosted API systems that cannot fit the competition;
- assume more refinement iterations necessarily improve reasoning;
- infer leader methods from forum speculation.

High-value direction:
- use N1 as a controlled open anchor, not the target frontier;
- obtain candidate-pool, selector and runtime evidence;
- identify which failure class creates the largest exact-score loss;
- preserve genuinely diverse hypotheses under the two-attempt budget;
- investigate efficient competition-fit mechanisms that can produce **large**, not incremental, generalization gains;
- keep Paper Prize evidence rigorous even if leaderboard competitiveness remains distant.

## 8. M1 consequence

M1 should still finish rather than panic and restart:

1. N1 hidden rerun remains necessary as our reproducible open anchor;
2. candidate-pool / selector / runtime / provenance instrumentation remains useful;
3. N2 stays conditional because another ~31% public notebook does not close a ~40-point live-frontier gap;
4. before M2, hypotheses must be ranked by **potential step-change leverage**, not just likelihood of +1–2 points;
5. we must search for public evidence from current 70%+ teams as it appears;
6. exact current top-8 threshold remains an open fact to retrieve, not something to estimate casually.

The scientific/Paper Prize path remains valuable even if current Progress Prize odds are low. A strong, reproducible mechanism can still be important even before it reaches the 70% live frontier.
