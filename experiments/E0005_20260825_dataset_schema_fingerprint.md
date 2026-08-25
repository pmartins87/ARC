# E0005 — N1 submission vs current official evaluation schema fingerprint

Status: **PASS (provenance mismatch reproduced exactly)**

```yaml
id: E0005
date: 2026-08-25
purpose: reproduce and fingerprint the dataset/submission schema mismatch discovered in E0004
n1_submission_sha256: ee0e21aa814c10b8b5751430b34b8e4d170ba7d2a0cfbf262c637b17d536d57c
official_source: arcprize/ARC-AGI-2 main, exported by GitHub Actions on 2026-08-24/25
official_export_artifact_sha256: f48c67ca78a92251c419804bfde7895d6ad6fec73479defb8d4b3aab2490be2d
status: PASS
```

## Structural fingerprints

### Current official GitHub evaluation challenges

```yaml
task_count: 120
output_slots: 167
task_ids_sha256: 5801e57e7883eb8b087df9d55e814dc7aee6eee332e29fd5ce083ad3b2a92659
test_count_signature_sha256: 2190a619ee3644c5a91a77c6f1d187ad0a2d1532969abd9e3d9a6361f4096870
canonical_challenges_sha256: 2858a6ca7691d38a4011405234feb2286b144881e50706e10cfcb20f6a2f1d02
```

### N1 Version 1 local `submission.json` schema

```yaml
task_count: 120
output_slots: 172
task_ids_sha256: 5801e57e7883eb8b087df9d55e814dc7aee6eee332e29fd5ce083ad3b2a92659
test_count_signature_sha256: 8675fec82665d4374c9c3e52d76eb05e3abe92144915c14cafcac9036458b77d
```

The task-ID hashes are identical, but the output-slot count and test-count-signature hashes differ. This proves that “same 120 task IDs” is not enough to establish a score-compatible dataset version.

## Exact per-task mismatches

Counts below are `(current official GitHub evaluation, N1 submission schema)`:

- `4a21e3da`: **(1, 2)**
- `abc82100`: **(1, 2)**
- `b6f77b65`: **(2, 3)**
- `f560132c`: **(1, 2)**
- `faa9f03d`: **(1, 2)**

All other shared task IDs have matching test-output counts.

## Interpretation

This is a dataset/provenance result, not a solver-quality result.

The current official GitHub evaluation export has **167** required output slots, while the local N1 Kaggle artifact has **172**. A blind scorer would either fail or, worse, tempt us to manually reconcile versions and create an invalid benchmark claim.

The project therefore adopts a fail-closed rule:

> no full N1 public score/error taxonomy is reported unless the challenge file and submission schema have compatible task/test-count fingerprints and the exact dataset version is recorded.

## Consequence

`src/arcsolver/provenance.py` and `scripts/fingerprint_arc_dataset.py` now make this check reusable for all later development/validation/heldout and Kaggle artifacts.

E0005 strengthens the Paper Prize's reproducibility/completeness record even though it contributes no leaderboard score.
