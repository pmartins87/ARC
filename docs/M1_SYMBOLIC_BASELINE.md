# M1 Symbolic Baseline S0

## Purpose

Provide a dependency-light, deterministic symbolic reference before any novel competition architecture is introduced.

S0 is a measurement instrument, not the intended final ARC Prize system.

## Implemented hypothesis families

1. Whole-grid D4 transforms (identity, rotations, flips, diagonal reflections) with verified color remapping.
2. Bounding-box crop of non-background content with D4 transform and color remapping.
3. Unique connected-component extraction using 4/8-connectivity, monochrome or all-foreground connectivity, six generic selectors, D4 transform, and color remapping.
4. Integer nearest-neighbor cell scaling after D4 transform.
5. Constant-output hypothesis when all demonstrations have the same output.

Every accepted hypothesis must reproduce every training demonstration exactly. No task-ID-specific rule exists.

## Attempt policy

Hypotheses are ranked by a fixed description-complexity prior. The first two distinct valid test predictions become `attempt_1` and `attempt_2`. If fewer than two verified hypotheses produce predictions, schema-safe deterministic fallbacks are used.

During CI, a regression exposed that the constant-output rule was ranked below two weaker fallbacks despite fitting all demonstrations. Its complexity prior was corrected and all 13 regression tests then passed. This ranking fix did not change the development benchmark conclusion below.

## Frozen development benchmark

GitHub Actions evaluated only the 60-task `evaluation/development` split from seed `arc-2026-v1`. Test outputs were stripped before inference. Validation and held-out were not used.

Result at commit `a0b31d0a7afbee3edbcc7b6c411bd99e5c0d0ce1`:

- tasks: 60;
- test outputs: 82;
- pass@1: **0.0%**;
- pass@2: **0.0%**;
- solved tasks: 0;
- fitted exact hypotheses: **0 across all 60 tasks**;
- runtime: **14.78 s** on GitHub Actions CPU.

Experiment record: `experiments/E0002_20260824_s0_symbolic_dev.md`.

## What the negative result tells us

The failure occurs before candidate ranking: the shallow DSL cannot exactly explain even the demonstrations of any development task. Therefore adding a cleverer top-2 policy to S0 cannot help yet.

An aggregate profiler of the training demonstrations (no test outputs) found:

- 39/60 tasks preserve dimensions across all demonstrations;
- 17/60 consistently shrink output area; 1/60 consistently enlarges it;
- 52/60 keep output colors within the input color set;
- 32/60 preserve the exact color set;
- 22/60 consistently remove colors;
- 7/60 consistently introduce colors.

This is compatible with ARC-AGI-2's emphasis on contextual rule application and compositional reasoning: many tasks preserve superficial grid/color statistics while requiring a more semantic transformation.

## M1 decision

**S0 is REJECTED as a serious standalone symbolic baseline/final solver.** It remains useful as a regression harness and a concrete lower bound.

We will not spend M1 enumerating random extra primitives until a few tasks happen to fit. A serious symbolic M1 reference must instead use a materially stronger published family (program synthesis / MDL / evolutionary search) or be explicitly marked `PARTIAL` when M1 closes.

Original solver invention belongs after the competitive neural baseline is reproduced and its error coverage is measured.
