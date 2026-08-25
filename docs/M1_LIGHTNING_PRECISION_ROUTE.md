# M1 — Lightning precision route on Kaggle L4 x4

Snapshot: 2026-08-25

## Decision

For the first E0006 deployment attempt, **prefer the official NVFP4 checkpoint executed through vLLM's W4A16 fallback path** over the BF16 checkpoint.

Preferred checkpoint:

`nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4`

BF16 remains the fidelity fallback/reference:

`nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16`

This is a deployment/feasibility choice, not a scientific claim that quantization is accuracy-neutral.

## Source evidence

NVIDIA's current NIM support matrix for `nemotron-3.5-lightning-30b-a3b` reports:

| Precision | TP | Minimum VRAM / GPU | Architecture requirement |
|---|---:|---:|---|
| BF16 | 4 | 20 GB | Ampere or newer (SM 8.0+) |
| W4A16 | 4 | **14 GB** | Ampere or newer (SM 8.0+) |
| NVFP4 native | 4 | 12 GB | Blackwell or newer (SM 10.0+) |

The same page states that Ada supports BF16 and W4A16 but not native NVFP4. A Kaggle L4 is Ada / SM 8.9 with 24 GB, so it clears the W4A16 TP4 architecture and memory floor with roughly **10 GB/GPU** nominal headroom versus ~4 GB/GPU for BF16.

NVIDIA also reports model-cache sizes ranging from about **19 GB for the NVFP4 checkpoint to ~63 GB for BF16**, materially reducing Kaggle attachment/storage friction.

Sources:
- NVIDIA NIM LLM support matrix: https://docs.nvidia.com/nim/large-language-models/latest/reference/support-matrix.html
- NVIDIA Lightning NVFP4 model card: https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4
- vLLM ModelOpt quantization docs: https://docs.vllm.ai/en/latest/features/quantization/modelopt/

## Why an NVFP4 checkpoint can be useful on non-Blackwell GPUs

vLLM documents `quantization="modelopt_fp4"` for ModelOpt NVFP4 checkpoints. On GPUs without a supported native FP4 GEMM kernel, vLLM can fall back to **weight-only W4A16 execution**, including Marlin, rather than requiring native Blackwell FP4 tensor cores.

NVIDIA's Lightning card likewise documents the same NVFP4 checkpoint serving through W4A16 kernels on non-native-FP4 hardware.

Therefore the name `NVFP4` describes stored checkpoint precision; it does **not** mean we need native NVFP4 arithmetic on L4.

## Gate-B first configuration

For the first L4 x4 compatibility smoke:
- checkpoint: NVFP4 release above;
- `--quantization modelopt_fp4`;
- TP=4;
- max model length 8192;
- BF16 activation/compute dtype where applicable;
- Mamba backend FlashInfer;
- Mamba SSM cache float16;
- stochastic rounding on, Philox rounds 5;
- no speculative decoding;
- eager execution for compatibility diagnosis;
- allow vLLM to choose the FP4/W4A16 linear/MoE kernel automatically first.

If automatic backend selection is the only failure, one bounded mechanical retry may force the documented W4A16 backend (`marlin` or `humming`) according to the actual startup log. Do not cycle through backends as a tuning search.

## Accuracy discipline

Quantization could change ARC accuracy. If the W4A16 route becomes viable and competitive enough to carry forward, later controlled work must compare it against BF16 on a common public development subset if BF16 itself can be deployed. Until then:
- W4A16 is the **preferred feasibility route**;
- BF16 is the **higher-fidelity reference/fallback**;
- no score equivalence is assumed.

## Consequence

The next model-attachment attempt should use the smaller NVFP4 checkpoint first. This reduces both model-transfer burden and VRAM pressure while remaining consistent with NVIDIA/vLLM's public non-Blackwell W4A16 deployment path.
