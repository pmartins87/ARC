# Paper Evidence Matrix

Use this file to prevent unsupported claims. Every final paper claim must map to a source, experiment, or explicit inference.

| Claim area | Evidence required | Current state | Gate |
|---|---|---|---|
| N1 is a valid competitive baseline | Kaggle version/runtime + hidden rerun score | Version 1 and 25m29s captured; hidden rerun pending | Wait for Kaggle result |
| Compact shallow symbolic DSL is insufficient alone | Frozen dev experiment | E0002: 0/82 exact outputs | Satisfied |
| Two attempts can add value | Exact rescue evidence | N1 local smoke artifact contains one attempt-2 rescue among 5 generated outputs | Preliminary only |
| Candidate discovery and final selection must be separated | Public NVARC evidence + our instrumentation | Candidate-pool oracle, selector-gap, rank and coverage tooling now exists | Satisfied as methodology |
| A selector gain comes from better selection rather than better generation | Same frozen candidate pool scored by controlled selectors | Instrumentation ready; full candidate dump not yet available | M2/M4 evidence gate |
| Alternative solver is complementary to N1 | Comparable task-level predictions | Not yet available; N2 is conditional rather than automatic | M1 PASS/PARTIAL gate |
| Final mechanism improves generalization | Frozen validation/heldout + Kaggle result | No original mechanism selected | M3–M7 |
| Final mechanism is novel | Closest-prior audit + mechanism-level difference + causal ablation | High-level prior-art boundaries frozen; specific mechanism not selected | Required before novelty claim |
| Final mechanism is universal beyond ARC | Theory + transfer/generalization evidence where feasible | Not established | Paper rubric gate |
| Improvement is not merely more compute | Runtime/coverage-controlled ablation | Not established | Required if final method adds compute |
| Pass@2 gain comes from deliberate diversity | pass@1/pass@2, rescue, duplicate-attempt and top-two disagreement metrics | Tooling exists; full evidence pending | M4 |
| Candidate diversity is useful rather than cosmetic | Unique exact rescues / oracle union, not only disagreement | Tooling exists; comparable candidate artifacts pending | M2–M4 |
| Negative findings constrain the theory | Reproducible failed/partial experiments with provenance | E0002, E0003 and E0004 already retained | Ongoing |

## Novelty discipline

`docs/M1_NOVELTY_BOUNDARIES.md` records categories that are already established in public ARC work: test-time training, synthetic curricula, recursive neural refinement, zero-pretraining per-task optimization, MDL/compression, evolutionary program refinement, masked diffusion/self-refinement, multi-view ensembles, candidate rescoring/top-two selection, neuro-symbolic object reasoning and visual/spatial priors.

A final novelty claim must be attached to a **specific mechanism or empirical finding**, not to one of those broad categories.

## Rule

A paper sentence that materially contributes to Accuracy, Universality, Progress, Theory, Completeness or Novelty must be traceable to this matrix before submission.
