# M2/M3 Experiment Contract

Snapshot: 2026-08-25
Status: pre-registration template only; no original competitive mechanism is disclosed here.

## Purpose

M2 and M3 are where the project stops merely reproducing public systems and begins testing original research hypotheses. This contract prevents leaderboard chasing, post-hoc storytelling and open-ended architecture drift.

Every serious hypothesis gets at most **two implementation/ablation rounds** before a forced decision: `KEEP`, `REJECT` or `INCONCLUSIVE`.

## Visibility prerequisite

Before writing a genuinely original competitive mechanism, apply the repository visibility gate. The public repository may contain this protocol, public baselines and measurement infrastructure; unpublished mechanisms and material unpublished score gains should not be committed publicly by default.

## Hypothesis pre-registration

Before implementation, record:

- experiment ID;
- one-sentence mechanism claim;
- closest three public prior methods;
- exact claimed difference from those methods;
- causal prediction: what metric should move if the mechanism works;
- negative prediction: what observation would falsify the idea;
- compute budget / runtime ceiling;
- dataset slice allowed for iteration;
- required control/ablation.

If the causal prediction cannot be stated, implementation should not start.

## Dataset discipline

### Continuous development

Use only the frozen **60-task evaluation-development** slice for repeated iteration.

### Milestone validation

The **30-task validation** slice is opened only at a declared milestone gate. It must not become a second continuously tuned development set.

### Heldout

The **30-task heldout** slice is used only for later milestone confirmation. A mechanism that succeeds on development and collapses on validation/heldout is not promoted merely because it once looked good.

Kaggle leaderboard score is an external competition signal, not the optimization objective for every micro-change.

## Required metrics

For every comparable run, capture as available:

### Accuracy
- exact pass@1;
- exact pass@2;
- correct outputs / total outputs;
- all-output task solve rate.

### Candidate discovery
- candidate-pool oracle pass@2;
- unique exact candidates;
- correct-candidate rank when present;
- number of canonical candidates.

### Selection
- selected pass@2 from the same frozen pool;
- oracle-to-selector gap;
- truth-present-but-not-top2 count;
- second-attempt rescues;
- duplicate-attempt rate;
- top-two disagreement / unique selector rescues.

### Complementarity
- exact outputs uniquely solved relative to current best component;
- oracle-union gain;
- leave-one-out contribution;
- overlap/Jaccard where useful.

### Cost
- wall-clock runtime;
- tasks processed / timed out / never started;
- GPU/CPU configuration;
- peak memory when available;
- materially changed candidate/search budget.

A raw score increase that comes only from processing more tasks is still useful for competition engineering, but must be labeled as a coverage/scheduling gain rather than a reasoning gain.

## Round 1 — minimal causal test

Implement the smallest version capable of testing the mechanism. Do not bundle unrelated improvements.

Round 1 should answer:

1. Does the predicted intermediate metric move?
2. Does exact accuracy move in the expected direction?
3. Is the effect large enough to justify a second round?
4. Is the effect attributable to the mechanism rather than extra compute?

### Round-1 decision

- `REJECT` if the predicted causal metric does not move or exact accuracy clearly worsens without a compensating strategic benefit.
- `INCONCLUSIVE` if instrumentation/provenance prevents attribution.
- advance to Round 2 only if there is a real signal worth refining.

## Round 2 — bounded refinement / ablation

Round 2 may fix one demonstrated weakness or test one necessary ablation. It must not turn into a new architecture family.

At the end of Round 2, force a decision:

### KEEP
Use when evidence indicates a reproducible advantage that survives the required control and has acceptable cost.

### REJECT
Use when the improvement disappears under the control/ablation, overfits development, or costs more than its measured contribution justifies.

### INCONCLUSIVE
Use when the idea remains scientifically plausible but cannot be resolved within the milestone timebox. Archive it and advance the roadmap.

No hypothesis receives a silent third serious round by renaming the experiment.

## Promotion to M3/M4

A component is not promoted solely because it has non-zero standalone accuracy. Promotion should require one or more of:

- material exact-score gain on the frozen development protocol;
- unique exact outputs that increase portfolio oracle coverage;
- a measurable reduction in candidate-discovery or selection failure;
- a strong runtime/coverage efficiency gain;
- a scientifically valuable causal result supporting the Paper Prize.

The stronger the compute cost, the stronger the evidence required.

## Paper-traceability rule

Every retained mechanism should leave behind:

- hypothesis statement;
- source/closest-prior record;
- configuration and commit;
- raw result artifact;
- ablation/control;
- failure analysis;
- KEEP/REJECT/INCONCLUSIVE decision.

This converts engineering work directly into material usable for the Paper Prize without rewriting history after the competition.
