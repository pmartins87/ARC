# E0007 — Visible ARC-AGI-2 training → evaluation distribution shift

Status: **PASS — measured, leakage-safe public-data diagnostic**

```yaml
id: E0007
date: 2026-08-25
source_repo: arcprize/ARC-AGI-2
source_ref: GitHub Actions checkout at run time
workflow_run: 32813608759
workflow_artifact: visible-distribution-shift
artifact_sha256: e40aa075149dfe32897e41342b8d215db05189f117463e8348fdb858d8fdf284
method: visible structural distribution profile; test outputs never read
hardware: GitHub Actions ubuntu-latest CPU
status: PASS
```

## Question

Are public evaluation tasks structurally harder/larger than public training tasks in ways that should affect our evaluation discipline, prompt/runtime budgeting and synthetic-data assumptions?

## Leakage guard

The profiler reads only:
- training demonstration inputs and outputs;
- test **inputs**.

It deliberately ignores test outputs even though the public evaluation repository contains them. No solver score is computed here.

## Measured results

### Task / test-slot structure

| Metric | Training | Evaluation |
|---|---:|---:|
| Tasks | 1000 | 120 |
| Test input slots | 1076 | 167 |
| Tasks with >1 test input | 69 (6.9%) | 45 (37.5%) |
| Mean test inputs/task | 1.076 | 1.392 |
| Max test inputs/task | 4 | 3 |

The current official public evaluation checkout therefore has a **5.43x higher multi-test-task fraction** than training.

Important: this does **not** compound leaderboard scoring as `p^2`; the official Kaggle metric scores each test output independently. See `docs/M1_METRIC_SOURCE_OF_TRUTH.md`.

### Visible demonstration input complexity

| Metric | Training | Evaluation | Eval / Train |
|---|---:|---:|---:|
| Median demo input area | 100 | 299 | **2.99x** |
| P90 demo input area | 400 | 720 | 1.80x |
| Median demo input colors | 3 | 5 | 1.67x |
| P90 demo input colors | 6 | 8 | 1.33x |

### Test-input complexity

| Metric | Training | Evaluation | Eval / Train |
|---|---:|---:|---:|
| Median test input area | 144 | 484 | **3.36x** |
| P90 test input area | 570 | 900 | 1.58x |
| Mean test input area | 226.17 | 507.13 | 2.24x |
| Median test input colors | 4 | 6 | **1.50x** |
| P90 test input colors | 7 | 9 | 1.29x |

Public evaluation test inputs are therefore materially larger and more color-rich than public training test inputs.

### Demonstration output complexity

| Metric | Training | Evaluation |
|---|---:|---:|
| Median demo output area | 93 | 225 |
| P90 demo output area | 324 | 625 |
| Median demo output colors | 3 | 4 |
| P90 demo output colors | 6 | 7 |

## Relation to current community discussion

A current Kaggle post reported training/evaluation median visible-grid area around 100/299, median colors 3/5, and multi-test fractions 6.9%/40.8%.

Our independent current-checkout measurement reproduces the **100→299** demonstration-area and **3→5** demonstration-color medians exactly, but measures **37.5%**, not 40.8%, for current evaluation tasks with multiple test inputs. The difference is consistent with public dataset version drift already seen in E0005; it is another reason to pin provenance rather than copy forum numbers.

The same post's `p^2` scoring interpretation is incorrect relative to official Kaggle rules and is not adopted.

## Consequences

1. **Evaluation split remains the right tuning proxy.** Training-only headline scores are structurally optimistic and should not drive M2 decisions.
2. **Prompt/runtime budgets must be sized on evaluation-like grids.** Median test-input area is over 3x the training median, so tokenization/prefill and tool execution benchmarks on small training tasks can materially understate competition cost.
3. **Synthetic curricula need evaluation-like complexity.** A generator dominated by training-size grids risks learning the wrong compute/representation regime even if it produces many tasks.
4. **Model context pressure is real.** Larger grids + more colors + multiple test inputs increase serialized prompt size and candidate-generation cost; this strengthens the case for measuring Lightning throughput on evaluation-shaped prompts, not toy prompts alone after the initial load smoke.
5. **Do not change the official scoring objective.** Multi-test prevalence matters for output count/runtime, not as all-or-nothing task scoring.
6. **Audit frozen split balance before M2.** Because only 120 evaluation tasks exist, the random 60/30/30 split should be checked for size/color/multi-test balance before using validation/heldout gates.

## Artifacts

- `src/arcsolver/distribution_profile.py`
- `scripts/profile_visible_distribution_shift.py`
- `.github/workflows/distribution-shift-profile.yml`
- GitHub Actions artifact `visible-distribution-shift` from run `32813608759`
