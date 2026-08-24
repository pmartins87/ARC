from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

from arcsolver.scoring import score_submission
from arcsolver.symbolic import make_symbolic_submission


def load_task_directory(path: Path) -> dict[str, dict[str, Any]]:
    tasks: dict[str, dict[str, Any]] = {}
    for task_file in sorted(path.glob("*.json")):
        with task_file.open("r", encoding="utf-8") as fh:
            tasks[task_file.stem] = json.load(fh)
    if not tasks:
        raise ValueError(f"no JSON tasks found in {path}")
    return tasks


def load_manifest(path: Path | None, split: str, task_ids: list[str]) -> list[str]:
    if path is None:
        return sorted(task_ids)
    with path.open("r", encoding="utf-8") as fh:
        manifest = json.load(fh)
    ids = manifest["splits"][split]
    unknown = sorted(set(ids) - set(task_ids))
    if unknown:
        raise ValueError(f"manifest contains unknown task IDs: {unknown[:5]}")
    return list(ids)


def hide_test_outputs(task: dict[str, Any]) -> tuple[dict[str, Any], list[list[list[int]]]]:
    challenge = {
        "train": task["train"],
        "test": [{"input": pair["input"]} for pair in task["test"]],
    }
    truth = [pair["output"] for pair in task["test"]]
    return challenge, truth


def pass1_accuracy(submission: dict[str, Any], solutions: dict[str, Any]) -> float:
    correct = 0
    total = 0
    for task_id, truth_outputs in solutions.items():
        for prediction, truth in zip(submission[task_id], truth_outputs):
            correct += int(prediction["attempt_1"] == truth)
            total += 1
    return correct / total if total else 0.0


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate the compact symbolic ARC baseline.")
    parser.add_argument("task_directory", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument(
        "--split",
        choices=("development", "validation", "heldout"),
        default="development",
    )
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    all_tasks = load_task_directory(args.task_directory)
    selected_ids = load_manifest(args.manifest, args.split, list(all_tasks))

    challenges: dict[str, Any] = {}
    solutions: dict[str, Any] = {}
    for task_id in selected_ids:
        challenge, truth = hide_test_outputs(all_tasks[task_id])
        challenges[task_id] = challenge
        solutions[task_id] = truth

    started = time.perf_counter()
    submission = make_symbolic_submission(challenges)
    elapsed = time.perf_counter() - started
    pass2 = score_submission(submission, solutions)
    pass1 = pass1_accuracy(submission, solutions)

    report = {
        "split": args.split if args.manifest else "all",
        "tasks": len(challenges),
        "test_outputs": pass2.total_outputs,
        "pass_at_1": pass1,
        "pass_at_2": pass2.accuracy,
        "correct_outputs_pass_at_2": pass2.correct_outputs,
        "runtime_seconds": elapsed,
    }
    print(json.dumps(report, indent=2, sort_keys=True))

    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        with args.json_out.open("w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2, sort_keys=True)
            fh.write("\n")


if __name__ == "__main__":
    main()
