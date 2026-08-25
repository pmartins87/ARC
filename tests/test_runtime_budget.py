import math

import pytest

from arcsolver.runtime_budget import (
    constant_duration_capacity,
    equal_task_seconds_for_target_coverage,
    lower_bound_speedup_for_capacity,
    minimum_uniform_speedup_for_fcfs_completion,
    score_ceiling_from_coverage,
    simulate_fcfs,
)


def test_fcfs_counts_completed_partial_and_never_started_tasks():
    tasks = [(f"t{i}", 6.0) for i in range(5)]
    report = simulate_fcfs(tasks, workers=2, budget_seconds=10.0)

    assert report.total_tasks == 5
    assert report.completed_tasks == 2
    assert report.started_but_incomplete_tasks == 2
    assert report.never_started_tasks == 1
    assert report.completion_fraction == 0.4
    assert report.worker_busy_seconds == (10.0, 10.0)
    assert report.worker_utilization == (1.0, 1.0)

    completed = [item.task_id for item in report.schedule if item.completed]
    incomplete = [item.task_id for item in report.schedule if not item.completed]
    assert completed == ["t0", "t1"]
    assert incomplete == ["t2", "t3"]


def test_speedup_can_turn_partial_coverage_into_full_completion():
    tasks = [(f"t{i}", 6.0) for i in range(4)]
    report = simulate_fcfs(tasks, workers=2, budget_seconds=10.0, speedup=1.2)

    assert report.completed_tasks == 4
    assert report.started_but_incomplete_tasks == 0
    assert report.never_started_tasks == 0
    assert math.isclose(report.worker_busy_seconds[0], 10.0)
    assert math.isclose(report.worker_busy_seconds[1], 10.0)


def test_aggregate_capacity_bound_can_understate_fifo_speedup_need():
    tasks = [("a", 8.0), ("b", 8.0), ("c", 8.0), ("d", 1.0), ("e", 1.0)]

    lower = lower_bound_speedup_for_capacity(tasks, workers=2, budget_seconds=10.0)
    exact_fcfs = minimum_uniform_speedup_for_fcfs_completion(
        tasks, workers=2, budget_seconds=10.0, tolerance=1e-7
    )

    assert math.isclose(lower, 1.3)
    assert exact_fcfs > lower
    assert math.isclose(exact_fcfs, 1.6, rel_tol=0, abs_tol=1e-5)


def test_score_ceiling_decomposes_coverage_without_claiming_generalization():
    assert score_ceiling_from_coverage(completion_fraction=0.75) == 0.75
    assert score_ceiling_from_coverage(
        completion_fraction=0.75, processed_exact_rate=0.4
    ) == pytest.approx(0.30)


def test_equal_duration_helpers_are_discrete_worker_models():
    # Each worker can finish three 3-second tasks in ten seconds.
    assert constant_duration_capacity(workers=4, budget_seconds=10, task_seconds=3) == 12

    # To finish at least 80/100 tasks on four workers, each worker needs 20 slots.
    assert equal_task_seconds_for_target_coverage(
        task_count=100,
        workers=4,
        budget_seconds=1000,
        target_coverage=0.80,
    ) == 50.0


def test_invalid_runtime_inputs_fail_closed():
    with pytest.raises(ValueError):
        simulate_fcfs([("x", 1.0)], workers=0, budget_seconds=10)
    with pytest.raises(ValueError):
        simulate_fcfs([("x", -1.0)], workers=1, budget_seconds=10)
    with pytest.raises(ValueError):
        simulate_fcfs([("x", 1.0), ("x", 2.0)], workers=1, budget_seconds=10)
    with pytest.raises(ValueError):
        score_ceiling_from_coverage(completion_fraction=1.1)
