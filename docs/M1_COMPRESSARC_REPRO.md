# M1 CompressARC Reproduction Plan

Snapshot: 2026-08-24

## Reference implementation

- GitHub: `iliao2345/CompressARC` — MIT licensed.
- Public Kaggle template: `https://www.kaggle.com/code/iliao2345/arc-agi-without-pretraining`
- The Kaggle notebook itself is Apache-2.0 licensed.

The authors explicitly describe the notebook as a template for benchmarking the ARC-AGI Without Pretraining method on ARC-AGI-2.

## Published execution evidence

Kaggle currently exposes version 10 of 11 with:
- runtime: **6m32s**;
- accelerator: **L4 x4**;
- competition input: ARC Prize 2025;
- additional dataset: CompressARC.

The authors report five successful ARC-AGI-2 semi-private runs scoring:

`1.67, 2.50, 1.67, 2.50, 4.17`

The variance is expected for a puzzle-specific stochastic training system. ARC Prize 2025 separately summarizes the paper method at roughly 4% ARC-AGI-2.

## Why this counts as the strong symbolic/MDL reference

CompressARC is materially different from S0:
- it trains a new model from scratch on each puzzle;
- it applies an MDL/compression objective rather than searching only a fixed shallow transform list;
- it creates puzzle-specific internal representations;
- it is fully self-contained once code/data are attached, which is compatible in principle with Kaggle's no-internet final execution model.

Its raw score is far below the ~31% neural public frontier, so it is a **reference for complementary reasoning**, not our expected final backbone.

## 2026 reproduction target C0

Goal: run the public template against the 2026 ARC-AGI-2 competition input with the smallest necessary compatibility changes only.

Acceptance evidence:
1. exact source notebook version recorded;
2. all attached code/data versions recorded;
3. L4 x4 run completes offline;
4. valid `submission.json` is emitted for the 2026 competition rerun;
5. public score and runtime recorded;
6. code changes limited to input-path/schema compatibility, not method tuning.

## Timebox / stop rule

C0 is useful but **cannot block M1**.

- Neural B1 reproduction has higher priority.
- If adapting the historical notebook to the 2026 competition is not cleanly reproducible inside the M1 window, mark C0 `PARTIAL` and use the published ARC-AGI-2 evidence as the methodological reference.
- Do not spend M1 optimizing CompressARC hyperparameters.

## Later relevance

CompressARC's potentially reusable ideas for M3–M5 are:
- single-puzzle learning;
- MDL/simplicity pressure;
- inference-time candidate collection;
- puzzle-specific adaptation without external pretraining.

Any later use must be justified by ablation against the competitive neural baseline.
