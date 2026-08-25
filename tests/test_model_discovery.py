from pathlib import Path

import pytest

from arcsolver.model_discovery import discover_hf_model_roots, choose_model_root


def _make_model(root: Path, name: str, *, tokenizer: str = "tokenizer_config.json") -> Path:
    model = root / name
    model.mkdir(parents=True)
    (model / "config.json").write_text("{}", encoding="utf-8")
    (model / tokenizer).write_text("{}", encoding="utf-8")
    return model


def test_discover_finds_complete_hf_model_roots(tmp_path: Path):
    expected = _make_model(tmp_path, "models/Nemotron-Lightning")
    incomplete = tmp_path / "models" / "incomplete"
    incomplete.mkdir()
    (incomplete / "config.json").write_text("{}", encoding="utf-8")

    assert discover_hf_model_roots(tmp_path) == [expected]


def test_discover_accepts_common_tokenizer_metadata(tmp_path: Path):
    a = _make_model(tmp_path, "a", tokenizer="tokenizer.json")
    b = _make_model(tmp_path, "b", tokenizer="tokenizer.model")

    assert discover_hf_model_roots(tmp_path) == [a, b]


def test_name_hint_is_case_insensitive(tmp_path: Path):
    expected = _make_model(tmp_path, "NVIDIA/Nemotron-3.5-Lightning")
    _make_model(tmp_path, "other/model")

    assert discover_hf_model_roots(tmp_path, name_hint="nEmOtRoN") == [expected]


def test_choose_unique_model_root(tmp_path: Path):
    model = _make_model(tmp_path, "only")
    assert choose_model_root([model]) == model


def test_choose_prefers_matching_root(tmp_path: Path):
    lightning = _make_model(tmp_path, "Nemotron-Lightning")
    other = _make_model(tmp_path, "Other")
    assert choose_model_root([other, lightning], prefer="lightning") == lightning


def test_choose_fails_closed_when_empty_or_ambiguous(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        choose_model_root([])

    a = _make_model(tmp_path, "a")
    b = _make_model(tmp_path, "b")
    with pytest.raises(RuntimeError, match="ambiguous"):
        choose_model_root([a, b])
