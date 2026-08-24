# ARC Prize 2026 — Project Status

Last updated: 2026-08-24

## Executive state

- **Current milestone:** M1 — Reproduce competitive baselines — **ACTIVE**.
- **Completed:** M0 — Foundation and rules freeze — **PASS**.
- **M1 timebox end:** 2026-09-02.
- **Primary competition deadline:** 2026-11-02 23:59 UTC.
- **Paper Track deadline:** 2026-11-09 23:59 UTC.
- **Current gate:** obtain N1 hidden rerun score and one strategically useful task-level alternative/comparison, then freeze the first evidence-based M2/M3 hypothesis.

## N1 — competitive Kaggle baseline

`ARC2 vanilla exact`

Our clean copy:
- Version 1 completed successfully;
- runtime: **25m29s**;
- accelerator: **GPU L4 x4**;
- valid `submission.json` generated;
- Kaggle competition submission was accepted for the private rerun;
- hidden competition rerun score: **PENDING / IN PROGRESS**.

Reference public notebook score at the 2026-08-24 snapshot: **31.39%**. This is third-party reference evidence until our rerun result arrives.

### Local smoke-output audit

The local/non-rerun `submission.json` is now audited and is **not a full 120-task performance artifact**:
- 120 task IDs / 172 output slots;
- **167/172** slots are `[[0]]` placeholders in both attempts;
- only **5 output slots across 4 tasks** contain generated candidates.

On those five generated outputs, against matching current official task outputs:
- pass@1: **3/5 = 60%**;
- pass@2: **4/5 = 80%**;
- one exact solve comes exclusively from attempt 2 (`36a08778[1]`);
- generated-attempt duplicate rate: **0/5**.

This is useful only as smoke evidence that the pipeline works and that pass@2 diversity can rescue exact solves. It must **not** be interpreted as the full N1 score.

A provenance mismatch was also discovered: the current official GitHub evaluation set has different test-pair counts from the Kaggle submission schema for five task IDs (`4a21e3da`, `abc82100`, `faa9f03d`, `b6f77b65`, `f560132c`). Future full public-evaluation audits must pin the Kaggle dataset version rather than silently substitute the current GitHub directory.

Experiments: `experiments/E0001_PENDING_N1_arc2_vanilla_exact.md` and `experiments/E0004_20260824_n1_local_smoke_audit.md`.

BlackCat/N0 is now fallback only and should not consume a run if N1 is accepted.

## S0 — compact symbolic baseline

**REJECT as standalone.**

Frozen 60-task evaluation-development result:
- 82 test outputs;
- pass@1: **0.0%**;
- pass@2: **0.0%**;
- exact fitted hypotheses: **0**;
- runtime: **14.78 s** on GitHub Actions CPU.

S0 remains only as a lower-bound/regression instrument. M1 will not grow a shallow DSL blindly.

Experiment: `experiments/E0002_20260824_s0_symbolic_dev.md`.

## NVARC / portfolio audit

The NVARC 2025 audit established a critical rule: standalone solver accuracy is insufficient. A component can generate unique correct candidates and still add zero final score if overlap is high or the final two-attempt selector drops those candidates.

Project measurement therefore separates:
1. **candidate-discovery ceiling / oracle union**;
2. **actual two-attempt selection efficiency**.

Pairwise and multi-solver tooling on `main` now measures exact coverage, unique wins, oracle union, leave-one-out contribution, second-attempt rescues, duplicate attempts and optional runtime-budget portfolios.

We will **not retrain TRM from scratch** in M1. Any N2 comparison must use a public checkpoint/notebook and answer a bounded complementarity question.

Docs: `docs/M1_NVARC_AUDIT.md`.

## C0 — CompressARC strong distinct reference

Methodological status: **RETAIN**.

Current task-level baseline status: **PARTIAL**.

A zero-GPU shortcut attempted to recover exact coverage from the authors' published `predictions_evaluation.npz`. A strict provenance audit rejected it:
- official current ARC-AGI-2 public evaluation: **120 tasks**;
- published CompressARC artifact source: **400 tasks**;
- official current tasks present in the source: **6**;
- official current tasks missing: **114**.

Therefore the 400-task artifact must not be reported as a current ARC-AGI-2 score. The probe fails closed. We will not spend a user Kaggle run merely to reproduce the historical low-single-digit CompressARC result unless later evidence gives a concrete complementarity reason.

Experiment: `experiments/E0003_20260824_compressarc_artifact_provenance.md`.
Docs: `docs/M1_COMPRESSARC_REPRO.md`.

## Evaluation discipline

- 1,000 public training tasks: training/development material.
- 120 public evaluation tasks: principal public proxy for hidden ARC-AGI-2 generalization.
- frozen operational split: **60 development / 30 validation / 30 heldout** using seed `arc-2026-v1`.
- continuous tuning is allowed only on the 60 development tasks.

## Compute policy

- **GitHub Actions:** deterministic tests, scoring, profiling and public-source audits.
- **Kaggle L4 x4:** neural baselines and all final competition-valid heavy runs.
- **Ryzen 9:** **NOT NEEDED now**. Activate only when a measured CPU-parallel workload has a plausible prize payoff.

The final solution must fit Kaggle constraints regardless of research hardware.

## Repository visibility

Keep `pmartins87/ARC` **PUBLIC through M1 measurement/audit work**.

Before committing a genuinely original competitive mechanism, unpublished ablation advantage or material new score improvement, trigger the visibility gate. Default action at that point: move private until the required open-source/writeup window.

## Immediate gates

### User-side

No new run or Ryzen work is required now. The only useful user-side evidence is the N1 competition result when Kaggle returns it.

### Research-side

1. treat E0004 as smoke evidence only and do not tune to its four generated tasks;
2. decide whether one N2 current NVARC/TRM run has enough information value to justify the quota;
3. seek comparable task-level predictions or a bounded frozen public-evaluation run where the exact dataset version is pinned;
4. measure overlap/oracle union rather than raw score alone;
5. close M1 **PASS or PARTIAL by 2026-09-02**;
6. freeze the first M2/M3 research hypothesis and trigger repository-visibility review before original competitive code.

## Finite-project rule

A missed milestone gate becomes `PARTIAL`; the best working artifact carries forward and the project advances. No phase can consume the whole schedule. No new architecture enters after the M6 freeze on 2026-10-23. ARC-AGI-2 R&D stops at the final code deadline; Paper Track work stops at its deadline; M9 is administration/outcome recording only.
