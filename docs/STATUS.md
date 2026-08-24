# Status

Last updated: 2026-08-24

## Competition enrollment

User-side Kaggle screenshots show:
- ARC Prize 2026 — ARC-AGI-2 with **Submit Prediction** available;
- ARC Prize 2026 — Paper Track with **View Writeups** and the account message that no writeup has been created yet.

Working assumption: both enrollments succeeded. Re-verify Kaggle account verification/prize eligibility before the entry deadline.

## Deadlines snapshot

ARC-AGI-2 official timeline:
- Entry/team merger deadline: 2026-10-26 23:59 UTC.
- Final submission deadline: 2026-11-02 23:59 UTC.
- Winners announcement: 2026-12-04.

Paper Track:
- Current Kaggle UI observed on 2026-08-24 shows submissions due **2026-11-09 18:59 GMT-5** (23:59 UTC).
- Because public pages/cached sources have shown a different day in some places, re-check the live Kaggle UI near submission time.

## Competition mechanics frozen in M0

- Submission filename: `submission.json`.
- Exactly two predictions (`attempt_1`, `attempt_2`) per test output.
- Exact-grid match only.
- Score is averaged over task test outputs.
- Kaggle notebook rerun; no internet.
- CPU/GPU notebook runtime <= 12h.
- L4x4 pool is available to this competition; 96 GB total GPU memory is advertised.
- Freely/publicly available external data and pretrained models are allowed under current Kaggle code requirements.
- Prize-eligible solutions must be open sourced.

## Repository state

- Repository initialized.
- Branch `research/m0-foundation` created.
- Exact pass@2 scorer implemented.
- Grid/schema validation implemented.
- Deterministic initial split generator implemented.
- Local regression suite: **4/4 PASS** before commit.
- Research protocol drafted.
- Gate-driven roadmap drafted.
- State-of-the-art map started.

## Important competitive risk

The repository is currently **public**. ARC requires open sourcing for prize eligibility, but not necessarily immediate publication during active research. To avoid donating novel competitive work before submission, the preferred posture is:

1. keep the repository private during active competitive development;
2. preserve full commit history and reproducibility internally;
3. make the required code/methods public for the prize/writeup window.

Until visibility is changed, do not commit a genuinely novel competitive mechanism in full detail.

## Active gate: M0

Remaining before M0 PASS:

1. audit official 2026 rules/eligibility and account-verification requirements;
2. inventory reproducible 2025/2026 offline baselines;
3. select the first serious Kaggle baseline to reproduce;
4. define experiment ledger format;
5. verify branch contents via PR/CI-style review.

## Next technical target

**M1 baseline reproduction.** First serious target: a 2026-compatible NVARC-derived public Kaggle baseline, followed by a compact symbolic baseline and a TRM-family component. We will record score, runtime, hardware, and failure coverage before designing novel hybrids.
