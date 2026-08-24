from __future__ import annotations

import pytest

from arcsolver.portfolio import analyze_portfolio


def _submission(correct: set[str]) -> dict[str, list[dict[str, list[list[int]]]]]:
    truths = {"a": 1, "b": 2, "c": 3, "d": 4}
    return {
        task_id: [
            {
                "attempt_1": [[truth if task_id in correct else 0]],
                "attempt_2": [[9]],
            }
        ]
        for task_id, truth in truths.items()
    }


def _solutions() -> dict[str, list[list[list[int]]]]:
    return {
        "a": [[[1]]],
        "b": [[[2]]],
        "c": [[[3]]],
        "d": [[[4]]],
    }


def test_portfolio_reports_unique_coverage_and_oracle_union() -> None:
    submissions = {
        "s1": _submission({"a", "b"}),
        "s2": _submission({"b", "c"}),
        "s3": _submission({"d"}),
    }

    report = analyze_portfolio(submissions, _solutions())

    assert report.oracle_union_correct_outputs == 4
    assert report.oracle_union_pass_at_2 == pytest.approx(1.0)
    rows = {row.name: row for row in report.solvers}
    assert rows["s1"].correct_outputs == 2
    assert rows["s2"].correct_outputs == 2
    assert rows["s3"].correct_outputs == 1
    assert rows["s1"].unique_outputs_vs_rest == 1
    assert rows["s2"].unique_outputs_vs_rest == 1
    assert rows["s3"].unique_outputs_vs_rest == 1
    assert rows["s1"].leave_one_out_union_loss == 1


def test_cost_aware_greedy_and_exact_budget_choice() -> None:
    submissions = {
        "s1": _submission({"a", "b"}),
        "s2": _submission({"b", "c"}),
        "s3": _submission({"d"}),
    }
    runtimes = {"s1": 10.0, "s2": 20.0, "s3": 5.0}

    report = analyze_portfolio(
        submissions,
        _solutions(),
        runtimes_seconds=runtimes,
        budgets_seconds=(15.0, 35.0),
    )

    assert [step.solver for step in report.greedy_order] == ["s1", "s3", "s2"]
    assert [step.cumulative_covered_outputs for step in report.greedy_order] == [2, 3, 4]

    choices = {choice.budget_seconds: choice for choice in report.budget_choices}
    assert choices[15.0].solvers == ("s1", "s3")
    assert choices[15.0].covered_outputs == 3
    assert choices[15.0].runtime_seconds == pytest.approx(15.0)
    assert choices[35.0].solvers == ("s1", "s2", "s3")
    assert choices[35.0].covered_outputs == 4


def test_budget_requires_complete_runtime_mapping() -> None:
    submissions = {
        "s1": _submission({"a"}),
        "s2": _submission({"b"}),
    }
    with pytest.raises(ValueError, match="runtime-name mismatch"):
        analyze_portfolio(
            submissions,
            _solutions(),
            runtimes_seconds={"s1": 1.0},
            budgets_seconds=(10.0,),
        )


def test_budget_without_runtime_is_rejected() -> None:
    with pytest.raises(ValueError, match="requires runtimes"):
        analyze_portfolio(
            {"s1": _submission({"a"})},
            _solutions(),
            budgets_seconds=(10.0,),
        )
