# E0003 — CompressARC public artifact provenance audit

Date: 2026-08-24
Milestone: M1
Status: **REJECT artifact shortcut / retain method as reference**

## Question

Can the public `iliao2345/CompressARC` `predictions_evaluation.npz` artifact be used to recover task-level exact coverage on the **current official ARC-AGI-2 120-task public evaluation set**, avoiding a new GPU run?

## Sources

- CompressARC pinned commit: `83a22218024d46273eb32b769a906340202ffb4d`
- Official ARC-AGI-2 repository checked by CI at commit `f3283f727488ad98fe575ea6a5ac981e4a188e49`
- Current official evaluation size: 120 tasks
- CompressARC published prediction artifact source challenge set: 400 tasks

## Result

The first unconstrained artifact probe correctly decoded the published hash history, but that result was **not accepted** because it measured the artifact's own 400-task source set rather than the current ARC-AGI-2 evaluation set.

A stricter provenance check then compared task IDs against the official ARC-AGI-2 evaluation directory.

Result:

- official ARC-AGI-2 evaluation tasks: **120**;
- official tasks present in the CompressARC artifact source: **6**;
- official tasks absent from the artifact source: **114**.

The strict probe therefore failed closed with:

`CompressARC artifact source is missing 114 official ARC-AGI-2 tasks`

This is the intended behavior of the provenance guard.

## Interpretation

The public prediction-history artifact cannot provide current ARC-AGI-2 task-level coverage. Any score recovered from all 400 artifact tasks answers a different benchmark question and must not be used as a 2026 ARC-AGI-2 score.

The CompressARC **method** remains scientifically relevant as a distinct no-pretraining / per-puzzle compression reference, but the zero-GPU artifact shortcut is rejected.

## Decision

1. Do not use the 400-task artifact score in M1 comparisons.
2. Do not spend a user Kaggle submission merely to reproduce the historical low-single-digit CompressARC score unless later evidence shows a plausible complementarity payoff.
3. Keep C0 as a methodological reference and mark direct current-ARC-AGI-2 task-level evidence **PARTIAL** unless a clean current run becomes strategically justified.
4. Preserve the provenance guard so future public artifacts cannot silently contaminate our comparison table.

## Compute impact

No Ryzen 9 and no Kaggle GPU were consumed by this audit. The invalid shortcut was detected in GitHub Actions before any additional user-side run.
