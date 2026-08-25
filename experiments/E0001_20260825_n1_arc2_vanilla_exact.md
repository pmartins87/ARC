# E0001 — N1 `ARC2 vanilla exact` Kaggle reproduction

Status: **PASS — competition rerun completed**

```yaml
id: E0001
date_started: 2026-08-24
date_completed: 2026-08-25
method: unchanged public Kaggle reproduction — ARC2 vanilla exact
source_url: https://www.kaggle.com/code/sorenravn/arc2-vanilla-exact
source_author: sorenravn
copied_notebook_version: 1
competition: ARC Prize 2026 - ARC-AGI-2
accelerator: L4 x4
internet: disabled in notebook environment
local_save_and_run_all_runtime: 25m29s
local_submission_json_sha256: ee0e21aa814c10b8b5751430b34b8e4d170ba7d2a0cfbf262c637b17d536d57c
public_reference_score_snapshot: 31.39
our_kaggle_public_score: 29.72
absolute_delta_pp_vs_reference: -1.67
submission_status: succeeded
status: PASS
```

## Result

Kaggle completed the competition rerun successfully and returned **Public Score 29.72** for our Version 1 reproduction.

The public source snapshot used when N1 was queued showed **31.39**, so our result is **1.67 percentage points lower**. This is a successful operational reproduction, not a byte-identical score reproduction. The acceptance rule for E0001 explicitly allowed a score difference pending provenance/runtime/randomness/container differences.

Do not treat 29.72 as a private-final score. It is the Kaggle **Public Score** produced after the competition reran the selected notebook version with its hidden competition input substitution. Final private ranking remains a separate end-of-competition quantity.

## Local execution evidence

Version 1 completed cleanly on L4 x4 in **25m29s** and produced `submission.json`. The local/non-rerun output was intentionally incomplete as a performance artifact: only 5 output slots across 4 tasks contained generated candidates and 167/172 slots were `[[0]]` placeholders. That exact smoke audit is recorded in `E0004_20260824_n1_local_smoke_audit.md`.

Therefore the local file must not be scored as though it were the full N1 system. The authoritative N1 leaderboard anchor for our project is now **29.72**.

## Interpretation

1. N1 is now our first end-to-end Kaggle-valid neural baseline.
2. The 1.67pp gap to the source snapshot is material enough to preserve as provenance evidence, but not useful enough to justify leaderboard-tuning or repeated reruns of the same public notebook.
3. The current live prize frontier is far above this regime, so M1 should now prioritize **step-change feasibility** rather than incremental tuning of N1.
4. The next high-information gate is E0006: bounded L4 x4 compatibility/throughput smoke for Nemotron 3.5 Lightning + the public NVIDIA NVARC environment.
5. No conclusion about candidate-generation vs selection vs coverage can be inferred from the single 29.72 aggregate score alone; use the prepared instrumentation on controlled public evaluation data.

## Decision

**KEEP as baseline anchor; STOP reproducing correlated ~30–32% public notebooks for score alone.**
