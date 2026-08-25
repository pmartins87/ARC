# M1 Diagnostic Candidate-Dump Plan

Snapshot: 2026-08-25
Status: prepared protocol only; no user run is requested while N1 hidden rerun is active.

## Goal

Obtain one source-pinned public-evaluation candidate artifact that lets us separate:

- model/adaptation failure;
- candidate-generation failure;
- top-two selection failure;
- timeout / scheduling coverage loss.

A plain leaderboard score cannot answer these questions.

## Public lineage evidence

The pinned Qwen/NVARC-lineage mirror

`MA-Zbida/arc2026-kaggle@4a3d6f33816807eacb7ea49846fadbca042abd69`

already writes per-output inference artifacts under `/kaggle/inference_outputs`. Each sample retains:

- `solution`;
- `beam_score`;
- `score_aug`.

The decoder later aggregates those artifacts into the two submitted guesses.

The same mirror deliberately restricts ordinary/non-rerun evaluation to four task IDs, while competition rerun mode processes the hidden test queue. Therefore simply downloading the normal notebook output cannot provide a full public candidate audit.

## Desired diagnostic artifact

For a bounded public/frozen run, preserve:

1. exact competition dataset bundle/version identifiers;
2. exact notebook/source commit or Kaggle script version;
3. model/checkpoint and utility-script versions;
4. list of task/output keys scheduled;
5. compressed candidate records for every processed output;
6. task/output keys not processed or timed out;
7. final `submission.json` generated from the same candidate pool;
8. wall-clock runtime and accelerator.

Solutions must be used only by the offline evaluator after inference; they must not influence candidate generation.

## First diagnostic scope

Default scope is the frozen **60-task evaluation-development** slice, not all 120 tasks. This gives enough error diversity for M1/M2 diagnosis while preserving the 30 validation and 30 heldout tasks as gates.

If runtime is too high for the 60-task slice, reduce by a predeclared deterministic subset rather than selecting tasks after seeing errors.

## Required outputs from the audit

Using `src/arcsolver/candidate_pool.py` and `scripts/audit_candidate_dump.py`, record:

- processed/missing outputs;
- candidate-pool oracle pass@2;
- final public-selector pass@2;
- oracle-selector gap;
- truth-present-but-not-top2 count;
- correct candidate rank median/p90;
- raw/unique candidate counts;
- duplicate generation rate;
- selector disagreement and unique rescues;
- runtime/coverage statistics where present.

Cross this with structural error taxonomy and portfolio complementarity only after exact dataset provenance is verified.

## Decision tree

### Large oracle-selector gap

Interpretation: candidate generation often finds the truth but selection wastes it. M2 should prioritize a selector/diversity hypothesis before expensive backbone changes.

### Small oracle-selector gap but low oracle coverage

Interpretation: top-two selection is not the main bottleneck; the exact answer rarely reaches the pool. M2 should focus on adaptation/search/refinement/candidate discovery.

### High missing-output / timeout rate

Interpretation: scheduling/coverage is a material competition bottleneck. First separate a runtime allocation improvement from a reasoning improvement.

### Mixed failure profile

Choose the mechanism with the highest expected exact-score gain per unit of Kaggle runtime and require a causal intermediate metric.

## Run trigger

Do **not** ask the user to run this while N1 hidden rerun is active.

After N1 finishes, perform the diagnostic only if one of these is true:

- a public compatible full candidate dump cannot be recovered elsewhere;
- M1 still cannot distinguish discovery from selection from existing evidence;
- the run can be configured as a diagnostic notebook version without consuming scarce competition submission quota unnecessarily.

The diagnostic does not need to be submitted to the competition unless submission itself is required to test the hypothesis.

## Stop rule

This protocol gets one bounded reproduction attempt. If the exact N1 lineage cannot be made to expose comparable frozen candidate artifacts cleanly within M1, mark candidate-level N1 evidence **PARTIAL** and advance. Do not let diagnostic perfection consume September.
