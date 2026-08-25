from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True)
class DatasetFingerprint:
    task_count: int
    output_slots: int
    task_ids_sha256: str
    test_count_signature_sha256: str
    canonical_challenges_sha256: str
    test_counts: dict[str, int]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FingerprintDiff:
    task_ids_match: bool
    output_slots_match: bool
    canonical_hash_match: bool
    missing_task_ids: tuple[str, ...]
    extra_task_ids: tuple[str, ...]
    test_count_mismatches: dict[str, tuple[int, int]]

    @property
    def compatible_schema(self) -> bool:
        return (
            self.task_ids_match
            and self.output_slots_match
            and not self.test_count_mismatches
        )

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["compatible_schema"] = self.compatible_schema
        return data


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def fingerprint_challenges(challenges: Mapping[str, Any]) -> DatasetFingerprint:
    """Fingerprint ARC challenge structure and canonical content.

    The test-count signature is deliberately independent of dictionary order and
    catches the provenance failure that matters for submission compatibility:
    same-looking task IDs with a different number of test outputs.
    """
    if not isinstance(challenges, Mapping) or not challenges:
        raise ValueError("challenges must be a non-empty mapping")

    test_counts: dict[str, int] = {}
    for task_id in sorted(challenges):
        task = challenges[task_id]
        if not isinstance(task, Mapping):
            raise ValueError(f"{task_id}: task must be a mapping")
        tests = task.get("test")
        if not isinstance(tests, list) or not tests:
            raise ValueError(f"{task_id}: task must contain a non-empty test list")
        test_counts[str(task_id)] = len(tests)

    task_ids = sorted(test_counts)
    output_slots = sum(test_counts.values())
    return DatasetFingerprint(
        task_count=len(task_ids),
        output_slots=output_slots,
        task_ids_sha256=_sha256_bytes("\n".join(task_ids).encode("utf-8")),
        test_count_signature_sha256=_sha256_bytes(_canonical_json_bytes(test_counts)),
        canonical_challenges_sha256=_sha256_bytes(_canonical_json_bytes(challenges)),
        test_counts=test_counts,
    )


def fingerprint_challenge_file(path: str | Path) -> DatasetFingerprint:
    source = Path(path)
    challenges = json.loads(source.read_text(encoding="utf-8"))
    return fingerprint_challenges(challenges)


def compare_fingerprints(
    reference: DatasetFingerprint,
    candidate: DatasetFingerprint,
) -> FingerprintDiff:
    reference_ids = set(reference.test_counts)
    candidate_ids = set(candidate.test_counts)
    shared = sorted(reference_ids & candidate_ids)
    mismatches = {
        task_id: (reference.test_counts[task_id], candidate.test_counts[task_id])
        for task_id in shared
        if reference.test_counts[task_id] != candidate.test_counts[task_id]
    }
    return FingerprintDiff(
        task_ids_match=reference_ids == candidate_ids,
        output_slots_match=reference.output_slots == candidate.output_slots,
        canonical_hash_match=(
            reference.canonical_challenges_sha256
            == candidate.canonical_challenges_sha256
        ),
        missing_task_ids=tuple(sorted(reference_ids - candidate_ids)),
        extra_task_ids=tuple(sorted(candidate_ids - reference_ids)),
        test_count_mismatches=mismatches,
    )


def submission_schema_fingerprint(submission: Mapping[str, Any]) -> DatasetFingerprint:
    """Create a structural fingerprint from an ARC submission JSON.

    Candidate grids are intentionally ignored. We synthesize a minimal challenge
    object carrying only the task IDs and number of output slots, then fingerprint
    that structure. The canonical content hash therefore describes the synthetic
    schema object, not the underlying challenge inputs.
    """
    if not isinstance(submission, Mapping) or not submission:
        raise ValueError("submission must be a non-empty mapping")
    challenges: dict[str, Any] = {}
    for task_id, outputs in submission.items():
        if not isinstance(outputs, list) or not outputs:
            raise ValueError(f"{task_id}: submission outputs must be a non-empty list")
        challenges[str(task_id)] = {"test": [{} for _ in outputs]}
    return fingerprint_challenges(challenges)
