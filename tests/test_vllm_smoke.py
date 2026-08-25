from __future__ import annotations

import pytest

from arcsolver.vllm_smoke import (
    VLLMSmokeConfig,
    build_vllm_serve_command,
    classify_server_failure,
)


def test_build_vllm_serve_command_matches_lightning_shape() -> None:
    config = VLLMSmokeConfig(model_path="/kaggle/input/lightning/model", port=8123)
    cmd = build_vllm_serve_command(config)

    assert cmd[:3] == ["vllm", "serve", "/kaggle/input/lightning/model"]
    assert ["--tensor-parallel-size", "4"] == cmd[
        cmd.index("--tensor-parallel-size") : cmd.index("--tensor-parallel-size") + 2
    ]
    assert "--enable-expert-parallel" in cmd
    assert ["--mamba-ssm-cache-dtype", "float32"] == cmd[
        cmd.index("--mamba-ssm-cache-dtype") : cmd.index("--mamba-ssm-cache-dtype") + 2
    ]
    assert ["--reasoning-parser", "nemotron_v3"] == cmd[
        cmd.index("--reasoning-parser") : cmd.index("--reasoning-parser") + 2
    ]
    assert ["--tool-call-parser", "qwen3_coder"] == cmd[
        cmd.index("--tool-call-parser") : cmd.index("--tool-call-parser") + 2
    ]
    assert "--enforce-eager" in cmd
    assert "--speculative-config" not in cmd


def test_optional_flags_can_be_disabled() -> None:
    config = VLLMSmokeConfig(
        model_path="/m",
        enable_expert_parallel=False,
        reasoning_parser=None,
        tool_call_parser=None,
        max_model_len=None,
        enforce_eager=False,
    )
    cmd = build_vllm_serve_command(config)
    assert "--enable-expert-parallel" not in cmd
    assert "--reasoning-parser" not in cmd
    assert "--tool-call-parser" not in cmd
    assert "--max-model-len" not in cmd
    assert "--enforce-eager" not in cmd


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"port": 0}, "port"),
        ({"tensor_parallel_size": 0}, "tensor_parallel_size"),
        ({"gpu_memory_utilization": 0.0}, "gpu_memory_utilization"),
        ({"max_model_len": -1}, "max_model_len"),
    ],
)
def test_config_validation(kwargs: dict[str, object], message: str) -> None:
    config = VLLMSmokeConfig(model_path="/m", **kwargs)
    with pytest.raises(ValueError, match=message):
        config.validate()


def test_failure_classification() -> None:
    assert classify_server_failure("CUDA out of memory", 1) == "OOM_LOAD_OR_INIT"
    assert classify_server_failure("No module named vllm", 1) == "DEPENDENCY_MISSING"
    assert classify_server_failure("invalid device function", 1) == "UNSUPPORTED_KERNEL_OR_ARCH"
    assert classify_server_failure("address already in use", 1) == "PORT_IN_USE"
    assert classify_server_failure("still waiting", None) == "STARTUP_TIMEOUT"
    assert classify_server_failure("unexpected exit", 2) == "SERVER_EXITED"
