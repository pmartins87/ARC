# ARC Prize 2026 — Project Status

Last updated: 2026-08-25

## Executive state

- **Current milestone:** M1 — Reproduce competitive baselines / feasibility — **ACTIVE**.
- **Completed:** M0 — Foundation and rules freeze — **PASS**.
- **M1 timebox end:** 2026-09-02.
- **Primary competition deadline:** 2026-11-02 23:59 UTC.
- **Paper Track:** active in parallel from the same evidence stream; internal safety deadline 2026-11-08 pending final re-verification of organizer date discrepancy.
- **N1 gate:** **PASS / COMPLETE**.
- **Current external gate:** E0006 Lightning + NVIDIA NVARC **L4 x4 compatibility/throughput smoke**.

## N1 — first end-to-end Kaggle neural baseline

`ARC2 vanilla exact`, unchanged public reproduction.

Evidence:
- copied notebook Version 1;
- `Save & Run All` runtime **25m29s**;
- accelerator **GPU L4 x4**;
- notebook Internet OFF;
- valid `submission.json`;
- competition rerun status **Succeeded**;
- Kaggle **Public Score 29.72**;
- frozen source snapshot reference **31.39**;
- reproduction delta **-1.67 percentage points**.

Interpretation:
- N1 is a successful operational reproduction and our first Kaggle-valid neural anchor;
- 29.72 is the Public Score from the competition rerun, **not** the final private score used at competition close;
- the 1.67pp source gap is preserved as provenance evidence rather than chased with repeated leaderboard reruns;
- correlated ~30–32% public notebooks are now low information value unless they expose a concrete complementarity or provenance question.

Experiment: `experiments/E0001_20260825_n1_arc2_vanilla_exact.md`.

### Local N1 smoke-output audit

The local non-rerun output was intentionally only a smoke artifact:
- 120 task IDs / 172 output slots;
- **167/172** slots placeholders `[[0]]`;
- only 5 generated outputs across 4 tasks;
- those generated outputs scored 3/5 pass@1 and 4/5 pass@2 against matching current official outputs;
- one exact rescue came only from attempt 2 (`36a08778[1]`).

A dataset-version mismatch also exists between the local Kaggle submission schema (172 slots) and the current official GitHub evaluation directory (167 slots). E0005 fingerprints this explicitly; cross-version auditing must pin provenance.

## Competitive frontier

Keep three regimes separate:

1. **our controlled N1 anchor:** 29.72;
2. **public-code notebooks:** strongest currently verified in our audit ~31.81 (`ARC Baseline Rebuild`, best Version 73);
3. **live prize frontier:** organizer-reported leaders ~70%+.

Therefore M2 must seek **step-change leverage**, not routine +0.x leaderboard tuning. The exact current 8th-place score remains unverified and must not be guessed.

## Evaluation protocol

Public ARC-AGI-2 structure:
- 1,000 training tasks: development/training/synthetic material;
- 120 public evaluation tasks: primary public proxy for hidden generalization.

E0007 measured a material visible train→evaluation shift without reading test outputs:
- median test-input area **144 → 484** (3.36x);
- median demo-input area **100 → 299**;
- median test-input colors **4 → 6**;
- multi-test-task fraction **6.9% → 37.5%**.

The original deterministic 60/30/30 evaluation split was then audited before any validation/heldout score was used. E0008 found validation/heldout structurally skewed: median test-input area **642.5 vs 285**. We therefore preserved the 60-task development set exactly and rebalanced only the still-unopened 60-task gate pool using visible features (training demonstrations + test inputs only).

Immutable gate manifest: `experiments/evaluation_split_v2.json`.

New validation/heldout medians:
- test-input area **473.5 / 484**;
- multi-test-task fraction **36.7% / 40.0%**;
- output-slot counts **42 / 43**.

No validation/heldout output or score was read during this rebalance.

## Instrumentation ready

