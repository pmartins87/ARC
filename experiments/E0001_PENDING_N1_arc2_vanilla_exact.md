# E0001 — N1 `ARC2 vanilla exact` Kaggle reproduction

Status: **HIDDEN COMPETITION RERUN IN PROGRESS**

```yaml
id: E0001
date: 2026-08-24
method: unchanged public Kaggle reproduction — ARC2 vanilla exact
source_url: https://www.kaggle.com/code/sorenravn/arc2-vanilla-exact
source_author: sorenravn
copied_notebook_version: 1
competition: ARC Prize 2026 - ARC-AGI-2
accelerator: L4 x4
internet: disabled in notebook environment
local_save_and_run_all_runtime: 25m29s
local_submission_json_sha256: ee0e21aa814c10b8b5751430b34b8e4d170ba7d2a0cfbf262c637b17d536d57c
public_reference_score: 31.39
our_hidden_rerun_score: PENDING
submission_status: accepted_for_private_rerun
status: PENDING_SCORE
```

## Local execution evidence

Version 1 completed cleanly on L4 x4 in **25m29s** and produced `submission.json`. The Kaggle submission dialog accepted Version 1 / `submission.json` and started the competition's private rerun.

The local/non-rerun output is intentionally incomplete as a performance artifact: only 5 output slots across 4 tasks contain generated candidates and 167/172 slots are `[[0]]` placeholders. The exact smoke audit is recorded separately in `E0004_20260824_n1_local_smoke_audit.md`.

Consequently, the local file must **not** be scored as though it were the full N1 system. The authoritative reproduction result is the Kaggle competition rerun score.

## Acceptance

`PASS` when the private competition rerun finishes and the returned score/version/runtime evidence is captured. A score different from the frozen public reference **31.39** does not automatically fail reproduction; first audit source version, attached input/model versions, randomness, competition rerun/container differences, and resource changes.

## Follow-up after PASS

1. freeze N1 as the first serious reproduced neural baseline;
2. compare its score to the public 31.39 reference and quantify reproduction delta;
3. use the source/pipeline audit plus bounded public-evaluation experiments for mechanism selection;
4. do not tune against leaderboard score alone.
