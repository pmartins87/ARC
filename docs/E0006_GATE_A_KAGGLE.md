# E0006 — Kaggle Gate A runbook

Snapshot: 2026-08-25

## Objective

Collect one competition-valid **environment/model-attachment diagnostic** for Nemotron 3.5 Lightning on Kaggle L4 x4 with Internet OFF. Gate A deliberately does **not** load the 30B checkpoint and does **not** submit to ARC.

Ready notebook:

`notebooks/E0006_lightning_gate_a_kaggle.ipynb`

Direct GitHub URL for Kaggle `File -> Import Notebook -> Link`:

`https://github.com/pmartins87/ARC/blob/main/notebooks/E0006_lightning_gate_a_kaggle.ipynb`

## Minimal user sequence

1. Create/open a blank Kaggle notebook.
2. `File -> Import Notebook -> Link` and paste the direct GitHub URL above.
3. Attach `nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16` as a Kaggle Model/Input if it is available through Kaggle/Hugging Face integration.
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

1. Search Kaggle Models for the exact Lightning checkpoint.
2. Use Hugging Face -> Kaggle integration/import to materialize a Kaggle model page, then attach it.
3. Use Kaggle's model/dataset import tooling from a remote public source.
4. Only as a last resort route the ~65.8 GB checkpoint through the user's PC.

As of the 2026-08-25 web audit, the official Hugging Face BF16 checkpoint is about **65.8 GB** and no exact Lightning Kaggle model page was found by public web search. Absence from web search is not proof that Kaggle's in-product model search cannot find/import it.

## Gate B rule

Do not attempt the large-model load until Gate A output is reviewed. If the Kaggle base image lacks the required local vLLM path, prepare an offline dependency input first rather than enabling Internet in the competition-valid load run.