On `main` we now have dependency-light tooling for:
- exact pass@1/pass@2 scoring;
- symbolic lower-bound evaluation;
- candidate-pool oracle vs selector gap;
- second-attempt rescues and duplicate attempts;
- candidate diversity and near-duplicate diagnostics;
- pairwise/multi-solver complementarity;
- runtime/task coverage under deadline;
- dataset/submission provenance fingerprints;
- visible distribution profiling and gate-balance audit;
- local NVIDIA NVARC-compatible transductive and inductive verification.

The project explicitly separates:
1. candidate discovery;
2. final two-attempt selection;
3. runtime/coverage;
4. hypothesis diversity/collapse;
5. provenance/version drift.

## S0 — shallow symbolic baseline

**REJECT standalone.**

Frozen development result:
- 60 tasks / 82 outputs;
- pass@1 **0.0%**;
- pass@2 **0.0%**;
- runtime ~14.78 s GitHub Actions CPU.

Retain only as lower-bound/regression instrumentation.

## N2 / N0 / C0 decisions

- **N2 TRM/NVARC ~31.11:** conditional only; skip for score alone.
- **N0 BlackCat:** retired fallback now that N1 validated the pipeline.
- **C0 CompressARC:** retain as conceptually distinct MDL/test-time-learning reference, but no routine Kaggle run in M1 because historical artifact provenance does not align with the current 2026 evaluation set.

## E0006 — current high-information gate

Preferred feasibility probe: **Nemotron 3.5 Lightning + NVIDIA NeMo Gym NVARC**.

Public evidence already established:
- NVIDIA publishes a NVARC environment with **transductive direct-grid** and **inductive executable `transform()`** modes;
- exact binary verification exists for both modes, with the inductive program executed in a restricted subprocess sandbox;
- public configs expose matched train/validation paths for both modes;
- Lightning has public vLLM / TP4 deployment guidance;
- NVIDIA's NIM support matrix reports a BF16 TP4 floor of **20 GB/GPU, minimum 4 GPUs**; Kaggle L4 x4 provides 24 GB/GPU, so the published memory floor is not an immediate blocker.

Prepared on `main`:
- inspect-only Kaggle smoke;
- bounded TP4 vLLM load + one short generation smoke;
- structured OOM/kernel/version failure capture;
- startup/token/memory instrumentation;
- local source-faithful direct-grid parser;
- local source-faithful inductive code extraction/execution verifier;
- guarded development-split probe path.

E0006 status: **PENDING_L4_SMOKE**.

Stop rule:
- one compatibility round;
- at most one bounded mechanical fix round;
- if viable, one frozen-development transductive-vs-inductive ablation;
- then KEEP / REJECT / INCONCLUSIVE.

This smoke is **not a competition submission** and should not consume leaderboard quota.

## Compute policy

- **GitHub Actions:** deterministic tests/profiling/public-source audits.
- **Kaggle L4 x4:** heavy neural feasibility and competition-valid runs.
- **Ryzen 9:** **not needed now**; activate only for a measured CPU-parallel workload with plausible prize payoff.

## Paper Prize / novelty discipline

The Paper Prize is a separate prize path sharing this experiment stream. Positive results, negative results, ablations, provenance decisions and failure modes are recorded during engineering.

Broad ingredients already treated as prior art include TTT, synthetic curricula, recursive refinement, MDL/test-time learning, program synthesis, multi-view candidate diversity, holistic judging, candidate rescoring and neuro-symbolic object reasoning. Novelty requires a specific mechanism plus causal evidence.

Before any genuinely original competitive mechanism or unpublished material score gain is committed publicly:

> **Visibility Gate atingido: não devemos publicar o próximo commit.**

Default then becomes private development until required open-source/writeup release.

## Immediate next action

Move from aggregate-baseline reproduction to **E0006 compatibility/throughput evidence**. Do not spend another ARC leaderboard submission merely to reproduce a nearby public score.

M1 still closes PASS or PARTIAL by 2026-09-02; a missed sub-gate cannot extend the milestone indefinitely.
