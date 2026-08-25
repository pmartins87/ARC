from __future__ import annotations

import argparse
import json
from math import ceil
from pathlib import Path
from statistics import mean, median
from typing import Any, Iterable

from arcsolver.nvarc_protocol import build_messages


def percentile(values: list[int], q: float) -> int:
    if not values:
        return 0
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, ceil(q * len(ordered)) - 1))
    return ordered[index]


def summarize(values: list[int]) -> dict[str, float | int]:
    if not values:
        return {"count": 0, "min": 0, "median": 0, "mean": 0.0, "p90": 0, "p95": 0, "max": 0}
    return {
        "count": len(values),
        "min": min(values),
        "median": median(values),
        "mean": mean(values),
        "p90": percentile(values, 0.90),
        "p95": percentile(values, 0.95),
        "max": max(values),
    }


def token_count(tokenizer: Any, messages: list[dict[str, str]]) -> int:
    encoded = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
    )
    if hasattr(encoded, "input_ids"):
        encoded = encoded.input_ids
    if isinstance(encoded, dict):
        encoded = encoded["input_ids"]
    if encoded and isinstance(encoded[0], list):
        if len(encoded) != 1:
            raise ValueError("unexpected batched tokenizer output")
        encoded = encoded[0]
    return len(encoded)


def load_manifest(path: Path) -> dict[str, list[str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    splits = payload.get("splits")
    if not isinstance(splits, dict):
        raise ValueError("manifest missing splits")
    return {name: list(ids) for name, ids in splits.items()}


def task_prompt_counts(
    tokenizer: Any,
    task: dict[str, Any],
    *,
    mode: str,
) -> Iterable[tuple[int, int, int]]:
    train = [{"input": pair["input"], "output": pair["output"]} for pair in task["train"]]
    for pair in task["test"]:
        # Deliberately read only test input here; public test output is irrelevant to prompt length.
        messages = build_messages(train, pair["input"], mode=mode)
        chars = sum(len(message["content"]) for message in messages)
        cells = sum(
            len(row)
            for train_pair in train
            for grid in (train_pair["input"], train_pair["output"])
            for row in grid
        ) + sum(len(row) for row in pair["input"])
        yield token_count(tokenizer, messages), chars, cells


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Measure exact Nemotron 3.5 Lightning chat-template prompt token counts on visible ARC inputs."
    )
    parser.add_argument("task_directory", type=Path)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--model", default="nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16")
    parser.add_argument("--mode", choices=("transductive", "inductive"), default="transductive")
    parser.add_argument("--json-out", type=Path, required=True)
    args = parser.parse_args()

    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(args.model)
    splits = load_manifest(args.manifest)
    split_reports: dict[str, Any] = {}
    all_tokens: list[int] = []
    all_chars: list[int] = []
    all_cells: list[int] = []

    for split_name in ("development", "validation", "heldout"):
        tokens: list[int] = []
        chars: list[int] = []
        cells: list[int] = []
        for task_id in splits[split_name]:
            task = json.loads((args.task_directory / f"{task_id}.json").read_text(encoding="utf-8"))
            for token_len, char_len, cell_count in task_prompt_counts(tokenizer, task, mode=args.mode):
                tokens.append(token_len)
                chars.append(char_len)
                cells.append(cell_count)
        all_tokens.extend(tokens)
        all_chars.extend(chars)
        all_cells.extend(cells)
        split_reports[split_name] = {
            "prompt_tokens": summarize(tokens),
            "prompt_chars": summarize(chars),
            "visible_grid_cells": summarize(cells),
            "over_context": {
                str(limit): sum(value > limit for value in tokens)
                for limit in (4096, 8192, 16384, 32768)
            },
        }

    report = {
        "model": args.model,
        "tokenizer_class": tokenizer.__class__.__name__,
        "mode": args.mode,
        "prompt_contract": (
            "nvidia_public_transductive" if args.mode == "transductive" else "controlled_inductive_v1"
        ),
        "all_public_evaluation_outputs": {
            "prompt_tokens": summarize(all_tokens),
            "prompt_chars": summarize(all_chars),
            "visible_grid_cells": summarize(all_cells),
            "over_context": {
                str(limit): sum(value > limit for value in all_tokens)
                for limit in (4096, 8192, 16384, 32768)
            },
        },
        "splits": split_reports,
        "leakage_guard": "Tokenization uses train inputs/outputs and test inputs only; test outputs are never read.",
    }
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
