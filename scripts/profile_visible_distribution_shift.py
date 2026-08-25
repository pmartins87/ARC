from __future__ import annotations

import argparse
import json
from pathlib import Path

from arcsolver.distribution_profile import compare_visible_splits, load_task_directory, profile_task_payloads


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Profile visible ARC train-vs-evaluation distribution differences without reading any test outputs."
        )
    )
    parser.add_argument("training_directory", type=Path)
    parser.add_argument("evaluation_directory", type=Path)
    parser.add_argument("--json-out", type=Path, required=True)
    args = parser.parse_args()

    training = profile_task_payloads(load_task_directory(args.training_directory))
    evaluation = profile_task_payloads(load_task_directory(args.evaluation_directory))
    report = compare_visible_splits(training, evaluation)

    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
