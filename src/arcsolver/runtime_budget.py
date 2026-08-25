from __future__ import annotations

from dataclasses import asdict, dataclass
import heapq
from math import ceil
from typing import Mapping, Sequence


@dataclass(frozen=True)
class ScheduledTask:
    task_id: str
    worker: int
    start_seconds: float
    planned_duration_seconds: float
    finish_seconds: float
    completed: bool


@dataclass(frozen=True)
class RuntimeSimulation:
    workers: int
    budget_seconds: float
    total_tasks: int
    completed_tasks: int
    started_but_incomplete_tasks: int
    never_started_tasks: int
    completion_fraction: float
    worker_busy_seconds: tuple[float, ...]
    worker_utilization: tuple[float, ...]
    schedule: tuple[ScheduledTask, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def simulate_fcfs(
    task_durations: Mapping[str, float] | Sequence[tuple[str, float]],
    *,
    workers: int,
    budget_seconds: float,
    speedup: float = 1.0,
) -> RuntimeSimulation:
    """Simulate a shared FIFO task queue on homogeneous workers.

    This intentionally models only coarse scheduling/coverage. A task that starts
    but would finish after the global deadline consumes the remaining worker
    budget and is counted incomplete. That matches the competition-relevant fact
    that partial work which never produces a usable final output does not earn
    exact ARC credit.
    """
    if workers < 1:
        raise ValueError("workers must be >= 1")
    if budget_seconds <= 0:
        raise ValueError("budget_seconds must be > 0")
    if speedup <= 0:
        raise ValueError("speedup must be > 0")

    items = list(task_durations.items() if isinstance(task_durations, Mapping) else task_durations)
    seen: set[str] = set()
    normalized: list[tuple[str, float]] = []
    for task_id, duration in items:
        if task_id in seen:
            raise ValueError(f"duplicate task id: {task_id}")
        seen.add(task_id)
        duration = float(duration)
        if duration <= 0:
            raise ValueError(f"{task_id}: duration must be > 0")
        normalized.append((str(task_id), duration / speedup))

    # Heap entries are (available_time, worker_id). Worker id makes ties deterministic.
    heap: list[tuple[float, int]] = [(0.0, worker) for worker in range(workers)]
    heapq.heapify(heap)
    busy = [0.0 for _ in range(workers)]
    schedule: list[ScheduledTask] = []
    completed = 0
    incomplete = 0
    next_index = 0

    while next_index < len(normalized):
        available, worker = heapq.heappop(heap)
        if available >= budget_seconds:
            # This worker cannot begin any more work. Leave it exhausted.
            heapq.heappush(heap, (budget_seconds, worker))
            if all(time >= budget_seconds for time, _ in heap):
                break
            continue

        task_id, duration = normalized[next_index]
        next_index += 1
        finish = available + duration
        is_complete = finish <= budget_seconds
        consumed = duration if is_complete else budget_seconds - available
        busy[worker] += consumed
        schedule.append(
            ScheduledTask(
                task_id=task_id,
                worker=worker,
                start_seconds=available,
                planned_duration_seconds=duration,
                finish_seconds=min(finish, budget_seconds),
                completed=is_complete,
            )
        )
        if is_complete:
            completed += 1
            heapq.heappush(heap, (finish, worker))
        else:
            incomplete += 1
            heapq.heappush(heap, (budget_seconds, worker))

    never_started = len(normalized) - next_index
    utilization = tuple(value / budget_seconds for value in busy)
    return RuntimeSimulation(
        workers=workers,
        budget_seconds=float(budget_seconds),
        total_tasks=len(normalized),
        completed_tasks=completed,
        started_but_incomplete_tasks=incomplete,
        never_started_tasks=never_started,
        completion_fraction=completed / len(normalized) if normalized else 1.0,
        worker_busy_seconds=tuple(busy),
        worker_utilization=utilization,
        schedule=tuple(schedule),
    )


def lower_bound_speedup_for_capacity(
    task_durations: Mapping[str, float] | Sequence[tuple[str, float]],
    *,
    workers: int,
    budget_seconds: float,
) -> float:
    """Return the idealized work-conservation lower bound on required speedup.

    This ignores FIFO/load-imbalance effects, so a real schedule may need more.
    A value <=1 means aggregate worker-seconds are sufficient in principle.
    """
    items = list(task_durations.items() if isinstance(task_durations, Mapping) else task_durations)
    if workers < 1:
        raise ValueError("workers must be >= 1")
    if budget_seconds <= 0:
        raise ValueError("budget_seconds must be > 0")
    durations = [float(duration) for _, duration in items]
    if any(duration <= 0 for duration in durations):
        raise ValueError("all durations must be > 0")
    if not durations:
        return 0.0
    aggregate = sum(durations) / (workers * budget_seconds)
    longest = max(durations) / budget_seconds
    return max(aggregate, longest)


def minimum_uniform_speedup_for_fcfs_completion(
    task_durations: Mapping[str, float] | Sequence[tuple[str, float]],
    *,
    workers: int,
    budget_seconds: float,
    tolerance: float = 1e-4,
    max_speedup: float = 1024.0,
) -> float:
    """Binary-search the smallest uniform speedup that completes the FIFO queue."""
    items = list(task_durations.items() if isinstance(task_durations, Mapping) else task_durations)
    if not items:
        return 0.0
    if tolerance <= 0:
        raise ValueError("tolerance must be > 0")

    low = max(0.0, lower_bound_speedup_for_capacity(items, workers=workers, budget_seconds=budget_seconds))
    # Speedup smaller than 1 is meaningful: it says the observed durations could
    # become slower and still fit. Start high at at least 1 for stable bracketing.
    high = max(1.0, low)
    while simulate_fcfs(items, workers=workers, budget_seconds=budget_seconds, speedup=high).completed_tasks < len(items):
        high *= 2.0
        if high > max_speedup:
            raise ValueError("completion not bracketed below max_speedup")

    for _ in range(80):
        if high - low <= tolerance:
            break
        mid = (low + high) / 2.0
        report = simulate_fcfs(items, workers=workers, budget_seconds=budget_seconds, speedup=mid)
        if report.completed_tasks == len(items):
            high = mid
        else:
            low = mid
    return high


def constant_duration_capacity(*, workers: int, budget_seconds: float, task_seconds: float) -> int:
    """Maximum count of equal-duration whole tasks under ideal worker packing."""
    if workers < 1 or budget_seconds <= 0 or task_seconds <= 0:
        raise ValueError("workers, budget_seconds and task_seconds must be positive")
    return workers * int(budget_seconds // task_seconds)


def score_ceiling_from_coverage(*, completion_fraction: float, processed_exact_rate: float = 1.0) -> float:
    """Upper bound on overall exact score when unprocessed tasks necessarily miss.

    `processed_exact_rate=1` gives the pure scheduling ceiling. Passing an
    observed exact rate on processed tasks gives a simple decomposition estimate;
    it is not a generalization forecast.
    """
    if not 0.0 <= completion_fraction <= 1.0:
        raise ValueError("completion_fraction must be in [0, 1]")
    if not 0.0 <= processed_exact_rate <= 1.0:
        raise ValueError("processed_exact_rate must be in [0, 1]")
    return completion_fraction * processed_exact_rate


def equal_task_seconds_for_target_coverage(
    *, task_count: int, workers: int, budget_seconds: float, target_coverage: float
) -> float:
    """Per-task duration required to complete at least target coverage, equal-task model."""
    if task_count < 0:
        raise ValueError("task_count must be >= 0")
    if workers < 1 or budget_seconds <= 0:
        raise ValueError("workers and budget_seconds must be positive")
    if not 0.0 < target_coverage <= 1.0:
        raise ValueError("target_coverage must be in (0, 1]")
    if task_count == 0:
        return float("inf")
    required_tasks = ceil(task_count * target_coverage)
    slots_per_worker = ceil(required_tasks / workers)
    return budget_seconds / slots_per_worker
