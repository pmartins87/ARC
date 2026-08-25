# Paper Evidence Matrix

Use this file to prevent unsupported claims. Every final paper claim must map to a source, experiment, or explicit inference.

| Claim area | Evidence required | Current state | Gate |
|---|---|---|---|
| N1 is a valid competitive baseline | Kaggle version/runtime + hidden rerun score | Version 1 and 25m29s captured; hidden rerun pending | Wait for Kaggle result |
| Compact shallow symbolic DSL is insufficient alone | Frozen dev experiment | E0002: 0/82 exact outputs | Satisfied |
| Two attempts can add value | Exact rescue evidence | N1 local smoke artifact contains one attempt-2 rescue among 5 generated outputs | Preliminary only |
| Candidate discovery and final selection must be separated | Public NVARC evidence + our instrumentation | Public evidence and complementarity tooling exist | Satisfied as methodology |
| Alternative solver is complementary to N1 | Comparable task-level predictions | Not yet available | M1 PASS/PARTIAL gate |
| Final mechanism improves generalization | Frozen validation/heldout + Kaggle result | No original mechanism selected | M3–M7 |
| Final mechanism is novel | Literature/source audit against closest prior art | Not established | Required before novelty claim |
| Final mechanism is universal beyond ARC | Theory + transfer/generalization evidence where feasible | Not established | Paper rubric gate |
| Improvement is not merely more compute | Runtime-controlled ablation | Not established | Required if final method adds compute |
| Pass@2 gain comes from deliberate diversity | pass@1/pass@2, rescue and duplicate-attempt metrics | Tooling exists; full evidence pending | M4 |

## Rule

A paper sentence that materially contributes to Accuracy, Universality, Progress, Theory, Completeness or Novelty must be traceable to this matrix before submission.
