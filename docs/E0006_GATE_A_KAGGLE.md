# E0006 — Kaggle Gate A runbook

Snapshot: 2026-08-26

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

## Frozen source revision

E0006 is pinned to Hugging Face revision:

`cc84af2fe71647d87f4486c064f320e1e7535243`

The upstream model repository is actively changing, so do not silently replace this checkpoint with a newer `main`. See `docs/E0006_MIRROR_PROVENANCE.md`.

## Observed Kaggle/Hugging Face behavior

The direct Hugging Face `Use this model -> Kaggle` path created only a starter notebook. A Quick Save did **not** create an attachable Kaggle Model. We then ran a tiny `hf_hub_download(..., filename="config.json")` reference successfully and saved another version; `Add Input` still returned only the user's own notebook rather than the Nemotron model. Therefore this automatic materialization path is classified **FAILED_FOR_THIS_CHECKPOINT / STOP** for E0006.

Do not repeat the starter-notebook/search loop.

## Current attachment path — cloud mirror

Target Kaggle Model handle:

`paulomartins87/nemotron-3-5-lightning/pyTorch/30b-a3b-nvfp4`

The first mirror run successfully reconstructed the full **21.6 GB** pinned snapshot and created the Kaggle model family, then began uploading the archive. The local browser tab later hit Chrome `Out of Memory` while rendering verbose upload progress. That browser failure does not prove server-side upload failure; model-version readiness must be verified separately.

### Verify first

Before retrying 21.6 GB, check whether the first upload completed:

- preferred: open the Kaggle model page and confirm a ready `30b-a3b-nvfp4` version; or
- from a Kaggle **draft** session run:

```python
import kagglehub
p = kagglehub.model_download(
    "paulomartins87/nemotron-3-5-lightning/pyTorch/30b-a3b-nvfp4",
    path="config.json",
)
print(p)
```

Inside a Kaggle draft notebook, current `kagglehub.model_download(...)` behavior attaches the model as a notebook datasource and returns its mounted path. A datasource must be attached **before** `Save Version`; the save execution is not allowed to attach a new datasource.

### If verification fails

Use the checked-in resilient mirror notebook:

`notebooks/E0006_mirror_nvfp4_to_kaggle.ipynb`

It replaces the original verbose ad-hoc upload cell. It:

1. pins the exact HF revision;
2. checks scratch-space headroom before large I/O;
3. resumes/reuses the local HF snapshot when possible;
4. writes a compact file/size manifest;
5. runs the Kaggle upload in a child process;
6. redirects detailed upload progress into `/tmp/e0006_kaggle_model_upload.log` rather than flooding the browser;
7. prints only five-minute heartbeats;
8. writes `/kaggle/working/e0006_mirror_status.json` and `e0006_mirror_manifest.json`.

Do not route the checkpoint through the user's PC.

## Gate A sequence once the mirror is ready

1. Open/import `notebooks/E0006_lightning_gate_a_kaggle.ipynb`.
2. Attach `paulomartins87/nemotron-3-5-lightning/pyTorch/30b-a3b-nvfp4` in `Add Input`, **or** use `kagglehub.model_download(...)` once in the draft session to attach it before saving.
3. Confirm the model appears in notebook Inputs.
4. Set accelerator to **GPU L4 x4**.
5. Set notebook Internet to **OFF**.
6. `Save Version -> Save & Run All`.
7. After completion, download only `/kaggle/working/e0006_gate_a_inspect.json` and return that tiny file to the project.

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

1. **Current:** pinned HF snapshot -> user-owned Kaggle Model via `kagglehub.model_upload`.
2. Verify/attach the created Kaggle Model via UI or draft-session `kagglehub.model_download` before `Save Version`.
3. If Kaggle refuses the large Model upload for a platform/quota reason, investigate a private Kaggle Dataset/artifact mirror only if competition rules permit it.
4. If the quantized route itself is blocked, reconsider BF16 only if storage and deployment evidence still justify it.
5. Only as a last resort route a large checkpoint through the user's PC.

NVIDIA's current model card lists the checkpoint license as **OpenMDW-1.1**; preserve that provenance and do not relabel it as Apache-2.0.

## Gate B rule

Do not attempt the large-model load until Gate A output is reviewed. Gate B auto-detects a ModelOpt/NVFP4 checkpoint and requests `modelopt_fp4`; vLLM may then select the available W4A16 kernel automatically. If backend selection alone fails, there is at most one bounded mechanical retry with a forced backend based on the actual log.

If the Kaggle base image lacks the required local vLLM path, prepare an offline dependency input first rather than enabling Internet in the competition-valid load run.
