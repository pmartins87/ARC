from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from arcsolver.gate_split import rebalance_gate_split


def load_tasks(task_directory: Path) -> dict[str, dict[str, Any]]:
    tasks: dict[str, dict[str, Any]] = {}
    for path in sorted(task_directory.glob("*.json")):
        tasks[path.stem] = json.loads(path.read_text(encoding="utf-8"))
    if not tasks:
        raise ValueError(f"no task JSON files found in {task_directory}")
    return tasks


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Preserve the frozen development split while rebalancing untouched validation/heldout gates "
            "using visible train examples and test inputs only."
        )
    )
    parser.add_argument("evaluation_directory", type=Path)
    parser.add_argument("parent_manifest", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--seed", default="arc-2026-gates-v2")
    args = parser.parse_args()

    tasks = load_tasks(args.evaluation_directory)
    parent = json.loads(args.parent_manifest.read_text(encoding="utf-8"))
    manifest = rebalance_gate_split(tasks, parent, seed=args.seed)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print({name: len(ids) for name, ids in manifest["splits"].items()})


if __name__ == "__main__":
    main()
