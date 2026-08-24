# ARC Prize 2026 — Project Status

Last updated: 2026-08-24

## Executive state

- **Current milestone:** M1 — Reproduce competitive baselines — **ACTIVE**.
- **Completed:** M0 — Foundation and rules freeze — **PASS**.
- **Merged M1 evidence:** S0 measurement/stop-rule, strong-baseline audit, complementarity analyzer, and 2026 SOTA refresh are on `main`.
- **Current gate:** obtain N1 hidden rerun score, obtain one bounded distinct candidate source, then measure exact-output complementarity/selection ceiling.
- **N1 local Kaggle execution:** unchanged `ARC2 vanilla exact` Version 1 — **COMPLETE**, 25m29s on L4 x4.
- **N1 competition submission:** submission panel reached with Version 1 / `submission.json`; hidden rerun score **PENDING/UNCONFIRMED**.
- **Fallback N0:** `BlackCat Stable Anchor — NVARC Guard` — skip unless N1 submission fails.
- **Strong distinct reference:** CompressARC C0 — **SELECTED / timeboxed**.
- **Controlled NVARC/TRM comparison:** N2 — **one run maximum after N1**, only if it yields comparable task-level evidence.
- **Primary competition end:** 2026-11-02 23:59 UTC.
- **Paper Track end:** 2026-11-09 23:59 UTC.
- **M1 timebox end:** 2026-09-02.

The finite roadmap and project definition-of-DONE are in `docs/ROADMAP.md`.

## Competition enrollment

User-side Kaggle screenshots show:
- ARC Prize 2026 — ARC-AGI-2 with submission controls available;
- ARC Prize 2026 — Paper Track with writeup controls and account-specific status.

Working conclusion: both enrollments appear successful. Re-verify identity/prize eligibility well before the entry deadline.

## Deadlines snapshot

ARC-AGI-2:
- Entry/team merger deadline: 2026-10-26 23:59 UTC.
- Final submission deadline: 2026-11-02 23:59 UTC.
- Winners announcement: 2026-12-04.

Paper Track:
- current live Kaggle UI and competition page show **2026-11-09 23:59 UTC**.

## M0 — PASS

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
- frozen split: **60 eval-development / 30 eval-validation / 30 eval-heldout**;
- seed/profile are recorded in the manifest;
- continuous iteration is allowed only on the 60-task development split.

### Public baseline landscape at 2026-08-24

Current Kaggle Code snapshot includes:
- `ARC2 vanilla exact`: **31.39** public score;
- `ARC 2026 NVARC TRM Evidence Cost V1`: **31.11**;
- `ARC 2026 NVARC TRM Aggressive Cost Order`: **31.11**;
- `BlackCat Stable Anchor — NVARC Guard`: current page around **26.81**, historical best **28.89 (V4)**.

These are third-party public scores unless explicitly labeled as our run.

### N1 — competitive Kaggle frontier

`ARC2 vanilla exact`

Reference URL: `https://www.kaggle.com/code/sorenravn/arc2-vanilla-exact`

Our clean copy:
- Version 1 executed successfully;
- runtime: **25m29s**;
- accelerator: **GPU L4 x4**;
- `submission.json` generated with 120 placeholder/public-evaluation tasks;
- Kaggle submission dialog correctly selected our notebook, Version 1 and `submission.json`;
- hidden competition rerun score is the remaining N1 evidence.

This validates the local notebook/model/output pipeline. N0 is now fallback only.

### S0 — compact symbolic baseline — REJECT as standalone

Measured on the frozen 60-task evaluation-development split:
- regression CI: **13/13 PASS** after the constant-output ranking correction;
- tasks: 60;
- test outputs: 82;
- pass@1: **0.0%**;
- pass@2: **0.0%**;
- fitted exact hypotheses: **0 across all 60 tasks**;
- runtime: **14.78 s** on GitHub Actions CPU.

Conclusion: shallow D4/crop/component/scale/color-map search is not a serious ARC-AGI-2 solver. Retain only as a lower-bound/regression instrument.

Experiment: `experiments/E0002_20260824_s0_symbolic_dev.md`.

### NVARC audit — key decision

