from __future__ import annotations

import argparse
import json
from pathlib import Path

from arcsolver.prompt_budget import load_visible_prompt_slots, profile_prompt_tokens


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Measure Nemotron/NVARC prompt-token pressure on public ARC evaluation tasks "
            "without reading test outputs."
        )
    )
    parser.add_argument("evaluation_directory", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument(
        "--model",
        default="nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16",
    )
    parser.add_argument("--json-out", type=Path, required=True)
    args = parser.parse_args()

    from huggingface_hub import HfApi
    from transformers import AutoTokenizer

    info = HfApi().model_info(args.model)
    tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)
    slots = load_visible_prompt_slots(args.evaluation_directory, manifest_path=args.manifest)
    report = profile_prompt_tokens(slots, tokenizer)
    report.update(
        {
            "model": args.model,
            "model_revision": info.sha,
            "visible_output_slots_profiled": len(slots),
            "leakage_guard": (
                "Training inputs/outputs and test inputs only. Test outputs are never copied into prompt records."
            ),
        }
    )

    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
