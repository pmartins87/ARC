# M1 Symbolic Baseline S0

## Purpose

Provide a dependency-light, fully deterministic symbolic reference solver before any novel competition architecture is introduced.

S0 is intentionally compact. It is a measurement instrument, not the intended final ARC Prize system.

## Current hypothesis families

1. Whole-grid D4 transforms (identity, rotations, flips, diagonal reflections) with verified color remapping.
2. Bounding-box crop of non-background content with D4 transform and color remapping.
3. Unique connected-component extraction using 4/8-connectivity, monochrome or all-foreground connectivity, six generic selectors, D4 transform, and color remapping.
4. Integer nearest-neighbor cell scaling after D4 transform.
5. Constant-output hypothesis when all demonstrations have the same output.

Every accepted hypothesis must reproduce every training demonstration exactly. No task-ID-specific rule exists.

## Attempt policy

Hypotheses are ranked by a fixed description-complexity prior. The first two *distinct* valid test predictions become `attempt_1` and `attempt_2`. If fewer than two verified hypotheses produce predictions, schema-safe deterministic fallbacks are used.

This is not yet the M3/M4 diversity mechanism. S0 only establishes an auditable pass@1/pass@2 reference.

## Evaluation discipline

CI may repeatedly evaluate only the 60-task `evaluation/development` split. Validation and held-out evaluation are milestone gates and must not become continuous tuning signals.

The GitHub Actions benchmark:

- clones the official `arcprize/ARC-AGI-2` repository;
- creates the frozen `arc-2026-v1` 60/30/30 split;
- hides test outputs before inference;
- runs S0 only on development;
- reports exact pass@1, pass@2, test-output count and runtime;
- stores the split manifest and JSON report as artifacts.

## M1 acceptance use

S0 satisfies the requirement for a reproducible compact symbolic baseline once its development score/runtime is captured and its tests pass. Its value later will be measured primarily by error complementarity against neural/TRM baselines, not by standalone score alone.
