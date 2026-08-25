# M1 — ARC-AGI-2 metric source of truth

Snapshot: 2026-08-25

## Official rule

The ARC Prize 2026 Kaggle evaluation page is explicit:

- each **task test output** has one ground-truth grid;
- for that output, either `attempt_1` or `attempt_2` matching exactly scores 1;
- otherwise that output scores 0;
- the final score is the average over the **total number of task test outputs**.

Therefore a multi-test-input task does **not** require every output in the task to be correct before any credit is awarded. Each test output contributes independently to the competition score.

Official source:
- https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/overview/code-requirements

## Why this note exists

A current Kaggle discussion post correctly highlights several useful distribution cautions (the shipped test file is swapped at rerun; evaluation is harder/different from training) but also states that a task with two test inputs contributes only if both outputs are correct, giving a `p^2` argument.

That scoring statement conflicts with the official competition metric above and must **not** be used in our optimization or paper.

Discussion for provenance only:
- https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/discussion/733900

Community measurements from that post should be treated as hypotheses to reproduce independently before use. In particular, its training-vs-evaluation distribution observations may still be useful even though its scoring interpretation is wrong.

## Repository verification

Our scorer is already aligned with the official rule:
- `src/arcsolver/scoring.py` iterates each test output independently and credits it when either of the two attempts exactly matches;
- `tests/test_scoring.py::test_accuracy_is_per_test_output` explicitly checks a two-output task where one output is solved and one is missed, expecting score **1/2 = 0.5**.

No scoring-code correction is needed.

## Research consequence

For pass@2 optimization:
- allocate attempts at the **output** level;
- do not artificially couple success across multiple test inputs of the same task in the competition metric;
- task-level all-output solve rate may still be reported as a diagnostic of coherent rule induction, but it is a secondary scientific metric, not the leaderboard objective;
- candidate selection/complementarity analysis should retain output-level exact score as its primary competition metric.

## Paper consequence

Whenever task-level and output-level accuracy are both reported, label them distinctly. The Paper Track must not imply that the official leaderboard uses all-or-nothing task-level scoring.