NVARC 2025 shows that adding a solver with non-zero standalone accuracy may add **zero** final score when its correct candidates overlap the stronger solver or the final scorer fails to retain its unique candidates.

Published NVARC evidence includes:
- Qwen3 2B 21.53 -> 22.50 when TRM candidates were added;
- stronger Qwen3 4B 27.22 -> 27.22 with the same general ensemble idea;
- TRM unique solves existed, but Qwen rescoring did not always select them.

Therefore M1 measures two separate ceilings:
1. candidate discovery / oracle union;
2. actual two-attempt selection efficiency.

We will **not retrain TRM from scratch** in M1. N2, if run, will use a public checkpoint/notebook and must answer a complementarity question rather than reproduce old training compute.

Full audit: `docs/M1_NVARC_AUDIT.md`.

### Multi-solver portfolio instrumentation

Pairwise complementarity is already on `main`. The current M1 branch adds a multi-solver oracle portfolio analyzer that records:
- each solver's exact pass@2 coverage;
- outputs unique vs all other components;
- leave-one-out union loss;
- oracle union ceiling;
- deterministic greedy coverage order;
- optional exact additive-runtime portfolio under declared budgets.

This is measurement infrastructure, not a novel solver. It exists to prevent redundant components from consuming Kaggle time.

### Strong distinct reference — CompressARC C0

Preferred reference: `iliao2345/CompressARC`.

Public evidence:
- MIT-licensed source;
- no-pretraining, per-puzzle neural compression/MDL approach;
- published Kaggle-oriented execution path on L4 x4;
- materially different inductive bias from N1.

C0 remains bounded: obtain comparable evidence if clean; do not optimize it inside M1. If compatibility/evidence is not clean by 2026-09-02, mark C0 `PARTIAL` and advance.

Docs: `docs/M1_STRONG_SYMBOLIC_AUDIT.md` and `docs/M1_COMPRESSARC_REPRO.md`.

### Aggregate development profile

Using training demonstrations only (no test outputs):
- 39/60 tasks preserve input/output dimensions in every demonstration;
- 17/60 consistently shrink area; 1/60 consistently enlarges area;
- 52/60 always keep output colors within the input color set;
- 32/60 preserve the exact color set;
- 22/60 consistently remove colors;
- 7/60 consistently introduce colors.

The dominant gap is contextual/compositional transformation rather than basic geometry/color bookkeeping.

## Compute policy

- **GitHub Actions:** tests, profiling, exact scoring and lightweight CPU measurements.
- **Kaggle L4 x4:** neural baselines, C0/N2 bounded experiments, heavy hybrid runs and final-valid execution.
- **Ryzen 9:** currently **NOT NEEDED**. Activate only when a measured CPU-parallel workload can improve the prize path (large search, synthetic generation, profiling/ablation).

The final solver must fit Kaggle even if the Ryzen later accelerates research.

## Repository visibility decision

**Keep `pmartins87/ARC` PUBLIC through M1 measurement work.**

The current branch contains public-source audit and generic measurement infrastructure. Before the first genuinely original competitive mechanism, unpublished ablation advantage, or material proprietary improvement is committed, trigger the visibility review. The default at that point is private until the required open-source window.

## Immediate gates

### User-side

Only one item remains for now:
- when Kaggle returns the N1 competition result, send/record the hidden/public score screen.

No Ryzen work and no additional notebook run is required until the research-side evidence says it is worth the quota.

### Research-side

1. land NVARC audit + multi-solver portfolio instrumentation after green CI;
2. finish bounded C0 evidence path;
3. choose at most one N2 TRM/NVARC comparison if it adds information beyond N1;
4. ingest comparable per-task outputs and compute candidate oracle union / redundancy;
5. close M1 PASS or PARTIAL by 2026-09-02;
6. freeze the first evidence-based M2/M3 hypothesis and trigger repository-visibility review before original competitive code.

## Finite-project rule

A milestone that misses its gate is marked `PARTIAL`; the best working artifact is carried forward and the project advances. No phase can consume the whole schedule. No new architecture enters after the M6 freeze on 2026-10-23. ARC-AGI-2 R&D stops at the final code deadline; Paper Track work stops at the paper deadline; M9 is administration/outcome recording only.
