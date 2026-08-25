from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from statistics import mean, median
from typing import Any, Iterable, Mapping, Sequence

from arcsolver.nvarc_protocol import AgentMode, build_messages


@dataclass(frozen=True)
class VisiblePromptSlot:
    task_id: str
    split: str
    test_index: int
    train: tuple[Mapping[str, Any], ...]
    test_input: list[list[int]]


@dataclass(frozen=True)
class NumericSummary:
    count: int
    minimum: float
    median: float
    mean: float
    p90: float
    p95: float
    maximum: float

    def to_dict(self) -> dict[str, float | int]:
        return asdict(self)


def _percentile_nearest_rank(values: Sequence[int], q: float) -> float:
    if not values:
        raise ValueError("cannot summarize empty values")
    if not 0.0 <= q <= 1.0:
        raise ValueError("q must be in [0, 1]")
    data = sorted(values)
    if q == 0:
        return float(data[0])
    rank = max(1, int((q * len(data)) + 0.9999999999))
    return float(data[min(len(data), rank) - 1])


def summarize(values: Iterable[int]) -> NumericSummary:
    data = list(values)
    if not data:
        raise ValueError("cannot summarize empty values")
    return NumericSummary(
        count=len(data),
        minimum=float(min(data)),
        median=float(median(data)),
        mean=float(mean(data)),
        p90=_percentile_nearest_rank(data, 0.90),
        p95=_percentile_nearest_rank(data, 0.95),
        maximum=float(max(data)),
    )


def load_split_membership(manifest_path: Path | None) -> dict[str, str]:
    if manifest_path is None:
        return {}
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    splits = payload.get("splits")
    if not isinstance(splits, dict):
        raise ValueError("manifest missing splits mapping")
    membership: dict[str, str] = {}
    for split_name, task_ids in splits.items():
        for task_id in task_ids:
            if task_id in membership:
                raise ValueError(f"task {task_id} appears in multiple splits")
            membership[str(task_id)] = str(split_name)
    return membership


def load_visible_prompt_slots(
    evaluation_directory: Path,
    *,
    manifest_path: Path | None = None,
) -> list[VisiblePromptSlot]:
    membership = load_split_membership(manifest_path)
    slots: list[VisiblePromptSlot] = []
    for path in sorted(evaluation_directory.glob("*.json")):
        task_id = path.stem
        payload = json.loads(path.read_text(encoding="utf-8"))
        train_raw = payload.get("train")
        test_raw = payload.get("test")
        if not isinstance(train_raw, list) or not isinstance(test_raw, list):
            raise ValueError(f"task {task_id} missing train/test arrays")

        # Training outputs are legitimate visible demonstrations. Test outputs are
        # deliberately never copied/read into the prompt-slot record.
        train: list[Mapping[str, Any]] = []
        for pair in train_raw:
            train.append({"input": pair["input"], "output": pair["output"]})

        split = membership.get(task_id, "unassigned")
        for test_index, pair in enumerate(test_raw):
            slots.append(
                VisiblePromptSlot(
                    task_id=task_id,
                    split=split,
                    test_index=test_index,
                    train=tuple(train),
                    test_input=pair["input"],
                )
            )
    if not slots:
        raise ValueError(f"no evaluation task slots found in {evaluation_directory}")
    return slots


def _token_count(tokenizer: Any, messages: list[dict[str, str]]) -> int:
    encoded = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True)
    if isinstance(encoded, dict):
        encoded = encoded.get("input_ids")
    if hasattr(encoded, "tolist"):
        encoded = encoded.tolist()
    if isinstance(encoded, list) and encoded and isinstance(encoded[0], list):
        if len(encoded) != 1:
            raise ValueError("unexpected batched chat-template output")
        encoded = encoded[0]
    if not isinstance(encoded, list):
        raise TypeError(f"unsupported tokenizer output type: {type(encoded).__name__}")
    return len(encoded)


def profile_prompt_tokens(
    slots: Sequence[VisiblePromptSlot],
    tokenizer: Any,
    *,
    modes: Sequence[AgentMode] = ("transductive", "inductive"),
    thresholds: Sequence[int] = (4096, 8192, 16384, 32768),
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for slot in slots:
        for mode in modes:
            messages = build_messages(slot.train, slot.test_input, mode=mode)
            tokens = _token_count(tokenizer, messages)
            rows.append(
                {
                    "task_id": slot.task_id,
                    "split": slot.split,
                    "test_index": slot.test_index,
                    "mode": mode,
                    "prompt_tokens": tokens,
                }
            )

    report: dict[str, Any] = {"modes": {}, "rows": rows}
    for mode in modes:
        mode_rows = [row for row in rows if row["mode"] == mode]
        counts = [int(row["prompt_tokens"]) for row in mode_rows]
        by_split: dict[str, Any] = {}
        for split in sorted({str(row["split"]) for row in mode_rows}):
            split_counts = [int(row["prompt_tokens"]) for row in mode_rows if row["split"] == split]
            by_split[split] = summarize(split_counts).to_dict()
        max_row = max(mode_rows, key=lambda row: int(row["prompt_tokens"]))
        report["modes"][mode] = {
            "summary": summarize(counts).to_dict(),
            "thresholds": {
                str(threshold): {
                    "count_over": sum(value > threshold for value in counts),
                    "fraction_over": sum(value > threshold for value in counts) / len(counts),
                }
                for threshold in thresholds
            },
            "by_split": by_split,
            "max_slot": max_row,
        }
    return report
