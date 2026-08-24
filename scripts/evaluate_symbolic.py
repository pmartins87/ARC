from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from pathlib import Path
from typing import Any

from arcsolver.scoring import score_submission
from arcsolver.symbolic import solve_task


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

    submission: dict[str, Any] = {}
    solutions: dict[str, Any] = {}
    details: dict[str, Any] = {}
    family_counts: Counter[str] = Counter()

    started = time.perf_counter()
    for task_id in selected_ids:
        challenge, truth = hide_test_outputs(all_tasks[task_id])
        predictions, hypotheses = solve_task(challenge)
        submission[task_id] = predictions
        solutions[task_id] = truth
        family_counts.update(hypothesis.family for hypothesis in hypotheses)

        output_pass1: list[bool] = []
        output_pass2: list[bool] = []
        for prediction, expected in zip(predictions, truth):
            p1 = prediction["attempt_1"] == expected
            p2 = p1 or prediction["attempt_2"] == expected
            output_pass1.append(p1)
            output_pass2.append(p2)

        details[task_id] = {
            "test_outputs": len(truth),
            "pass1_outputs": output_pass1,
            "pass2_outputs": output_pass2,
            "task_solved_pass1": bool(output_pass1) and all(output_pass1),
            "task_solved_pass2": bool(output_pass2) and all(output_pass2),
            "hypothesis_count": len(hypotheses),
            "hypothesis_families": sorted({hypothesis.family for hypothesis in hypotheses}),
            "top_hypotheses": [hypothesis.description for hypothesis in hypotheses[:5]],
        }
    elapsed = time.perf_counter() - started

    pass2 = score_submission(submission, solutions)
    correct_pass1 = sum(
        int(prediction["attempt_1"] == expected)
        for task_id, expected_outputs in solutions.items()
        for prediction, expected in zip(submission[task_id], expected_outputs)
    )
    total_outputs = pass2.total_outputs
    pass1 = correct_pass1 / total_outputs if total_outputs else 0.0
    solved_tasks_pass1 = sum(int(item["task_solved_pass1"]) for item in details.values())
    solved_tasks_pass2 = sum(int(item["task_solved_pass2"]) for item in details.values())

    report = {
        "split": args.split if args.manifest else "all",
        "tasks": len(selected_ids),
        "test_outputs": total_outputs,
        "pass_at_1": pass1,
        "pass_at_2": pass2.accuracy,
        "correct_outputs_pass_at_1": correct_pass1,
        "correct_outputs_pass_at_2": pass2.correct_outputs,
        "solved_tasks_pass_at_1": solved_tasks_pass1,
        "solved_tasks_pass_at_2": solved_tasks_pass2,
        "runtime_seconds": elapsed,
        "fitted_hypothesis_family_counts": dict(sorted(family_counts.items())),
        "task_details": details,
    }
    print(json.dumps({key: value for key, value in report.items() if key != "task_details"}, indent=2, sort_keys=True))

    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        with args.json_out.open("w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2, sort_keys=True)
            fh.write("\n")


if __name__ == "__main__":
    main()
