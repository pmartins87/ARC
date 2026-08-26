from __future__ import annotations

import numpy as np
import pytest

from arcsolver.logit_projection import (
    gathered_teacher_forced_nll_numpy,
    legacy_arc_token_nll_numpy,
    legacy_teacher_forced_nll_numpy,
    projected_arc_token_nll_numpy,
    transfer_reduction_factor,
)


def test_arc_token_projection_matches_full_vocab_reference() -> None:
    rng = np.random.default_rng(20260826)
    logits = rng.normal(size=(7, 257)) * 4.0
    scores = rng.uniform(0.0, 5.0, size=7)
    token_ids = [0, 1, 2, 3, 5, 8, 13, 21, 55, 89, 144, 233]

    reference = legacy_arc_token_nll_numpy(logits, scores, token_ids)
    projected = projected_arc_token_nll_numpy(logits, scores, token_ids)

    np.testing.assert_allclose(projected, reference, rtol=0.0, atol=1e-12)
    np.testing.assert_array_equal(np.argsort(projected, axis=1), np.argsort(reference, axis=1))


def test_teacher_forced_gather_matches_full_vocab_reference() -> None:
    rng = np.random.default_rng(17)
    logits = rng.normal(size=(4, 23, 311)) * 3.0
    targets = rng.integers(0, logits.shape[-1], size=logits.shape[:2])

    reference = legacy_teacher_forced_nll_numpy(logits, targets)
    gathered = gathered_teacher_forced_nll_numpy(logits, targets)

    np.testing.assert_allclose(gathered, reference, rtol=0.0, atol=1e-12)
    np.testing.assert_allclose(gathered.sum(axis=1), reference.sum(axis=1), rtol=0.0, atol=1e-11)
    np.testing.assert_array_equal(np.argsort(gathered.sum(axis=1)), np.argsort(reference.sum(axis=1)))


def test_large_logits_are_numerically_stable() -> None:
    logits = np.array([[10000.0, 9999.0, -10000.0, 0.0], [-9000.0, -8999.0, -9001.0, -8998.0]])
    scores = [0.0, 1.25]
    token_ids = [0, 3]

    reference = legacy_arc_token_nll_numpy(logits, scores, token_ids)
    projected = projected_arc_token_nll_numpy(logits, scores, token_ids)

    assert np.isfinite(projected).all()
    np.testing.assert_allclose(projected, reference, rtol=0.0, atol=1e-12)


def test_transfer_reduction_factor() -> None:
    assert transfer_reduction_factor(151936, 12) == pytest.approx(12661.333333333334)
    with pytest.raises(ValueError):
        transfer_reduction_factor(10, 11)
