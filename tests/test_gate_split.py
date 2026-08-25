from __future__ import annotations

from copy import deepcopy

from arcsolver.gate_split import rebalance_gate_split, visible_task_features


def task(area: int, colors: int, test_count: int = 1) -> dict:
    width = max(1, area)
    row = [i % colors for i in range(width)]
    grid = [row]
    return {
        "train": [
            {"input": grid, "output": grid},
            {"input": grid, "output": grid},
        ],
        "test": [
            {"input": grid, "output": [[9]]}
            for _ in range(test_count)
        ],
    }


def parent_manifest() -> dict:
    return {
        "metadata": {"profile": "evaluation", "seed": "arc-2026-v1", "task_count": 8},
        "splits": {
            "development": ["d0", "d1"],
            "validation": ["g0", "g2", "g4"],
            "heldout": ["g1", "g3", "g5"],
        },
    }


def make_tasks() -> dict:
    return {
        "d0": task(2, 2),
        "d1": task(3, 2),
        "g0": task(10, 2, 1),
        "g1": task(11, 2, 1),
        "g2": task(100, 5, 2),
        "g3": task(101, 5, 2),
        "g4": task(300, 8, 3),
        "g5": task(301, 8, 3),
    }


def test_visible_features_ignore_test_outputs() -> None:
    original = task(12, 3, 2)
    changed = deepcopy(original)
    changed["test"][0]["output"] = [[1, 2, 3], [4, 5, 6]]
    changed["test"][1]["output"] = [[7]]
    assert visible_task_features("x", original) == visible_task_features("x", changed)


def test_rebalance_is_deterministic_and_preserves_development() -> None:
    tasks = make_tasks()
    first = rebalance_gate_split(tasks, parent_manifest(), seed="s")
    second = rebalance_gate_split(tasks, parent_manifest(), seed="s")
    assert first == second
    assert first["splits"]["development"] == ["d0", "d1"]
    assert len(first["splits"]["validation"]) == 3
    assert len(first["splits"]["heldout"]) == 3
    assert set(first["splits"]["validation"]).isdisjoint(first["splits"]["heldout"])
    assert set(first["splits"]["validation"] + first["splits"]["heldout"]) == {
        "g0", "g1", "g2", "g3", "g4", "g5"
    }


def test_nearby_structural_pairs_are_split_across_gates() -> None:
    result = rebalance_gate_split(make_tasks(), parent_manifest(), seed="pair-test")
    validation = set(result["splits"]["validation"])
    heldout = set(result["splits"]["heldout"])
    for a, b in (("g0", "g1"), ("g2", "g3"), ("g4", "g5")):
        assert (a in validation and b in heldout) or (b in validation and a in heldout)


def test_parent_overlap_is_rejected() -> None:
    parent = parent_manifest()
    parent["splits"]["heldout"][0] = "g0"
    try:
        rebalance_gate_split(make_tasks(), parent)
    except ValueError as exc:
        assert "overlap" in str(exc)
    else:
        raise AssertionError("expected overlap rejection")
