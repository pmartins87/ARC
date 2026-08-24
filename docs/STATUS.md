# Status

Last updated: 2026-08-24

## Competition enrollment

User-side Kaggle screenshots show:
- ARC Prize 2026 — ARC-AGI-2 with **Submit Prediction** available;
- ARC Prize 2026 — Paper Track with **View Writeups** and the account message that no writeup has been created yet.

Working conclusion: both enrollments appear successful. Re-verify Kaggle account/identity/prize eligibility well before the entry deadline.

## Deadlines snapshot

ARC-AGI-2 official timeline:
- Entry/team merger deadline: 2026-10-26 23:59 UTC.
- Final submission deadline: 2026-11-02 23:59 UTC.
- Winners announcement: 2026-12-04.

Paper Track:
- Current live Kaggle UI and current Kaggle competition page both show **2026-11-09 23:59 UTC** (18:59 GMT-5).

## Competition mechanics frozen in M0

- Submission filename: `submission.json`.
- Exactly two predictions (`attempt_1`, `attempt_2`) per test output.
- Exact-grid match only.
- Score is averaged over test outputs.
- Kaggle notebook rerun; no internet.
- CPU/GPU notebook runtime <= 12h.
- L4x4 pool is available to this competition; 96 GB total GPU memory is advertised.
- Freely/publicly available external data and pretrained models are allowed under current Kaggle code requirements.
- Prize-eligible solutions must be open sourced.
- Grand Prize artifacts must be attached/open sourced within the competition writeup window.

## Repository state

### M0 foundation — PASS

PR #1 was squash-merged to `main`.

Implemented/documented:
- exact pass@2 scorer;
- grid/schema validation;
- identity smoke baseline;
- Python project/test scaffold;
- research/leakage protocol;
- gate-driven roadmap;
- state-of-the-art map;
- experiment ledger contract.

Initial local regression suite: **4/4 PASS** before M0 merge.

### M1 evaluation protocol — active

We corrected the benchmark hierarchy after the baseline audit:
- the 1,000 training tasks are uncalibrated and are primarily training/development material;
- the 120 public evaluation tasks are calibrated to the hidden evaluation distributions and are therefore our primary public generalization benchmark;
- the operational evaluation split is now 60 eval-development / 30 eval-validation / 30 eval-heldout;
- the split generator produces exact deterministic counts and carries a seed/profile in the manifest.

The split logic was checked against synthetic 120- and 1,000-ID sets, yielding exactly 60/30/30 and 700/150/150 respectively.

## Important competitive risk

The repository is currently **public**. ARC requires open sourcing for prize eligibility, but not immediate publication during active research. To avoid donating novel competitive work before submission, the preferred posture is:

1. keep the repository private during active competitive development;
2. preserve full commit history and reproducibility internally;
3. make required code/methods public for the prize/writeup window.

Until visibility is changed, do not commit a genuinely novel competitive mechanism in full detail.

## Current public baseline landscape

At the 2026-08-24 audit, Kaggle's public Code page shows public notebook scores in roughly the 29–31% range, including 31.39 for `ARC2 vanilla exact` and 31.11 for two NVARC/TRM variants. These are third-party reported scores and have not yet been reproduced by us.

## Active experiment: B0 pipeline anchor

Selected first reproduction target:

`BlackCat Stable Anchor — NVARC Guard`

Reason: public, directly copyable, NVARC-derived, L4x4 runtime around 25 minutes, and reported best public score 28.89. The first run must be unchanged so it establishes a clean account/notebook/model/submission baseline.

Detailed protocol: `docs/M1_BASELINE_AUDIT.md`.

## Next user-side action

1. Change repository visibility to **Private** before we begin committing novel competitive mechanisms.
2. On Kaggle, copy and run the B0 baseline unchanged, then submit it and record/send the resulting score and runtime.

## Next research-side action

After B0:
- reproduce one 31.11–31.39 public frontier notebook;
- isolate TRM marginal contribution;
- build/reproduce a symbolic baseline;
- compare solved-task overlap and runtime;
- only then freeze the first novel hybrid hypothesis.
