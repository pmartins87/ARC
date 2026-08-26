# M1 — semantics-preserving logit transfer optimization

Snapshot: 2026-08-26
Status: **MECHANICAL OPTIMIZATION / STRATEGY-NEUTRAL UNTIL RUNTIME MEASURED**

## Motivation

The public Qwen/NVARC-style solver computes probabilities over the full model vocabulary but ultimately needs only a tiny subset of values in two hot paths:

1. DFS expansion evaluates the fixed ARC output-token set;
2. teacher-forced rescoring needs the log-probability of the known target token at each answer position.

A user-side Kaggle workspace patch also described moving these reductions onto GPU before returning values to CPU. The repository now encodes the mathematical equivalence independently rather than trusting an unmeasured patch.

## Reference model scale

The official Qwen3-4B configuration currently reports vocabulary size **151,936**.

The public NVARC ARC vocabulary contains **12** output/control token ids. Therefore retaining only those DFS columns reduces the number of per-row values that need to cross GPU→CPU by a theoretical factor of:

`151936 / 12 = 12,661.33x`

For teacher-forced scoring, only one target-token value is needed per answer position after the full-vocabulary normalizer is computed, so the materialized/transfer output can shrink from `vocab_size` values to one value per position.

This is an **element-count / transfer-volume observation**, not a measured end-to-end speedup. The full-vocabulary normalization itself still has to be computed.

## Semantics contract

The optimization is permitted only if all of these remain unchanged:

- full-vocabulary logsumexp/log-softmax normalizer;
- ARC token ids;
- candidate threshold;
- candidate ordering;
- DFS recursion/order;
- teacher-forced target ids and masks;
- final NLL aggregation/ranking;
- decoding budget and global deadline.

The safe transformation is:

> compute the same full-vocabulary normalizer on device, retain/gather only the token values actually consumed downstream, and transfer that small result rather than the full vocabulary tensor.

## Regression oracle

`src/arcsolver/logit_projection.py` provides CPU NumPy reference helpers for:

- legacy full-vocabulary ARC-token NLL;
- projected ARC-token NLL;
- legacy full-vocabulary teacher-forced NLL;
- gathered target-token teacher-forced NLL.

`tests/test_logit_projection.py` verifies on deterministic random tensors and extreme logits that:

- projected ARC-token NLL equals the full-vocabulary reference to numerical tolerance;
- candidate ordering is identical;
- gathered teacher-forced NLL equals the full-vocabulary reference;
- aggregate answer ranking is identical;
- the logsumexp implementation remains stable for very large logits.

No Kaggle score claim is attached to this optimization until a controlled runtime experiment exists.

## Why it matters for M1/M2

Runtime/coverage is itself a possible score bottleneck: a solver that spends less time moving huge logits can devote the fixed sandbox budget to completing more tasks or preserving the original search budget with more margin.

However, this optimization does **not** create new reasoning capability by itself. It should be classified separately from candidate-discovery, selection, or representation improvements. If it only lowers runtime without changing completed task coverage, it is engineering headroom rather than an ARC reasoning result.

## Source boundary

The broad public solver structure and 12-token ARC vocabulary are prior art from public NVARC/Qwen-family notebooks. The regression implementation in this repository is an independent small mathematical test harness; it does not reproduce a full external notebook.
