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

## Observed Kaggle/Hugging Face behavior

The direct Hugging Face `Use this model -> Kaggle` path created only a starter notebook. A Quick Save did **not** create an attachable Kaggle Model. We then ran a tiny `hf_hub_download(..., filename="config.json")` reference successfully and saved another version; `Add Input` still returned only the user's own notebook rather than the Nemotron model. Therefore this automatic materialization path is classified **FAILED_FOR_THIS_CHECKPOINT / STOP** for E0006.

Do not repeat the starter-notebook/search loop.

## Current attachment path — cloud mirror

Use a temporary Kaggle notebook with Internet ON to mirror the public Hugging Face checkpoint directly into a Kaggle Model owned by the user:

1. Download the full HF repository with `huggingface_hub.snapshot_download` into the VM cache/scratch area, **not `/kaggle/working`**.
2. Upload the resulting snapshot directory with `kagglehub.model_upload` using a Kaggle model handle under the user's account.
3. The bytes move cloud-to-cloud; do not route the checkpoint through the user's PC.
4. Once the Kaggle Model exists, return to `notebooks/E0006_lightning_gate_a_kaggle.ipynb`, attach that Kaggle Model in `Add Input`, set **L4 x4**, set Internet **OFF**, then `Save Version -> Save & Run All`.
5. Return `/kaggle/working/e0006_gate_a_inspect.json` for review.

### Live mirror status — 2026-08-25

The temporary Kaggle VM reported **1026.8 GiB free** before transfer. The Hugging Face snapshot download completed successfully at approximately **21.6 GB**, reconstructing the full checkpoint. KaggleHub then successfully created the user-owned model `paulomartins87/nemotron-3-5-lightning` and the variation handle `paulomartins87/nemotron-3-5-lightning/pyTorch/30b-a3b-nvfp4`. The client is currently uploading the generated ~21.6 GB archive to Kaggle Models. This establishes that storage, source download and Kaggle model creation all work; only completion of the large upload remains before Gate A attachment.

Kaggle documents `/kaggle/working` saved output at up to 20 GB, so a large checkpoint mirror should not rely on notebook output persistence. KaggleHub is authenticated by default inside Kaggle notebooks and its supported `model_upload(<username>/<model>/<framework>/<variation>, local_model_dir)` API is the preferred upload mechanism.

No ARC competition submission is made in this flow.

## What the Gate A notebook verifies

- exactly four CUDA devices are visible;
- each GPU exposes roughly 24 GiB;
- an attached local Hugging Face-style Nemotron/Lightning model root exists;
- checkpoint size/shard count/config metadata are readable without network access;
- installed versions of torch/transformers/accelerate/vLLM/FlashInfer/safetensors/Triton;
- free working-disk space;
- offline environment variables.

`PASS_GATE_A` means only that the environment and model attachment are suitable to attempt Gate B. It does **not** imply the model will fit or run.

## Model attachment fallback order

1. **Current:** cloud-to-cloud HF snapshot -> user-owned Kaggle Model via `kagglehub.model_upload`.
2. If Kaggle refuses the large Model upload for a platform/quota reason, investigate a Kaggle Dataset/private artifact mirror only if competition rules permit it.
3. If the quantized route itself is blocked, reconsider BF16 only if storage and deployment evidence still justify it.
4. Only as a last resort route a large checkpoint through the user's PC.

NVIDIA's current model card lists the checkpoint license as **OpenMDW-1.1**; preserve that provenance and do not relabel it as Apache-2.0.

## Gate B rule

Do not attempt the large-model load until Gate A output is reviewed. Gate B auto-detects a ModelOpt/NVFP4 checkpoint and requests `modelopt_fp4`; vLLM may then select the available W4A16 kernel automatically. If backend selection alone fails, there is at most one bounded mechanical retry with a forced backend based on the actual log.

If the Kaggle base image lacks the required local vLLM path, prepare an offline dependency input first rather than enabling Internet in the competition-valid load run.
