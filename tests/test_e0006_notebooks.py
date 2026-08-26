from __future__ import annotations

import json
from pathlib import Path


NOTEBOOKS = (
    Path("notebooks/E0006_lightning_gate_a_kaggle.ipynb"),
    Path("notebooks/E0006_lightning_gate_b_kaggle.ipynb"),
    Path("notebooks/E0006_mirror_nvfp4_to_kaggle.ipynb"),
)


def test_e0006_notebooks_are_valid_json_and_python() -> None:
    for path in NOTEBOOKS:
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert payload.get("nbformat") == 4
        cells = payload.get("cells")
        assert isinstance(cells, list) and cells

        code_cells = [cell for cell in cells if cell.get("cell_type") == "code"]
        assert code_cells, f"{path} has no code cells"

        for index, cell in enumerate(code_cells):
            source = cell.get("source", [])
            text = "".join(source) if isinstance(source, list) else str(source)
            compile(text, f"{path}#code-cell-{index}", "exec")
