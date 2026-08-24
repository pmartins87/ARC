from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from arcsolver.compare import compare_submissions, diagnose_submission


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Measure ARC pass@1/pass@2 diagnostics and exact-solve complementarity."
    )
    parser.add_argument("solutions", type=Path)
    parser.add_argument("submission_a", type=Path)
    parser.add_argument("--name-a", default="solver_a")
    parser.add_argument("--submission-b", type=Path)
    parser.add_argument("--name-b", default="solver_b")
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    solutions = load_json(args.solutions)
    submission_a = load_json(args.submission_a)

    if args.submission_b is None:
        report = diagnose_submission(args.name_a, submission_a, solutions).to_dict()
    else:
        submission_b = load_json(args.submission_b)
        report = compare_submissions(
            args.name_a,
            submission_a,
            args.name_b,
            submission_b,
            solutions,
        ).to_dict()

    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
