# M1 — NVIDIA ARC post-training resource audit

Snapshot: 2026-08-25

Purpose: determine whether newly public NVIDIA ARC-specific data/models create a materially better competition-fit path than spending M1 on another ~31% Qwen/NVARC sibling.

This is a public-source audit. It does **not** claim that any current ARC Prize leaderboard leader uses these assets.

## 1. Nemotron-SFT-ARC-AGI-v1

Official dataset:
- https://huggingface.co/datasets/nvidia/Nemotron-SFT-ARC-AGI-v1

The current data card describes multi-turn agentic reasoning traces from open-weight models solving ARC puzzles. Important facts:

- upstream pool: **304,491 successful runs over 72,980 unique problem IDs**;
- wide curated blend: **67,529 records / 67,529 unique problems**, ~6.1 GB;
- deep curated blend: **207,569 records / 64,467 unique problems**, up to 8 solutions/problem, ~13 GB;
- traces can contain natural-language reasoning, tool calls and tool outputs;
- exact solution matching was used for automatic correctness filtering;
- ARC-AGI / ARC-AGI-2 evaluation IDs are explicitly blacklisted by the stated curation sampler;
- large generating-model contributors include Kimi K2.5 and Qwen3-235B, with additional DeepSeek/Qwen/GLM-family traces.

This is qualitatively different from N1's puzzle-time LoRA adaptation. It exposes successful **reasoning/tool trajectories** at scale and is therefore relevant to both learned priors and tool-use distillation.

### Licensing gate

There is a live metadata inconsistency that must be treated conservatively:

- the prose data card states **CC BY 4.0**, with Apache 2.0 / MIT additional information;
- the current Hugging Face repository metadata still displays **`pending-legal-review`**;
- the NVIDIA discussion that introduced the data card says that this metadata value was a placeholder pending final legal approval.

Therefore we do **not** yet treat the dataset license as clean enough for prize-critical redistribution. Research inspection is useful; packaging/training for a final prize notebook remains gated on a resolved license record and Kaggle-rule compatibility.

Sources:
- https://huggingface.co/datasets/nvidia/Nemotron-SFT-ARC-AGI-v1
- https://huggingface.co/datasets/nvidia/Nemotron-SFT-ARC-AGI-v1/discussions/1

## 2. Nemotron-RL-ARC-AGI-v1

Official companion dataset:
- https://huggingface.co/datasets/nvidia/Nemotron-RL-ARC-AGI-v1

Current public metadata:
- **21,028 rows**;
- ~443 MB;
- same broad ARC post-training resource family;
- included in NVIDIA's Nemotron Post-Training v3 collection.

This is a possible source for reward-/policy-style adaptation later, but it is lower priority than establishing whether a ready-made competition-fit checkpoint already absorbed useful ARC behavior.

## 3. Nemotron 3.5 Lightning 30B-A3B — newly important candidate

Official model:
- https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16
- https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4
- https://build.nvidia.com/nvidia/nemotron-3.5-lightning-30b-a3b/modelcard

Released **2026-08-11**, the model is:
- **30B total / 3B active** MoE;
- hybrid Mamba-2 + MoE + attention;
- reasoning and tool-call capable;
- long-context;
- open weights under **OpenMDW 1.1** according to the official model card.

The official training disclosure is the key ARC signal. It lists, among its post-training sources:

- **Synthetic ARC-AGI Ultra Data — 192,016 records**, sourced from ARC-AGI-2 / ARC dataset collection;
- an **ARC-AGI Gym Environment**;
- a **Synthetic Terminus Ultra Agentic Reasoning Blend** whose listed seed sources include ARC-AGI-2.

Thus Lightning is not merely a generic 30B reasoning model: official NVIDIA documentation says ARC-specific data is part of its post-training mixture.

### Critical missing fact

The release benchmark table does **not** publish an ARC-AGI-2 score. A targeted source search has not established an official Lightning ARC-AGI-2 evaluation.

Therefore this model is a **high-information candidate, not a proven baseline**. We must not infer an ARC score from the fact that it saw synthetic ARC training data.

## 4. Competition-fit analysis

### Raw weight footprint

Public artifacts give useful upper/lower bounds:

- BF16 GGUF conversion: about **63.2 GB** target weights;
- Q8 GGUF conversion: about **33.6–35 GB**;
- Q4 conversion: about **18.9 GB** in the ggml-org artifact;
- official NVFP4 checkpoint is designed for much smaller deployment footprints than BF16.

Kaggle L4 x4 provides roughly 96 GB aggregate VRAM, so the raw BF16 target weights are not automatically disqualified by aggregate capacity. However, raw-weight fit is not runtime fit: KV/Mamba state, kernels, tensor parallelism, framework support and the ARC harness must also fit.

### Hardware caveat

The official Lightning NVFP4 card explicitly lists Blackwell and Hopper, plus Ampere through W4A16. **L4 is Ada Lovelace and is not explicitly listed in that official compatibility statement.**

Therefore:

> direct official NVFP4-on-L4 compatibility is **UNVERIFIED**.

Do not burn a competition run merely because the file size looks small.

A community GGUF path exists and can materially reduce footprint, but its ARC accuracy, multi-GPU L4 throughput and prize-use licensing/provenance must be validated before adoption.

Sources:
- https://huggingface.co/ggml-org/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF
- https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4

## 5. Why this changes M1 priorities

The live competition frontier is ~70%+, while another public NVARC sibling is ~31%. A new model with documented ARC-specific post-training and only 3B active parameters has higher information value than reproducing another correlated ~31% notebook **if** it can be made competition-valid.

This does not justify an immediate full hidden rerun. The bounded sequence is:

1. prove legal/provenance status of the exact checkpoint/data path;
2. prove L4 x4 load/inference compatibility without a full competition submission where possible;
3. freeze a minimal ARC prompt/tool schema faithful to the model's training format;
4. benchmark a tiny smoke subset for functionality only;
5. if functional, use the frozen 60-task development protocol for an exact score and candidate-diversity audit;
6. compare unique exact wins, runtime and selector complementarity against N1;
7. only then decide whether it deserves a competition submission or M2 role.

## 6. Decision state

**RETAIN — HIGH-PRIORITY M1/M2 CANDIDATE, UNVALIDATED.**

Reasons to retain:
- recent release;
- ARC-specific official training disclosure;
- low active-parameter count;
- open weights;
- potentially plausible aggregate 4xL4 footprint;
- agentic/tool traces align with the strongest 2026 scientific evidence around executable reasoning.

Reasons not to promote yet:
- no official ARC-AGI-2 score found;
- official NVFP4 L4 support not established;
- exact inference stack under Kaggle offline constraints not proven;
- SFT dataset license metadata is inconsistent;
- training on ARC-style data is not evidence of hidden-task generalization.

## 7. Anti-speculation rule

Public discussion may associate NVIDIA ARC assets with current leaderboard leaders. Until a team publishes its method or a reproducible artifact establishes the connection, **we will not attribute nvbanana/rabbithole performance to Nemotron datasets or models.**

This candidate stands on its own public evidence and should be tested on that basis.
