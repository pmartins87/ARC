from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
import platform
import sys
import time
from pathlib import Path
from typing import Any

from arcsolver.model_discovery import choose_model_root, discover_hf_model_roots


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


def package_version(name: str) -> str | None:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def classify_exception(exc: BaseException) -> str:
    text = f"{type(exc).__name__}: {exc}".lower()
    if isinstance(exc, ModuleNotFoundError):
        return "DEPENDENCY_MISSING"
    if "out of memory" in text or "cuda oom" in text:
        return "OOM_LOAD"
    if any(token in text for token in ("unsupported", "not implemented", "no kernel", "kernel", "architecture")):
        return "UNSUPPORTED_KERNEL_OR_ARCH"
    if any(token in text for token in ("connection", "http", "offline mode", "local_files_only")):
        return "OFFLINE_RESOURCE_ERROR"
    return "GENERATION_ERROR"


def inspect_cuda() -> dict[str, Any]:
    report: dict[str, Any] = {
        "torch_available": False,
        "cuda_available": False,
        "device_count": 0,
        "devices": [],
    }
    try:
        import torch
    except Exception as exc:  # pragma: no cover - depends on target runtime
        report["torch_error"] = f"{type(exc).__name__}: {exc}"
        return report

    report["torch_available"] = True
    report["torch_version"] = getattr(torch, "__version__", None)
    report["cuda_runtime"] = getattr(torch.version, "cuda", None)
    report["cuda_available"] = bool(torch.cuda.is_available())
    if not torch.cuda.is_available():
        return report

    count = torch.cuda.device_count()
    report["device_count"] = count
    for index in range(count):
        props = torch.cuda.get_device_properties(index)
        report["devices"].append(
            {
                "index": index,
                "name": props.name,
                "total_memory_gib": props.total_memory / 1024**3,
                "capability": list(torch.cuda.get_device_capability(index)),
            }
        )
    return report


def gpu_memory_snapshot() -> list[dict[str, Any]]:
    try:
        import torch
    except Exception:
        return []
    if not torch.cuda.is_available():
        return []

    rows = []
    for index in range(torch.cuda.device_count()):
        rows.append(
            {
                "index": index,
                "allocated_gib": torch.cuda.memory_allocated(index) / 1024**3,
                "reserved_gib": torch.cuda.memory_reserved(index) / 1024**3,
                "max_allocated_gib": torch.cuda.max_memory_allocated(index) / 1024**3,
                "max_reserved_gib": torch.cuda.max_memory_reserved(index) / 1024**3,
            }
        )
    return rows


def inspect_environment(input_root: Path, model_hint: str | None) -> dict[str, Any]:
    candidates = discover_hf_model_roots(input_root, name_hint=model_hint)
    return {
        "status": "INSPECT_ONLY",
        "python": sys.version,
        "platform": platform.platform(),
        "input_root": str(input_root),
        "input_root_exists": input_root.exists(),
        "offline_env": {
            "HF_HUB_OFFLINE": os.environ.get("HF_HUB_OFFLINE"),
            "TRANSFORMERS_OFFLINE": os.environ.get("TRANSFORMERS_OFFLINE"),
        },
        "packages": {
            name: package_version(name)
            for name in ("torch", "transformers", "accelerate", "vllm", "flashinfer-python")
        },
        "cuda": inspect_cuda(),
        "model_candidates": [str(path) for path in candidates],
    }


def resolve_model_path(args: argparse.Namespace) -> Path:
    if args.model_path is not None:
        path = Path(args.model_path)
        if not path.exists():
            raise FileNotFoundError(f"MODEL_NOT_FOUND: {path}")
        return path
    candidates = discover_hf_model_roots(args.input_root, name_hint=args.model_hint)
    try:
        return choose_model_root(candidates, prefer=args.model_hint)
    except FileNotFoundError as exc:
        raise FileNotFoundError("MODEL_NOT_FOUND: no attached local model matched") from exc


