# M1 — Minimal-manual Kaggle attachment plan for Nemotron 3.5 Lightning

Snapshot: 2026-08-25

## Goal

Make the Lightning feasibility test require as little user-side work as possible and avoid downloading/uploading ~60+ GB through the user's PC.

## Kaggle-supported path

Kaggle's current Models documentation says Hugging Face integration can create a Kaggle model page from an HF model by:
1. opening the Hugging Face model page;
2. choosing **Use this model → Kaggle**;
3. creating/saving the generated Kaggle notebook;
4. after that, the model has a Kaggle model page and can be attached from **Add Input → Models**.

Kaggle also documents that notebooks can attach Models as input data sources and that model variations may be up to 100 GB. The BF16 Lightning checkpoint is therefore not excluded by Kaggle's documented per-variation upload ceiling.

Sources:
- https://www.kaggle.com/docs/models
- https://www.kaggle.com/docs/notebooks
- https://www.kaggle.com/product-announcements/470613

## Preferred path for us

We should first try to use the Hugging Face-linked Kaggle model integration, **not** manually download the checkpoint to the user's computer.

Target:
- `nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16`

If the linked model can be attached as a Kaggle datasource, final competition notebooks can remain internet-off while the model files are provisioned as an input artifact before execution.

## User-side sequence when the gate is reached

Do not ask the user to do this while N1 is still running unless necessary.

When ready:
1. open the official HF model page;
2. `Use this model` → `Kaggle`;
3. create the generated notebook and save one version;
4. verify the resulting Kaggle model page exists;
5. in a fresh diagnostic notebook, attach that model through `Add Input`;
6. select GPU L4 x4 and Internet OFF;
7. run the repository's **inspect-only** smoke first;
8. only if package/model discovery is valid, run the vLLM load/generation smoke.

This does **not** submit anything to the ARC competition leaderboard.

## Fallbacks

If HF-linked model attachment does not materialize local weight files:
1. search Kaggle Models again for a community/NVIDIA mirror;
2. use Kaggle Models upload/import tooling rather than browser file upload;
3. only as a last resort consider local download + `kagglehub` upload.

Do not route 60+ GB through the user's PC unless all lower-friction paths fail.

## Dependency issue

The official Lightning model card currently documents vLLM `v0.27.1`. A Kaggle notebook with Internet OFF cannot fetch a missing/newer vLLM package during the final run.

Therefore the first diagnostic is intentionally split:
- **inspect mode:** reports installed `vllm`, `torch`, `transformers`, GPUs and attached model roots without loading the model;
- **load mode:** runs only if the environment is compatible or a competition-valid attached package/wheel solution has been prepared.

If Kaggle's base image lacks a compatible vLLM, we must package dependencies as an attached Kaggle input/package before treating the route as competition-valid.

## Success condition

A single user action session should produce machine-readable artifacts:
- `lightning_vllm_smoke.json`;
- `lightning_vllm_serve.log`;
- GPU inventory and memory snapshots;
- exact local checkpoint path;
- vLLM startup result;
- one short generation latency/token count.

Those artifacts are enough for a GO/NO-GO decision without consuming a competition submission.
