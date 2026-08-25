from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from arcsolver.distribution_profile import profile_task_payloads


def load_tasks_by_id(task_directory: Path) -> dict[str, dict[str, Any]]:
    tasks: dict[str, dict[str, Any]] = {}
    for path in sorted(task_directory.glob("*.json")):
        tasks[path.stem] = json.loads(path.read_text(encoding="utf-8"))
    if not tasks:
        raise ValueError(f"no task JSON files found in {task_directory}")
    return tasks


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit visible structural balance of the frozen 60/30/30 public evaluation split."
    )
    parser.add_argument("evaluation_directory", type=Path)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--json-out", type=Path, required=True)
    args = parser.parse_args()

    tasks = load_tasks_by_id(args.evaluation_directory)
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    splits = manifest.get("splits")
    if not isinstance(splits, dict):
        raise ValueError("manifest missing splits mapping")
    metadata = manifest.get("metadata") or {}

    report: dict[str, Any] = {
        "manifest_profile": metadata.get("profile"),
        "manifest_seed": metadata.get("seed"),
        "manifest_task_count": metadata.get("task_count"),
        "splits": {},
        "leakage_guard": "Only training demonstrations and test inputs are profiled; test outputs are never read.",
    }
    seen: set[str] = set()
    for split_name in ("development", "validation", "heldout"):
        task_ids = list(splits.get(split_name, []))
        if not task_ids:
            raise ValueError(f"manifest split {split_name!r} is empty")
        overlap = seen.intersection(task_ids)
        if overlap:
            raise ValueError(f"manifest split overlap detected: {sorted(overlap)[:5]}")
        seen.update(task_ids)
        missing = sorted(set(task_ids) - set(tasks))
        if missing:
            raise ValueError(f"evaluation directory missing manifest tasks: {missing[:5]}")
        profile = profile_task_payloads(tasks[task_id] for task_id in task_ids)
        report["splits"][split_name] = profile.to_dict()

    report["unassigned_task_ids"] = sorted(set(tasks) - seen)

    # Compact spread diagnostics. Ratios near 1 mean the frozen split is structurally balanced.
    metrics = {
        "test_input_area_median": [
            report["splits"][name]["test_input_area"]["median"]
            for name in ("development", "validation", "heldout")
        ],
        "test_input_area_p90": [
            report["splits"][name]["test_input_area"]["p90"]
            for name in ("development", "validation", "heldout")
        ],
        "test_input_colors_median": [
            report["splits"][name]["test_input_colors"]["median"]
            for name in ("development", "validation", "heldout")
        ],
        "multi_test_task_fraction": [
            report["splits"][name]["multi_test_task_fraction"]
            for name in ("development", "validation", "heldout")
        ],
        "train_input_area_median": [
            report["splits"][name]["train_input_area"]["median"]
            for name in ("development", "validation", "heldout")
        ],
    }
    report["spread"] = {
        key: {
            "minimum": min(values),
            "maximum": max(values),
            "max_over_min": (max(values) / min(values) if min(values) else None),
            "values_dev_val_heldout": values,
        }
        for key, values in metrics.items()
    }

    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
