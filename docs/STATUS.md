# ARC Prize 2026 — Project Status

Last updated: 2026-08-24

## Executive state

- **Current milestone:** M1 — Reproduce competitive baselines — **ACTIVE**.
- **Completed:** M0 — Foundation and rules freeze — **PASS**.
- **Current gate:** reproduce the 2026 public baseline frontier and establish a score/runtime/complementarity table containing at least one serious neural and one symbolic baseline.
- **Current experiment:** B0 — unchanged `BlackCat Stable Anchor — NVARC Guard` reproduction.
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

Kaggle's public Code page showed public notebook scores roughly in the 29–31% range, including 31.39 for `ARC2 vanilla exact` and 31.11 for NVARC/TRM variants. These are third-party public scores and are **not yet our reproduced results**.

### B0 — pipeline anchor

Selected first reproduction:

`BlackCat Stable Anchor — NVARC Guard`

Reason: public, directly copyable, NVARC-derived, L4x4 runtime reported around 25 minutes, and reported best public score 28.89.

First run policy: unchanged notebook. We want a clean account/notebook/model/submission anchor before changing any mechanism.

Detailed protocol: `docs/M1_BASELINE_AUDIT.md`.

## Repository visibility decision

**Keep `pmartins87/ARC` PUBLIC through M1.**

This phase contains infrastructure, public baselines, reproduction methodology, and other material whose competitive secrecy value is low. Public visibility is useful for CI/reproducibility.

Important qualification: follower count does not protect a public repository from GitHub search/indexing.

**Privacy trigger:** before committing a genuinely original competitive mechanism, unpublished ablation result, or material improvement that we would not want copied, reassess visibility. The default at that trigger is to move private until the required open-source/writeup window.

This means there is no need to change visibility now.

## Immediate actions

### User-side
1. Run B0 unchanged on Kaggle using the required accelerator/settings.
2. Submit it to the competition.
3. Record/send public score and runtime.

### Research-side after B0
1. reproduce one ~31.11–31.39 public frontier notebook;
2. isolate TRM marginal contribution where possible;
3. establish/reproduce a symbolic baseline;
4. compare exact-solve overlap and runtime;
5. close M1 with a baseline/error map;
6. decide repository visibility before the first novel M2/M3 commit.

## Finite-project rule

A milestone that misses its gate is marked `PARTIAL`; the best working artifact is carried forward and the project advances. No phase can consume the whole schedule. No new architecture enters after the M6 freeze on 2026-10-23. ARC-AGI-2 R&D stops at the final code deadline; Paper Track work stops at the paper deadline; M9 is administration/outcome recording only.
