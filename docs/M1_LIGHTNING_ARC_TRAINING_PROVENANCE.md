# M1 — Nemotron 3.5 Lightning ARC training provenance

Snapshot: 2026-08-25

## Why this matters

Nemotron 3.5 Lightning is not merely a generic 30B reasoning model that happens to look interesting for ARC. NVIDIA's own released model card explicitly lists ARC-specific material in the post-training corpus. This substantially raises the information value of a competition-fit feasibility probe while still providing **no score guarantee**.

## Primary-source facts

Official model:
- `nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16`
- 30B total parameters / 3B active;
- hybrid Mamba-2 + MoE + Attention architecture;
- OpenMDW-1.1;
- release date 2026-08-11;
- post-training data cutoff May 2026.

The model card's detailed post-training disclosure explicitly lists:
- **ARC-AGI Gym Environment**;
- **Synthetic ARC-AGI Ultra Data — 192,016 records**, sourced from ARC-AGI-2 and the ARC dataset collection;
- an additional **Synthetic Terminus Ultra Agentic Reasoning Blend** whose listed seed sources include ARC-AGI-2.

Source:
- https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16

This establishes direct ARC-specific post-training provenance for the released Lightning checkpoint. It does **not** establish its ARC-AGI-2 evaluation score, hidden-set score, or relation to any current Kaggle leader.

## Public ARC SFT dataset

NVIDIA separately releases `nvidia/Nemotron-SFT-ARC-AGI-v1`.

Important facts from its dataset card:
- successful multi-turn agentic ARC traces from open-weight reasoning models;
- 304,491 successful upstream runs over 72,980 unique problem IDs before curated blends;
- wide blend: 67,529 records / 67,529 unique problems;
- deep blend: 207,569 records / 64,467 unique problems;
- ARC-AGI / ARC-AGI-2 evaluation IDs are stated to be blacklisted from the construction pool;
- average trace lengths are very large (roughly 20.9k–35.1k output tokens depending on blend), reinforcing our throughput concern;
- public tree is roughly 18.4 GB at the current snapshot.

Source:
- https://huggingface.co/datasets/nvidia/Nemotron-SFT-ARC-AGI-v1

### License caution

The Hugging Face metadata currently displays `pending-legal-review`, while the dataset card text says CC BY 4.0 with additional Apache/MIT lineage information. We therefore treat raw-dataset redistribution/training as **license-clarification required**. This inconsistency does not change the separately stated OpenMDW-1.1 license on the released Lightning model weights.

## Public ARC RL dataset

NVIDIA also releases `nvidia/Nemotron-RL-ARC-AGI-v1`, which is especially relevant because its task contract matches the NVARC verifier we audited.

The dataset card states:
- two variants over the same problems: `transductive` and `python_inductive`;
- transductive = direct final-grid output;
- python_inductive = Python `transform(grid)` executed with a 30-second timeout;
- exact binary reward, no LLM judge and no partial credit;
- 10,000 train problems per variant;
- 514 validation problems per variant;
- the 514 validation problems are the union of ARC-AGI-1 evaluation plus ARC-AGI-2 evaluation (deduplicated);
- all 514 validation IDs are blacklisted from the 10k training sample;
- released size is about 443–587 MB depending on representation/metadata view.

Source:
- https://huggingface.co/datasets/nvidia/Nemotron-RL-ARC-AGI-v1

This gives us an unusually clean public causal baseline question:

> With the same released ARC-post-trained checkpoint and compute budget, does direct grid prediction or executable-program induction generalize better on a frozen ARC-AGI-2 development split?

That question is prior-art reproduction/measurement. It is not our novelty.

## Deployment source facts

The official Lightning card currently documents vLLM `v0.27.1` and gives the following useful memory-constrained serving choices:
- vLLM server;
- Mamba backend `flashinfer`;
- Mamba SSM cache `float16` for the memory-constrained H100 path;
- reasoning parser `nemotron_v3`;
- tool parser `qwen3_coder`;
- no speculative decoding is required for the baseline path;
- lower `max-model-len` is explicitly recommended when memory-constrained.

NVIDIA's separate evaluation recipe uses TP=4 + expert parallelism. That matches our four competition GPUs in count, though not in GPU class/interconnect.

Sources:
- model card above;
- https://github.com/NVIDIA-NeMo/Nemotron/blob/main/docs/nemotron/lightning35/evaluate.md
- https://github.com/NVIDIA-NeMo/Nemotron/blob/main/src/nemotron/recipes/lightning35/stage3_eval/config/default.yaml

## Decision impact

E0006 is promoted from a generic-model feasibility check to a **high-information ARC-specific feasibility check**.

What would count as success at the next gate:
1. checkpoint is locally attachable in a Kaggle notebook with internet disabled;
2. vLLM can initialize across L4 x4 without OOM/unsupported-kernel failure;
3. one short ARC request completes and reports usable latency/VRAM;
4. only then do we spend a bounded frozen-development run comparing transductive vs inductive behavior.

What would count as failure:
- model cannot initialize on L4 x4 under a reasonable reduced context;
- required kernels/backend do not support L4 and no competition-valid low-risk fallback exists;
- throughput is so low that even optimistic hidden-task coverage is incompatible with the 12-hour envelope.

No hidden leaderboard submission is needed for these deployment gates.
