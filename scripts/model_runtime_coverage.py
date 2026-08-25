from __future__ import annotations

import argparse
import json
from pathlib import Path

from arcsolver.runtime_budget import (
    lower_bound_speedup_for_capacity,
    minimum_uniform_speedup_for_fcfs_completion,
    simulate_fcfs,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Model FIFO task coverage under a global runtime budget. Input JSON must map "
            "task IDs to observed/planned task durations in seconds."
        )
    )
    parser.add_argument("durations", type=Path)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument(
        "--budget-seconds",
        type=float,
        default=12 * 3600 - 600,
        help="global budget; defaults to 11h50m, matching the pinned public Qwen lineage",
    )
    parser.add_argument("--speedup", type=float, default=1.0)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    durations = json.loads(args.durations.read_text(encoding="utf-8"))
    if not isinstance(durations, dict):
        raise ValueError("duration JSON must be an object mapping task IDs to seconds")

    simulation = simulate_fcfs(
        durations,
        workers=args.workers,
        budget_seconds=args.budget_seconds,
        speedup=args.speedup,
    )
    lower = lower_bound_speedup_for_capacity(
        durations, workers=args.workers, budget_seconds=args.budget_seconds
    )
    exact = minimum_uniform_speedup_for_fcfs_completion(
        durations, workers=args.workers, budget_seconds=args.budget_seconds
    )

    report = simulation.to_dict()
    report["aggregate_capacity_speedup_lower_bound"] = lower
    report["minimum_uniform_speedup_for_this_fcfs_order"] = exact

    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
