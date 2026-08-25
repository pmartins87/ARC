# E0006 — Kaggle Gate A runbook

Snapshot: 2026-08-25

## Objective

Collect one competition-valid **environment/model-attachment diagnostic** for Nemotron 3.5 Lightning on Kaggle L4 x4 with Internet OFF. Gate A deliberately does **not** load the 30B checkpoint and does **not** submit to ARC.

Ready notebook:

`notebooks/E0006_lightning_gate_a_kaggle.ipynb`

Direct GitHub URL for Kaggle `File -> Import Notebook -> Link`:

`https://github.com/pmartins87/ARC/blob/main/notebooks/E0006_lightning_gate_a_kaggle.ipynb`

## Preferred checkpoint

Attach **`nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4`** first.

Despite the checkpoint name, L4 will not use native NVFP4 arithmetic. NVIDIA/vLLM document a **W4A16 fallback execution path** for non-Blackwell GPUs. NVIDIA's current NIM support matrix gives W4A16 TP4 a 14 GB/GPU floor on SM 8.0+ hardware; L4 is Ada / SM 8.9 with 24 GB. This gives materially more headroom than the 20 GB/GPU BF16 TP4 floor.

The BF16 checkpoint remains the higher-fidelity fallback/reference if later needed.

## Minimal user sequence

1. Create/open a blank Kaggle notebook.
2. `File -> Import Notebook -> Link` and paste the direct GitHub URL above.
3. Attach `nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4` as a Kaggle Model/Input if available through Kaggle/Hugging Face integration.
4. Set accelerator to **GPU L4 x4**.
5. Set notebook Internet to **OFF**.
6. `Save Version -> Save & Run All`.
7. After completion, download only `/kaggle/working/e0006_gate_a_inspect.json` and return that tiny file to the project.

No ARC competition submission is made in this flow.

## What the notebook verifies

- exactly four CUDA devices are visible;
- each GPU exposes roughly 24 GiB;
- an attached local Hugging Face-style Nemotron/Lightning model root exists;
- checkpoint size/shard count/config metadata are readable without network access;
- installed versions of torch/transformers/accelerate/vLLM/FlashInfer/safetensors/Triton;
- free working-disk space;
- offline environment variables.

`PASS_GATE_A` means only that the environment and model attachment are suitable to attempt Gate B. It does **not** imply the model will fit or run.

## Model attachment fallback order

1. Search Kaggle Models for the exact NVFP4 Lightning checkpoint.
2. Use Hugging Face -> Kaggle integration/import to materialize a Kaggle model page, then attach it.
3. Use Kaggle's model/dataset import tooling from the public Hugging Face source.
4. If the quantized route cannot be materialized, repeat the attachment search with the BF16 reference.
5. Only as a last resort route a large checkpoint through the user's PC.

NVIDIA's NIM documentation reports model-cache sizes ranging from about **19 GB for NVFP4 to ~63 GB for BF16**, so the quantized route also reduces attachment/storage burden substantially.

## Gate B rule

Do not attempt the large-model load until Gate A output is reviewed. Gate B auto-detects a ModelOpt/NVFP4 checkpoint and requests `modelopt_fp4`; vLLM may then select the available W4A16 kernel automatically. If backend selection alone fails, there is at most one bounded mechanical retry with a forced backend based on the actual log.

If the Kaggle base image lacks the required local vLLM path, prepare an offline dependency input first rather than enabling Internet in the competition-valid load run.
