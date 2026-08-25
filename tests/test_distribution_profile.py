from __future__ import annotations

import pytest

from arcsolver.distribution_profile import compare_visible_splits, percentile_nearest_rank, profile_task_payloads


def test_percentile_nearest_rank() -> None:
    assert percentile_nearest_rank([1, 2, 3, 4, 5], 0.0) == 1
    assert percentile_nearest_rank([1, 2, 3, 4, 5], 0.5) == 3
    assert percentile_nearest_rank([1, 2, 3, 4, 5], 0.9) == 5
    assert percentile_nearest_rank([1, 2, 3, 4, 5], 1.0) == 5


def test_profile_ignores_test_outputs_even_if_present() -> None:
    tasks = [
        {
            "train": [
                {"input": [[0, 1]], "output": [[1, 0]]},
                {"input": [[0], [2]], "output": [[2], [0]]},
            ],
            "test": [
                {"input": [[0, 1], [2, 0]], "output": "INTENTIONALLY_NOT_A_GRID"},
                {"input": [[3]], "output": None},
            ],
        },
        {
            "train": [{"input": [[0]], "output": [[1]]}],
            "test": [{"input": [[0, 0, 2]]}],
        },
    ]
    profile = profile_task_payloads(tasks)
    assert profile.tasks == 2
    assert profile.train_demo_pairs == 3
    assert profile.test_input_slots == 3
    assert profile.multi_test_tasks == 1
    assert profile.multi_test_task_fraction == 0.5
    assert profile.test_input_area.median == 3.0
    assert profile.test_input_colors.median == 2.0


def test_compare_reports_eval_over_train_ratios() -> None:
    training = profile_task_payloads(
        [{"train": [{"input": [[0]], "output": [[0]]}], "test": [{"input": [[0]]}]}]
    )
    evaluation = profile_task_payloads(
        [
            {
                "train": [{"input": [[0, 1]], "output": [[0, 1]]}],
                "test": [{"input": [[0, 1]]}, {"input": [[0, 1]]}],
            }
        ]
    )
    report = compare_visible_splits(training, evaluation)
    ratios = report["evaluation_over_training"]
    assert ratios["test_input_area_median_ratio"] == 2.0
    assert ratios["test_input_color_median_ratio"] == 2.0
    assert evaluation.multi_test_task_fraction == 1.0
    assert training.multi_test_task_fraction == 0.0
    assert ratios["multi_test_task_fraction_ratio"] is None
    assert "Test outputs are never read" in report["leakage_guard"]


def test_invalid_empty_tasks() -> None:
    with pytest.raises(ValueError, match="at least one task"):
        profile_task_payloads([])
