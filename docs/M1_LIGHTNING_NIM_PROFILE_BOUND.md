# M1 — Official Nemotron 3.5 Lightning TP4 profile bound

Snapshot: 2026-08-25

## New primary-source evidence

NVIDIA's current NIM support matrix publishes profile floors for `nvidia/nemotron-3.5-lightning-30b-a3b`.

For **BF16, TP=4, PP=1**, NVIDIA reports:
- minimum VRAM per GPU: **20 GB**;
- minimum GPU count: **4**;
- architecture requirement: **Ampere or newer (SM 8.0+)**;
- NIM release family: 2.0.10 support-matrix snapshot.

The support matrix explicitly warns that this minimum is a profile floor for model weights and runtime allocations. It does **not** include arbitrary extra headroom for large KV caches at high context length or high concurrency.

Primary source:
- https://docs.nvidia.com/nim/large-language-models/latest/reference/support-matrix.html

NVIDIA's Lightning NIM guide also states that the BF16 model cache is roughly **63 GB**, that lower-memory deployments should prefer higher tensor parallelism and tune memory if needed, and that startup/download behavior can be substantial. This is useful deployment evidence but the NIM container itself is not our intended Kaggle execution vehicle.

Source:
- https://docs.nvidia.com/nim/large-language-models/latest/get-started/advanced/get-started-nemotron-3.5-lightning.html

## L4 comparison

NVIDIA's L4 product page states:
- GPU memory: **24 GB**;
- architecture: **Ada Lovelace**;
- BF16 Tensor Core support;
- interconnect: PCIe Gen4 x16;
- memory bandwidth: 300 GB/s.

NVIDIA's CUDA compute-capability table lists L4 at **compute capability 8.9**.

Sources:
- https://www.nvidia.com/data-center/l4/
- https://developer.nvidia.com/cuda/gpus

Against the NIM BF16 TP4 profile floor:
- L4 VRAM: 24 GB vs profile floor 20 GB;
- nominal floor headroom: **4 GB/GPU**;
- nominal floor headroom fraction: **16.7% of each L4's VRAM**;
- four-GPU aggregate nominal headroom: **16 GB**;
- GPU count: 4 vs minimum 4;
- architecture: SM 8.9 vs minimum SM 8.0.

Therefore the target Kaggle L4 x4 hardware **passes NVIDIA's published BF16 TP4 profile floor on VRAM, GPU count and architecture**.

## What this proves

It materially strengthens deployment feasibility. The previous argument was only a raw-weight arithmetic estimate (~62–63 GB weights over 96 GB aggregate VRAM). We now have a vendor-published runtime profile that places the BF16 TP4 floor below 24 GB per GPU.

This is strong evidence that a four-GPU, 24-GB-per-GPU deployment is technically plausible in the model family.

## What this does not prove

It does **not** prove that our exact Kaggle setup will work because:
- NVIDIA NIM profiles are a different packaging/runtime path from the bare vLLM process we intend to test;
- the support matrix does not list Kaggle L4 as a specifically verified GPU/profile pair;
- L4 inter-GPU communication in Kaggle is PCIe and may be a throughput bottleneck;
- vLLM/FlashInfer kernels in the Kaggle image still need direct validation on SM 8.9;
- 4 GB/GPU nominal profile headroom is not generous for long context, concurrent sequences, temporary buffers or fragmentation;
- the 12-hour competition budget is ultimately a throughput/coverage constraint, not just a loadability constraint.

So E0006 remains a **measured smoke gate**, not a paper calculation.

## Decision impact

The deployment hypothesis is upgraded from:

> `raw weights do not rule out 4xL4`

To:

> `the target 4xL4 hardware satisfies NVIDIA's published BF16 TP4 NIM profile floor, but bare-vLLM Kaggle compatibility and throughput remain unverified`.

That is enough to justify one bounded no-leaderboard L4 x4 smoke once the current N1 rerun no longer occupies the user-side workflow.

## Reproducible calculation

Repository utility:
- `src/arcsolver/profile_headroom.py`
- `scripts/check_profile_headroom.py`

Reference inputs:
```text
GPU VRAM = 24 GB
profile minimum VRAM = 20 GB
GPU count = 4
profile minimum GPU count = 4
L4 compute capability = 8.9
required compute capability = 8.0
```

Expected result:
```text
per-GPU headroom = 4 GB
aggregate headroom = 16 GB
memory floor = PASS
GPU count floor = PASS
architecture floor = PASS
```
