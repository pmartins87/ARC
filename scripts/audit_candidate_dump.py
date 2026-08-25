from __future__ import annotations

import argparse
import bz2
import json
import pickle
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any

from arcsolver.candidate_pool import audit_candidate_pools


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_trusted_qwen_dump(
    dump_path: Path, *, solutions_path: Path | None = None
) -> tuple[dict[str, list[dict[str, Any]]], dict[str, Any]]:
    """Load a trusted Qwen/NVARC-lineage validation dump.

    The public baseline stores inference samples as Python pickles inside a zip.
    Pickle is intentionally unsafe for untrusted input, so this function is only
    exposed by the CLI behind an explicit `--trusted-pickle` acknowledgement.
    """
    pools: dict[str, list[dict[str, Any]]] = {}
    solutions: dict[str, Any] | None = None

    with zipfile.ZipFile(dump_path, "r") as archive:
        for member in archive.namelist():
            path = PurePosixPath(member)
            if path.name == "arc-agi_evaluation_solutions.json":
                solutions = json.loads(archive.read(member).decode("utf-8"))
                continue
            if "inference_outputs" not in path.parts or not path.name:
                continue
            payload = bz2.decompress(archive.read(member))
            outputs = pickle.loads(payload)  # noqa: S301 - trusted, explicit CLI opt-in
            if not isinstance(outputs, list):
                raise ValueError(f"{member}: expected list of candidate samples")
            output_key = path.name.split(".")[0]
            pools.setdefault(output_key, []).extend(outputs)

    if solutions is None:
        if solutions_path is None:
            raise FileNotFoundError(
                "solutions not embedded in dump; pass --solutions with the pinned matching file"
            )
        solutions = _load_json(solutions_path)

    return pools, solutions


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Audit a trusted Qwen/NVARC inference dump, separating candidate-pool oracle "
            "coverage from the two public top-2 selectors."
        )
    )
    parser.add_argument("dump", type=Path)
    parser.add_argument("--solutions", type=Path)
    parser.add_argument(
        "--trusted-pickle",
        action="store_true",
        help="required acknowledgement: the dump contains pickle payloads and must be trusted",
    )
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    if not args.trusted_pickle:
        parser.error(
            "refusing to unpickle without --trusted-pickle; only use dumps produced by a trusted run/source"
        )

    pools, solutions = load_trusted_qwen_dump(args.dump, solutions_path=args.solutions)
    report = audit_candidate_pools(pools, solutions)
    rendered = json.dumps(report.to_dict(), indent=2, sort_keys=True)
    print(rendered)

    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
