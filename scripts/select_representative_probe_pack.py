from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from arcsolver.representative_probe import select_representative_tasks


def load_tasks(task_directory: Path) -> dict[str, dict[str, Any]]:
    tasks: dict[str, dict[str, Any]] = {}
    for path in sorted(task_directory.glob("*.json")):
        tasks[path.stem] = json.loads(path.read_text(encoding="utf-8"))
    if not tasks:
        raise ValueError(f"no task JSON files found in {task_directory}")
    return tasks


def main() -> None:
    parser = argparse.ArgumentParser(description="Select a leakage-safe representative ARC probe pack from one manifest split.")
    parser.add_argument("task_directory", type=Path)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--split", default="development")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--json-out", type=Path, required=True)
    args = parser.parse_args()

    tasks = load_tasks(args.task_directory)
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    splits = manifest.get("splits")
    if not isinstance(splits, dict) or args.split not in splits:
        raise ValueError(f"manifest missing split {args.split!r}")

    report = select_representative_tasks(tasks, list(splits[args.split]), count=args.count)
    report["manifest_metadata"] = manifest.get("metadata", {})
    report["split"] = args.split

    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
