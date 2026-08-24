# M1 Baseline Audit

Snapshot: 2026-08-24

## Purpose

Before developing a novel solver, establish reproducible competition baselines on both the Kaggle execution path and an independent symbolic path. The baseline phase must prove that our account/notebook/model/submission pipeline works and produce score/runtime/error-complementarity references.

## Current public-code frontier snapshot

The live ARC-AGI-2 Kaggle Code page currently exposes:

- `ARC2 vanilla exact` — reported public score **31.39**;
- `ARC 2026 NVARC TRM Evidence Cost V1` — **31.11**;
- `ARC 2026 NVARC TRM Aggressive Cost Order` — **31.11**;
- `ARC AGI2 Minimal Augmentation Specialist` — **28.89**;
- additional recent symbolic/hybrid notebooks without a stable reported score in the current snapshot.

These are third-party Kaggle-reported numbers, not yet reproduced by this project.

## Baseline B0 — Kaggle pipeline anchor

First user-side reproduction target:

**BlackCat Stable Anchor — NVARC Guard**

Public notebook:
https://www.kaggle.com/code/lucifer19/blackcat-stable-anchor-nvarc-guard

Observed public metadata at audit time:
- current visible public score: **26.81**;
- historical best: **28.89 (V4)**;
- visible runtime: approximately **24m48s**;
- accelerator: L4 x4;
- language: Python;
- license: Apache 2.0;
- model input includes a Qwen3 4B grid SFT model.

The exact copied version must be recorded because the current notebook score and historical best are different.

Why start below the maximum public score:
1. it has a stable direct public notebook we can copy exactly;
2. runtime is short enough for a cheap end-to-end pipeline test;
3. it is NVARC-derived and therefore connects directly to the 2025 winning family;
4. after exact reproduction, movement to the 31.11–31.39 public frontier is easier to diagnose than starting with a more opaque stack.

## B0 run protocol

The first run is a **reproduction**, not an optimization experiment.

1. Open the public notebook.
2. Record which source version is being copied.
3. Click `Copy & Edit`.
4. Preserve code and model inputs unchanged for the first run.
5. Select L4 x4 if the notebook requests/permits it.
6. Keep internet disabled for competition-compatible execution.
7. Run/save a complete version.
8. Submit that finished version to ARC-AGI-2.
9. Record:
   - copied notebook/version;
   - accelerator;
   - runtime;
   - public score;
   - any errors/warnings;
   - attached model/dataset versions.

## B0 acceptance criteria

`PASS` requires:
- successful notebook completion;
- valid `submission.json`;
- accepted Kaggle submission;
- score and runtime captured;
- result entered in the experiment ledger.

A score difference from the source notebook is not automatically failure. First investigate notebook version, model input version, randomness, Kaggle container changes, and competition rerun differences.

## S0 — independent symbolic reference

Status: **IMPLEMENTED / BENCHMARK PENDING**.

The project now has its own compact verified symbolic solver rather than relying exclusively on third-party symbolic code. It contains whole-grid D4 transforms, crop, component selection, scaling, color remapping and constant-output hypotheses; every fitted rule must reproduce every training demonstration exactly.

The evaluator strips test outputs before inference and records per-task pass@1/pass@2 telemetry. GitHub Actions is configured to clone the official ARC-AGI-2 data and run S0 continuously only on the frozen 60-task evaluation-development split.

Documentation: `docs/M1_SYMBOLIC_BASELINE.md`.

S0 is not a candidate final architecture yet. Its important M1 role is to reveal errors complementary to the neural/NVARC family.

## Next baselines

### B1 — public frontier
Preferred first target: **`ARC2 vanilla exact` (31.39 public score)** if the live notebook remains directly reproducible when B0 finishes. Fallback: one of the 31.11 NVARC/TRM notebooks.

B1 is not modified until an unchanged reproduction is recorded.

### B2 — isolated TRM contribution
Measure the TRM-family component independently, including pass@1/pass@2 marginal value and runtime cost.

### S0/B1 overlap analysis
On public offline tasks where predictions and truths are available, compare:
- both solve;
- neural only;
- symbolic only;
- neither solves;
- marginal gain from second attempt;
- runtime per solver.

This overlap, rather than standalone symbolic score, will drive the first original M2/M3 hypothesis.

## M1 gate

M1 is complete only when we have at least:
- one serious neural/NVARC-family baseline reproduced;
- one measured symbolic/program-synthesis baseline;
- exact per-output scoring locally;
- runtime and error-overlap measurements;
- a justified first research hypothesis based on measured failure gaps.

M1 timebox ends 2026-09-02. If a component cannot be reproduced by then, mark it `PARTIAL`, preserve the best evidence, and advance rather than extending M1 indefinitely.
