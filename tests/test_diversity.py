from arcsolver.diversity import compare_grids, summarize_attempt_pairs, summarize_candidate_diversity


def test_compare_grids():
    a = [[0, 1], [1, 0]]
    b = [[0, 1], [0, 1]]
    result = compare_grids(a, b)
    assert result.exact_duplicate is False
    assert result.same_shape is True
    assert result.same_color_signature is True
    assert result.normalized_cell_disagreement == 0.5


def test_candidate_summary():
    a = [[0, 1], [1, 0]]
    b = [[0, 1], [1, 0]]
    c = [[0, 1], [0, 0]]
    d = [[0, 1, 0]]
    result = summarize_candidate_diversity([a, b, c, d], near_duplicate_threshold=0.25)
    assert result.candidates == 4
    assert result.unique_exact_candidates == 3
    assert result.exact_duplicate_fraction == 0.25
    assert result.distinct_shapes == 2
    assert result.modal_shape_fraction == 0.75
    assert result.same_shape_pair_fraction == 0.5
    assert result.median_same_shape_cell_disagreement == 0.25


def test_attempt_summary():
    pairs = [
        ([[1]], [[1]]),
        ([[1, 0]], [[1, 1]]),
        ([[1]], [[1, 0]]),
        ([[1, 0]], [[2, 0]]),
    ]
    result = summarize_attempt_pairs(pairs)
    assert result.outputs == 4
    assert result.exact_duplicate_outputs == 1
    assert result.different_shape_outputs == 1
    assert result.same_shape_outputs == 3
    assert result.median_same_shape_cell_disagreement == 0.5
