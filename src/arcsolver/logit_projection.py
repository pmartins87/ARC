from __future__ import annotations

from collections.abc import Sequence

import numpy as np


def legacy_arc_token_nll_numpy(
    logits: np.ndarray,
    base_scores: Sequence[float],
    token_ids: Sequence[int],
) -> np.ndarray:
    """Reference semantics for the old full-vocabulary NLL path.

    This NumPy implementation exists as a CPU-only oracle for regression tests.
    It computes full-vocabulary log-softmax first and only then selects the ARC
    vocabulary columns, matching the mathematical operation used by the public
    baseline before its GPU/CPU transfer optimization.
    """
    values = np.asarray(logits, dtype=np.float64)
    scores = np.asarray(base_scores, dtype=np.float64).reshape(-1, 1)
    if values.ndim != 2:
        raise ValueError("logits must be rank 2 [batch, vocab]")
    if values.shape[0] != scores.shape[0]:
        raise ValueError("base_scores length must match batch size")
    ids = np.asarray(token_ids, dtype=np.int64)
    if ids.ndim != 1 or ids.size == 0:
        raise ValueError("token_ids must be a non-empty 1D sequence")
    if np.any(ids < 0) or np.any(ids >= values.shape[1]):
        raise ValueError("token id outside vocabulary")

    max_values = values.max(axis=-1, keepdims=True)
    logsumexp = max_values + np.log(np.exp(values - max_values).sum(axis=-1, keepdims=True))
    log_probs = values - logsumexp
    return scores - log_probs[:, ids]


def projected_arc_token_nll_numpy(
    logits: np.ndarray,
    base_scores: Sequence[float],
    token_ids: Sequence[int],
) -> np.ndarray:
    """Equivalent NLL result while materializing only selected token columns.

    The normalizer still uses the complete vocabulary, so probabilities are
    unchanged. Only the selected log-probability columns are retained after the
    normalizer is computed. This models the intended GPU optimization: perform
    full-vocabulary reduction on-device, transfer only the small ARC-token slice.
    """
    values = np.asarray(logits, dtype=np.float64)
    scores = np.asarray(base_scores, dtype=np.float64).reshape(-1, 1)
    if values.ndim != 2:
        raise ValueError("logits must be rank 2 [batch, vocab]")
    if values.shape[0] != scores.shape[0]:
        raise ValueError("base_scores length must match batch size")
    ids = np.asarray(token_ids, dtype=np.int64)
    if ids.ndim != 1 or ids.size == 0:
        raise ValueError("token_ids must be a non-empty 1D sequence")
    if np.any(ids < 0) or np.any(ids >= values.shape[1]):
        raise ValueError("token id outside vocabulary")

    max_values = values.max(axis=-1, keepdims=True)
    logsumexp = max_values + np.log(np.exp(values - max_values).sum(axis=-1, keepdims=True))
    selected_logits = values[:, ids]
    selected_log_probs = selected_logits - logsumexp
    return scores - selected_log_probs


def legacy_teacher_forced_nll_numpy(logits: np.ndarray, target_ids: np.ndarray) -> np.ndarray:
    """Reference teacher-forced token NLL using full log-probability tensors."""
    values = np.asarray(logits, dtype=np.float64)
    targets = np.asarray(target_ids, dtype=np.int64)
    if values.ndim != 3:
        raise ValueError("logits must be rank 3 [batch, time, vocab]")
    if targets.shape != values.shape[:2]:
        raise ValueError("target_ids must have shape [batch, time]")
    if np.any(targets < 0) or np.any(targets >= values.shape[-1]):
        raise ValueError("target id outside vocabulary")

    max_values = values.max(axis=-1, keepdims=True)
    logsumexp = max_values + np.log(np.exp(values - max_values).sum(axis=-1, keepdims=True))
    log_probs = values - logsumexp
    batch = np.arange(values.shape[0])[:, None]
    time = np.arange(values.shape[1])[None, :]
    return -log_probs[batch, time, targets]


def gathered_teacher_forced_nll_numpy(logits: np.ndarray, target_ids: np.ndarray) -> np.ndarray:
    """Equivalent teacher-forced NLL retaining only target-token logits.

    The full-vocabulary logsumexp remains mathematically identical, but the
    output tensor is [batch, time] rather than [batch, time, vocab].
    """
    values = np.asarray(logits, dtype=np.float64)
    targets = np.asarray(target_ids, dtype=np.int64)
    if values.ndim != 3:
        raise ValueError("logits must be rank 3 [batch, time, vocab]")
    if targets.shape != values.shape[:2]:
        raise ValueError("target_ids must have shape [batch, time]")
    if np.any(targets < 0) or np.any(targets >= values.shape[-1]):
        raise ValueError("target id outside vocabulary")

    max_values = values.max(axis=-1, keepdims=True)
    logsumexp = max_values + np.log(np.exp(values - max_values).sum(axis=-1, keepdims=True))
    batch = np.arange(values.shape[0])[:, None]
    time = np.arange(values.shape[1])[None, :]
    selected_logits = values[batch, time, targets]
    return -(selected_logits - logsumexp[..., 0])


def transfer_reduction_factor(vocab_size: int, selected_tokens: int) -> float:
    """Theoretical element-count reduction for a selected-token transfer."""
    if vocab_size <= 0 or selected_tokens <= 0 or selected_tokens > vocab_size:
        raise ValueError("require 0 < selected_tokens <= vocab_size")
    return vocab_size / selected_tokens
