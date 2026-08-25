# M1 Runtime / Coverage Audit

Snapshot: 2026-08-25
Status: public-source scheduling analysis; no original competitive mechanism is disclosed here.

## Why runtime is part of accuracy

ARC scoring gives zero exact credit to an output that is never produced. In a competition notebook with a hard global wall-clock limit, reasoning quality and task coverage are therefore coupled:

> overall score = exact solves that survive both reasoning **and** runtime coverage.

A faster implementation can increase leaderboard score even if it solves no individual processed task more intelligently, simply by reaching more tasks before the deadline. That is a legitimate competition gain, but it must be labeled as a coverage/scheduling gain rather than a reasoning breakthrough in the Paper Prize.

## Public Qwen/NVARC lineage facts

Pinned source:

`MA-Zbida/arc2026-kaggle@4a3d6f33816807eacb7ea49846fadbca042abd69`

The public notebook/source shows:

- a global end time initialized to `12 * 3600 - 600` seconds after start, i.e. **11h50m** of nominal working budget before the Kaggle 12h ceiling;
- four GPU worker processes (`mp.spawn(..., nprocs=4)`), matching L4 x4;
- a shared task queue;
- fresh puzzle-specific LoRA state restoration and task-time training per puzzle;
- augmented candidate decoding and rescoring after adaptation;
- recursive DFS search with an internal wall-clock condition;
- a normal/non-rerun path restricted to exactly four public tasks;
- a competition-rerun path that loads the hidden test challenges and does not apply that four-task smoke filter.

This makes long competition-rerun duration expected by design. The 25m29s local N1 save and the multi-hour private rerun are not comparable workloads.

## N1 patch intent

The `ARC2 vanilla exact` notebook description visible in the public/source lineage emphasizes a minimal performance patch in the logits hot paths while preserving the baseline's task-time training, augmentation, decoding thresholds, candidate aggregation and submission schema.

That is important scientifically: a score increase caused by reducing CPU↔GPU transfer / redundant KV-cache work may be primarily a **coverage gain**. We should measure it separately from candidate quality.

## New runtime model

`src/arcsolver/runtime_budget.py` adds a deterministic coarse scheduler for later measured per-task timings.

It models:

- FIFO tasks;
- homogeneous workers;
- a global budget;
- tasks completed before the deadline;
- tasks started but cut off by the deadline;
- tasks never started;
- worker busy time / utilization;
- uniform speedup needed to complete a fixed queue.

It also distinguishes two speedup quantities:

1. **aggregate capacity lower bound** — total work divided by total worker-seconds, plus the longest-task constraint;
2. **actual FIFO speedup for the observed order** — can be larger because queue ordering/load imbalance wastes capacity.

This distinction matters when four GPUs independently pull tasks from a shared queue.

## Coverage ceiling

If only a fraction `c` of required outputs can be fully processed, the pure scheduling ceiling is at most `c` even with a perfect solver on processed outputs.

If a measured solver has exact rate `p` on the processed subset, `c × p` is a simple decomposition estimate for that exact workload. It is **not** a hidden-score forecast because task difficulty and runtime can be correlated.

The project tooling deliberately labels this as a coverage decomposition, not a generalization model.

## What timing data we need

For a future frozen diagnostic run, preserve per task/output where feasible:

- queue start time;
- task start/end time;
- training duration;
- candidate-generation duration;
- rescoring/selection duration;
- timeout/cutoff state;
- whether any valid candidates were committed;
- task order / worker ID.

With those observations we can answer questions such as:

- how many tasks are lost to the global deadline;
- whether runtime has a heavy tail;
- how much uniform speedup would materially increase coverage;
- whether changing queue order matters independently of reasoning;
- whether a candidate-quality improvement consumes so much runtime that overall exact score falls.

## Competition vs paper interpretation

### Competition engineering

Coverage gains count. If a mechanically equivalent solver reaches more tasks and scores higher, keep the improvement if it is robust and competition-valid.

### Paper claim

Do not present a coverage-only improvement as evidence of better abstract reasoning. Report:

- same-task accuracy where possible;
- processed-task count;
- runtime;
- timeout rate;
- overall score separately.

A scientifically stronger result would improve candidate/selection accuracy under a comparable compute budget, or demonstrate a principled runtime-allocation policy with causal controls.

## Current decision

While N1 private rerun is running:

- do not launch another Kaggle submission;
- do not use Ryzen 9;
- prepare timing/coverage instrumentation and source analysis;
- wait for the N1 result before deciding whether runtime coverage is the first measured M2 bottleneck.

The runtime model is infrastructure, not a proposed novel solution.
