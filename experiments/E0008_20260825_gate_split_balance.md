# E0008 — Frozen evaluation gate balance / v2 adoption

Status: **PASS — v2 materially reduces visible structural skew without reading test outputs**

```yaml
id: E0008
date: 2026-08-25
parent_split: arc-2026-v1
candidate_split: arc-2026-gates-v2
development_tasks: 60 (preserved exactly)
validation_tasks: 30
heldout_tasks: 30
workflow_run: 32815554041
workflow_artifact: visible-distribution-shift
artifact_sha256: a4c6c460586b2de7b9efd471d59319a3f92f52bd3a72b184c46c887e0d08606a
v2_manifest_sha256: 0a03d5aba5670b779522b6f2bde55f165ba87c2f2a0f123dd0b969e9acbd2bc3
v1_balance_sha256: a7126e67e6efdc8d72e92b482517a9a05362e7221a884945c792f1644044724c
v2_balance_sha256: acab209c2b3cb857528fea664f3871077d67e4596a46c79a4988cf0c4b1520a8
status: PASS
```

## Why this experiment was necessary

The original deterministic hash split was reproducible but not structurally balanced. Before any validation/heldout scoring, E0007/E0008 measured a large visible-feature skew:

| Metric (dev / validation / heldout) | v1 |
|---|---|
| median test-input area | 484 / 642.5 / 285 |
| multi-test task fraction | 36.7% / 30.0% / 46.7% |
| median train-input area | 324 / 380.5 / 242 |
| median test-input colors | 6 / 7 / 7 |

The largest problem was validation-vs-heldout grid size. Validation's median test input was more than 2.25x heldout's, creating a strong risk that milestone gates would disagree because of split structure rather than method quality.

## v2 construction

Development is preserved exactly because it has already been used for S0 and diagnostics.

Only the **untouched** 60-task validation+heldout pool is reassigned. For each task, the rebalancer extracts:

- number of test inputs;
- median/max test-input area;
- median test-input color count;
- median training-input area;
- median training-input color count.

Test outputs are never read. Features are rank-normalized, structurally nearest tasks are paired, and exactly one member of each pair is assigned to validation and one to heldout using a deterministic seed. This yields 30/30 gates.

## Measured result

| Metric (dev / validation / heldout) | v1 | v2 |
|---|---|---|
| median test-input area | 484 / 642.5 / 285 | **484 / 473.5 / 484** |
| max/min ratio, median test area | 2.254 | **1.022** |
| multi-test task fraction | 36.7 / 30.0 / 46.7% | **36.7 / 36.7 / 40.0%** |
| max/min ratio, multi-test fraction | 1.556 | **1.091** |
| median train-input area | 324 / 380.5 / 242 | **324 / 261 / 300** |
| max/min ratio, train-input area | 1.572 | **1.241** |
| median test-input colors | 6 / 7 / 7 | 6 / 6.5 / 7 |
| P90 test-input area | 900 / 900 / 900 | 900 / 900 / 900 |
| test output slots | 82 / 40 / 45 | **82 / 42 / 43** |

The improvement is large enough to adopt v2 for future validation/heldout gates.

## Protocol decision

**ADOPT `experiments/evaluation_split_v2.json` for all future Level C/D gates.**

This is a one-time pre-gate correction, not a result-driven resplit:

- no validation score has been used for architecture selection;
- no heldout score has been opened;
- no test output was used to create or choose v2;
- development remains unchanged, preserving all M1 history;
- v1 remains archived as provenance and should not be reused for confirmatory claims.

After this adoption, v2 is immutable. Any future change requires a new protocol version and explicit invalidation of confirmatory claims made on prior gates.

## Artifacts

- `src/arcsolver/gate_split.py`
- `scripts/make_gate_split_v2.py`
- `scripts/profile_eval_split_balance.py`
- `experiments/evaluation_split_v2.json`
