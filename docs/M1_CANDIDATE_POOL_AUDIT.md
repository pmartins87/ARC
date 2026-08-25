# M1 Candidate-Pool / Selector Audit

Snapshot: 2026-08-25
Status: public-source measurement infrastructure; no original competitive mechanism is disclosed here.

## Why this exists

ARC-AGI-2 allows exactly two guesses per test output. In the current Qwen/NVARC family, the model does not directly emit only two guesses: it generates a larger candidate pool and then ranks that pool down to two submitted outputs.

That creates two distinct failure modes:

1. **candidate-discovery failure** — the exact truth never appears in the generated pool;
2. **selection failure** — the truth is present in the pool but is not ranked into the final top two.

M1 must measure those separately before M2 changes either generation or selection.

## Pinned public reference

The implementation is grounded in the public 2026 Qwen mirror:

`MA-Zbida/arc2026-kaggle@4a3d6f33816807eacb7ea49846fadbca042abd69`

Relevant reference file:

`tune_selection.py`

The public dump schema stores repeated samples with:

- `solution` — candidate grid;
- `beam_score` — DFS / decoding evidence;
- `score_aug` — augmentation-rescoring evidence.

Repeated exact grids are canonicalized and aggregated into candidate evidence.

## Public selectors reproduced

### `score_kgmon`

For each canonical candidate:

- inference term = number of times the candidate was generated;
- augmentation term = mean augmentation NLL;
- final ranking score = votes minus mean augmentation NLL.

### `score_full_probmul_3`

For each canonical candidate, using the public baseline constant 3:

- accumulate `(3 - beam_score)` over inference observations;
- for each sample, accumulate `(3 - augmentation_score)` across its augmentation scores;
- average those per-sample augmentation sums;
- add inference and augmentation terms.

The project reproduces these selectors as public baselines. Any later selector that is genuinely original must pass the repository-visibility gate before public implementation.

## New project measurements

`src/arcsolver/candidate_pool.py` now measures:

- total expected test outputs;
- processed vs missing inference outputs;
- raw generated samples;
- unique canonical candidates;
- duplicate-sample fraction;
- mean / median / p90 unique candidate count;
- candidate-pool oracle exact coverage;
- selected pass@2 for each public selector;
- oracle-to-selector gap;
- truth-present-but-not-top2 count;
- correct-candidate rank median and p90;
- selector-unique exact rescues;
- disagreement rate between the selectors' final top-two sets.

Missing outputs count as misses rather than disappearing from the denominator. Extra output keys fail closed as a dataset/provenance mismatch.

## Trusted dump CLI

`scripts/audit_candidate_dump.py` reads the public Qwen/NVARC-style validation dump format and emits a JSON audit.

The upstream dump format uses Python pickle payloads inside a zip. Pickle can execute arbitrary code when loading untrusted data. The CLI therefore refuses to load unless the caller explicitly passes `--trusted-pickle` and the source is known/trusted (for example, a dump produced by our own Kaggle run or a pinned source we have audited).

## Why this is high leverage

A leaderboard increase can come from very different causes:

- better task-time adaptation;
- more candidate coverage;
- better ranking of already-good candidates;
- processing more tasks before the time limit.

Without candidate-pool telemetry, those mechanisms are confounded. With it, a future experiment can answer a sharper question such as:

> Did the modification create new exact candidates, or merely change which existing candidates survive into the two allowed attempts?

That distinction matters both for prize engineering and for the Paper Prize's theory/progress claims.

## Acceptance gate

This instrumentation is ready when CI passes regression tests showing that:

- repeated exact candidates are deduplicated correctly;
- the two public selectors can be measured independently;
- an oracle hit can be separated from a top-two selection miss;
- missing task outputs count against the score;
- dataset mismatches fail closed.

No Kaggle run or Ryzen work is required to complete this infrastructure gate.
