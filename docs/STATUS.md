# ARC Prize 2026 — Project Status

Last updated: 2026-08-24

## Executive state

- **Current milestone:** M1 — Reproduce competitive baselines — **ACTIVE**.
- **Completed:** M0 — Foundation and rules freeze — **PASS**.
- **Current gate:** reproduce a competitive neural/NVARC-family baseline and obtain a materially stronger symbolic/program-synthesis reference; then build an error/complementarity map.
- **User-side experiment:** B0 — unchanged `BlackCat Stable Anchor — NVARC Guard` Kaggle reproduction — **PENDING USER RUN**.
- **Research-side experiment:** S0 — compact verified symbolic baseline — **MEASURED / REJECT as standalone**.
- **Primary competition end:** 2026-11-02 23:59 UTC.
- **Paper Track end:** 2026-11-09 23:59 UTC.
- **M1 timebox end:** 2026-09-02.

The finite roadmap and project definition-of-DONE are in `docs/ROADMAP.md`.

## Competition enrollment

User-side Kaggle screenshots show:
- ARC Prize 2026 — ARC-AGI-2 with **Submit Prediction** available;
- ARC Prize 2026 — Paper Track with **View Writeups** and the account message that no writeup has been created yet.

Working conclusion: both enrollments appear successful. Re-verify Kaggle account/identity/prize eligibility well before the entry deadline.

## Deadlines snapshot

ARC-AGI-2:
- Entry/team merger deadline: 2026-10-26 23:59 UTC.
- Final submission deadline: 2026-11-02 23:59 UTC.
- Winners announcement: 2026-12-04.

Paper Track:
- Current live Kaggle UI and current competition page show **2026-11-09 23:59 UTC**.

## M0 — PASS

PR #1 was merged to `main`.

Implemented/documented:
- exact pass@2 scorer;
- grid/schema validation;
- identity smoke baseline;
- Python project/test scaffold;
- research/leakage protocol;
- experiment ledger contract;
- initial state-of-the-art map;
- competition mechanics/deadline snapshot.

## M1 — ACTIVE

### Evaluation discipline

- 1,000 training tasks: uncalibrated training/development material.
- 120 public evaluation tasks: primary public proxy for hidden ARC-AGI-2 generalization.
- operational frozen split: **60 eval-development / 30 eval-validation / 30 eval-heldout**;
- seed/profile are recorded in the manifest;
- continuous iteration is allowed only on the 60-task development split.

### Public baseline landscape at 2026-08-24

Current Kaggle Code page shows:
- `ARC2 vanilla exact`: **31.39** public score;
- `ARC 2026 NVARC TRM Evidence Cost V1`: **31.11**;
- `ARC 2026 NVARC TRM Aggressive Cost Order`: **31.11**;
- `BlackCat Stable Anchor — NVARC Guard`: current page reports **26.81**, historical best **28.89 (V4)**, runtime about 24m48s on L4 x4.

These are third-party public scores and are not yet our reproduced results.

### B0 — Kaggle pipeline anchor

Selected first user-side reproduction:

`BlackCat Stable Anchor — NVARC Guard`

First run policy: unchanged notebook. Record exact source version, L4 x4 runtime and public score. B0 exists to prove the account/notebook/model/submission path before B1 targets the ~31% frontier.

Detailed protocol: `docs/M1_BASELINE_AUDIT.md`.

### S0 — compact symbolic baseline — REJECT as standalone

A PR-triggered GitHub Actions benchmark is now working, so symbolic changes can be measured before merge on the frozen development split.

Measured result at commit `a0b31d0a7afbee3edbcc7b6c411bd99e5c0d0ce1`:
- regression CI: **13/13 PASS** after correcting the constant-output ranking bug;
- development tasks: 60;
- test outputs: 82;
- pass@1: **0.0%**;
- pass@2: **0.0%**;
- fitted exact hypotheses: **0 across all 60 tasks**;
- runtime: **14.78 s** on GitHub Actions CPU.

Conclusion: S0 is too shallow to count as the serious symbolic M1 baseline. It remains as a lower-bound/regression instrument. We will not extend M1 by blindly enumerating more primitives.

Experiment: `experiments/E0002_20260824_s0_symbolic_dev.md`.

### Aggregate development profile

Using training demonstrations only (no test outputs):
- 39/60 tasks preserve input/output dimensions in every demonstration;
- 17/60 consistently shrink area; 1/60 consistently enlarges area;
- 52/60 always keep output colors within the input color set;
- 32/60 preserve the exact color set;
- 22/60 consistently remove colors;
- 7/60 consistently introduce colors.

The main gap is therefore contextual/compositional transformation rather than basic geometry/color bookkeeping.

## Compute policy

- **GitHub Actions:** deterministic tests, aggregate profiling and fast CPU symbolic development measurements.
- **Ryzen 9:** later large CPU search, synthetic generation, profiling and ablations where local parallelism materially helps.
- **Kaggle L4 x4:** neural baselines, heavy hybrid runs and all final competition-valid executions.

The final solution must fit Kaggle limits even when the Ryzen 9 helps discover it.

## Repository visibility decision

**Keep `pmartins87/ARC` PUBLIC through M1.**

M1 contains infrastructure, public baseline reproduction and diagnostic work whose secrecy value is low. Reassess before the first genuinely original competitive mechanism or unpublished material improvement is committed.

## Immediate gates

### User-side
1. Run B0 unchanged on Kaggle.
2. Submit it to the competition.
3. Record/send exact notebook version, public score and runtime.

### Research-side
1. close/merge the S0 measurement PR after green checks and ledger/status capture;
2. audit a materially stronger published symbolic/program-synthesis reference (SOAR / CompressARC / licensed Kaggle equivalent) without letting M1 become an implementation sink;
3. prepare B1 frontier reproduction target and comparison protocol;
4. after B0/B1, compare neural predictions with symbolic/program-synthesis coverage and freeze the first evidence-based research hypothesis.

## Finite-project rule

A milestone that misses its gate is marked `PARTIAL`; the best working artifact is carried forward and the project advances. No phase can consume the whole schedule. No new architecture enters after the M6 freeze on 2026-10-23. ARC-AGI-2 R&D stops at the final code deadline; Paper Track work stops at the paper deadline; M9 is administration/outcome recording only.
