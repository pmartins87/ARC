# E0006 — CUDA 12.9 offline wheelhouse result

Date: 2026-08-27 (user local time)

## Result

**PASS — `WHEELHOUSE_READY`.**

The no-GPU Kaggle wheelhouse build completed with an exact CUDA 12.9 runtime bundle and a successful offline dependency-closure check.

Observed artifact:

- wheel files: **194**
- total bytes: **6,470,976,929**
- total size: **6.027 GiB**
- frozen vLLM wheel: `vllm-0.27.1+cu129-cp38-abi3-manylinux_2_28_x86_64.whl`
- frozen vLLM SHA-256: `bf0d52faa2a51e7a01c6856a7a8a2d1307fd0ff711415d34168a67ffac0fa47b`
- `flashinfer-cubin==0.6.16.post3`: **present**
- FlashInfer cubin size: **1,062,693,258 bytes**
- FlashInfer cubin SHA-256: `c79fba990aee2a7c7ef64208bb65900e45fe23c3a223f3dfc21eef225f43cba2`
- offline validation used `pip --no-index --find-links` against the saved wheelhouse
- offline validation return code: **0**

The resolved runtime contains the expected critical stack, including `torch 2.13.0+cu129`, `vllm 0.27.1+cu129`, `triton 3.7.1`, `flashinfer-python 0.6.16.post3`, and the explicit `flashinfer-cubin 0.6.16.post3` package.

## Interpretation

Dependency closure is now proven without Internet. This removes the previous blocker where the competition L4 base image lacked vLLM/FlashInfer and where a generic PyPI install attempted to rebuild a broad CUDA 13 stack.

This result does **not** yet prove that the runtime imports cleanly in a fresh Kaggle process, nor that the Nemotron checkpoint can load on L4 x4. Therefore Gate B remains blocked.

## Next gate

Run a **no-GPU, Internet-OFF import smoke** using the saved wheelhouse output as an attached Kaggle input. The smoke must:

1. locate the frozen vLLM and FlashInfer cubin wheels from `/kaggle/input`;
2. verify their frozen SHA-256 values;
3. confirm `NemotronHForCausalLM` appears in the frozen vLLM wheel code;
4. install the runtime into an isolated `/tmp` target using `--no-index` only;
5. import `torch`, `transformers`, `flashinfer`, `vllm`, and the vLLM model registry in a fresh subprocess;
6. record installed runtime size and remaining disk space.

Only `OFFLINE_IMPORT_READY` may release the bounded L4 TP=4 Gate B.
