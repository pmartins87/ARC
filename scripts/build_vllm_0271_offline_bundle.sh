#!/usr/bin/env bash
set -euo pipefail

# Build an offline wheel bundle for the exact CUDA 12.9 x86_64 vLLM release
# referenced by NVIDIA Nemotron 3.5 Lightning documentation.
#
# Run this ONLY in an internet-enabled disposable build environment with
# Python 3.12/x86_64. Do not run it inside the final ARC L4 notebook, where
# Internet must remain disabled.

OUT_DIR="${1:-./vllm-0.27.1-cu129-wheels}"
mkdir -p "$OUT_DIR"

VLLM_URL="https://github.com/vllm-project/vllm/releases/download/v0.27.1/vllm-0.27.1%2Bcu129-cp38-abi3-manylinux_2_28_x86_64.whl"
TORCH_INDEX="https://download.pytorch.org/whl/cu129"

python - <<'PY'
import platform, sys
if sys.version_info[:2] != (3, 12):
    raise SystemExit(f"Expected Python 3.12 for Kaggle-target bundle, got {sys.version.split()[0]}")
if platform.machine() not in {"x86_64", "AMD64"}:
    raise SystemExit(f"Expected x86_64 build host, got {platform.machine()}")
print("build_host_ok", sys.version.split()[0], platform.machine())
PY

python -m pip download \
  --dest "$OUT_DIR" \
  --extra-index-url "$TORCH_INDEX" \
  "$VLLM_URL"

python - "$OUT_DIR" <<'PY'
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
files = []
for path in sorted(root.glob("*.whl")):
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    files.append({"name": path.name, "bytes": path.stat().st_size, "sha256": h.hexdigest()})

manifest = {
    "purpose": "offline Kaggle dependency bundle for E0006",
    "vllm_release": "0.27.1",
    "vllm_cuda_variant": "cu129",
    "target_python": "3.12",
    "target_arch": "x86_64",
    "wheel_count": len(files),
    "total_bytes": sum(item["bytes"] for item in files),
    "files": files,
}
(root / "MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
print(json.dumps({k: manifest[k] for k in ("wheel_count", "total_bytes")}, indent=2))
PY

echo "Bundle written to: $OUT_DIR"
echo "Offline install pattern:"
echo "  python -m pip install --no-index --find-links=$OUT_DIR 'vllm==0.27.1+cu129'"
