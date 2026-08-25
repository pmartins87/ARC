from __future__ import annotations

import argparse
import json
from pathlib import Path

from arcsolver.provenance import (
    compare_fingerprints,
    fingerprint_challenge_file,
    submission_schema_fingerprint,
)


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Fingerprint ARC challenge/submission schemas and fail visibly on task/test-count provenance drift."
        )
    )
    parser.add_argument("challenge", type=Path)
    parser.add_argument(
        "--submission",
        type=Path,
        help="optional submission.json to compare structurally against the challenge file",
    )
    parser.add_argument(
        "--compare-challenge",
        type=Path,
        help="optional second challenge JSON to compare against the reference challenge",
    )
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    reference = fingerprint_challenge_file(args.challenge)
    report: dict[str, object] = {"reference": reference.to_dict()}

    if args.submission is not None:
        submission = _load_json(args.submission)
        submission_fp = submission_schema_fingerprint(submission)
        report["submission"] = submission_fp.to_dict()
        report["submission_diff"] = compare_fingerprints(reference, submission_fp).to_dict()

    if args.compare_challenge is not None:
        candidate = fingerprint_challenge_file(args.compare_challenge)
        report["candidate_challenge"] = candidate.to_dict()
        report["candidate_diff"] = compare_fingerprints(reference, candidate).to_dict()

    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
