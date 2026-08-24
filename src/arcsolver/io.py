from __future__ import annotations

import json
from pathlib import Path
from typing import Any

Grid = list[list[int]]


def load_json(path: str | Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as fh:
        return json.load(fh)


def save_json(data: Any, path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, separators=(",", ":"))


def validate_grid(grid: Grid) -> None:
    if not isinstance(grid, list) or not grid:
        raise ValueError("grid must be a non-empty list of rows")
    width = len(grid[0])
    if width == 0:
        raise ValueError("grid rows must be non-empty")
    if not 1 <= len(grid) <= 30 or not 1 <= width <= 30:
        raise ValueError("grid dimensions must be in [1, 30]")
    for row in grid:
        if not isinstance(row, list) or len(row) != width:
            raise ValueError("grid must be rectangular")
        for value in row:
            if type(value) is not int or not 0 <= value <= 9:
                raise ValueError("grid values must be integers in [0, 9]")
