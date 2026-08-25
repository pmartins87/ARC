# M1 N2 Decision — 2026 TRM/NVARC Comparison

Snapshot: 2026-08-25
Status: conditional run decision; no user run required while N1 hidden rerun is active.

## Current public frontier snapshot

The ARC Prize 2026 Kaggle code page currently exposes these directly comparable public notebooks near the top of the code leaderboard:

- `ARC2 vanilla exact` — **31.39** public score (our N1 source);
- `ARC 2026 NVARC TRM Evidence Cost V1` — **31.11**;
- `ARC 2026 NVARC TRM Aggressive Cost Order` — **31.11**;
- `ARC2 champion E48` — **29.86**;
- `ARC-AGI-2 Public Frontier Perfpatch Evidence Lab` — **29.03**;
- `ARC AGI2 Minimal Augmentation Specialist` — **28.89**.

Sources:
- https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/code
- https://www.kaggle.com/code/christopherdaleman/arc-2026-nvarc-trm-evidence-cost-v1

The `arc-prize-trm-031` Kaggle dataset is associated with both 31.11 TRM/NVARC notebooks on the current code page. This is evidence that the two notebooks share at least one important resource/input lineage; it is **not** evidence that their complete code paths or predictions are identical.

## Why raw score alone does not justify N2

N1 and the 31.11 notebooks are separated by only 0.28 public percentage points and sit in the same broad NVARC/Qwen/TRM ecosystem. A second 12-hour-eligible competition rerun that yields only another leaderboard number would tell us little about *which* outputs differ.

The M1 question is not “can another public notebook also score around 31%?” It is:

> Does a materially different TRM/NVARC candidate source add exact outputs that N1 misses, and can those candidates survive the two-attempt selector?

Therefore N2 has high information value only when it yields task-level or candidate-level evidence suitable for overlap/oracle analysis.

## Preferred N2

If a second public run becomes justified, the preferred controlled comparison is:

`ARC 2026 NVARC TRM Evidence Cost V1`

Reason:

- it is currently 31.11, close enough to N1 to be a serious comparison;
- its title/resource lineage explicitly exposes TRM/NVARC evidence, matching the complementarity question;
- we already have portfolio and candidate-pool instrumentation prepared to measure unique exact wins rather than raw score alone.

The aggressive-cost sibling is secondary. Two siblings at the same 31.11 score should not both consume user submission quota unless source audit proves a specific orthogonal question.

## Standalone TRM checkpoint evidence

ARC Prize published verification checkpoints for Tiny Recursive Models with reported ARC-AGI-2 public-evaluation replication of **6.2%**. The published reproduction recipe required an 8xH100 training node for roughly 20–30 hours, so retraining from scratch is outside our M1 cost envelope.

Source:
- https://huggingface.co/arcprize/trm_arc_prize_verification

The checkpoint remains potentially useful later as a *candidate source* if inference can be made cheap enough and exact-output complementarity is demonstrated. Its low standalone score does not automatically make it useless; NVARC 2025 already showed why unique candidates and selection matter more than isolated accuracy. But it does not justify heavy training now.

## N2 trigger rule

Do **not** launch N2 while N1 hidden rerun is still active.

After N1 completes, launch N2 only if at least one condition is met:

1. N1 materially underperforms the 31.39 source reference and N2 is needed to distinguish source/runtime scheduling effects;
2. N2 can expose a full public `submission.json` or richer candidate dump for exact complementarity analysis;
3. source inspection identifies a concrete mechanism difference whose value cannot be answered from public artifacts alone.

Otherwise mark N2 comparison **PARTIAL** and preserve Kaggle quota for experiments that test an actual research hypothesis.

## Decision while waiting for N1

Proceed with zero-user-action work:

- finish candidate-pool/selector audit tooling;
- search for compatible public candidate artifacts;
- keep literature/novelty map current;
- prepare Paper Prize evidence structure;
- do not consume another Kaggle submission;
- do not use Ryzen 9.
