from __future__ import annotations

from math import sqrt
from statistics import median
from typing import Any

from arcsolver.distribution_profile import grid_area, grid_color_count

FEATURE_NAMES = (
    "train_pairs",
    "test_slots",
    "train_input_area_median",
    "train_output_area_median",
    "test_input_area_median",
    "test_input_area_max",
    "test_input_colors_median",
    "test_input_colors_max",
)


def visible_task_features(task: dict[str, Any]) -> dict[str, float]:
    """Return task-level features using train pairs and test inputs only."""
    train = task.get("train")
    test = task.get("test")
    if not isinstance(train, list) or not train or not isinstance(test, list) or not test:
        raise ValueError("task must contain non-empty train and test lists")

    train_in_areas = [grid_area(pair["input"]) for pair in train]
    train_out_areas = [grid_area(pair["output"]) for pair in train]
    test_areas = [grid_area(pair["input"]) for pair in test]
    test_colors = [grid_color_count(pair["input"]) for pair in test]

    return {
        "train_pairs": float(len(train)),
        "test_slots": float(len(test)),
        "train_input_area_median": float(median(train_in_areas)),
        "train_output_area_median": float(median(train_out_areas)),
        "test_input_area_median": float(median(test_areas)),
        "test_input_area_max": float(max(test_areas)),
        "test_input_colors_median": float(median(test_colors)),
        "test_input_colors_max": float(max(test_colors)),
    }


def _normalize(feature_rows: dict[str, dict[str, float]]) -> dict[str, tuple[float, ...]]:
    ranges: dict[str, tuple[float, float]] = {}
    for name in FEATURE_NAMES:
        values = [row[name] for row in feature_rows.values()]
        ranges[name] = (min(values), max(values))

    normalized: dict[str, tuple[float, ...]] = {}
    for task_id, row in feature_rows.items():
        values: list[float] = []
        for name in FEATURE_NAMES:
            lo, hi = ranges[name]
            values.append(0.0 if hi == lo else (row[name] - lo) / (hi - lo))
        normalized[task_id] = tuple(values)
    return normalized


def _distance(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    return sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def select_representative_tasks(
    tasks_by_id: dict[str, dict[str, Any]],
    candidate_ids: list[str],
    *,
    count: int = 8,
) -> dict[str, Any]:
    """Select a deterministic visible-feature coverage pack.

    Selection never reads test outputs. It anchors the median-like task, large-area,
    high-color, and multi-test extremes, then uses farthest-point coverage.
    """
    ids = sorted(dict.fromkeys(candidate_ids))
    if not ids:
        raise ValueError("candidate_ids must be non-empty")
    missing = sorted(set(ids) - set(tasks_by_id))
    if missing:
        raise ValueError(f"missing task ids: {missing[:5]}")
    if not 1 <= count <= len(ids):
        raise ValueError("count must be between 1 and number of candidates")

    rows = {task_id: visible_task_features(tasks_by_id[task_id]) for task_id in ids}
    normalized = _normalize(rows)

    component_medians = tuple(median([normalized[task_id][i] for task_id in ids]) for i in range(len(FEATURE_NAMES)))
    median_anchor = min(ids, key=lambda task_id: (_distance(normalized[task_id], component_medians), task_id))

    anchors = [
        median_anchor,
        min(ids, key=lambda task_id: (-rows[task_id]["test_input_area_max"], task_id)),
        min(ids, key=lambda task_id: (-rows[task_id]["test_input_colors_max"], task_id)),
        min(ids, key=lambda task_id: (-rows[task_id]["test_slots"], task_id)),
        min(ids, key=lambda task_id: (-rows[task_id]["train_input_area_median"], task_id)),
    ]

    selected: list[str] = []
    reasons: dict[str, list[str]] = {}
    anchor_labels = ("median_visible_profile", "max_test_area", "max_test_colors", "max_test_slots", "max_demo_area")
    for task_id, label in zip(anchors, anchor_labels):
        reasons.setdefault(task_id, []).append(label)
        if task_id not in selected and len(selected) < count:
            selected.append(task_id)

    while len(selected) < count:
        remaining = [task_id for task_id in ids if task_id not in selected]
        next_id = max(
            remaining,
            key=lambda task_id: (
                min(_distance(normalized[task_id], normalized[chosen]) for chosen in selected),
                task_id,
            ),
        )
        selected.append(next_id)
        reasons.setdefault(next_id, []).append("farthest_visible_feature_coverage")

    return {
        "selection_method": "visible anchors + normalized farthest-point coverage",
        "feature_names": list(FEATURE_NAMES),
        "candidate_count": len(ids),
        "selected_count": len(selected),
        "selected_task_ids": selected,
        "selected": [
            {
                "task_id": task_id,
                "reasons": reasons.get(task_id, []),
                "features": rows[task_id],
            }
            for task_id in selected
        ],
        "leakage_guard": "Selection uses training inputs/outputs and test inputs only; test outputs are never read.",
    }
