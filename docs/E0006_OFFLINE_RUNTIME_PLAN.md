# E0006 — Offline runtime plan after Gate A

Snapshot: 2026-08-27
Status: **PREP / no further L4 authorized yet**

## Why Gate B is paused

Gate A measured the actual ARC Kaggle image:

- Python 3.12.13
- torch 2.10.0+cu128
- CUDA runtime 12.8
- transformers 5.0.0
- triton 3.6.0
- no vLLM
- no FlashInfer

The Nemotron 3.5 Lightning NVFP4 model card identifies **vLLM 0.27.1** as the validated vLLM release.

The exact `v0.27.1` vLLM CUDA requirements pin materially newer runtime components, including:

- torch 2.13.0
- flashinfer-python 0.6.16.post3
- flashinfer-cubin 0.6.16.post3
- additional CUDA/kernel packages including Humming/CUTLASS dependencies.

Therefore installing vLLM directly into the Kaggle base environment would mutate a known-good torch 2.10/cu128 stack and is not an acceptable first move.

## Principle

**Do dependency work without L4.**

We will not spend another L4 minute until we know exactly what an offline vLLM runtime would install and whether it can be isolated from the Kaggle base image.

## Stage D0 — dependency-resolution probe (CPU / Internet ON)

Run `notebooks/E0006_vllm_dependency_probe_kaggle.ipynb` in a generic Kaggle notebook with:

- Accelerator: None
- Internet: ON

The notebook performs no installation and no model load. It records:

- current Python/torch/transformers/triton environment;
- a `pip --dry-run --report` resolution for `vllm[flashinfer]==0.27.1`;
- packages that would replace or conflict with the base stack;
- the vLLM 0.27.1 release-wheel metadata relevant to x86_64.

Output: `/kaggle/working/e0006_vllm_dependency_probe.json`.

## Stage D1 — build candidate offline runtime (CPU / Internet ON)

Only after D0 review.

Preferred approach is an **isolated runtime input**, not an in-place base-environment upgrade. The exact format will be selected from D0 evidence:

1. wheelhouse + deterministic offline install into a temporary target directory, or
2. pre-populated target/site-packages tree mounted as a Kaggle input if relocation tests pass.

The build must freeze package versions and SHA-256 hashes.

## Stage D2 — import-only offline smoke

After an offline bundle exists, attach it to an ARC-linked notebook with Internet OFF and run only:

- Python import/version checks for torch, vLLM and FlashInfer;
- CUDA driver/runtime visibility;
- kernel-package discovery;
- no model load.

This should complete quickly. It is the first point at which another L4 run may be justified, because native CUDA compatibility cannot be proven from CPU metadata alone.

## Stage B — bounded TP4 model load

Only if D2 passes.

Gate B must be regenerated from the measured runtime rather than blindly using the old command line. The current old notebook is frozen and must not be run as-is.

The source-faithful model facts to preserve are:

- architecture: `NemotronHForCausalLM`;
- quantization: ModelOpt NVFP4;
- non-native-FP4 GPUs can use W4A16 fallback;
- L4 is Ada / SM 8.9;
- checkpoint has 52 shards and is already mounted offline.

## Stop rules

- No Internet in ARC-valid L4 runs.
- No second heavy model-load attempt without a specific failure-class hypothesis.
- Do not replace torch/transformers globally in the competition notebook unless the isolated-runtime path is proven impossible.
- Do not spend L4 on dependency resolution or downloads.
- Preserve the 19.5 GiB working-disk constraint measured by Gate A.
