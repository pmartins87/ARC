from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def bucket(task_id: str) -> int:
    digest = hashlib.sha256(task_id.encode("ascii")).digest()
    return int.from_bytes(digest[:8], "big") % 100


def split_name(task_id: str) -> str:
    b = bucket(task_id)
    if b < 70:
        return "development"
    if b < 85:
        return "validation"
    return "heldout"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("challenges", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    with args.challenges.open("r", encoding="utf-8") as fh:
        tasks = json.load(fh)

    manifest = {name: [] for name in ("development", "validation", "heldout")}
    for task_id in sorted(tasks):
        manifest[split_name(task_id)].append(task_id)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)

    print({name: len(ids) for name, ids in manifest.items()})


if __name__ == "__main__":
    main()
