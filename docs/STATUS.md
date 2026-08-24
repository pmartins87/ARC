# ARC Prize 2026 — Project Status

Last updated: 2026-08-24

## Executive state

- **Current milestone:** M1 — Reproduce competitive baselines — **ACTIVE**.
- **Completed:** M0 — Foundation and rules freeze — **PASS**.
- **Merged M1 evidence:** PR #3 — S0 symbolic measurement / stop-rule — **PASS and merged**.
- **Current gate:** reproduce a competitive neural frontier baseline and obtain a bounded strong symbolic/MDL reference; then build an error/complementarity map.
- **Next user-side run:** N1 — unchanged `ARC2 vanilla exact` — **PENDING USER RUN**.
- **Fallback user-side run:** N0 — `BlackCat Stable Anchor — NVARC Guard` — only if N1 fails to establish the Kaggle pipeline.
- **Research-side symbolic reference:** CompressARC C0 — **SELECTED / bounded reproduction plan prepared**.
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
- current live Kaggle UI and competition page show **2026-11-09 23:59 UTC**.

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
- frozen split: **60 eval-development / 30 eval-validation / 30 eval-heldout**;
- seed/profile are recorded in the manifest;
- continuous iteration is allowed only on the 60-task development split.

### Public baseline landscape at 2026-08-24

Current Kaggle Code page shows:
- `ARC2 vanilla exact`: **31.39** public score;
- `ARC 2026 NVARC TRM Evidence Cost V1`: **31.11**;
- `ARC 2026 NVARC TRM Aggressive Cost Order`: **31.11**;
- `BlackCat Stable Anchor — NVARC Guard`: current page around **26.81**, historical best **28.89 (V4)**, runtime about 24m48s on L4 x4.

These are third-party public scores and are not yet our reproduced results.

### N1 — competitive Kaggle frontier — FIRST USER RUN

`ARC2 vanilla exact`

URL: `https://www.kaggle.com/code/sorenravn/arc2-vanilla-exact`

Decision: **run N1 directly instead of spending the first run on the weaker BlackCat anchor.** A successful unchanged N1 run validates the same account/notebook/model/submission pipeline and simultaneously establishes our strongest public baseline. This removes one redundant user-side run from the finite project.

Protocol: `docs/M1_KAGGLE_RUN_QUEUE.md`.

### N0 — BlackCat — FALLBACK ONLY

Retain the previously selected BlackCat notebook as a simpler recovery anchor if N1 fails for environment/input reasons. Skip N0 entirely if N1 submits successfully.

### S0 — compact symbolic baseline — REJECT as standalone

PR #3 was squash-merged after green CI/benchmark checks.

Measured result on the frozen 60-task evaluation-development split:
- regression CI: **13/13 PASS** after fixing the constant-output ranking bug;
- tasks: 60;
- test outputs: 82;
- pass@1: **0.0%**;
- pass@2: **0.0%**;
- fitted exact hypotheses: **0 across all 60 tasks**;
- runtime: **14.78 s** on GitHub Actions CPU.

Conclusion: shallow D4/crop/component/scale/color-map search is not a serious ARC-AGI-2 evaluation solver. S0 remains only as a lower-bound/regression instrument.

Experiment: `experiments/E0002_20260824_s0_symbolic_dev.md`.

### Strong symbolic/MDL reference — CompressARC selected

Preferred reference: `iliao2345/CompressARC`.

Public evidence:
- GitHub code: MIT license;
- Kaggle template: Apache-2.0;
- template runtime shown as **6m32s on L4 x4**;
- authors explicitly intended the template for ARC-AGI-2 benchmarking;
- five reported successful semi-private ARC-AGI-2 runs: **1.67, 2.50, 1.67, 2.50, 4.17**.

C0 will attempt a bounded 2026 compatibility reproduction. It cannot block M1; if adaptation is not clean by 2026-09-02, mark C0 `PARTIAL` and advance.

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

- **GitHub Actions:** deterministic tests, aggregate profiling and fast CPU symbolic development measurements.
- **Ryzen 9:** later large CPU search, synthetic generation, profiling and ablations where local parallelism materially helps.
- **Kaggle L4 x4:** neural baselines, CompressARC-style GPU work, heavy hybrid runs and all final competition-valid executions.

The final solution must fit Kaggle limits even when the Ryzen 9 helps discover it.

## Repository visibility decision

**Keep `pmartins87/ARC` PUBLIC through M1.**

M1 contains infrastructure, public baseline reproduction and diagnostic work whose secrecy value is low. Reassess before the first genuinely original competitive mechanism or unpublished material improvement is committed.

## Immediate gates

### User-side
1. Copy/run/submit N1 (`ARC2 vanilla exact`) unchanged.
2. Send the exact source/copied version, public score and runtime/status; a screenshot is sufficient.
3. Run N0 only if N1 fails to establish a valid submission.

### Research-side
1. finalize the N1 comparison/experiment record template while the user run is pending;
2. bound C0 CompressARC compatibility work rather than optimizing it;
3. audit N1/NVARC resources after the reproduced run;
4. after N1, choose one controlled TRM/NVARC comparison rather than accumulating redundant public notebooks;
5. close M1 with a baseline/error map and freeze the first evidence-based research hypothesis.

## Finite-project rule

A milestone that misses its gate is marked `PARTIAL`; the best working artifact is carried forward and the project advances. No phase can consume the whole schedule. No new architecture enters after the M6 freeze on 2026-10-23. ARC-AGI-2 R&D stops at the final code deadline; Paper Track work stops at the paper deadline; M9 is administration/outcome recording only.
