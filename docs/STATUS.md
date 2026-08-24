# ARC Prize 2026 — Project Status

Last updated: 2026-08-24

## Executive state

- **Current milestone:** M1 — Reproduce competitive baselines — **ACTIVE**.
- **Completed:** M0 — Foundation and rules freeze — **PASS**.
- **Current gate:** establish a reproducible score/runtime/complementarity table containing a competitive neural baseline and an independent symbolic baseline.
- **User-side experiment:** B0 — unchanged `BlackCat Stable Anchor — NVARC Guard` Kaggle reproduction.
- **Research-side experiment:** S0 — compact verified symbolic baseline — implementation complete; measured development benchmark pending/automated through GitHub Actions.
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

Initial local regression suite: **4/4 PASS** before M0 merge.

## M1 — ACTIVE

The benchmark hierarchy was corrected during the baseline audit:
- 1,000 training tasks are uncalibrated training/development material;
- 120 public evaluation tasks are the main public proxy for hidden ARC-AGI-2 generalization;
- operational evaluation split: 60 eval-development / 30 eval-validation / 30 eval-heldout;
- split generator is deterministic and records seed/profile.

Synthetic split regression checks produced exactly 60/30/30 and 700/150/150 for 120- and 1,000-ID inputs respectively.

### Public baseline landscape at 2026-08-24

Current Kaggle Code page shows:
- `ARC2 vanilla exact`: **31.39** public score;
- `ARC 2026 NVARC TRM Evidence Cost V1`: **31.11**;
- `ARC 2026 NVARC TRM Aggressive Cost Order`: **31.11**;
- `BlackCat Stable Anchor — NVARC Guard`: current page reports **26.81**, with **28.89** as its historical best (V4), runtime about 24m48s on L4 x4.

These are third-party public scores and are **not yet our reproduced results**.

### B0 — Kaggle pipeline anchor

Selected first user-side reproduction:

`BlackCat Stable Anchor — NVARC Guard`

Reason: direct public notebook, NVARC-derived, known L4 x4 runtime around 25 minutes, and sufficient to verify the complete account/notebook/model/submission pipeline before we reproduce the ~31% frontier.

First run policy: unchanged notebook. Record the exact notebook version used, because the current public version and historical best differ.

Detailed protocol: `docs/M1_BASELINE_AUDIT.md`.

### S0 — compact symbolic baseline

Implemented on `main`:
- whole-grid D4 transforms with exact demonstration verification and color remapping;
- non-background crop hypotheses;
- connected-component extraction under 4/8-connectivity and monochrome/all-foreground grouping;
- generic largest/smallest/top/bottom/left/right selectors;
- integer cell scaling;
- constant-output hypothesis;
- deterministic complexity ranking;
- two distinct predictions when verified hypotheses permit;
- regression tests;
- offline evaluator that strips test outputs before inference;
- GitHub Actions CI;
- GitHub Actions public-development benchmark using the official `arcprize/ARC-AGI-2` repository and the frozen 60/30/30 split.

S0 is intentionally a reference solver rather than the final architecture. Its key later metric is complementarity with neural/TRM errors, not standalone score alone.

Documentation: `docs/M1_SYMBOLIC_BASELINE.md`.

## Compute policy

- **GitHub Actions:** deterministic unit/regression tests and fast CPU symbolic development benchmark.
- **Ryzen 9:** later large CPU search, synthetic generation, profiling and ablations where local parallelism helps.
- **Kaggle L4 x4 / competition compute:** neural baselines, heavy hybrid runs and all final competition-valid executions.

The final solution must fit Kaggle limits even when the Ryzen 9 is used to discover or optimize it.

## Repository visibility decision

**Keep `pmartins87/ARC` PUBLIC through M1.**

This phase contains infrastructure, public baselines, reproduction methodology, and material whose competitive secrecy value is low. Public visibility is useful for CI/reproducibility.

Follower count does not protect a public repository from GitHub search/indexing.

**Privacy trigger:** before committing a genuinely original competitive mechanism, unpublished ablation result, or material improvement that we would not want copied, reassess visibility. The default at that trigger is to move private until the required open-source/writeup window.

## Immediate gates

### User-side
1. Run B0 unchanged on Kaggle.
2. Submit it to the competition.
3. Record/send exact notebook version, public score and runtime.

### Research-side
1. obtain/record S0 CI test status and development score/runtime;
2. reproduce one ~31.11–31.39 public frontier notebook after B0;
3. isolate TRM marginal contribution where feasible;
4. compare neural vs symbolic exact-solve overlap on public offline material;
5. close M1 with a baseline/error map;
6. decide repository visibility before the first novel competitive commit.

## Finite-project rule

A milestone that misses its gate is marked `PARTIAL`; the best working artifact is carried forward and the project advances. No phase can consume the whole schedule. No new architecture enters after the M6 freeze on 2026-10-23. ARC-AGI-2 R&D stops at the final code deadline; Paper Track work stops at the paper deadline; M9 is administration/outcome recording only.
