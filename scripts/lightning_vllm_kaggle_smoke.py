from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from arcsolver.model_discovery import choose_model_root, discover_hf_model_roots
from arcsolver.vllm_smoke import VLLMSmokeConfig, build_vllm_serve_command, classify_server_failure


DEFAULT_PROMPT = """Find the common rule that maps each input grid to its output grid, then solve the test input. Return only the final grid.

Train 1
Input:
0 1
0 0
Output:
1 0
0 0

Train 2
Input:
0 0 1
0 0 0
Output:
1 0 0
0 0 0

Test Input:
0 0
1 0
"""


def request_json(url: str, *, payload: dict[str, Any] | None = None, timeout: float = 10.0) -> Any:
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


def wait_for_health(base_url: str, process: subprocess.Popen[Any], *, timeout_s: float, poll_s: float = 5.0) -> tuple[bool, float]:
    started = time.perf_counter()
    while time.perf_counter() - started < timeout_s:
        if process.poll() is not None:
            return False, time.perf_counter() - started
        try:
            with urllib.request.urlopen(f"{base_url}/health", timeout=3.0) as response:
                if 200 <= response.status < 300:
                    return True, time.perf_counter() - started
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            pass
        time.sleep(poll_s)
    return False, time.perf_counter() - started


def nvidia_smi_snapshot() -> list[dict[str, Any]]:
    executable = shutil.which("nvidia-smi")
    if executable is None:
        return []
    cmd = [
        executable,
        "--query-gpu=index,name,memory.total,memory.used,memory.free,utilization.gpu",
        "--format=csv,noheader,nounits",
    ]
    try:
        completed = subprocess.run(cmd, capture_output=True, text=True, timeout=15, check=True)
    except Exception:
        return []
    rows: list[dict[str, Any]] = []
    for line in completed.stdout.splitlines():
        fields = [field.strip() for field in line.split(",")]
        if len(fields) != 6:
            continue
        index, name, total, used, free, util = fields
        rows.append(
            {
                "index": int(index),
                "name": name,
                "memory_total_mib": int(total),
                "memory_used_mib": int(used),
                "memory_free_mib": int(free),
                "utilization_gpu_percent": int(util),
            }
        )
    return rows


def tail_text(path: Path, max_chars: int = 20000) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    return text[-max_chars:]


