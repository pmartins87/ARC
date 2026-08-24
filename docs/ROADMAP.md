# ARC Prize 2026 Roadmap

## Competition target

Primary: ARC-AGI-2 Progress Prize / Grand Prize eligibility.
Secondary: Paper Track using the same system and experiments.

The roadmap is gate-driven. Calendar dates are planning bounds, not permission to advance with weak evidence.

## M0 — Foundation and rules freeze

**Gate:** repository, exact scorer, test-output schema, evaluation policy, source map, and reproducible experiment format exist and are checked.

Deliverables:
- official rules/deadlines snapshot;
- exact pass@2 scorer;
- deterministic initial split tooling;
- state-of-the-art audit;
- competition-risk register.

## M1 — Reproduce competitive baselines

**Purpose:** establish what is already achievable before inventing new architecture.

Required baselines:
1. trivial/schema baseline;
2. compact symbolic/program-synthesis baseline;
3. 2025 NVARC-style public Kaggle baseline or closest reproducible 2026 version;
4. TRM-family baseline that fits available compute;
5. one MDL/program-synthesis baseline (CompressARC or equivalent) where feasible.

**Gate:** reproducible score/runtime table with at least one serious neural and one serious symbolic baseline.

## M2 — Structural solver core

Build a general-purpose representation and verified program-search layer:
- color/background hypotheses;
- 4- and 8-connected components;
- bounding boxes, masks, holes, symmetry, containment, adjacency;
- object relations;
- geometric transforms;
- color transforms;
- extraction/crop/composition;
- line/ray/region operations;
- compact DSL;
- exact demonstration verifier.

**Gate:** measurable held-out gain over the selected symbolic baseline without task-ID rules.

## M3 — Two-attempt inference

Develop candidate ranking and deliberate attempt diversity.

Test:
- top-2 independent scores;
- semantic-program diversity;
- representation diversity;
- uncertainty-conditioned second attempts;
- consensus/ensemble selection.

**Gate:** statistically credible pass@2 gain on held-out tasks with no material pass@1 regression.

## M4 — Learned search guidance / refinement

Only after symbolic search telemetry exists, train or adapt a model to prioritize useful hypotheses.

Candidate families:
- small recursive model/TRM-derived guidance;
- learned primitive/operator proposal;
- learned object-role prediction;
- synthetic-task curriculum;
- test-time refinement constrained by exact demonstration verification.

**Gate:** positive ablation against the same search budget and runtime envelope.

## M5 — Ensemble under Kaggle budget

Combine complementary solvers rather than merely stacking correlated variants.

Optimize:
- solver routing;
- time allocation by task difficulty;
- early stopping;
- shared perception/cache;
- candidate normalization;
- final two-attempt selection.

**Gate:** full offline notebook finishes safely within Kaggle's 12-hour limit with margin and improves hidden/public competition score.

## M6 — Prize submission hardening

- deterministic/offline packaging;
- dependency freeze;
- failure-safe submission generation;
- complete task-ID/output coverage validator;
- multiple dry runs;
- runtime margin;
- final Kaggle submissions.

**Gate:** final notebook reproducibly emits valid `submission.json` with zero missing tasks/attempts.

## M7 — Grand Prize / Paper Track package

Prepare:
- public notebook;
- open-source repository release;
- 1,500-word Kaggle writeup;
- optional PDF paper/project link;
- ablation table;
- method diagram;
- reproducibility instructions;
- limitations and negative results.

**Gate:** every scientific claim maps to an experiment artifact and commit.

## Decision rules

- Do not keep an idea because it sounds intelligent; keep it because it scores.
- Prefer complementary errors over redundant ensemble members.
- A leaderboard improvement that fails internal held-out validation is suspect.
- A paper idea that does not improve score can survive only if it yields strong conceptual evidence under the Paper Track rubric.
- Freeze the final system early enough to permit repeated full offline runs.
