from __future__ import annotations

from pathlib import Path


def discover_hf_model_roots(root: str | Path, *, name_hint: str | None = None) -> list[Path]:
    """Find local Hugging Face-style model roots without importing ML libraries.

    A directory is considered a model root when it contains ``config.json`` and
    at least one tokenizer metadata file. ``name_hint`` is a case-insensitive
    substring filter on the full path. The function is deliberately filesystem-
    only so it can be tested in CI and used in internet-off Kaggle notebooks.
    """
    base = Path(root)
    if not base.exists():
        return []

    hint = name_hint.lower() if name_hint else None
    roots: set[Path] = set()
    tokenizer_names = {
        "tokenizer.json",
        "tokenizer_config.json",
        "tokenizer.model",
    }
    for config in base.rglob("config.json"):
        parent = config.parent
        if hint is not None and hint not in str(parent).lower():
            continue
        if any((parent / name).exists() for name in tokenizer_names):
            roots.add(parent)
    return sorted(roots)


def choose_model_root(candidates: list[Path], *, prefer: str | None = None) -> Path:
    if not candidates:
        raise FileNotFoundError("no local Hugging Face-style model root found")
    if prefer:
        needle = prefer.lower()
        preferred = [path for path in candidates if needle in str(path).lower()]
        if len(preferred) == 1:
            return preferred[0]
        if len(preferred) > 1:
            candidates = preferred
    if len(candidates) != 1:
        rendered = ", ".join(str(path) for path in candidates[:10])
        raise RuntimeError(f"ambiguous model roots ({len(candidates)}): {rendered}")
    return candidates[0]
