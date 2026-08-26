from __future__ import annotations

import argparse
import json
import os
import zipfile
from collections import Counter
from pathlib import Path
from typing import Iterable


UNSAFE_SERIALIZED_SUFFIXES = {".pkl", ".pickle", ".pt", ".pth", ".ckpt", ".joblib"}


def classify(path: str) -> str:
    low = path.lower()
    name = Path(low).name
    suffix = Path(low).suffix

    if name in {"submission.json", "submission.csv"} or "submission" in name:
        return "submission"
    if suffix in {".pkl", ".pickle"} or any(token in low for token in ("candidate", "beam", "dump", "prediction")):
        return "candidate_or_serialized_dump"
    if suffix in {".log", ".out", ".err"} or "log" in name:
        return "log"
    if suffix in {".json", ".jsonl", ".csv", ".tsv", ".parquet"} or any(
        token in low for token in ("metric", "score", "telemetry", "trace", "runtime")
    ):
        return "structured_telemetry"
    if suffix in {".pt", ".pth", ".ckpt", ".safetensors", ".bin"}:
        return "model_or_checkpoint"
    if suffix in {".py", ".ipynb", ".sh", ".ps1"}:
        return "code"
    if suffix in {".zip", ".tar", ".gz", ".tgz", ".7z"}:
        return "nested_archive"
    return "other"


def record(path: str, size: int) -> dict[str, object]:
    suffix = Path(path).suffix.lower()
    return {
        "path": path,
        "bytes": int(size),
        "suffix": suffix,
        "category": classify(path),
        "unsafe_to_deserialize_without_trust": suffix in UNSAFE_SERIALIZED_SUFFIXES,
    }


def inventory_directory(root: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in sorted(root.rglob("*")):
        if path.is_file():
            rows.append(record(str(path.relative_to(root)), path.stat().st_size))
    return rows


def inventory_zip(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with zipfile.ZipFile(path) as archive:
        for info in sorted(archive.infolist(), key=lambda item: item.filename):
            if info.is_dir():
                continue
            rows.append(record(info.filename, info.file_size))
    return rows


def summarize(rows: Iterable[dict[str, object]]) -> dict[str, object]:
    rows = list(rows)
    categories = Counter(str(row["category"]) for row in rows)
    suffixes = Counter(str(row["suffix"]) or "<none>" for row in rows)
    unsafe = [str(row["path"]) for row in rows if row["unsafe_to_deserialize_without_trust"]]
    candidate_like = [
        str(row["path"])
        for row in rows
        if row["category"] in {"candidate_or_serialized_dump", "structured_telemetry"}
    ]
    return {
        "file_count": len(rows),
        "total_bytes": sum(int(row["bytes"]) for row in rows),
        "categories": dict(sorted(categories.items())),
        "suffixes": dict(sorted(suffixes.items())),
        "unsafe_serialized_files": unsafe,
        "candidate_or_telemetry_files": candidate_like,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Inventory a public notebook-output directory or ZIP without extracting or deserializing files. "
            "Use this before trusting pickle/checkpoint artifacts."
        )
    )
    parser.add_argument("source", type=Path)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    source = args.source
    if source.is_dir():
        kind = "directory"
        rows = inventory_directory(source)
    elif source.is_file() and zipfile.is_zipfile(source):
        kind = "zip"
        rows = inventory_zip(source)
    else:
        raise SystemExit(f"source must be a directory or ZIP archive: {source}")

    payload = {
        "source": str(source),
        "source_kind": kind,
        "safety": (
            "Inventory only. No archive member is extracted and no pickle/checkpoint is deserialized. "
            "Treat serialized artifacts as untrusted until provenance is established."
        ),
        "summary": summarize(rows),
        "files": rows,
    }
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
