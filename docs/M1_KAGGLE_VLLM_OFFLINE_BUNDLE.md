# M1 — Kaggle / vLLM offline dependency plan

Snapshot: 2026-08-25

## Why this is a separate gate

ARC Prize 2026 L4 x4 notebooks must run with **Internet OFF**. A model checkpoint fitting in VRAM is not enough: the exact serving stack must also be locally available and binary-compatible.

## Current Kaggle image evidence

The current public `Kaggle/docker-python` main branch is based on a May 2026 Colab GPU runtime and uses a Python **3.12** package path. A repository search does not currently show vLLM as an explicit Kaggle-added dependency.

This does not prove the live ARC image lacks vLLM because the Colab base image can contribute packages independently. Therefore our inspect-only smoke remains the authority for the actual competition session.

Sources:
- https://github.com/Kaggle/docker-python/blob/main/Dockerfile.tmpl
- https://github.com/Kaggle/docker-python

## Current official vLLM release artifact

NVIDIA's Lightning model card references **vLLM 0.27.1**. The official vLLM GitHub release publishes a CUDA 12.9, x86_64, CPython ABI3 wheel:

`vllm-0.27.1+cu129-cp38-abi3-manylinux_2_28_x86_64.whl`

Official release metadata:
- release date: 2026-08-11;
- wheel size: **545,751,073 bytes** (~520.5 MiB);
- SHA-256: `bf0d52faa2a51e7a01c6856a7a8a2d1307fd0ff711415d34168a67ffac0fa47b`.

The ABI3 tag makes the wheel compatible with Python versions newer than 3.8 subject to the package's own supported range, so Python 3.12 is not ruled out by the wheel tag.

Sources:
- https://github.com/vllm-project/vllm/releases/tag/v0.27.1
- https://docs.vllm.ai/en/stable/getting_started/installation/gpu/

vLLM's installation docs emphasize that its CUDA wheels are tightly coupled to CUDA/PyTorch binary versions and recommend using the wheel's bundled dependency stack rather than mixing arbitrary existing PyTorch builds.

## Kaggle precedent

Public Kaggle work demonstrates the general packaging pattern:
- vLLM has been run successfully on L4 x4 in earlier competitions;
- recent 2026 AIMO notebooks build **offline wheel bundles** in an Internet-enabled notebook, save the wheels as output, then consume them in Internet-off inference notebooks;
- one recent public wheel-builder output is about 5.4 GB, showing that the dependency bundle is materially larger than the vLLM wheel itself.

Examples:
- https://www.kaggle.com/code/rsmits/vllm-load-multiple-models
- https://www.kaggle.com/code/abdullahmeda/load-72b-awq-model-using-vllm-on-l4-x4
- https://www.kaggle.com/code/nguyennguyen599/aimo3-vllm-wheel

Historical success is platform precedent only. It does not validate vLLM 0.27.1 + Lightning on the current ARC image.

## Reproducible bundle builder

Prepared script:
- `scripts/build_vllm_0271_offline_bundle.sh`

The builder:
1. requires Python 3.12/x86_64 in the Internet-enabled build environment;
2. downloads the exact official CUDA 12.9 vLLM wheel plus resolved dependencies;
3. uses the PyTorch CUDA 12.9 index;
4. computes SHA-256 for every wheel;
5. **fails closed** if the official vLLM wheel digest is not exactly the GitHub-release digest;
6. writes `MANIFEST.json` with file hashes and total bundle size.

Offline install pattern after the bundle is attached:

```bash
python -m pip install --no-index --find-links=/kaggle/input/<bundle> 'vllm==0.27.1+cu129'
```

Do not execute that installation blindly before Gate A inventory. If the live Kaggle image already contains an exact compatible vLLM stack, replacing it may be unnecessary or harmful.

## Decision tree

1. **Inspect current L4 session.** Record Python, CUDA, torch, vLLM, FlashInfer and GPU inventory.
2. If a compatible Lightning-capable vLLM is already present, use it and avoid package replacement.
3. If vLLM is absent/too old, create the pinned offline bundle in a separate Internet-enabled notebook and attach it as input.
4. Install with `--no-index` so the L4 run never depends on network resolution.
5. Run one Lightning load/generation smoke.
6. Record exact versions and hashes in E0006.

## User-work minimization

The intended user workflow is still small:
- no 5-GB wheel bundle through the user's PC if Kaggle notebook output can be reused as an input;
- no 60+-GB model weights through the user's PC if Hugging Face → Kaggle model attachment works;
- no competition submission is consumed by either dependency or model-load smoke.

The remaining uncertainty is environmental, so more paper analysis cannot substitute for the single bounded L4 smoke once we reach that gate.
