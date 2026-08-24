from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

PROFILES = {
    "evaluation": (0.50, 0.25, 0.25),
    "training": (0.70, 0.15, 0.15),
}


def stable_key(task_id: str, seed: str) -> bytes:
    return hashlib.sha256(f"{seed}:{task_id}".encode("utf-8")).digest()


def split_ids(task_ids: list[str], profile: str, seed: str) -> dict[str, list[str]]:
    if profile not in PROFILES:
        raise ValueError(f"unknown profile: {profile}")

    dev_ratio, validation_ratio, _ = PROFILES[profile]
    ordered = sorted(task_ids, key=lambda task_id: stable_key(task_id, seed))
    n = len(ordered)
    n_dev = int(round(n * dev_ratio))
    n_validation = int(round(n * validation_ratio))
    n_dev = min(n_dev, n)
    n_validation = min(n_validation, n - n_dev)

    return {
        "development": ordered[:n_dev],
        "validation": ordered[n_dev : n_dev + n_validation],
        "heldout": ordered[n_dev + n_validation :],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create deterministic ARC split manifests from challenge task IDs."
    )
    parser.add_argument("challenges", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--profile",
        choices=sorted(PROFILES),
        default="evaluation",
        help="evaluation => 50/25/25; training => 70/15/15",
    )
    parser.add_argument(
        "--seed",
        default="arc-2026-v1",
        help="immutable split seed once a milestone begins",
    )
    args = parser.parse_args()

    with args.challenges.open("r", encoding="utf-8") as fh:
        tasks = json.load(fh)
    if not isinstance(tasks, dict):
        raise ValueError("challenges JSON must be keyed by task ID")

    manifest = {
        "metadata": {
            "profile": args.profile,
            "seed": args.seed,
            "task_count": len(tasks),
        },
        "splits": split_ids(list(tasks), args.profile, args.seed),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
        fh.write("\n")

    print({name: len(ids) for name, ids in manifest["splits"].items()})


if __name__ == "__main__":
    main()
