# M1 Dataset / Submission Provenance Fingerprint

Snapshot: 2026-08-25
Status: evaluation-integrity infrastructure; no competitive solver logic.

## Why this became necessary

The N1 local smoke audit exposed a concrete provenance trap: a 120-task submission schema and the current 120-task official GitHub evaluation set shared the same task-ID universe but differed in the number of test outputs for five task IDs.

A check that verifies only “120 tasks” or even “same task IDs” is therefore insufficient. Two ARC datasets can look aligned while requiring a different number of predictions.

## New fingerprint

`src/arcsolver/provenance.py` records three independent levels of identity:

1. **task-ID identity**
   - sorted task IDs;
   - SHA-256 over the sorted ID list.

2. **submission-schema identity**
   - number of test outputs for every task;
   - total output slots;
   - SHA-256 over the task → test-count signature.

3. **full challenge-content identity**
   - canonical order-independent JSON SHA-256 over the challenge object.

This lets us distinguish:

- exactly the same challenge content;
- same submission schema but different inputs/training examples;
- same task IDs but changed test-output counts;
- missing/extra task IDs.

## Fail-closed comparison

`compare_fingerprints` reports:

- missing task IDs;
- extra task IDs;
- test-count mismatches with `(reference, candidate)` counts;
- total-output-slot mismatch;
- full canonical-content mismatch.

A dataset/submission pair is considered structurally compatible only when task IDs, total output slots and every per-task test count match.

The full content hash is stricter: it should match only when the challenge content itself is identical, not merely submission-compatible.

## Submission fingerprint

`submission_schema_fingerprint` ignores candidate grid values and fingerprints only:

- task IDs;
- number of output records per task.

This means we can verify a `submission.json` against a pinned challenge file before scoring or interpreting results, without contaminating provenance checks with model predictions.

## CLI

`scripts/fingerprint_arc_dataset.py`

supports:

- fingerprinting a challenge JSON;
- comparing a `submission.json` schema to it;
- comparing a second challenge file to the reference;
- writing a machine-readable JSON report.

## Required use from M2 onward

Every serious experiment should record, when available:

- exact challenge/input file fingerprint;
- submission schema fingerprint;
- source dataset/Kaggle bundle version metadata;
- model/checkpoint version;
- code commit/notebook version.

If a result is compared across datasets whose fingerprints differ, the difference must be intentional and explicitly documented.

## Paper value

This infrastructure does not improve ARC score directly. It protects scientific validity:

- prevents scores from being attributed to the wrong dataset version;
- prevents hidden schema drift from masquerading as model failure;
- supports exact reproduction of validation/heldout claims;
- makes negative results auditable instead of ambiguous.

The five-task mismatch discovered in E0004 is the motivating example and should remain in the final research log even if later Kaggle bundles eliminate the discrepancy.
