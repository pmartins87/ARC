from copy import deepcopy

from arcsolver.representative_probe import select_representative_tasks, visible_task_features


def _task(size: int, colors: int, test_slots: int = 1):
    row = [i % colors for i in range(size)]
    grid = [row[:] for _ in range(size)]
    out = [r[:] for r in grid]
    return {
        "train": [{"input": grid, "output": out}],
        "test": [{"input": grid, "output": [[9]]} for _ in range(test_slots)],
    }


def test_visible_features_ignore_test_output():
    task = _task(3, 3, 2)
    changed = deepcopy(task)
    changed["test"][0]["output"] = [[1, 2, 3], [4, 5, 6]]
    assert visible_task_features(task) == visible_task_features(changed)


def test_selector_is_deterministic_and_candidate_bounded():
    tasks = {
        "a": _task(2, 2),
        "b": _task(3, 3),
        "c": _task(4, 4, 2),
        "d": _task(5, 5),
        "e": _task(6, 6, 3),
        "f": _task(7, 7),
    }
    first = select_representative_tasks(tasks, list(tasks), count=4)
    second = select_representative_tasks(tasks, list(reversed(tasks)), count=4)
    assert first["selected_task_ids"] == second["selected_task_ids"]
    assert len(first["selected_task_ids"]) == 4
    assert set(first["selected_task_ids"]).issubset(tasks)


def test_selector_unchanged_when_only_test_outputs_change():
    tasks = {
        "a": _task(2, 2),
        "b": _task(3, 3),
        "c": _task(4, 4, 2),
        "d": _task(5, 5),
        "e": _task(6, 6, 3),
    }
    altered = deepcopy(tasks)
    for task in altered.values():
        for pair in task["test"]:
            pair["output"] = [[8, 8], [8, 8]]
    assert select_representative_tasks(tasks, list(tasks), count=4)["selected_task_ids"] == select_representative_tasks(altered, list(altered), count=4)["selected_task_ids"]
