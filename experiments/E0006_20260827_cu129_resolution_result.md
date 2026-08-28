# E0006 D1 — Exact CUDA 12.9 resolution result

Date: 2026-08-27

Status: **PASS / RESOLUTION_OK_REVIEW_SIZE**

The no-GPU Kaggle dry run for the exact official `vllm 0.27.1+cu129` wheel resolved successfully under Python 3.12.

Key findings:

- `vllm==0.27.1+cu129` selected from the official vLLM release wheel.
- Frozen wheel SHA-256 remains `bf0d52faa2a51e7a01c6856a7a8a2d1307fd0ff711415d34168a67ffac0fa47b`.
- `torch==2.13.0+cu129`, `torchaudio==2.11.0+cu129`, `torchvision==0.28.0+cu129` and `triton==3.7.1` resolved successfully.
- `flashinfer-python==0.6.16.post3` resolved successfully.
- Planned install count: 102.
- All planned artifact sizes were resolved; known download size is 5,271,803,989 bytes = **4.91 GiB** before adding the explicit FlashInfer cubin package.
- Only two packages were flagged by the coarse `cuda13` name/version detector: `nvidia-ml-py==13.610.43` and `nvidia-cuda-nvdisasm==13.3.73`. The core runtime remains CUDA 12.9 (`torch +cu129` and CUDA 12.9 NVIDIA libraries).

Important correction before bundle build:

vLLM v0.27.1's CUDA requirements explicitly require `flashinfer-cubin==0.6.16.post3`, but that package is deliberately excluded from vLLM's install requirements because it is hosted on FlashInfer's own wheel index. Therefore the D1 resolver did not include it automatically. The offline bundle builder must add it explicitly.

Decision:

- Generic PyPI runtime remains rejected.
- Exact CUDA 12.9 route is accepted for bundle construction.
- Gate B remains **NOT AUTHORIZED**.
- Next step: build the zero-GPU offline wheelhouse with explicit `flashinfer-cubin==0.6.16.post3`, verify SHA-256s, and prove dependency closure with `pip --no-index --find-links` before any import smoke or L4 use.

Notebook: `notebooks/E0006_vllm_cu129_wheelhouse_builder_kaggle.ipynb`.
