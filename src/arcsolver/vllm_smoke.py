from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class VLLMSmokeConfig:
    model_path: str
    host: str = "127.0.0.1"
    port: int = 8000
    tensor_parallel_size: int = 4
    gpu_memory_utilization: float = 0.88
    max_model_len: int | None = 8192
    enable_expert_parallel: bool = True
    mamba_backend: str | None = "flashinfer"
    mamba_ssm_cache_dtype: str = "float16"
    enable_mamba_cache_stochastic_rounding: bool = True
    mamba_cache_philox_rounds: int | None = 5
    reasoning_parser: str | None = "nemotron_v3"
    tool_call_parser: str | None = "qwen3_coder"
    enable_auto_tool_choice: bool = True
    trust_remote_code: bool = False
    dtype: str = "bfloat16"
    enforce_eager: bool = True

    def validate(self) -> None:
        if not self.model_path:
            raise ValueError("model_path must be non-empty")
        if self.port <= 0 or self.port > 65535:
            raise ValueError("port must be in 1..65535")
        if self.tensor_parallel_size <= 0:
            raise ValueError("tensor_parallel_size must be positive")
        if not 0.0 < self.gpu_memory_utilization <= 1.0:
            raise ValueError("gpu_memory_utilization must be in (0, 1]")
        if self.max_model_len is not None and self.max_model_len <= 0:
            raise ValueError("max_model_len must be positive when provided")
        if self.mamba_cache_philox_rounds is not None and self.mamba_cache_philox_rounds <= 0:
            raise ValueError("mamba_cache_philox_rounds must be positive when provided")

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return asdict(self)


def build_vllm_serve_command(config: VLLMSmokeConfig, *, executable: str = "vllm") -> list[str]:
    """Build the conservative Lightning vLLM smoke command.

    The command follows NVIDIA's current Lightning 3.5 vLLM guidance where it
    materially affects compatibility, but deliberately lowers context length,
    disables speculative decoding, and enables eager execution for the first L4
    feasibility gate. The H100 memory-constrained recipe uses float16 Mamba SSM
    cache, which is also the conservative choice for 24 GiB L4s.
    """
    config.validate()
    cmd = [
        executable,
        "serve",
        str(Path(config.model_path)),
        "--host",
        config.host,
        "--port",
        str(config.port),
        "--tensor-parallel-size",
        str(config.tensor_parallel_size),
        "--gpu-memory-utilization",
        str(config.gpu_memory_utilization),
        "--dtype",
        config.dtype,
        "--mamba-ssm-cache-dtype",
        config.mamba_ssm_cache_dtype,
    ]
    if config.mamba_backend:
        cmd += ["--mamba-backend", config.mamba_backend]
    if config.enable_mamba_cache_stochastic_rounding:
        cmd.append("--enable-mamba-cache-stochastic-rounding")
    if config.mamba_cache_philox_rounds is not None:
        cmd += ["--mamba-cache-philox-rounds", str(config.mamba_cache_philox_rounds)]
    if config.max_model_len is not None:
        cmd += ["--max-model-len", str(config.max_model_len)]
    if config.enable_expert_parallel:
        cmd.append("--enable-expert-parallel")
    if config.reasoning_parser:
        cmd += ["--reasoning-parser", config.reasoning_parser]
    if config.tool_call_parser:
        cmd += ["--tool-call-parser", config.tool_call_parser]
    if config.enable_auto_tool_choice and config.tool_call_parser:
        cmd.append("--enable-auto-tool-choice")
    if config.trust_remote_code:
        cmd.append("--trust-remote-code")
    if config.enforce_eager:
        cmd.append("--enforce-eager")
    return cmd


def classify_server_failure(log_tail: str, returncode: int | None) -> str:
    text = log_tail.lower()
    if "out of memory" in text or "cuda oom" in text:
        return "OOM_LOAD_OR_INIT"
    if "no space left on device" in text:
        return "DISK_EXHAUSTED"
    if "no module named" in text or "command not found" in text:
        return "DEPENDENCY_MISSING"
    if "unrecognized arguments" in text or "no such option" in text:
        return "VLLM_VERSION_OR_FLAG_MISMATCH"
    if any(token in text for token in ("unsupported", "not implemented", "no kernel", "invalid device function")):
        return "UNSUPPORTED_KERNEL_OR_ARCH"
    if "model architecture" in text and "not supported" in text:
        return "UNSUPPORTED_MODEL_ARCH"
    if "address already in use" in text:
        return "PORT_IN_USE"
    if returncode is None:
        return "STARTUP_TIMEOUT"
    return "SERVER_EXITED"
