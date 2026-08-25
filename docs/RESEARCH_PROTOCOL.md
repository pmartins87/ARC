# Research Protocol

## Goal

Optimize for ARC Prize 2026 prize eligibility and private-evaluation performance while producing evidence strong enough for the Paper Track.

## Dataset roles

ARC-AGI-2 exposes two public distributions with different roles:

- **1,000 training tasks:** primary material for development, augmentation, synthetic-data generation, training, and fast diagnostics.
- **120 public evaluation tasks:** the closest public proxy for competition generalization. Official ARC documentation states that the semi-private and private evaluation sets are calibrated to the same human-facing difficulty as the public evaluation set.

For that reason, the 1,000-task training corpus is **not** our principal architecture-selection benchmark. We may split it for development diagnostics, but claims about generalization and milestone gates are driven by a sealed split of the 120 public evaluation tasks.

## Evaluation hierarchy

### Level A — training/development
Use the 1,000 ARC-AGI-2 training tasks for implementation, synthetic curricula, primitive coverage, debugging, and rapid iteration. A deterministic 70/15/15 diagnostic split may be used here, but it is not treated as evidence of competition-level generalization.

### Level B — eval-development (60 tasks)
A fixed 60-task subset of the 120 public evaluation tasks. This is the only public-evaluation subset that may be inspected routinely while developing architecture and failure taxonomies.

### Level C — eval-validation (30 tasks)
A fixed 30-task subset used for architecture selection and ablations. Do not add task-specific rules because of individual failures here. Prefer aggregate diagnostics and family-level conclusions.

### Level D — eval-heldout (30 tasks)
A fixed 30-task sealed subset opened only at milestone gates. Repeated tuning against this subset is prohibited. Any manual inspection after opening is logged and causes the split to be considered consumed for future confirmatory claims.

### Level E — Kaggle hidden evaluation
This is the competition target. Kaggle replaces the placeholder test challenges during rerun with unseen tasks. Leaderboard gains are evidence, not proof of generality; avoid repeated leaderboard probing as a substitute for internal validation.

## Split construction and versioning

The original operational manifest (`arc-2026-v1`) used `scripts/make_split.py` to produce exact 60/30/30 counts from the 120 public evaluation task IDs. Ordering was deterministic from a cryptographic hash of `(seed, task_id)`.

E0007/E0008 then performed a **label-free structural audit before any Level C/D score was used**. It found that the untouched v1 validation and heldout gates were strongly skewed in visible difficulty proxies: median test-input area was 642.5 for validation versus 285 for heldout.

Because development had already been used, its 60 task IDs are preserved exactly. Only the still-unopened 60-task validation+heldout pool was rebalanced using training examples and test inputs only. `scripts/make_gate_split_v2.py` pairs structurally nearest tasks in rank-normalized visible-feature space and sends one member of each pair to validation and one to heldout. Test outputs are never read.

The adopted gate manifest is:

- `experiments/evaluation_split_v2.json`
- profile: `evaluation-gates-v2`
- seed: `arc-2026-gates-v2`
- SHA-256: `0a03d5aba5670b779522b6f2bde55f165ba87c2f2a0f123dd0b969e9acbd2bc3`

Measured visible balance improved materially: validation/heldout median test-input area is 473.5/484 and multi-test-task fraction is 36.7%/40.0%. Development remains unchanged.

This is a one-time **pre-gate protocol correction**, not a result-driven resplit. From adoption onward, v2 is immutable. Any future change requires an explicit new protocol version and invalidates confirmatory claims that depended on an older gate definition.

Before strong scientific claims, continue to inspect the corpus for structural/near-duplicate families. If a grouped-family split is ever needed, it must be defined before using the affected gate scores and cannot retroactively rescue a failed result.

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

Always report the benchmark context with a score: training/eval-dev/eval-validation/eval-heldout/Kaggle; pass@1/pass@2; hardware; runtime; and whether the number is ours or third-party reported.

## Two-attempt policy

ARC gives two attempts for each test output. Attempt 2 is a scarce resource. We measure:

1. duplicate-attempt rate;
2. structural diversity between attempts;
3. marginal exact accuracy supplied by attempt 2;
4. whether diversity hurts attempt-1 quality.

A diversity mechanism is accepted only if it increases pass@2 on validation and survives a held-out gate.

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
- Never create a rule whose only justification is one validation/evaluation/test task.
- Log manual inspection of eval-validation/eval-heldout failures.
- Deduplicate synthetic data against public evaluation/test material where possible.
- Keep v2 gate manifest immutable after adoption.
- Treat Kaggle leaderboard probing as a scarce diagnostic, not an optimization loop.

## Public/private repository policy

Prize eligibility requires open sourcing, but competitive work does not need to be public throughout active development. Keep novel, unsubmitted competitive insights private until the required open-source/writeup window unless there is a deliberate reason to publish earlier. Preserve complete history and reproducibility internally so release can be made cleanly when required.
