# ARC Prize 2026 — Paper Track Plan

Snapshot: 2026-08-25

## What we are competing in

This project currently targets **two separate prize tracks that share one research program**:

1. **ARC-AGI-2 competition** — Kaggle code competition. Primary objective: maximize exact pass@2 on the hidden ARC-AGI-2 evaluation under Kaggle constraints.
2. **ARC Prize 2026 Paper Prize** — separate judged writeup competition. A valid paper must be linked to a working Kaggle code submission from ARC-AGI-2 or ARC-AGI-3. A high leaderboard score helps the Accuracy criterion but is not required for paper eligibility.

We are **not currently entering ARC-AGI-3**. ARC-AGI-3 is a third independent competition track with interactive environments and would require a separate agent architecture.

Operationally, the project remains one research effort because the same experiments, ablations, code, failure analysis and conceptual contribution can support both ARC-AGI-2 and the Paper Prize.

## Prize logic

### ARC-AGI-2

- Progress Prizes reward leaderboard performance.
- Grand Prize rewards the strongest Solution Writeup under six equally weighted dimensions: Accuracy, Universality, Progress, Theory, Completeness and Novelty.
- Bonus Prize is tied to reaching the competition's 85% target.

### Paper Prize

Paper submissions are judged on:
- Accuracy;
- Universality;
- Progress;
- Theory;
- Completeness;
- Novelty.

This means the paper track is not a consolation prize. A method can be scientifically valuable even if it is not top-8 on the ARC-AGI-2 leaderboard, provided it demonstrates a real working submission and contributes genuinely useful insight.

## Deadline policy

The ARC Prize site lists papers due 2026-11-08, while the Kaggle Paper Track page currently lists 2026-11-09 23:59 UTC. To avoid depending on a discrepancy, this repository uses **2026-11-08 as the internal hard deadline** for paper completion/submission readiness.

ARC-AGI-2 code deadline remains 2026-11-02 23:59 UTC.

## Paper development strategy

Do not wait until November to write the paper. Build it continuously from evidence.

### During M1–M2

- maintain prior-work map;
- record negative results;
- freeze evaluation protocol;
- identify which failure modes are generation, selection, adaptation or runtime failures;
- avoid novelty claims until literature/source audit supports them.

### During M3–M5

- every serious hypothesis gets an explicit experiment and ablation plan;
- preserve failed hypotheses when scientifically informative;
- distinguish competition engineering gains from reasoning/scientific gains;
- measure generalization on frozen validation/heldout gates.

### During M6–M7

- freeze architecture;
- reproduce final numbers;
- prepare tables and figures from experiment ledger;
- audit claims against code and results.

### During M8

- write final concise paper;
- attach the corresponding public Kaggle notebook/code submission;
- complete open-source obligations;
- submit before the internal 2026-11-08 deadline.

## Current working research question

The broad research pressure from current public evidence is:

> How much of the benefit of iterative hypothesis/refinement can be compressed into a self-contained, offline Kaggle solver under a strict two-attempt ARC output budget?

This is **not yet a novelty claim** and does not identify a final mechanism. The specific original mechanism, if any, must pass the repository visibility gate before being committed publicly.

## Paper acceptance gate

The Paper Track becomes a serious submission when all of the following exist:

- one working Kaggle submission linked to the claimed method;
- reproducible experiment ledger;
- at least one clearly stated contribution supported by evidence;
- prior-work audit showing what is actually new or newly demonstrated;
- ablations separating the contribution from baseline effects;
- validation/heldout evidence that does not rely on leaderboard tuning;
- final writeup covering approach, results, theory, limitations and reproducibility.
