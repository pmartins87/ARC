# M1 CompressARC Reference / Reproduction Decision

Snapshot: 2026-08-24

## Reference implementation

- GitHub: `iliao2345/CompressARC` — MIT licensed.
- Public Kaggle template: `https://www.kaggle.com/code/iliao2345/arc-agi-without-pretraining`
- The Kaggle notebook itself is Apache-2.0 licensed.

CompressARC remains a useful methodological reference because it trains a fresh puzzle-specific model from scratch under a compression/MDL framing, which is materially different from the Qwen/NVARC lineage.

## Published execution evidence

The historical Kaggle template ran on L4 x4 in roughly 6m32s. Published ARC-AGI-2 semi-private runs were low-single-digit and variable (`1.67, 2.50, 1.67, 2.50, 4.17`). ARC Prize 2025 separately summarized the method at roughly 4% ARC-AGI-2.

Its raw score is far below the current ~31% public Qwen/NVARC-derived frontier, so C0 is relevant only if it supplies **unique exact candidates**.

## Provenance audit of the public prediction artifact

We tested whether the authors' public `predictions_evaluation.npz` could give us C0 task-level coverage without a new GPU run.

The shortcut is **REJECTED** for the current benchmark:

- current official ARC-AGI-2 public evaluation: **120 tasks**;
- task histories in the published CompressARC artifact source set: **400 tasks**;
- current official tasks present in that source: **6**;
- current official tasks missing: **114**.

Therefore the public artifact cannot be scored or treated as task-level evidence for the current ARC-AGI-2 120-task evaluation set. The strict provenance probe fails closed rather than silently reporting a misleading score.

Experiment: `experiments/E0003_20260824_compressarc_artifact_provenance.md`.

## M1 decision

C0 is now **PARTIAL as a current task-level baseline** and retained as a methodological reference.

We will not spend a user Kaggle run on the historical template merely to reproduce a ~1.7–4.2% score. A current C0 run becomes justified only if later portfolio evidence gives a concrete reason to believe the distinct MDL/no-pretraining candidate distribution can add enough unique exact outputs to offset the run and integration cost.

This is a finite-project stop rule, not a claim that CompressARC is scientifically unimportant.

## Later relevance

Potentially reusable ideas for M3–M5 remain:
- single-puzzle learning;
- MDL/simplicity pressure;
- inference-time candidate collection;
- puzzle-specific adaptation without external pretraining.

Any later use must be justified by controlled ablation against the competitive baseline and must fit the final Kaggle execution constraints.
