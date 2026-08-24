# M1 Baseline Audit

Snapshot: 2026-08-24

## Purpose

Before developing a novel solver, establish a reproducible competition baseline on the actual Kaggle execution path. The baseline must prove that our account/notebook/model/submission pipeline works and give us a score/runtime reference.

## Current public-code frontier snapshot

The ARC-AGI-2 Kaggle Code page currently exposes public notebooks around the low-30% range, including:

- `ARC2 vanilla exact` — reported public score 31.39;
- `ARC 2026 NVARC TRM Evidence Cost V1` — reported public score 31.11;
- `ARC 2026 NVARC TRM Aggressive Cost Order` — reported public score 31.11;
- `ARC AGI2 Minimal Augmentation Specialist` — reported public score 28.89.

These are third-party Kaggle-reported numbers, not yet reproduced by this project.

## Baseline B0 — pipeline anchor

First reproduction target:

**BlackCat Stable Anchor — NVARC Guard**

Public notebook:
https://www.kaggle.com/code/lucifer19/blackcat-stable-anchor-nvarc-guard

Observed public metadata at audit time:
- best reported public score: 28.89 (version 4);
- visible version runtime: approximately 24m48s;
- accelerator: L4 x4;
- language: Python;
- license: Apache 2.0;
- model input includes a Qwen3 4B grid SFT model.

Why start below the maximum public score:
1. it has a stable direct public notebook we can copy exactly;
2. runtime is short enough for a cheap end-to-end pipeline test;
3. it is NVARC-derived and therefore connects directly to the 2025 winning family;
4. after exact reproduction, movement to the 31.11–31.39 public frontier is easier to diagnose than starting with an opaque higher-scoring stack.

## B0 run protocol

The first run is a **reproduction**, not an optimization experiment.

1. Open the public notebook.
2. Click `Copy & Edit`.
3. Preserve code and model inputs unchanged for the first run.
4. Select L4 x4 if the notebook requests/permits it.
5. Keep internet disabled for competition-compatible execution.
6. Run/save a complete version.
7. Submit that finished version to ARC-AGI-2.
8. Record:
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

## Next baselines after B0

### B1 — public frontier
Reproduce one currently available 31.11–31.39 public notebook.

### B2 — isolated TRM contribution
Measure the TRM-family component independently, including pass@1/pass@2 marginal value and runtime cost.

### B3 — symbolic baseline
Build/reproduce a dependency-light symbolic/program-synthesis solver and measure its complementary solved-task set against neural baselines.

## M1 gate

M1 is not complete until we have at least:
- one serious neural/NVARC-family baseline;
- one serious symbolic/program-synthesis baseline;
- exact per-output scoring locally;
- runtime and error-overlap measurements;
- a justified first research hypothesis based on measured failure gaps.
