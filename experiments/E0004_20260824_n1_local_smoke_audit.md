# E0004 — N1 local smoke-output audit

Status: **PASS (scope-limited smoke evidence)**

```yaml
id: E0004
date: 2026-08-24
method: audit of the local/non-rerun output from N1 ARC2 vanilla exact Version 1
submission_sha256: ee0e21aa814c10b8b5751430b34b8e4d170ba7d2a0cfbf262c637b17d536d57c
submission_bytes: 23253
notebook_runtime: 25m29s
accelerator: L4 x4
notebook_version: 1
competition_hidden_rerun: PENDING
status: PASS_SCOPE_LIMITED
```

## What the local file actually contains

The saved `submission.json` has:
- 120 task IDs;
- 172 output slots;
- **167/172 slots are the `[[0]]` placeholder in both attempts**;
- only **5 output slots across 4 tasks** contain real generated candidates: `0934a4d8`, `36a08778` (2 outputs), `981571dc`, and `aa4ec2a5`.

Therefore this file is a **smoke/non-rerun artifact**, not a full 120-task evaluation of the N1 method. It must not be interpreted as a ~2–3% baseline or used to estimate the hidden competition score.

## Why only those four tasks were generated

A later source audit found a highly specific explanation in the pinned public 2026 Qwen/NVARC-lineage mirror:

`MA-Zbida/arc2026-kaggle@4a3d6f33816807eacb7ea49846fadbca042abd69`

Its notebook contains an explicit non-rerun guard:

- when `rerun_mode` is false, the work queue keeps only `0934a4d8`, `36a08778`, `981571dc`, and `aa4ec2a5`;
- when `rerun_mode` is true, it loads the competition `arc-agi_test_challenges.json` and does **not** apply that four-task filter;
- the notebook writes all decoded candidates under `/kaggle/inference_outputs`, then builds `submission.json` from whatever was processed.

Those are **exactly the same four task IDs** that contain generated candidates in our N1 local artifact. This is strong lineage evidence that the 25m29s local save is deliberately a four-task smoke path, while the Kaggle competition rerun activates the long full hidden path.

Caveat: the pinned mirror is not claimed to be byte-identical to Søren Ravn Andersen's N1 source. The exact task-ID match plus the matching Qwen/TTT/DFS architecture makes this explanation strongly supported, but the claim is kept at lineage level.

This also explains why the competition submission can remain `Notebook Running` for many hours even though the saved local version took only ~25 minutes: the two executions take different code paths and workloads.

## Exact results on the five generated outputs

Against the matching current official ARC-AGI-2 public tasks:
- pass@1: **3/5 = 60%**;
- pass@2: **4/5 = 80%**;
- second-attempt rescues: **1/5** (`36a08778`, output 1);
- duplicate generated attempts: **0/5**.

Per generated output:
- `0934a4d8[0]`: both attempts wrong; both have the correct 9x3 shape; each differs from truth in 8/27 cells (70.37% pixel agreement, still zero ARC exact credit).
- `36a08778[0]`: attempt 1 exact; attempt 2 differs in 8/256 cells.
- `36a08778[1]`: attempt 1 differs in 47/900 cells; attempt 2 exact — direct evidence that pass@2 diversity matters.
- `981571dc[0]`: attempt 1 exact; attempt 2 is the placeholder.
- `aa4ec2a5[0]`: attempt 1 exact; attempt 2 differs in 93/702 cells.

## Provenance caveat discovered

The current official `arcprize/ARC-AGI-2` evaluation directory has the same 120 task IDs, but its number of test pairs differs from the Kaggle submission schema for five tasks:
- `4a21e3da`: submission 2 vs current official 1;
- `abc82100`: 2 vs 1;
- `faa9f03d`: 2 vs 1;
- `b6f77b65`: 3 vs 2;
- `f560132c`: 2 vs 1.

Those five tasks are placeholders in this smoke file, so the generated-candidate results above remain valid. However, a full 120-task exact audit must pin the Kaggle competition dataset version rather than silently substitute the current GitHub task directory.

## Decision

1. Keep N1 competition rerun as **PENDING** until Kaggle returns its score.
2. Do not infer N1 full-set error taxonomy from this local file.
3. Preserve the strongest smoke lesson: a structurally different second attempt produced one of four exact generated-output wins.
4. Do not spend another Kaggle run merely to reproduce the smoke result.
5. Any later public-evaluation ablation must explicitly run enough frozen evaluation tasks to produce non-placeholder candidates and must record the exact Kaggle dataset version.
6. Treat the long hidden rerun as the expected full-path workload rather than comparing its duration directly to the 25m29s smoke save.
