from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from arcsolver.error_audit import audit_submission_structure


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_official_task_dir(task_dir: Path) -> tuple[dict[str, list[list[list[int]]]], dict[str, list[list[list[int]]]]]:
    solutions: dict[str, list[list[list[int]]]] = {}
    test_inputs: dict[str, list[list[list[int]]]] = {}
    for path in sorted(task_dir.glob("*.json")):
        task = _load_json(path)
        task_id = path.stem
        tests = task.get("test")
        if not isinstance(tests, list) or not tests:
            raise ValueError(f"{task_id}: invalid or empty test pairs")
        test_inputs[task_id] = [pair["input"] for pair in tests]
        solutions[task_id] = [pair["output"] for pair in tests]
    if not solutions:
        raise ValueError(f"no task JSON files found in {task_dir}")
    return solutions, test_inputs


def _restrict(
    submission: dict[str, Any],
    solutions: dict[str, Any],
    test_inputs: dict[str, Any],
    task_ids: set[str],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    missing_submission = sorted(task_ids - set(submission))
    if missing_submission:
        raise ValueError(f"submission missing selected tasks: {missing_submission[:5]}")
    missing_truth = sorted(task_ids - set(solutions))
    if missing_truth:
        raise ValueError(f"official data missing selected tasks: {missing_truth[:5]}")
    return (
        {task_id: submission[task_id] for task_id in sorted(task_ids)},
        {task_id: solutions[task_id] for task_id in sorted(task_ids)},
        {task_id: test_inputs[task_id] for task_id in sorted(task_ids)},
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Audit an ARC submission against official public task outputs, including exact pass@2, "
            "shape failures, color-set groups, duplicate attempts and solved task IDs."
        )
    )
    parser.add_argument("submission", type=Path)
    parser.add_argument("official_task_dir", type=Path)
    parser.add_argument("--name", default="submission")
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--split", choices=("development", "validation", "heldout"))
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    if (args.manifest is None) != (args.split is None):
        parser.error("--manifest and --split must be supplied together")

    submission = _load_json(args.submission)
    solutions, test_inputs = _load_official_task_dir(args.official_task_dir)

    if args.manifest is not None:
        manifest = _load_json(args.manifest)
        task_ids = set(manifest["splits"][args.split])
        submission, solutions, test_inputs = _restrict(
            submission, solutions, test_inputs, task_ids
        )

    report = audit_submission_structure(args.name, submission, solutions, test_inputs)
    rendered = json.dumps(report.to_dict(), indent=2, sort_keys=True)
    print(rendered)
    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
