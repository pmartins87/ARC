from __future__ import annotations

import argparse
import json
import re
import zipfile
from collections import Counter
from pathlib import Path
from typing import Iterable


UNSAFE_SERIALIZED_SUFFIXES = {".pkl", ".pickle", ".pt", ".pth", ".ckpt", ".joblib"}
HEX_TASK_RE = re.compile(r"^[0-9a-f]{8}(?:[_\.].*)?$", re.IGNORECASE)


def classify(path: str, magic: str | None = None) -> str:
    low = path.lower()
    name = Path(low).name
    suffix = Path(low).suffix

    if name in {"submission.json", "submission.csv"} or "submission" in name:
        return "submission"
    if magic == "bz2":
        return "bz2_compressed_artifact"
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


def identify_magic(prefix: bytes) -> str | None:
    if prefix.startswith(b"BZh"):
        return "bz2"
    if prefix.startswith(b"PK\x03\x04"):
        return "zip"
    if prefix.startswith(b"\x1f\x8b"):
        return "gzip"
    if prefix.startswith(b"\x80"):
        return "pickle_protocol_binary"
    return None


def looks_like_nvarc_candidate_dump(path: str, magic: str | None) -> bool:
    low = path.lower()
    name = Path(low).name
    return bool(
        magic == "bz2"
        and (
            "inference_outputs" in low
            or "inference-output" in low
            or HEX_TASK_RE.match(name)
        )
    )


def record(path: str, size: int, prefix: bytes = b"") -> dict[str, object]:
    suffix = Path(path).suffix.lower()
    magic = identify_magic(prefix)
    nvarc_like = looks_like_nvarc_candidate_dump(path, magic)
    unsafe = suffix in UNSAFE_SERIALIZED_SUFFIXES or magic in {"bz2", "pickle_protocol_binary"}
    return {
        "path": path,
        "bytes": int(size),
        "suffix": suffix,
        "magic": magic,
        "category": classify(path, magic),
        "nvarc_candidate_dump_signature": nvarc_like,
        "unsafe_to_deserialize_without_trust": unsafe,
    }


def inventory_directory(root: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        try:
            with path.open("rb") as handle:
                prefix = handle.read(4)
        except OSError:
            prefix = b""
        rows.append(record(str(path.relative_to(root)), path.stat().st_size, prefix))
    return rows


def inventory_zip(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with zipfile.ZipFile(path) as archive:
        for info in sorted(archive.infolist(), key=lambda item: item.filename):
            if info.is_dir():
                continue
            try:
                with archive.open(info, "r") as handle:
                    prefix = handle.read(4)
            except (OSError, RuntimeError, zipfile.BadZipFile):
                prefix = b""
            rows.append(record(info.filename, info.file_size, prefix))
    return rows


def summarize(rows: Iterable[dict[str, object]]) -> dict[str, object]:
    rows = list(rows)
    categories = Counter(str(row["category"]) for row in rows)
    suffixes = Counter(str(row["suffix"]) or "<none>" for row in rows)
    magics = Counter(str(row["magic"]) for row in rows if row["magic"])
    unsafe = [str(row["path"]) for row in rows if row["unsafe_to_deserialize_without_trust"]]
    nvarc_like = [str(row["path"]) for row in rows if row["nvarc_candidate_dump_signature"]]
    candidate_like = [
        str(row["path"])
        for row in rows
        if row["category"] in {"candidate_or_serialized_dump", "structured_telemetry", "bz2_compressed_artifact"}
    ]
    return {
        "file_count": len(rows),
        "total_bytes": sum(int(row["bytes"]) for row in rows),
        "categories": dict(sorted(categories.items())),
        "suffixes": dict(sorted(suffixes.items())),
        "magic_signatures": dict(sorted(magics.items())),
        "unsafe_serialized_files": unsafe,
        "nvarc_candidate_dump_signature_files": nvarc_like,
        "candidate_or_telemetry_files": candidate_like,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Inventory a public notebook-output directory or ZIP without extracting or deserializing files. "
            "Reads at most four header bytes per file so BZ2/NVARC-style candidate artifacts can be flagged safely."
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
            "Inventory only. Archive members are not extracted and serialized objects are not deserialized. "
            "At most four header bytes are read for magic-signature classification. Treat flagged artifacts as untrusted "
            "until provenance is established."
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