def run_transformers_smoke(args: argparse.Namespace) -> dict[str, Any]:
    # Force local-only behavior before importing any Hugging Face library.
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

    model_path = resolve_model_path(args)
    report: dict[str, Any] = {
        "status": "STARTING",
        "mode": "transformers",
        "model_path": str(model_path),
        "device_map": args.device_map,
        "max_new_tokens": args.max_new_tokens,
        "environment": inspect_environment(args.input_root, args.model_hint),
    }

    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        if not torch.cuda.is_available():
            raise RuntimeError("CUDA is not available")

        for index in range(torch.cuda.device_count()):
            torch.cuda.reset_peak_memory_stats(index)

        load_started = time.perf_counter()
        tokenizer = AutoTokenizer.from_pretrained(
            str(model_path),
            local_files_only=True,
            trust_remote_code=args.trust_remote_code,
        )
        model = AutoModelForCausalLM.from_pretrained(
            str(model_path),
            local_files_only=True,
            trust_remote_code=args.trust_remote_code,
            torch_dtype=torch.bfloat16,
            device_map=args.device_map,
            low_cpu_mem_usage=True,
        )
        report["load_seconds"] = time.perf_counter() - load_started
        report["memory_after_load"] = gpu_memory_snapshot()

        messages = [{"role": "user", "content": args.prompt}]
        if hasattr(tokenizer, "apply_chat_template"):
            rendered = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
            )
        else:
            rendered = args.prompt

        inputs = tokenizer(rendered, return_tensors="pt")
        input_device = next(model.parameters()).device
        inputs = {key: value.to(input_device) for key, value in inputs.items()}
        input_tokens = int(inputs["input_ids"].shape[-1])

        generation_started = time.perf_counter()
        with torch.inference_mode():
            output = model.generate(
                **inputs,
                max_new_tokens=args.max_new_tokens,
                do_sample=False,
                pad_token_id=(tokenizer.eos_token_id if tokenizer.pad_token_id is None else tokenizer.pad_token_id),
            )
        generation_seconds = time.perf_counter() - generation_started
        generated_tokens = int(output.shape[-1]) - input_tokens
        continuation = output[0, input_tokens:]

        report.update(
            {
                "status": "PASS",
                "input_tokens": input_tokens,
                "generated_tokens": generated_tokens,
                "generation_seconds": generation_seconds,
                "generated_tokens_per_second": (
                    generated_tokens / generation_seconds if generation_seconds > 0 else None
                ),
                "output_text": tokenizer.decode(continuation, skip_special_tokens=False),
                "memory_after_generation": gpu_memory_snapshot(),
            }
        )
        return report
    except Exception as exc:  # pragma: no cover - target-GPU diagnostic path
        report.update(
            {
                "status": "FAIL",
                "failure_class": classify_exception(exc),
                "exception_type": type(exc).__name__,
                "exception": str(exc),
                "memory_at_failure": gpu_memory_snapshot(),
            }
        )
        return report


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Offline-first Nemotron Lightning Kaggle feasibility smoke. Default mode only inspects "
            "the environment; it does not load a large model."
        )
    )
    parser.add_argument("--mode", choices=("inspect", "transformers"), default="inspect")
    parser.add_argument("--input-root", type=Path, default=Path("/kaggle/input"))
    parser.add_argument("--model-path")
    parser.add_argument("--model-hint", default="nemotron")
    parser.add_argument("--device-map", default="balanced")
    parser.add_argument("--max-new-tokens", type=int, default=32)
    parser.add_argument("--trust-remote-code", action="store_true")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

    if args.mode == "inspect":
        report = inspect_environment(args.input_root, args.model_hint)
        cuda = report["cuda"]
        if cuda.get("cuda_available") and cuda.get("device_count") != 4:
            report["warning"] = f"expected 4 GPUs for target smoke, found {cuda.get('device_count')}"
    else:
        if args.max_new_tokens <= 0:
            parser.error("--max-new-tokens must be positive")
        report = run_transformers_smoke(args)

    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
