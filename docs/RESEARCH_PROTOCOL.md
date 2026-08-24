# Research Protocol

## Goal

Optimize for ARC Prize 2026 prize eligibility and private-evaluation performance while producing evidence strong enough for the Paper Track.

## Evaluation hierarchy

### Level A — development
Use only ARC-AGI-2 training tasks selected for development. Fast iteration is allowed.

### Level B — internal validation
A deterministic split of the 1,000 public training tasks is used for architecture selection. The first split is hash-based and therefore reproducible, but it is **not assumed to be family-independent**. We will add structural/near-duplicate clustering before making strong generalization claims.

### Level C — internal held-out
Held-out training tasks are opened only at milestone gates. Repeated tuning against this split is prohibited.

### Level D — official public evaluation (120 tasks)
Use sparingly as an external generalization check. Aggregate scores are permitted. Until later milestones, do not add task-specific rules because of individual public-evaluation failures. Any manual inspection of evaluation tasks must be logged.

### Level E — Kaggle hidden evaluation
This is the competition target. Kaggle replaces the placeholder test challenges during rerun with unseen tasks. Leaderboard gains are evidence, not proof of generality; avoid repeated leaderboard probing as a substitute for internal validation.

## Metrics

Primary:

- exact output accuracy under official **pass@2** scoring;
- pass@1 accuracy for diagnostic purposes;
- pass@2 gain over pass@1;
- Kaggle rerun score.

Secondary:

- wall-clock runtime;
- peak RAM/VRAM;
- candidate programs explored per task;
- fraction of tasks with multiple demonstration-consistent hypotheses;
- solver coverage by transformation family;
- calibration of candidate ranking;
- failure taxonomy.

## Two-attempt policy

ARC gives two attempts for each test output. Attempt 2 must be treated as a scarce resource. We will measure:

1. duplicate-attempt rate;
2. structural diversity between attempts;
3. marginal exact accuracy supplied by attempt 2;
4. whether diversity hurts attempt-1 quality.

A diversity mechanism is accepted only if it increases pass@2 on held-out data.

## Experiment ledger

Every material experiment records:

- experiment ID;
- date/time;
- git commit SHA;
- dataset/split manifest SHA;
- method/config;
- random seed(s);
- hardware;
- runtime;
- pass@1 and pass@2;
- per-family diagnostics when available;
- conclusion: KEEP / REJECT / INCONCLUSIVE.

## Scientific-claim policy

No component is called novel merely because we independently conceived it. Before a novelty claim, compare against at least:

- ARC Prize 2025 winning high-score systems;
- TRM and later recursive-reasoning variants;
- SOAR/evolutionary program synthesis;
- CompressARC/MDL-style test-time learning;
- neuro-symbolic/program-synthesis ARC work;
- relevant 2026 ARC-AGI-2 public systems.

Claims require ablations. Examples:

- dual representation vs pixels only;
- object representation vs grid only;
- verified synthesis vs unconstrained generation;
- diversity-aware attempt 2 vs top-two-by-score;
- learned search guidance vs heuristic guidance;
- refinement loop on/off.

## Reproducibility

Core scoring and schema code should remain dependency-light. Competition notebooks must run without internet and within Kaggle limits. Any external data/model must be freely and publicly available and packaged as allowed by Kaggle.

## Leakage controls

- Never hard-code a solution keyed by task ID.
- Never create a rule whose only justification is one evaluation/test task.
- Log manual inspection of official evaluation failures.
- Deduplicate synthetic data against public evaluation/test material where possible.
- Keep split manifests immutable once a milestone begins.

## Public/private repository policy

Prize eligibility requires open sourcing, but competitive work does not need to be public throughout development. Keep novel, unsubmitted competitive insights private until the open-source/writeup window unless there is a reason to publish earlier.
