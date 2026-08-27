# E0006 — No-GPU dependency probe result

Date: 2026-08-27

## Verdict

**PASS as diagnostic / REJECT generic PyPI installation path.**

The Kaggle no-GPU dry run for `vllm[flashinfer]==0.27.1` returned successfully, but the generic resolver planned **105 package installs/changes**. That path would replace major parts of the Kaggle base environment and is therefore not authorized for the competition-valid L4 runtime.

## Base no-GPU environment observed

- Python 3.12.13
- torch 2.10.0+cpu
- transformers 5.0.0
- accelerate 1.13.0
- safetensors 0.7.0
- vLLM absent
- FlashInfer absent

The earlier L4 Gate A observed the GPU image variant as torch 2.10.0+cu128 / CUDA runtime 12.8 / Triton 3.6.0. Do not conflate the no-GPU CPU torch build with the L4 image.

## Generic resolver critical changes

The dry run selected:

- vLLM 0.27.1
- torch 2.13.0
- torchaudio 2.11.0
- torchvision 0.28.0
- Triton 3.7.1
- transformers 5.16.1
- flashinfer-python 0.6.16.post3

It also proposed a large CUDA 13.x dependency family and many auxiliary packages. This is too broad to install blindly into the Kaggle base image and too expensive/risky to discover during an L4 run.

## Important release evidence

The official vLLM v0.27.1 GitHub release publishes a dedicated Linux x86_64 **CUDA 12.9** wheel:

`vllm-0.27.1+cu129-cp38-abi3-manylinux_2_28_x86_64.whl`

Recorded release digest:

`sha256:bf0d52faa2a51e7a01c6856a7a8a2d1307fd0ff711415d34168a67ffac0fa47b`

The official vLLM installation guidance recommends pairing CUDA-specific vLLM wheels with the matching PyTorch index. PyTorch publishes `torch 2.13.0+cu129` for CPython 3.12 / Linux x86_64.

## Decision

Do **not** build the offline bundle from the generic PyPI `vllm` resolution.

Next diagnostic, still **zero L4 cost**:

1. resolve the exact vLLM `+cu129` release wheel;
2. add the PyTorch CUDA 12.9 index and FlashInfer wheel index;
3. verify whether `torch 2.13.0+cu129` is selected rather than the generic/CUDA-13 stack;
4. estimate the complete wheelhouse byte size before downloading/persisting it;
5. only then build a private Kaggle dependency input/runtime bundle.

Gate B remains **NOT AUTHORIZED** until that runtime bundle passes an offline import probe.
