# E0006 — D3 offline import smoke result

Date: 2026-08-28

## Decision

**PASS — OFFLINE_IMPORT_READY**

The saved CUDA 12.9 wheelhouse was attached to a fresh Kaggle notebook with Accelerator=None and Internet=OFF. The runtime was installed into an isolated `/tmp/e0006_runtime` target and imported successfully without network access.

## Observed runtime

- vLLM: `0.27.1+cu129`
- torch: `2.13.0+cu129`
- torch CUDA build: `12.9`
- transformers: `5.16.1`
- Triton: `3.7.1`
- flashinfer-python: `0.6.16.post3`
- flashinfer-cubin: `0.6.16.post3`
- safetensors: `0.8.0`
- vLLM frozen wheel SHA-256: PASS
- FlashInfer cubin SHA-256: PASS
- `NemotronHForCausalLM` registration evidence in frozen vLLM wheel: PASS
- critical imports (`torch`, `transformers`, `flashinfer`, `vllm`, model registry): PASS
- install return code: 0
- import probe return code: 0
- isolated runtime installed size: **14.477 GiB**
- install time: **248.89 s**
- import-probe time: **48.767 s**

The no-GPU notebook correctly reported `torch_cuda_available=false`; this is expected because D3 intentionally used no accelerator. Triton also reported no active driver and disabled GPU functions, which is likewise expected in this gate.

## Dependency-conflict warnings

Pip emitted conflicts against unrelated packages preinstalled in the Kaggle base image. These do not invalidate D3 because the E0006 runtime was installed under an isolated `--target /tmp/e0006_runtime` and the probe explicitly imported from that target. We must preserve the same isolation for subsequent gates rather than mutating the base environment.

## Next gate

Do **not** load Nemotron yet. Before the TP4 model-load Gate B, run one bounded **GPU runtime preflight** on L4 x4 with Internet OFF using the same wheelhouse. It must prove:

1. `torch 2.13.0+cu129` sees exactly four NVIDIA L4 GPUs;
2. each L4 reports compute capability 8.9;
3. a tiny CUDA operation succeeds on every GPU;
4. vLLM/FlashInfer/Triton import on the real GPU driver;
5. `NemotronHForCausalLM` imports from vLLM;
6. a four-process NCCL all-reduce succeeds.

Only a clean `GPU_RUNTIME_READY` result may release the full TP4 model-load Gate B.
