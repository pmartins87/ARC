from __future__ import annotations

import json
from pathlib import Path


def test_e0006_gate_a_notebook_is_valid_and_inspect_only() -> None:
    path = Path("notebooks/E0006_lightning_gate_a_kaggle.ipynb")
    payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload["nbformat"] == 4
    assert len(payload["cells"]) == 2
    assert payload["cells"][0]["cell_type"] == "markdown"
    assert payload["cells"][1]["cell_type"] == "code"

    code = "".join(payload["cells"][1]["source"])
    assert "/kaggle/working/e0006_gate_a_inspect.json" in code
    assert 'HF_HUB_OFFLINE' in code
    assert 'TRANSFORMERS_OFFLINE' in code
    assert 'device_count' in code
    assert 'config.json' in code

    # Gate A must stay inspect-only. It may inventory vLLM as a package, but it
    # must not load a model, start a server, install packages, or use network IO.
    forbidden = (
        "AutoModelForCausalLM",
        "from_pretrained(",
        "vllm serve",
        "subprocess",
        "requests.",
        "urllib",
        "wget",
        "curl ",
        "pip install",
        "kagglehub.model_download",
        "hf_hub_download",
        "snapshot_download",
    )
    for token in forbidden:
        assert token not in code
