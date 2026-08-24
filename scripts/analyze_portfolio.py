from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from arcsolver.portfolio import analyze_portfolio


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _parse_named_path(values: list[str]) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"expected NAME=PATH, got {value!r}")
        name, raw_path = value.split("=", 1)
        if not name or not raw_path:
            raise ValueError(f"expected NAME=PATH, got {value!r}")
        if name in result:
            raise ValueError(f"duplicate solver name: {name}")
        result[name] = Path(raw_path)
    return result


def _parse_named_float(values: list[str]) -> dict[str, float]:
    result: dict[str, float] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"expected NAME=SECONDS, got {value!r}")
        name, raw = value.split("=", 1)
        if name in result:
            raise ValueError(f"duplicate runtime name: {name}")
        result[name] = float(raw)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Measure multi-solver exact-output coverage, unique contributions, "
            "oracle union and optional runtime-budget portfolios."
        )
    )
    parser.add_argument("solutions", type=Path)
    parser.add_argument(
        "--solver",
        action="append",
        default=[],
        metavar="NAME=PATH",
        help="submission JSON; repeat once per solver",
    )
    parser.add_argument(
        "--runtime",
        action="append",
        default=[],
        metavar="NAME=SECONDS",
        help="optional runtime mapping; if used, provide one entry for every solver",
    )
    parser.add_argument(
        "--budget",
        action="append",
        default=[],
        type=float,
        metavar="SECONDS",
        help="optional exact additive runtime budget; may be repeated",
    )
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    solver_paths = _parse_named_path(args.solver)
    if not solver_paths:
        parser.error("at least one --solver NAME=PATH is required")

    submissions = {name: _load_json(path) for name, path in solver_paths.items()}
    solutions = _load_json(args.solutions)
    runtimes = _parse_named_float(args.runtime) if args.runtime else None

    report = analyze_portfolio(
        submissions,
        solutions,
        runtimes_seconds=runtimes,
        budgets_seconds=tuple(args.budget),
    )
    rendered = json.dumps(report.to_dict(), indent=2, sort_keys=True)
    print(rendered)

    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
