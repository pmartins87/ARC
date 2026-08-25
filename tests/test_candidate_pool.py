from arcsolver.candidate_pool import (
    audit_candidate_pools,
    candidate_features,
    canonical_grid,
    rank_score_full_probmul_3,
    rank_score_kgmon,
)


def _sample(solution, beam_score, score_aug):
    return {
        "solution": solution,
        "beam_score": beam_score,
        "score_aug": score_aug,
    }


def test_candidate_features_deduplicate_exact_grids_and_count_votes():
    samples = [
        _sample([[1, 2]], 1.0, [1.0, 2.0]),
        _sample([[1, 2]], 2.0, [2.0, 3.0]),
        _sample([[2, 1]], 0.5, [0.5, 0.7]),
    ]
    candidates = candidate_features(samples)

    assert len(candidates) == 2
    assert candidates[0].votes == 2
    assert candidates[0].beam_scores == [1.0, 2.0]
    assert candidates[0].score_aug == [[1.0, 2.0], [2.0, 3.0]]
    assert canonical_grid(candidates[1].solution) == ((2, 1),)


def test_public_selectors_can_disagree_on_top_two():
    # Two high-vote but weak-likelihood distractors beat truth under KGMon.
    # Strong likelihood evidence makes truth rank first under probmul_3.
    samples = [
        _sample([[1]], 2.0, [2.0, 2.0]),
        _sample([[2]], 2.9, [2.9, 2.9]),
        _sample([[2]], 2.9, [2.9, 2.9]),
        _sample([[3]], 2.8, [2.8, 2.8]),
        _sample([[3]], 2.8, [2.8, 2.8]),
    ]
    candidates = candidate_features(samples)

    kgmon = rank_score_kgmon(candidates)
    probmul = rank_score_full_probmul_3(candidates)

    assert canonical_grid(kgmon[0]) == ((3,),)
    assert canonical_grid(kgmon[1]) == ((2,),)
    assert canonical_grid(kgmon[2]) == ((1,),)
    assert canonical_grid(probmul[0]) == ((1,),)


def test_audit_separates_pool_oracle_selection_and_missing_coverage():
    solutions = {
        "aaaa0000": [[[1]], [[4]]],
        "bbbb0000": [[[7]]],
    }
    pools = {
        "aaaa0000_0": [
            _sample([[1]], 2.0, [2.0, 2.0]),
            _sample([[2]], 2.9, [2.9, 2.9]),
            _sample([[2]], 2.9, [2.9, 2.9]),
            _sample([[3]], 2.8, [2.8, 2.8]),
            _sample([[3]], 2.8, [2.8, 2.8]),
        ],
        "aaaa0000_1": [
            _sample([[5]], 1.0, [1.0, 1.0]),
        ],
        # bbbb0000_0 is intentionally missing: it must count as a miss.
    }

    report = audit_candidate_pools(pools, solutions)

    assert report.total_outputs == 3
    assert report.processed_outputs == 2
    assert report.missing_outputs == 1
    assert report.missing_output_keys == ["bbbb0000_0"]
    assert report.raw_samples == 6
    assert report.unique_candidates == 4
    assert abs(report.duplicate_sample_fraction - (1.0 / 3.0)) < 1e-12

    assert report.oracle_exact_hits == 1
    assert report.oracle_pass_at_2 == 1.0 / 3.0

    assert report.selectors["score_kgmon"].exact_hits == 0
    assert report.selectors["score_kgmon"].truth_in_pool_not_top2 == 1
    assert report.selectors["score_kgmon"].correct_rank_median == 3.0
    assert report.selector_gap["score_kgmon"] == 1.0 / 3.0

    assert report.selectors["score_full_probmul_3"].exact_hits == 1
    assert report.selectors["score_full_probmul_3"].pass_at_2 == 1.0 / 3.0
    assert report.selector_gap["score_full_probmul_3"] == 0.0
    assert report.selector_unique_rescues["score_full_probmul_3"] == 1

    assert report.top2_disagreement_outputs == 1
    assert report.top2_disagreement_rate == 0.5


def test_audit_rejects_dataset_mismatch_instead_of_silently_scoring():
    solutions = {"aaaa0000": [[[1]]]}
    pools = {
        "aaaa0000_0": [_sample([[1]], 1.0, [1.0])],
        "foreign_0": [_sample([[1]], 1.0, [1.0])],
    }

    try:
        audit_candidate_pools(pools, solutions)
    except ValueError as exc:
        assert "unknown output keys" in str(exc)
    else:
        raise AssertionError("dataset mismatch should fail closed")
