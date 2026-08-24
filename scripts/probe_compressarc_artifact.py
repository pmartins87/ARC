from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _solution_hash(solution_grids: list[list[list[int]]]) -> int:
    """Mirror CompressARC preprocessing.Task._create_solution_tensor hash payload."""
    frozen = tuple(tuple(tuple(row) for row in grid) for grid in solution_grids)
    return hash(frozen)


def _task_order(challenges: dict[str, Any]) -> list[str]:
    # CompressARC preprocessing uses list(problems.keys()); preserve JSON insertion order.
    return list(challenges.keys())


def _normalize_pick_pair(raw: Any) -> tuple[int, int]:
    values = list(raw)
    if len(values) != 2:
        raise ValueError(f"expected two logged picks, got {len(values)}")
    return int(values[0]), int(values[1])


def probe(
    npz_path: Path,
    challenges_path: Path,
    solutions_path: Path,
    *,
    iteration: int,
    manifest_path: Path | None,
    split_name: str | None,
) -> dict[str, Any]:
    challenges = _load_json(challenges_path)
    solutions = _load_json(solutions_path)
    if set(challenges) != set(solutions):
        raise ValueError("challenge/solution task IDs differ")

    ordered_ids = _task_order(challenges)
    stored = np.load(npz_path, allow_pickle=True)
    if "solution_picks_histories" not in stored:
        raise ValueError("NPZ is missing solution_picks_histories")
    histories = stored["solution_picks_histories"]
    if len(histories) != len(ordered_ids):
        raise ValueError(
            f"artifact has {len(histories)} task histories but challenge file has {len(ordered_ids)} tasks"
        )

    allowed: set[str] | None = None
    if manifest_path is not None:
        manifest = _load_json(manifest_path)
        if split_name is None:
            raise ValueError("split_name is required when manifest_path is provided")
        try:
            allowed = set(manifest["splits"][split_name])
        except KeyError as exc:
            raise ValueError(f"split {split_name!r} not found in manifest") from exc

    rows: list[dict[str, Any]] = []
    for task_index, task_id in enumerate(ordered_ids):
        if allowed is not None and task_id not in allowed:
            continue
        history = histories[task_index]
        if len(history) == 0:
            raise ValueError(f"{task_id}: empty solution-pick history")
        selected_index = len(history) - 1 if iteration < 0 else min(iteration, len(history) - 1)
        pick1, pick2 = _normalize_pick_pair(history[selected_index])
        truth_hash = _solution_hash(solutions[task_id])
        pass1 = pick1 == truth_hash
        pass2 = pass1 or pick2 == truth_hash
        rows.append(
            {
                "task_id": task_id,
                "task_index": task_index,
                "iteration_index": selected_index,
                "history_length": len(history),
                "pass_at_1": pass1,
                "pass_at_2": pass2,
                "second_attempt_rescue": (not pass1) and pass2,
            }
        )

    solved1 = sum(int(row["pass_at_1"]) for row in rows)
    solved2 = sum(int(row["pass_at_2"]) for row in rows)
    rescues = sum(int(row["second_attempt_rescue"]) for row in rows)
    total = len(rows)
    selected_iterations = sorted({int(row["iteration_index"]) for row in rows})
    history_lengths = sorted({int(row["history_length"]) for row in rows})

    return {
        "source": {
            "npz": str(npz_path),
            "challenges": str(challenges_path),
            "solutions": str(solutions_path),
        },
        "selection": {
            "requested_iteration": iteration,
            "actual_iteration_indices": selected_iterations,
            "history_lengths": history_lengths,
            "manifest": str(manifest_path) if manifest_path else None,
            "split": split_name,
        },
        "summary": {
            "total_tasks": total,
            "solved_pass_at_1": solved1,
            "solved_pass_at_2": solved2,
            "second_attempt_rescues": rescues,
            "pass_at_1": solved1 / total if total else 0.0,
            "pass_at_2": solved2 / total if total else 0.0,
        },
        "solved_task_ids_pass_at_1": [row["task_id"] for row in rows if row["pass_at_1"]],
        "solved_task_ids_pass_at_2": [row["task_id"] for row in rows if row["pass_at_2"]],
        "tasks": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Read the public CompressARC prediction-history NPZ without rerunning GPU training, "
            "and recover exact pass@1/pass@2 task coverage."
        )
    )
    parser.add_argument("npz", type=Path)
    parser.add_argument("challenges", type=Path)
    parser.add_argument("solutions", type=Path)
    parser.add_argument(
        "--iteration",
        type=int,
        default=-1,
        help="0-based history index; -1 selects each task's final stored iteration",
    )
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--split", choices=("development", "validation", "heldout"))
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    if (args.manifest is None) != (args.split is None):
        parser.error("--manifest and --split must be supplied together")

    report = probe(
        args.npz,
        args.challenges,
        args.solutions,
        iteration=args.iteration,
        manifest_path=args.manifest,
        split_name=args.split,
    )
    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
