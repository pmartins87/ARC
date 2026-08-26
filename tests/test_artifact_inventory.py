from __future__ import annotations

import importlib.util
import zipfile
from pathlib import Path


SCRIPT = Path("scripts/inventory_artifacts.py")
spec = importlib.util.spec_from_file_location("inventory_artifacts", SCRIPT)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_inventory_zip_does_not_deserialize_and_classifies(tmp_path: Path) -> None:
    archive_path = tmp_path / "outputs.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr("submission.json", "{}")
        archive.writestr("logs/runtime.log", "ok")
        archive.writestr("candidate_dump.pkl", b"not actually a pickle")
        archive.writestr("metrics/trace.jsonl", "{}\n")
        archive.writestr("weights/model.safetensors", b"123")
        archive.writestr("src/solver.py", "print('x')")

    rows = module.inventory_zip(archive_path)
    by_path = {row["path"]: row for row in rows}

    assert by_path["submission.json"]["category"] == "submission"
    assert by_path["logs/runtime.log"]["category"] == "log"
    assert by_path["candidate_dump.pkl"]["category"] == "candidate_or_serialized_dump"
    assert by_path["candidate_dump.pkl"]["unsafe_to_deserialize_without_trust"] is True
    assert by_path["metrics/trace.jsonl"]["category"] == "structured_telemetry"
    assert by_path["weights/model.safetensors"]["category"] == "model_or_checkpoint"
    assert by_path["src/solver.py"]["category"] == "code"

    summary = module.summarize(rows)
    assert summary["file_count"] == 6
    assert "candidate_dump.pkl" in summary["unsafe_serialized_files"]
    assert "candidate_dump.pkl" in summary["candidate_or_telemetry_files"]
    assert "metrics/trace.jsonl" in summary["candidate_or_telemetry_files"]


def test_inventory_directory(tmp_path: Path) -> None:
    (tmp_path / "nested").mkdir()
    (tmp_path / "nested" / "scores.csv").write_text("x\n", encoding="utf-8")
    rows = module.inventory_directory(tmp_path)
    assert len(rows) == 1
    assert rows[0]["path"] == "nested/scores.csv"
    assert rows[0]["category"] == "structured_telemetry"
