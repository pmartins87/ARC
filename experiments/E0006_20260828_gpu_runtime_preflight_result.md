# E0006 — L4 x4 GPU runtime preflight result

Date: 2026-08-28
Status: **PASS / parser false-negative**

## Observed run

The D4 preflight executed on Kaggle with four NVIDIA L4 GPUs, Internet OFF, and the frozen CUDA 12.9 wheelhouse attached.

Observed runtime:

- `torch 2.13.0+cu129`;
- `vllm 0.27.1+cu129`;
- `triton 3.7.1`;
- `flashinfer-python 0.6.16.post3`;
- `flashinfer-cubin 0.6.16.post3`;
- four `NVIDIA L4` devices, SM 8.9, 22.034 GiB reported per GPU;
- simple CUDA tensor operation succeeded independently on all four devices;
- `NemotronHForCausalLM` imported successfully from the frozen vLLM runtime;
- 4-process NCCL all-reduce exited with return code 0 and every rank observed the expected sum `10.0`.

## Why the JSON said BLOCKED_GPU_RUNTIME

The preflight parser expected one `E0006_NCCL {json}` record per stdout line. `torch.distributed.run` interleaved two rank prints on the same physical line:

`E0006_NCCL {...}E0006_NCCL {...}`

The first `json.loads()` therefore raised `JSONDecodeError: Extra data`. This happened **after** NCCL itself had already completed successfully. The raw stdout contains all four rank records and each reports `sum = 10.0`.

This is a harness/parser defect, not a CUDA, NCCL, driver, vLLM, FlashInfer, or hardware failure.

## Decision

D4 is reclassified **GPU_RUNTIME_READY / PASS** from the raw evidence. Do not spend another L4 run merely to reproduce the parser result.

Before Gate B, materialize the already validated isolated runtime as a reusable Kaggle notebook output with Accelerator=None. This avoids paying the approximately four-minute offline `pip --target` installation cost again on every L4 run.

Gate B may be released only after that reusable runtime image is materialized and attached alongside the frozen Nemotron checkpoint.
