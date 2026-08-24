from __future__ import annotations

import pytest

from arcsolver.compare import compare_submissions, diagnose_submission


def test_diagnostics_count_second_attempt_rescues_and_duplicates() -> None:
    solutions = {
        "t1": [[[1]], [[2]]],
        "t2": [[[3]]],
    }
    submission = {
        "t1": [
            {"attempt_1": [[0]], "attempt_2": [[1]]},
            {"attempt_1": [[2]], "attempt_2": [[2]]},
        ],
        "t2": [{"attempt_1": [[0]], "attempt_2": [[0]]}],
    }

    diagnostics = diagnose_submission("x", submission, solutions)

    assert diagnostics.correct_outputs_pass1 == 1
    assert diagnostics.correct_outputs_pass2 == 2
    assert diagnostics.total_outputs == 3
    assert diagnostics.second_attempt_rescues == 1
    assert diagnostics.duplicate_attempt_outputs == 2
    assert diagnostics.solved_tasks_pass1 == 0
    assert diagnostics.solved_tasks_pass2 == 1
    assert diagnostics.pass1 == pytest.approx(1 / 3)
    assert diagnostics.pass2 == pytest.approx(2 / 3)


def test_complementarity_reports_unique_wins_and_oracle_union() -> None:
    solutions = {
        "a": [[[1]]],
        "b": [[[2]]],
        "c": [[[3]]],
        "d": [[[4]]],
    }
    solver_a = {
        "a": [{"attempt_1": [[1]], "attempt_2": [[0]]}],
        "b": [{"attempt_1": [[2]], "attempt_2": [[0]]}],
        "c": [{"attempt_1": [[0]], "attempt_2": [[0]]}],
        "d": [{"attempt_1": [[0]], "attempt_2": [[0]]}],
    }
    solver_b = {
        "a": [{"attempt_1": [[1]], "attempt_2": [[9]]}],
        "b": [{"attempt_1": [[0]], "attempt_2": [[0]]}],
        "c": [{"attempt_1": [[0]], "attempt_2": [[3]]}],
        "d": [{"attempt_1": [[0]], "attempt_2": [[0]]}],
    }

    report = compare_submissions("A", solver_a, "B", solver_b, solutions)

    assert report.both_correct_outputs == 1
    assert report.only_a_correct_outputs == 1
    assert report.only_b_correct_outputs == 1
    assert report.neither_correct_outputs == 1
    assert report.oracle_union_correct_outputs == 3
    assert report.oracle_union_pass2 == pytest.approx(0.75)
    assert report.correct_set_jaccard == pytest.approx(1 / 3)
    assert report.marginal_union_gain_over_best == pytest.approx(0.25)
    assert report.both_solved_tasks == 1
    assert report.only_a_solved_tasks == 1
    assert report.only_b_solved_tasks == 1
    assert report.neither_solved_tasks == 1
    assert report.oracle_union_solved_tasks == 3


def test_validation_rejects_missing_task() -> None:
    solutions = {"a": [[[1]]], "b": [[[2]]]}
    submission = {"a": [{"attempt_1": [[1]], "attempt_2": [[1]]}]}

    with pytest.raises(ValueError, match="task-id mismatch"):
        diagnose_submission("x", submission, solutions)
