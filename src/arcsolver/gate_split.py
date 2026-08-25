from __future__ import annotations

from dataclasses import dataclass
import hashlib
from math import sqrt
from statistics import median
from typing import Any, Mapping


@dataclass(frozen=True)
class VisibleTaskFeatures:
    task_id: str
    test_count: int
    test_area_median: float
    test_area_max: float
    test_color_median: float
    train_input_area_median: float
    train_input_color_median: float


def _grid_area(grid: list[list[int]]) -> int:
    if not grid or not grid[0]:
        raise ValueError("grid must be non-empty")
    width = len(grid[0])
    if any(len(row) != width for row in grid):
        raise ValueError("grid must be rectangular")
    return len(grid) * width


def _grid_colors(grid: list[list[int]]) -> int:
    return len({cell for row in grid for cell in row})


def visible_task_features(task_id: str, task: Mapping[str, Any]) -> VisibleTaskFeatures:
    """Extract only leakage-safe structure from an ARC task.

    Training inputs/outputs and test *inputs* are allowed. Any test output key is
    deliberately ignored so changing a visible public test answer cannot affect
    the split assignment.
    """
    train = list(task.get("train", []))
    tests = list(task.get("test", []))
    if not train or not tests:
        raise ValueError(f"{task_id}: task must contain train and test examples")

    test_areas = [_grid_area(pair["input"]) for pair in tests]
    test_colors = [_grid_colors(pair["input"]) for pair in tests]
    train_areas = [_grid_area(pair["input"]) for pair in train]
    train_colors = [_grid_colors(pair["input"]) for pair in train]

    return VisibleTaskFeatures(
        task_id=task_id,
        test_count=len(tests),
        test_area_median=float(median(test_areas)),
        test_area_max=float(max(test_areas)),
        test_color_median=float(median(test_colors)),
        train_input_area_median=float(median(train_areas)),
        train_input_color_median=float(median(train_colors)),
    )


def _stable_digest(seed: str, text: str) -> bytes:
    return hashlib.sha256(f"{seed}:{text}".encode("utf-8")).digest()


def _rank_normalize(values: Mapping[str, float]) -> dict[str, float]:
    """Map values to deterministic [0,1] average ranks, preserving ties."""
    if not values:
        return {}
    ordered = sorted(values.items(), key=lambda item: (item[1], item[0]))
    n = len(ordered)
    result: dict[str, float] = {}
    i = 0
    while i < n:
        j = i + 1
        while j < n and ordered[j][1] == ordered[i][1]:
            j += 1
        average_index = (i + (j - 1)) / 2.0
        normalized = average_index / (n - 1) if n > 1 else 0.5
        for k in range(i, j):
            result[ordered[k][0]] = normalized
        i = j
    return result


def normalized_feature_vectors(features: Mapping[str, VisibleTaskFeatures]) -> dict[str, tuple[float, ...]]:
    fields = (
        "test_count",
        "test_area_median",
        "test_area_max",
        "test_color_median",
        "train_input_area_median",
        "train_input_color_median",
    )
    ranks: list[dict[str, float]] = []
    for field in fields:
        ranks.append(_rank_normalize({task_id: float(getattr(feature, field)) for task_id, feature in features.items()}))
    return {task_id: tuple(rank[task_id] for rank in ranks) for task_id in features}


def _distance(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    return sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def nearest_neighbor_pairs(
    features: Mapping[str, VisibleTaskFeatures], *, seed: str
) -> list[tuple[str, str]]:
    """Pair structurally similar tasks using only visible leakage-safe features."""
    if len(features) % 2:
        raise ValueError("gate pool must contain an even number of tasks")
    vectors = normalized_feature_vectors(features)
    remaining = set(features)
    pairs: list[tuple[str, str]] = []

    while remaining:
        first = min(remaining, key=lambda task_id: _stable_digest(seed, f"first:{task_id}"))
        remaining.remove(first)
        second = min(
            remaining,
            key=lambda task_id: (
                _distance(vectors[first], vectors[task_id]),
                _stable_digest(seed, f"mate:{first}:{task_id}"),
            ),
        )
        remaining.remove(second)
        pairs.append((first, second))
    return pairs


def rebalance_gate_split(
    tasks: Mapping[str, Mapping[str, Any]],
    parent_manifest: Mapping[str, Any],
    *,
    seed: str = "arc-2026-gates-v2",
) -> dict[str, Any]:
    """Preserve development and rebalance untouched validation/heldout gates.

    The method is label-free: it never reads test outputs. It should only be
    adopted before validation/heldout scores are inspected.
    """
    splits = parent_manifest.get("splits")
    if not isinstance(splits, Mapping):
        raise ValueError("parent manifest missing splits")

    development = list(splits.get("development", []))
    validation = list(splits.get("validation", []))
    heldout = list(splits.get("heldout", []))
    gate_pool = validation + heldout
    if len(set(development + gate_pool)) != len(development) + len(gate_pool):
        raise ValueError("parent manifest contains overlap")
    if len(gate_pool) % 2:
        raise ValueError("combined validation+heldout pool must be even")

    missing = sorted(set(development + gate_pool) - set(tasks))
    if missing:
        raise ValueError(f"tasks missing from task mapping: {missing[:5]}")

    feature_map = {task_id: visible_task_features(task_id, tasks[task_id]) for task_id in gate_pool}
    pairs = nearest_neighbor_pairs(feature_map, seed=seed)

    new_validation: list[str] = []
    new_heldout: list[str] = []
    for a, b in pairs:
        if _stable_digest(seed, f"side:{a}:{b}")[0] % 2 == 0:
            new_validation.append(a)
            new_heldout.append(b)
        else:
            new_validation.append(b)
            new_heldout.append(a)

    new_validation.sort(key=lambda task_id: _stable_digest(seed, f"order:{task_id}"))
    new_heldout.sort(key=lambda task_id: _stable_digest(seed, f"order:{task_id}"))

    parent_metadata = dict(parent_manifest.get("metadata") or {})
    return {
        "metadata": {
            "profile": "evaluation-gates-v2",
            "seed": seed,
            "task_count": len(development) + len(gate_pool),
            "development_source": "parent manifest preserved byte-for-byte as task-id set/order",
            "gate_rebalance": "nearest-neighbor visible-feature pairing; one task per pair to each gate",
            "leakage_guard": "training examples and test inputs only; test outputs ignored",
            "parent_profile": parent_metadata.get("profile"),
            "parent_seed": parent_metadata.get("seed"),
        },
        "splits": {
            "development": development,
            "validation": new_validation,
            "heldout": new_heldout,
        },
        "pair_count": len(pairs),
    }