def resolve_model_path(input_root: Path, explicit: str | None, hint: str | None) -> Path:
    if explicit:
        path = Path(explicit)
        if not path.exists():
            raise FileNotFoundError(f"MODEL_NOT_FOUND: {path}")
        return path
    candidates = discover_hf_model_roots(input_root, name_hint=hint)
    return choose_model_root(candidates, prefer=hint)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Launch a conservative, offline vLLM tensor-parallel smoke for Nemotron 3.5 Lightning on Kaggle. "
            "This is a feasibility diagnostic, not a leaderboard submission."
        )
    )
    parser.add_argument("--input-root", type=Path, default=Path("/kaggle/input"))
    parser.add_argument("--model-path")
    parser.add_argument("--model-hint", default="nemotron")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--startup-timeout-seconds", type=float, default=1800.0)
    parser.add_argument("--gpu-memory-utilization", type=float, default=0.88)
    parser.add_argument("--max-model-len", type=int, default=8192)
    parser.add_argument("--max-tokens", type=int, default=64)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    parser.add_argument("--log-path", type=Path, default=Path("/kaggle/working/lightning_vllm_serve.log"))
    parser.add_argument("--json-out", type=Path, default=Path("/kaggle/working/lightning_vllm_smoke.json"))
    parser.add_argument("--trust-remote-code", action="store_true")
    parser.add_argument("--no-expert-parallel", action="store_true")
    parser.add_argument("--no-enforce-eager", action="store_true")
    parser.add_argument("--keep-server", action="store_true")
    args = parser.parse_args()

    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

    report: dict[str, Any] = {
        "status": "STARTING",
        "purpose": "deployment_feasibility_only",
        "internet_required": False,
        "gpu_before": nvidia_smi_snapshot(),
    }
    process: subprocess.Popen[Any] | None = None

    try:
        if shutil.which("vllm") is None:
            raise RuntimeError("vllm executable not found in the Kaggle image")
        model_path = resolve_model_path(args.input_root, args.model_path, args.model_hint)
        config = VLLMSmokeConfig(
            model_path=str(model_path),
            port=args.port,
            tensor_parallel_size=4,
            gpu_memory_utilization=args.gpu_memory_utilization,
            max_model_len=args.max_model_len,
            enable_expert_parallel=not args.no_expert_parallel,
            trust_remote_code=args.trust_remote_code,
            enforce_eager=not args.no_enforce_eager,
        )
        command = build_vllm_serve_command(config)
        report["model_path"] = str(model_path)
        report["server_config"] = config.to_dict()
        report["command"] = command

        args.log_path.parent.mkdir(parents=True, exist_ok=True)
        with args.log_path.open("w", encoding="utf-8") as log_file:
            process = subprocess.Popen(command, stdout=log_file, stderr=subprocess.STDOUT, text=True)

        base_url = f"http://127.0.0.1:{args.port}"
        healthy, startup_seconds = wait_for_health(
            base_url,
            process,
            timeout_s=args.startup_timeout_seconds,
        )
        report["startup_seconds"] = startup_seconds
        report["gpu_after_startup"] = nvidia_smi_snapshot()
        if not healthy:
            log_tail = tail_text(args.log_path)
            returncode = process.poll()
            report.update(
                {
                    "status": "FAIL",
                    "failure_class": classify_server_failure(log_tail, returncode),
                    "server_returncode": returncode,
                    "log_tail": log_tail,
                }
            )
        else:
            models = request_json(f"{base_url}/v1/models", timeout=15.0)
            model_ids = [item.get("id") for item in models.get("data", []) if item.get("id")]
            if not model_ids:
                raise RuntimeError("vLLM health passed but /v1/models exposed no model id")
            served_model = model_ids[0]
            payload = {
                "model": served_model,
                "messages": [{"role": "user", "content": args.prompt}],
                "temperature": args.temperature,
                "max_tokens": args.max_tokens,
            }
            generation_started = time.perf_counter()
            response = request_json(f"{base_url}/v1/chat/completions", payload=payload, timeout=600.0)
            generation_seconds = time.perf_counter() - generation_started
            usage = response.get("usage") or {}
            completion_tokens = usage.get("completion_tokens")
            choices = response.get("choices") or []
            message = choices[0].get("message", {}) if choices else {}
            report.update(
                {
                    "status": "PASS",
                    "served_model": served_model,
                    "generation_seconds": generation_seconds,
                    "prompt_tokens": usage.get("prompt_tokens"),
                    "completion_tokens": completion_tokens,
                    "completion_tokens_per_second": (
                        completion_tokens / generation_seconds
                        if isinstance(completion_tokens, (int, float)) and generation_seconds > 0
                        else None
                    ),
                    "output_text": message.get("content"),
                    "reasoning_text": message.get("reasoning_content"),
                    "gpu_after_generation": nvidia_smi_snapshot(),
                    "log_tail": tail_text(args.log_path, max_chars=8000),
                }
            )
    except Exception as exc:
        report.update(
            {
                "status": "FAIL",
                "failure_class": "HARNESS_OR_REQUEST_ERROR",
                "exception_type": type(exc).__name__,
                "exception": str(exc),
                "gpu_at_failure": nvidia_smi_snapshot(),
                "log_tail": tail_text(args.log_path) if args.log_path.exists() else "",
            }
        )
    finally:
        if process is not None and process.poll() is None and not args.keep_server:
            process.terminate()
            try:
                process.wait(timeout=30)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=10)
        report["server_kept_alive"] = bool(args.keep_server and process is not None and process.poll() is None)
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
