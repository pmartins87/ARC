# M1 — Lightning Kaggle packaging path

Snapshot: 2026-08-25

Goal: minimize manual work if E0006 reaches the L4x4 smoke gate.

## 1. Model attachment path

Kaggle's current model documentation supports Hugging Face model integration. From a Hugging Face model page, `Use this model -> Kaggle` can create/open a Kaggle notebook with the model integration; models attached to a notebook appear in its Input pane and are pinned as notebook resources when a version is saved.

Relevant docs:
- https://www.kaggle.com/docs/models
- https://www.kaggle.com/blog/kaggle-hugging-face-integration

Target public checkpoint:
- `nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16`

This is preferable to making the user manually download ~60+ GB locally and re-upload it.

## 2. Offline scoring requirement

The ARC competition's scoring rerun has no internet. Therefore the saved notebook version must already contain/attach every required model and package resource before submission.

Kaggle's notebook/package documentation explicitly notes that Save execution cannot attach new resources dynamically and that dependencies/resources used for a competition scoring session must be saved/pinned beforehand.

Implication: a successful interactive `from_pretrained()` download is insufficient unless Kaggle records the model as an attached input for the saved version.

## 3. Inference software path

Official Lightning serving guidance currently targets vLLM 0.27.1. The exact Kaggle base image version is not assumed.

Preferred order:
1. inspect the live Kaggle image only when we open the smoke notebook;
2. if compatible vLLM is already present, use it;
3. otherwise use Kaggle's dependency mechanism or attach a pinned offline wheel bundle;
4. do not enable notebook internet in the final competition-valid version;
5. record exact package versions in E0006.

A second deployment option is the official `ggml-org` GGUF conversion running through llama.cpp. This is attractive for footprint and broad CUDA support, but it is a **community conversion/inference path** rather than NVIDIA's reference vLLM route, so any ARC accuracy change must be measured rather than assumed.

GGUF source:
- https://huggingface.co/ggml-org/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF

Current public sizes include approximately:
- Q4_0: 18.9 GB plus MTP file;
- Q8_0: 33.6 GB plus MTP file;
- BF16: 63.2 GB plus MTP file.

## 4. Smoke notebook scope

The first Lightning Kaggle notebook, if triggered, is **not submitted to the competition**. It should do only:

- print accelerator/device topology;
- print package versions;
- locate the attached checkpoint without network;
- initialize the chosen inference runtime at a deliberately short context length;
- record per-GPU peak memory after load;
- run one tiny ARC-style prompt in transductive mode;
- optionally run one python-inductive generation and local verifier execution;
- measure prefill/generation wall time and token counts;
- exit.

No full public-evaluation run until this passes.

## 5. Manual-work target

If this gate is reached, the intended user workflow is only a small number of Kaggle UI actions:
- open/create the prepared smoke notebook;
- ensure L4 x4 and Internet OFF;
- attach the preselected model/dependencies if Kaggle has not done so automatically;
- Save & Run All;
- send the resulting output/error screenshot.

Everything else should be prepared in the repository first.

## 6. Decision

**Packaging path is plausible and does not require a local 60 GB download/upload by default.**

The remaining unknown is execution feasibility on L4/Ada, not access to the public checkpoint.
