from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from arcsolver.diversity import summarize_attempt_pairs


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def is_placeholder(grid: Any) -> bool:
    return grid == [[0]]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Measure structural diversity between attempt_1 and attempt_2 in an ARC submission."
    )
    parser.add_argument("submission", type=Path)
    parser.add_argument(
        "--exclude-double-placeholder",
        action="store_true",
        help="Exclude output slots where both attempts are exactly [[0]].",
    )
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    submission = load_json(args.submission)
    pairs = []
    selected_slots = 0
    skipped_double_placeholders = 0

    for task_id, outputs in sorted(submission.items()):
        if not isinstance(outputs, list):
            raise ValueError(f"{task_id}: outputs must be a list")
        for index, prediction in enumerate(outputs):
            if not isinstance(prediction, dict):
                raise ValueError(f"{task_id}[{index}]: prediction must be an object")
            if "attempt_1" not in prediction or "attempt_2" not in prediction:
                raise ValueError(f"{task_id}[{index}]: both attempts are required")
            a1 = prediction["attempt_1"]
            a2 = prediction["attempt_2"]
            if args.exclude_double_placeholder and is_placeholder(a1) and is_placeholder(a2):
                skipped_double_placeholders += 1
                continue
            pairs.append((a1, a2))
            selected_slots += 1

    report = summarize_attempt_pairs(pairs).to_dict()
    report["selected_slots"] = selected_slots
    report["skipped_double_placeholders"] = skipped_double_placeholders
    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)

    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
