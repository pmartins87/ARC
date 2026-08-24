from __future__ import annotations

import pytest

from arcsolver.error_audit import audit_submission_structure


def test_structural_audit_separates_shape_and_content_failures() -> None:
    solutions = {
        "a": [[[1, 1]]],
        "b": [[[2], [2]]],
        "c": [[[3]]],
    }
    test_inputs = {
        "a": [[[0, 0]]],        # same shape; truth colors introduce 1
        "b": [[[2, 0]]],        # different shape; truth colors subset input
        "c": [[[3]]],           # same shape; truth colors subset input
    }
    submission = {
        "a": [{"attempt_1": [[0, 0]], "attempt_2": [[1, 1]]}],  # rescued
        "b": [{"attempt_1": [[2, 0]], "attempt_2": [[0, 2]]}],  # both wrong shape
        "c": [{"attempt_1": [[0]], "attempt_2": [[0]]}],        # right shape, wrong content
    }

    report = audit_submission_structure("s", submission, solutions, test_inputs)
    data = report.to_dict()

    assert data["total_outputs"] == 3
    assert data["correct_outputs_pass2"] == 1
    assert data["pass_at_2"] == pytest.approx(1 / 3)
    assert data["same_shape_targets"] == 2
    assert data["different_shape_targets"] == 1
    assert data["correct_same_shape_targets"] == 1
    assert data["correct_different_shape_targets"] == 0
    assert data["at_least_one_attempt_right_shape"] == 2
    assert data["both_attempts_wrong_shape"] == 1
    assert data["shape_right_but_content_wrong"] == 1
    assert data["second_attempt_rescues"] == 1
    assert data["duplicate_attempt_outputs"] == 1
    assert data["solved_task_ids"] == ("a",)
    assert data["unsolved_task_ids"] == ("b", "c")
    assert data["failure_reason_counts"] == {
        "both_attempts_wrong_shape": 1,
        "shape_right_content_wrong": 1,
    }


def test_structural_audit_rejects_missing_test_input_tasks() -> None:
    solutions = {"a": [[[1]]], "b": [[[2]]]}
    submission = {
        "a": [{"attempt_1": [[1]], "attempt_2": [[0]]}],
        "b": [{"attempt_1": [[2]], "attempt_2": [[0]]}],
    }
    with pytest.raises(ValueError, match="test-input task-id mismatch"):
        audit_submission_structure("s", submission, solutions, {"a": [[[1]]]})
