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
VLLM_EXPECTED_SHA256="bf0d52faa2a51e7a01c6856a7a8a2d1307fd0ff711415d34168a67ffac0fa47b"
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

python - "$OUT_DIR" "$VLLM_EXPECTED_SHA256" <<'PY'
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
expected_vllm_sha = sys.argv[2]
files = []
vllm_matches = []
for path in sorted(root.glob("*.whl")):
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    digest = h.hexdigest()
    row = {"name": path.name, "bytes": path.stat().st_size, "sha256": digest}
    files.append(row)
    if path.name.startswith("vllm-0.27.1+cu129-"):
        vllm_matches.append(row)

if len(vllm_matches) != 1:
    raise SystemExit(f"Expected exactly one vLLM 0.27.1+cu129 wheel, found {len(vllm_matches)}")
if vllm_matches[0]["sha256"] != expected_vllm_sha:
    raise SystemExit(
        "Official vLLM wheel SHA-256 mismatch: "
        f"expected {expected_vllm_sha}, got {vllm_matches[0]['sha256']}"
    )

manifest = {
    "purpose": "offline Kaggle dependency bundle for E0006",
    "vllm_release": "0.27.1",
    "vllm_cuda_variant": "cu129",
    "vllm_official_release_sha256": expected_vllm_sha,
    "target_python": "3.12",
    "target_arch": "x86_64",
    "wheel_count": len(files),
    "total_bytes": sum(item["bytes"] for item in files),
    "files": files,
}
(root / "MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
print(json.dumps({k: manifest[k] for k in ("wheel_count", "total_bytes", "vllm_official_release_sha256")}, indent=2))
PY

echo "Bundle written to: $OUT_DIR"
echo "Offline install pattern:"
echo "  python -m pip install --no-index --find-links=$OUT_DIR 'vllm==0.27.1+cu129'"
