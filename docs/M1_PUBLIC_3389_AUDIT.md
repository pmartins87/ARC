# M1 — Public 33.89 notebook audit

Snapshot: 2026-08-26
Status: **INSPECT-ONLY CANDIDATE / NO LEADERBOARD RUN AUTHORIZED**

## Object

Public Kaggle notebook:

`Failed in AIMO`

Author: Koushik Rudra (+1 collaborator shown by Kaggle)

URL:
`https://www.kaggle.com/code/koushikrudra/failed-in-aimo`

## Verified public evidence

Kaggle currently reports:

- competition: **ARC Prize 2026 — ARC-AGI-2**;
- Public Score: **33.89**;
- Best Score: **33.89, Version 1**;
- runtime: **26m11s**;
- accelerator: **GPU L4 x4**;
- language: Python;
- license: **Apache 2.0**;
- inputs: **3 files**;
- outputs: **44 files**;
- run status: successful.

This supersedes 31.81 as the strongest public-code Kaggle score currently verified by this project. It does **not** change the live prize frontier, which remains a separate ~70%+ regime in our latest evidence.

## Related public clone evidence

A public clone titled `Failed in AIMO on Docker-v169-v03` exposes these inputs:

- model: `qwen3_4b_bfloat16-v02-01-01`;
- dataset/dependency: `flash-attn-2.8.2`;
- notebook dependency: `unsloth-2025.9.7-torch-2.8.0-py3.12-patched`.

That clone reports **29.86** and **22m44s** on L4 x4. This is evidence that at least one public derivative belongs to the Qwen/NVARC-style family, but it is **not enough to prove** which exact mechanisms account for the original 33.89 result.

## Why this is more valuable than another score-only baseline

The key feature is not the +2.08pp relative to the previous 31.81 public best. The key feature is the **44 output files** from a successful, short L4 x4 run.

If those outputs include candidate dumps, per-task traces, selector evidence, runtime/coverage logs, or intermediate predictions, they could answer M1 questions that a leaderboard number cannot:

1. Is exact-answer loss dominated by candidate discovery or candidate selection?
2. How many unique candidates survive per test output?
3. How much of pass@2 comes from second-attempt rescues?
4. Does a better public run obtain its gain by processing more tasks within the budget?
5. Is its candidate source complementary to N1, or merely a stronger tuning of the same family?

## Decision

**Do not submit a copy to the competition merely to reproduce 33.89.**

Priority order:

1. inspect/download public notebook artifacts without running the competition notebook if Kaggle exposes them directly;
2. classify the 44 outputs by file name/type/size;
3. if a trusted candidate dump is available, run the existing `scripts/audit_candidate_dump.py` instrumentation offline;
4. compare architecture/configuration provenance with N1;
5. authorize a Kaggle reproduction only if a specific unresolved high-information question still requires execution.

A score-only reproduction is low information because 33.89 remains far below the live prize frontier.

## Evidence we do not yet have

Do not infer any of the following until artifacts/source inspection establishes them:

- exact candidate count or selector used by the 33.89 version;
- exact reason for the +4.17pp versus our N1 score;
- complementarity at task level;
- whether its 44 outputs contain candidate pools rather than ordinary logs/checkpoints;
- whether the public clone faithfully preserves the original 33.89 configuration.

## M1 consequence

This notebook becomes **P33**: a public artifact-audit candidate, not a leaderboard candidate.

P33 can satisfy part of M1 evidence buckets B/C/D if its outputs expose task-level/candidate-level telemetry. E0006 remains the next user-side GPU feasibility gate because it tests a materially different ARC-post-trained open-weight route rather than another correlated score-only Qwen baseline.
