# E0006 — NVFP4 mirror provenance

Snapshot: 2026-08-26

## Purpose

Freeze the exact external model bytes targeted by E0006 before any Kaggle L4 x4 deployment result is interpreted. This is deployment/provenance evidence only; it is not a score claim.

## Source

- Hugging Face repository: `nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4`
- Frozen source revision observed in the successful Kaggle-side `hf_hub_download` / `snapshot_download` path: `cc84af2fe71647d87f4486c064f320e1e7535243`
- Observed reconstructed snapshot size in the Kaggle mirror run: approximately **21.6 GB**.
- License: **OpenMDW-1.1**. Do not relabel the mirrored weights as Apache-2.0.

The upstream Hugging Face repository is actively changing. E0006 must therefore remain pinned to the revision above. A future upstream refresh is a new model artifact/version and must not silently replace this checkpoint inside an existing experiment.

## Target Kaggle model

- Handle: `paulomartins87/nemotron-3-5-lightning/pyTorch/30b-a3b-nvfp4`
- Purpose: private/cloud-local attachment for competition-valid Internet-OFF feasibility testing.
- The model family object was created successfully during the first mirror attempt.
- The first 21.6 GB upload began after the full source snapshot had been reconstructed.
- The browser frontend later hit a local Chrome `Out of Memory` page while upload progress was being rendered. This does **not** establish either server-side upload success or failure. Completion remains `UNCONFIRMED` until a ready Kaggle model variation/version can be opened or downloaded.

## Verification rule

A mirror is considered **READY** only when at least one of the following succeeds:

1. Kaggle model UI shows a ready version for variation `30b-a3b-nvfp4`, with the expected model files; or
2. in a Kaggle draft session, `kagglehub.model_download("paulomartins87/nemotron-3-5-lightning/pyTorch/30b-a3b-nvfp4", path="config.json")` returns a readable local file.

Kaggle's current notebook resource behavior attaches a model datasource when `kagglehub.model_download(...)` is executed in the draft environment. The datasource must be attached before `Save Version`; save execution itself is not allowed to attach a new datasource.

## Retry discipline

If the first upload is incomplete, use `notebooks/E0006_mirror_nvfp4_to_kaggle.ipynb` rather than the original verbose ad-hoc cell. The resilient notebook:

- pins the exact HF revision;
- resumes/reuses the local source snapshot when available;
- validates a lightweight file manifest before upload;
- runs `kagglehub.model_upload` in a child process;
- redirects detailed upload progress to `/tmp/e0006_kaggle_model_upload.log` so the browser frontend is not flooded;
- emits only five-minute heartbeat lines;
- writes compact status and manifest JSON files.

Do not route the model through the user's PC.

## Downstream binding

Gate A and Gate B results must record the attached Kaggle model path/version. If the Kaggle mirror later receives another version, an E0006 result is valid only for the version actually attached to that run.
