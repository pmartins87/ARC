from __future__ import annotations

import json
from pathlib import Path

from arcsolver.prompt_budget import load_visible_prompt_slots, profile_prompt_tokens, summarize


class RecordingTokenizer:
    def __init__(self) -> None:
        self.rendered: list[str] = []

    def apply_chat_template(self, messages, *, tokenize, add_generation_prompt):
        assert tokenize is True
        assert add_generation_prompt is True
        text = "\n".join(message["content"] for message in messages)
        self.rendered.append(text)
        return list(range(len(text)))


def test_summary_nearest_rank() -> None:
    result = summarize([1, 2, 3, 4, 100])
    assert result.count == 5
    assert result.median == 3
    assert result.maximum == 100
    assert result.p90 == 100


def test_visible_slots_never_copy_test_output(tmp_path: Path) -> None:
    evaluation = tmp_path / "evaluation"
    evaluation.mkdir()
    (evaluation / "taskx.json").write_text(
        json.dumps(
            {
                "train": [
                    {"input": [[0, 1]], "output": [[1, 0]]},
                ],
                "test": [
                    {"input": [[2, 3]], "output": [[9, 9], [9, 9]]},
                    {"input": [[4, 5]], "output": [[8, 8], [8, 8]]},
                ],
            }
        ),
        encoding="utf-8",
    )
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps({"splits": {"development": ["taskx"], "validation": [], "heldout": []}}),
        encoding="utf-8",
    )

    slots = load_visible_prompt_slots(evaluation, manifest_path=manifest)
    assert len(slots) == 2
    assert slots[0].split == "development"
    assert not hasattr(slots[0], "expected_output")

    tokenizer = RecordingTokenizer()
    report = profile_prompt_tokens(slots, tokenizer, thresholds=(10, 100000))
    assert len(report["rows"]) == 4
    rendered = "\n".join(tokenizer.rendered)
    assert "99\n99" not in rendered
    assert "88\n88" not in rendered
    assert "01" in rendered
    assert "10" in rendered
    assert "23" in rendered
    assert "45" in rendered
    assert set(report["modes"]) == {"transductive", "inductive"}
