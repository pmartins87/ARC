# M1 Diversity / Selection Audit

Snapshot: 2026-08-25
Status: prior-art and measurement framing; no original competitive mechanism is disclosed here.

## Why this audit matters now

ARC-AGI-2 allows only two submitted attempts per test output. A solver can therefore fail in at least four distinct ways:

1. it never generates the correct hypothesis;
2. it generates the correct hypothesis but ranks it below the top two;
3. it spends both attempts on near-duplicates of the same wrong hypothesis;
4. refinement/search collapses an initially useful minority hypothesis into the dominant wrong mode.

NVARC 2025 already established (2): a candidate source can contribute unique exact solves without improving the final score if the selector drops them.

Johan Land's 2026 paper adds strong prior-art evidence for (3) and (4): its hosted solver deliberately generates candidates independently across text, image and code modalities and reports that prescriptive templates and iterative refinement reduced hypothesis diversity and degraded performance in the tested regime.

Sources:
- NVARC: https://github.com/1ytic/NVARC
- `Modality-Driven Search with Holistic Trace Judging for ARC-AGI-2`: https://arxiv.org/abs/2606.31543
- public implementation: https://github.com/beetree/ARC-AGI

## Johan Land 2026 — what is source-supported

The paper reports:

- **72.9%** ARC-AGI-2 semi-private at **$38.99/task**;
- **76.1%** public evaluation at **$19.69/task**;
- candidate generation across independent **text, image and code** modalities;
- holistic judging that compares complete candidate reasoning traces jointly rather than selecting by majority vote alone;
- correct minority hypotheses can be recovered when the modal answer is wrong;
- prescriptive prompting templates and iterative refinement systematically reduced hypothesis diversity and degraded performance in the reported experiments.

The public repository describes a multi-model reflective solver using frontier models, long-horizon reasoning, agentic code generation/execution, visual reasoning, and logic/consistency judges.

## What is NOT transferable directly to our competition notebook

The published system uses online frontier models and a much larger per-task budget. It is not a legal direct ARC Prize 2026 Kaggle solution because competition evaluation has no internet.

Therefore M1 should not copy the architecture literally. The useful question is narrower:

> Can a self-contained 4xL4 solver preserve useful hypothesis diversity and select minority-correct candidates using evidence already available inside its local candidate pool?

This question is still **not a novelty claim**. Diversity-aware generation/selection and holistic judging are prior art at a broad level.

## Tension with the 2025 refinement-loop thesis

ARC Prize 2025 emphasized refinement loops because repeated proposal/execution/repair produced large gains across several systems.

The 2026 diversity result does not invalidate that. It creates a conditional hypothesis:

- refinement is useful when it corrects errors while preserving independent modes;
- refinement can be harmful when it homogenizes candidates around the same attractive but wrong interpretation.

This means iteration count alone is a poor causal variable. Future experiments should measure **what happens to the candidate distribution** as refinement proceeds.

## Measurement requirements for our offline pipeline

Before designing a new selector/generator, record as many of these as the available candidate artifacts permit:

### Candidate discovery
- number of raw samples;
- number of unique canonical grids;
- candidate-pool oracle exact coverage;
- correct-candidate rank under public selectors.

### Structural diversity
- number of distinct output shapes;
- frequency of the modal shape;
- distinct color-set signatures;
- pairwise grid disagreement for same-shape candidates;
- near-duplicate concentration.

### Two-attempt diversity
- exact duplicate rate;
- same-shape vs different-shape attempts;
- normalized cell disagreement when shapes match;
- second-attempt exact rescues;
- cases where attempt 2 is different but never uniquely correct.

### Selection quality
- truth-in-pool-but-not-top2;
- oracle-to-selector gap;
- selector disagreement;
- selector-unique exact rescues;
- candidate evidence supporting minority hypotheses (votes, likelihood/rescore, augmentation consistency) where available.

### Refinement trajectory (only if later architecture exposes it)
- unique candidate count by iteration;
- entropy/concentration proxy by iteration;
- exact-oracle coverage by iteration;
- whether correct candidates disappear, survive or improve in rank.

## Interpretation rules

### High disagreement, no unique rescues

Diversity is cosmetic. Producing different guesses is not useful unless it adds exact coverage.

### Low disagreement, nonzero oracle-selector gap

The selector may be wasting a good candidate pool by collapsing on correlated top guesses.

### High candidate oracle, low submitted pass@2

Selection/diversity is a direct bottleneck.

### Low candidate oracle

A smarter selector cannot recover answers that are never generated. Prioritize adaptation/search/representation/generation.

### Diversity falls while oracle coverage falls across refinement

Direct evidence of harmful collapse in our own system.

### Diversity falls while exact accuracy rises

Collapse may be beneficial concentration rather than a problem. Do not optimize diversity as an end in itself.

## M2 implication

No original diversity mechanism should be chosen before N1 or a source-pinned diagnostic candidate dump exposes the relevant bottleneck.

If the measured candidate pool has a large oracle-selector gap, selection becomes a high-leverage M2 category. If candidate oracle itself is low, the first M2 mechanism should target candidate discovery even though selection remains scientifically interesting.

## Novelty boundary

The following cannot be claimed as novel by themselves:

- “generate candidates from multiple modalities”;
- “use a judge to select candidates”;
- “compare full reasoning traces”;
- “preserve diversity”;
- “avoid majority vote”;
- “use a diverse second attempt.”

Any future Paper Prize novelty must be a specific competition-fit mechanism/theory/result beyond this prior art and must pass `docs/M1_NOVELTY_BOUNDARIES.md` plus the M2/M3 causal-ablation contract.
