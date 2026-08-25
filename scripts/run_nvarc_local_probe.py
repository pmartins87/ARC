from __future__ import annotations

import argparse
import json
import time
import urllib.request
from pathlib import Path
from typing import Any

from arcsolver.nvarc_protocol import build_messages, verify_response


def request_json(url: str, *, payload: dict[str, Any] | None = None, timeout: float = 600.0) -> Any:
    data = None
    headers: dict[str, str] = {}
    method = "GET"
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
        method = "POST"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def load_manifest(path: Path, split: str) -> list[str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    splits = payload.get("splits") or {}
    task_ids = list(splits.get(split, []))
    if not task_ids:
        raise ValueError(f"manifest split {split!r} is empty")
    return task_ids


def load_task(path: Path) -> dict[str, Any]:
    task = json.loads(path.read_text(encoding="utf-8"))
    if not task.get("train") or not task.get("test"):
        raise ValueError(f"invalid ARC task: {path}")
    return task


def response_text(response: dict[str, Any]) -> tuple[str, str | None, dict[str, Any]]:
    choices = response.get("choices") or []
    if not choices:
        raise ValueError("chat response has no choices")
    message = choices[0].get("message") or {}
    content = message.get("content") or ""
    reasoning = message.get("reasoning_content")
    usage = response.get("usage") or {}
    return str(content), (str(reasoning) if reasoning is not None else None), usage


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run a bounded NVARC-compatible probe against an already-running local vLLM server."
    )
    parser.add_argument("task_directory", type=Path)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--split", choices=("development", "validation", "heldout"), default="development")
    parser.add_argument("--allow-gate", action="store_true", help="required to touch validation/heldout")
    parser.add_argument("--mode", choices=("transductive", "inductive"), default="transductive")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--model")
    parser.add_argument("--limit-tasks", type=int, default=3)
    parser.add_argument("--attempts", type=int, choices=(1, 2), default=1)
    parser.add_argument("--max-tokens", type=int, default=2048)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=20260825)
    parser.add_argument("--request-timeout-seconds", type=float, default=900.0)
    parser.add_argument("--transform-timeout-seconds", type=float, default=30.0)
    parser.add_argument("--json-out", type=Path, default=Path("/kaggle/working/nvarc_probe.json"))
    parser.add_argument("--jsonl-out", type=Path, default=Path("/kaggle/working/nvarc_probe_raw.jsonl"))
    args = parser.parse_args()

    if args.split != "development" and not args.allow_gate:
        parser.error("validation/heldout are sealed: pass --allow-gate only at an approved milestone gate")
    if args.limit_tasks <= 0:
        parser.error("--limit-tasks must be positive")
    if args.max_tokens <= 0:
        parser.error("--max-tokens must be positive")

    models = request_json(f"{args.base_url}/v1/models", timeout=30.0)
    model_ids = [item.get("id") for item in models.get("data", []) if item.get("id")]
    model = args.model or (model_ids[0] if model_ids else None)
    if not model:
        raise RuntimeError("vLLM endpoint exposed no model id")

    task_ids = load_manifest(args.manifest, args.split)[: args.limit_tasks]
    args.jsonl_out.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []

    with args.jsonl_out.open("w", encoding="utf-8") as raw_file:
        for task_id in task_ids:
            task = load_task(args.task_directory / f"{task_id}.json")
            train = [{"input": pair["input"], "output": pair["output"]} for pair in task["train"]]
            for test_index, pair in enumerate(task["test"]):
                if "output" not in pair:
                    raise ValueError(
                        f"{task_id}[{test_index}] has no public output; this probe only supports public development data"
                    )
                test_input = pair["input"]
                expected = pair["output"]
                messages = build_messages(train, test_input, mode=args.mode)
                attempts: list[dict[str, Any]] = []

                for attempt_index in range(args.attempts):
                    payload = {
                        "model": model,
                        "messages": messages,
                        "max_tokens": args.max_tokens,
                        "temperature": args.temperature,
                        "seed": args.seed + attempt_index,
                    }
                    started = time.perf_counter()
                    response = request_json(
                        f"{args.base_url}/v1/chat/completions",
                        payload=payload,
                        timeout=args.request_timeout_seconds,
                    )
                    elapsed = time.perf_counter() - started
                    content, reasoning, usage = response_text(response)
                    verified = verify_response(
                        content,
                        test_input=test_input,
                        expected_output=expected,
                        mode=args.mode,
                        timeout_seconds=args.transform_timeout_seconds,
                    )
                    attempt = {
                        "attempt_index": attempt_index + 1,
                        "seed": args.seed + attempt_index,
                        "request_seconds": elapsed,
                        "usage": usage,
                        "content": content,
                        "reasoning_content": reasoning,
                        "verification": verified.to_dict(),
                    }
                    attempts.append(attempt)

                row = {
                    "task_id": task_id,
                    "test_index": test_index,
                    "mode": args.mode,
                    "attempts": attempts,
                    "pass_at_1": bool(attempts[0]["verification"]["exact_match"]),
                    "pass_at_2": any(attempt["verification"]["exact_match"] for attempt in attempts[:2]),
                }
                rows.append(row)
                raw_file.write(json.dumps(row, sort_keys=True) + "\n")
                raw_file.flush()

    total = len(rows)
    pass1 = sum(row["pass_at_1"] for row in rows)
    pass2 = sum(row["pass_at_2"] for row in rows)
    extraction_attempts = [
        attempt["verification"]["extraction_successful"]
        for row in rows
        for attempt in row["attempts"]
    ]
    request_seconds = [attempt["request_seconds"] for row in rows for attempt in row["attempts"]]
    completion_tokens = [
        attempt["usage"].get("completion_tokens")
        for row in rows
        for attempt in row["attempts"]
        if isinstance(attempt["usage"].get("completion_tokens"), int)
    ]

    report = {
        "status": "PASS",
        "purpose": "bounded_local_development_probe",
        "model": model,
        "mode": args.mode,
        "prompt_contract": (
            "nvidia_public_transductive" if args.mode == "transductive" else "controlled_inductive_v1"
        ),
        "split": args.split,
        "task_count": len(task_ids),
        "output_count": total,
        "attempts_per_output": args.attempts,
        "max_tokens": args.max_tokens,
        "temperature": args.temperature,
        "pass_at_1_correct": pass1,
        "pass_at_1": pass1 / total if total else 0.0,
        "pass_at_2_correct": pass2,
        "pass_at_2": pass2 / total if total else 0.0,
        "attempt2_rescues": pass2 - pass1,
        "extraction_success_rate": (
            sum(extraction_attempts) / len(extraction_attempts) if extraction_attempts else 0.0
        ),
        "request_seconds_total": sum(request_seconds),
        "request_seconds_mean": sum(request_seconds) / len(request_seconds) if request_seconds else 0.0,
        "completion_tokens_total": sum(completion_tokens),
        "raw_jsonl": str(args.jsonl_out),
        "leakage_guard": "Only development tasks by default; test outputs are withheld from prompts and used only after generation for exact scoring.",
    }
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
