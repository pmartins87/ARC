# M1 NVARC / 2026 Frontier Audit

Date: 2026-08-24
Status: public-source audit; no original competitive mechanism is disclosed here.

## Purpose

M1 needs to identify what is worth reproducing before M2/M3 spend compute on new architecture work. This document isolates the parts of NVARC that materially affected ARC-AGI-2 under Kaggle constraints, and converts them into explicit project decisions.

## Source-grounded NVARC decomposition

NVARC's 2025 winning system had three material ingredients:

1. **Synthetic curriculum at scale.** The published pipeline generated puzzle descriptions, mixed descriptions into harder concepts, generated input-grid programs, and generated output-grid programs. The final ARChitects training mix contained about 3.25M augmented samples drawn from real and synthetic sources.
2. **Qwen3 4B test-time adaptation / ARChitects lineage.** NVARC used a compact grid representation, task-time fine-tuning, batch DFS candidate generation, and augmentation-based candidate rescoring.
3. **TRM as a complementary candidate source.** TRM was pretrained, then fine-tuned at test time. For the ensemble it generated more than the two submission attempts; those candidates were passed into the Qwen candidate scorer.

Primary sources:
- https://www.kaggle.com/competitions/arc-prize-2025/writeups/nvarc
- https://github.com/1ytic/NVARC
- https://arcprize.org/blog/arc-prize-2025-results-analysis

## The important negative result: standalone score is not enough

NVARC reported that its TRM could solve some puzzles the Qwen component missed, yet the ensemble often failed to convert those unique candidates into additional leaderboard points because the Qwen scorer did not always rank them into the final two attempts.

Published examples of the effect:
- a Qwen3 2B submission at 21.53 improved to 22.50 with TRM;
- a stronger Qwen3 4B submission at 27.22 remained 27.22 after TRM was added;
- the authors explicitly noted that most TRM solves overlapped Qwen solves and some unique TRM solves were not selected.

This gives M1 a hard lesson:

> A component is useful only if it adds **unique exact candidates** and the final selector reliably preserves those candidates inside the two-attempt budget.

Accordingly, raw solver score is not an acceptance gate for future components. We must measure candidate complementarity and selection loss.

## Candidate scoring details worth preserving

The NVARC writeup describes two selection lessons:

- candidate solutions were rescored under the **same set of eight augmentations** so scores were comparable across candidates;
- post-competition experiments improved selection by combining how often a candidate was found during DFS with an ensemble of augmentation log-probabilities.

This reinforces a separation that will remain explicit in our project:

1. **candidate discovery ceiling** — does any component generate the true output at all?
2. **selection efficiency** — when the truth is in the candidate pool, does our two-attempt selector retain it?

We should never attribute a selection failure to the generator, or a generation failure to the selector.

## TRM reproduction decision

The official NVARC TRM reproduction path is not an efficient first baseline for us:

- original pretraining used 8xH100;
- the published training set had 4,073 puzzles expanded with 256 augmentations to ~1.04M samples;
- the Kaggle-oriented evaluation uses four GPUs and test-time fine-tuning;
- NVARC reports ~10% public score for its best standalone TRM reproduction, while current 2026 public notebooks already incorporate stronger NVARC/TRM-derived modifications around the low-30% frontier.

Therefore **we will not retrain TRM from scratch** in M1. That would consume compute without answering the immediate prize question.

A TRM-family run is accepted into M1 only if it satisfies all of:

- uses a published checkpoint / reproducible public notebook;
- fits 2026 Kaggle L4x4 and 12-hour constraints;
- provides per-task predictions or candidate artifacts we can compare against N1;
- is selected as one controlled complementarity experiment, not a notebook collection exercise.

## Current 2026 baseline queue

### N1 — primary baseline

`ARC2 vanilla exact`

Public reference at the 2026-08-24 snapshot:
- public score: 31.39%;
- runtime: about 25 minutes;
- hardware: L4 x4;
- Qwen3 4B grid model lineage.

User-side clean reproduction has been launched/submitted; hidden rerun score is pending at the time of this audit.

### N2 — controlled TRM/NVARC comparison

Choose exactly one current public NVARC/TRM notebook after N1 is confirmed. Current public references include notebooks reported around 31.11%.

N2 exists to answer one question only:

> Does a materially different TRM/NVARC candidate path add unique exact outputs relative to N1, or is it largely redundant?

If we cannot obtain task-level predictions suitable for the frozen public evaluation split within the M1 timebox, mark this comparison PARTIAL and move on.

### C0 — strong no-pretraining reference

CompressARC remains the bounded alternative reference because it attacks each puzzle from scratch with a compression/MDL objective. It is scientifically distinct from N1 and therefore potentially more valuable for complementarity than another near-clone of Qwen TTT.

M1 will not optimize CompressARC. We only need enough evidence to determine whether its candidate distribution is usefully different.

## Cost-aware stop rules

A new component is not promoted merely because it has non-zero accuracy.

For any solver component S, record:

- standalone pass@2;
- exact-output set;
- outputs uniquely solved vs the current portfolio;
- oracle union gain;
- selection gain after the actual two-attempt selector;
- runtime / GPU-memory cost;
- output-shape failure rate and invalid-output rate.

Reject or defer a component when any is true:

- unique oracle gain < 1 percentage point and runtime cost is material;
- all or nearly all exact solves are already covered by the stronger component;
- it requires retraining beyond our M1 timebox;
- its inference path cannot fit Kaggle final constraints;
- its apparent gain depends on inspecting held-out answers or task-specific manual rules.

The 1pp threshold is an M1 triage rule, not a scientific law; M3/M6 may revisit a cheap component if its marginal compute is negligible.

## Research pressure for M2/M3

The combined evidence from NVARC, the 2025 ARChitects masked-diffusion system, SOAR, and 2026 hosted-agent results points toward **iterative refinement** rather than a larger list of one-shot primitives.

The open engineering question that fits our competition constraints is:

> How much of the benefit of iterative hypothesis/program refinement can be compressed into a self-contained, offline Kaggle solver with a strict two-attempt output budget?

This is a research direction, not a novelty claim. Before any specific original mechanism is committed, the repository-visibility gate must be revisited.

## M1 exit evidence still required

M1 can close PASS/PARTIAL when we have:

1. N1 hidden rerun score and runtime;
2. one bounded alternative candidate source (N2 or C0) with comparable task-level outputs, or a documented PARTIAL reason;
3. complementarity/oracle-union analysis;
4. a decision on the first M2/M3 hypothesis based on measured error structure;
5. visibility decision before original competitive code is published.
