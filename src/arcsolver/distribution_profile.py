from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import mean, median
import json
from typing import Any, Iterable

Grid = list[list[int]]


def grid_area(grid: Grid) -> int:
    if not isinstance(grid, list) or not grid or not all(isinstance(row, list) and row for row in grid):
        raise ValueError("grid must be a non-empty rectangular list")
    width = len(grid[0])
    if any(len(row) != width for row in grid):
        raise ValueError("grid must be rectangular")
    return len(grid) * width


def grid_color_count(grid: Grid) -> int:
    grid_area(grid)
    return len({int(cell) for row in grid for cell in row})


def percentile_nearest_rank(values: Iterable[int], q: float) -> float:
    data = sorted(values)
    if not data:
        raise ValueError("cannot compute percentile of empty data")
    if not 0.0 <= q <= 1.0:
        raise ValueError("q must be in [0, 1]")
    if q == 0.0:
        return float(data[0])
    index = max(0, min(len(data) - 1, int((q * len(data) + 0.9999999999)) - 1))
    return float(data[index])


@dataclass(frozen=True)
class ScalarSummary:
    count: int
    minimum: float
    median: float
    mean: float
    p90: float
    maximum: float

    def to_dict(self) -> dict[str, float | int]:
        return asdict(self)


def summarize(values: Iterable[int]) -> ScalarSummary:
    data = list(values)
    if not data:
        raise ValueError("cannot summarize empty data")
    return ScalarSummary(
        count=len(data),
        minimum=float(min(data)),
        median=float(median(data)),
        mean=float(mean(data)),
        p90=percentile_nearest_rank(data, 0.90),
        maximum=float(max(data)),
    )


@dataclass(frozen=True)
class VisibleSplitProfile:
    tasks: int
    train_demo_pairs: int
    test_input_slots: int
    multi_test_tasks: int
    multi_test_task_fraction: float
    train_pairs_per_task: ScalarSummary
    test_inputs_per_task: ScalarSummary
    train_input_area: ScalarSummary
    train_output_area: ScalarSummary
    test_input_area: ScalarSummary
    train_input_colors: ScalarSummary
    train_output_colors: ScalarSummary
    test_input_colors: ScalarSummary

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        return result


def profile_task_payloads(tasks: Iterable[dict[str, Any]]) -> VisibleSplitProfile:
    task_list = list(tasks)
    if not task_list:
        raise ValueError("at least one task is required")

    train_pair_counts: list[int] = []
    test_counts: list[int] = []
    train_input_areas: list[int] = []
    train_output_areas: list[int] = []
    test_input_areas: list[int] = []
    train_input_colors: list[int] = []
    train_output_colors: list[int] = []
    test_input_colors: list[int] = []

    for task in task_list:
        train = task.get("train")
        test = task.get("test")
        if not isinstance(train, list) or not train:
            raise ValueError("task train must be a non-empty list")
        if not isinstance(test, list) or not test:
            raise ValueError("task test must be a non-empty list")
        train_pair_counts.append(len(train))
        test_counts.append(len(test))

        for pair in train:
            inp = pair["input"]
            out = pair["output"]
            train_input_areas.append(grid_area(inp))
            train_output_areas.append(grid_area(out))
            train_input_colors.append(grid_color_count(inp))
            train_output_colors.append(grid_color_count(out))

        for pair in test:
            inp = pair["input"]
            # Deliberately ignore test outputs even when public files contain them.
            test_input_areas.append(grid_area(inp))
            test_input_colors.append(grid_color_count(inp))

    multi_test_tasks = sum(count > 1 for count in test_counts)
    return VisibleSplitProfile(
        tasks=len(task_list),
        train_demo_pairs=sum(train_pair_counts),
        test_input_slots=sum(test_counts),
        multi_test_tasks=multi_test_tasks,
        multi_test_task_fraction=multi_test_tasks / len(task_list),
        train_pairs_per_task=summarize(train_pair_counts),
        test_inputs_per_task=summarize(test_counts),
        train_input_area=summarize(train_input_areas),
        train_output_area=summarize(train_output_areas),
        test_input_area=summarize(test_input_areas),
        train_input_colors=summarize(train_input_colors),
        train_output_colors=summarize(train_output_colors),
        test_input_colors=summarize(test_input_colors),
    )


def load_task_directory(task_directory: Path) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    for path in sorted(task_directory.glob("*.json")):
        tasks.append(json.loads(path.read_text(encoding="utf-8")))
    if not tasks:
        raise ValueError(f"no task JSON files found in {task_directory}")
    return tasks


def compare_visible_splits(training: VisibleSplitProfile, evaluation: VisibleSplitProfile) -> dict[str, Any]:
    def ratio(eval_value: float, train_value: float) -> float | None:
        return eval_value / train_value if train_value else None

    return {
        "training": training.to_dict(),
        "evaluation": evaluation.to_dict(),
        "evaluation_over_training": {
            "test_input_area_median_ratio": ratio(evaluation.test_input_area.median, training.test_input_area.median),
            "test_input_area_p90_ratio": ratio(evaluation.test_input_area.p90, training.test_input_area.p90),
            "test_input_color_median_ratio": ratio(evaluation.test_input_colors.median, training.test_input_colors.median),
            "multi_test_task_fraction_ratio": ratio(
                evaluation.multi_test_task_fraction, training.multi_test_task_fraction
            ),
            "train_demo_area_median_ratio": ratio(
                evaluation.train_input_area.median, training.train_input_area.median
            ),
        },
        "leakage_guard": (
            "Only training demonstration inputs/outputs and test inputs are profiled. "
            "Test outputs are never read."
        ),
    }
