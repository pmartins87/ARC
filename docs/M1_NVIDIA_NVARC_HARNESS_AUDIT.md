# M1 — NVIDIA NeMo Gym NVARC / competition-fit harness audit

Snapshot: 2026-08-25

## Executive finding

A higher-value public artifact exists than we had previously recognized: **NVIDIA NeMo Gym already ships an ARC-specific `nvarc` environment with both direct-grid and executable-program modes.**

This materially reduces guesswork around an ARC-native agent interface. We do not need to invent a tool/harness format before testing Nemotron-family models; an upstream Apache-2.0 reference exists.

It is still a research harness, not a ready Kaggle submission and not evidence that Nemotron 3.5 Lightning achieves a particular ARC score.

## 1. Provenance

Upstream repository:
- https://github.com/NVIDIA-NeMo/Gym

NVARC source:
- `resources_servers/nvarc/`
- first commit for the current resource server: `fb99c89e0a68f3f89f1e18fe1a8a6f1c8cfbb54c`
- commit date: 2026-04-06
- commit title: `feat: Introduce NVARC Resource Server with inductive and transductive modes (#1003)`

The commit message explicitly says it adds:
- transductive grid output;
- inductive Python-code output;
- sandboxed code execution;
- configs/request-response models;
- example data and unit tests.

Code license: **Apache 2.0**.

## 2. Two upstream modes

### Transductive

The model predicts the final grid directly. The verifier parses a valid board from the response and awards reward 1.0 only for an exact match.

This is closest to the final Kaggle output contract.

### Inductive

The model emits Python containing a `transform(input_grid)` function. Upstream extracts the code, executes it in a subprocess sandbox and converts the result to a grid. Reward is again binary exact match.

Important public implementation details:
- default transform timeout: **30 seconds**;
- dangerous filesystem/network/process modules are blocked by the sandbox;
- code must define `transform`;
- output is normalized from NumPy/Torch-like containers to JSON-compatible values;
- final verification remains exact-grid equality.

This is directly relevant to the program-synthesis hypothesis family already identified in the literature audit, but the idea itself is now unquestionably prior art.

Sources:
- https://github.com/NVIDIA-NeMo/Gym/blob/main/resources_servers/nvarc/README.md
- https://github.com/NVIDIA-NeMo/Gym/blob/main/resources_servers/nvarc/app.py
- https://github.com/NVIDIA-NeMo/Gym/blob/main/resources_servers/nvarc/configs/inductive.yaml

## 3. Dataset/harness reproducibility boundary

The public repo is sufficient to reproduce the **verifier and environment semantics**, but not the complete NVARC training data used internally:

- the example JSONL is committed;
- inductive config points to `resources_servers/nvarc/data/python_inductive/train.jsonl` and `validation.jsonl`;
- the NVARC README explicitly says train/validation paths are configured but **not committed**.

Therefore we can source-faithfully reproduce the interface and verifier, but we cannot claim to reproduce NVIDIA's complete training set from this repository alone.

The related public `Nemotron-SFT-ARC-AGI-v1` dataset remains separately useful, subject to its currently inconsistent license metadata described in `docs/M1_NEMOTRON_ARC_RESOURCE_AUDIT.md`.

## 4. Relation to the older `arc_agi` NeMo Gym resource server

NeMo Gym also has a simpler `arc_agi` resource server. It:
- formats ARC-AGI-1 and ARC-AGI-2 datasets;
- parses final grids from model text;
- verifies exact equality;
- documents local vLLM evaluation using Nemotron 3 Nano.

The dedicated `nvarc` resource server is more relevant to our research because it explicitly supports **induction of executable transformation programs** in addition to direct grid prediction.

Source:
- https://github.com/NVIDIA-NeMo/Gym/blob/main/resources_servers/arc_agi/README.md

## 5. Nemotron 3.5 Lightning serving evidence

Official NVIDIA/vLLM sources materially improve the feasibility picture:

- vLLM announced day-0 Nemotron 3.5 Lightning support;
- official NVIDIA evaluation uses vLLM with the `nemotron_v3` reasoning parser and `qwen3_coder` tool parser;
- the released evaluation config defaults to **tensor parallel size 4**;
- NVIDIA's base-model Gym suite says the BF16 model is ~31.6B parameters / ~62 GB of weights and that **TP=4 is the validated configuration**;
- the same source says smaller TP works where weights/cache fit.

This matches the number of competition GPUs exactly, although the validation hardware is not Kaggle L4.

Sources:
- https://github.com/NVIDIA-NeMo/Nemotron/blob/main/docs/nemotron/lightning35/evaluate.md
- https://github.com/NVIDIA-NeMo/Gym/blob/main/nemotron_recipes/lightning-3.5/base/base-suite.yaml
- https://blog.vllm.ai/2026/08/10/nemotron-3-5-lightning-vllm.html

## 6. L4 x4 raw-memory bound

NVIDIA lists each L4 as:
- 24 GB GPU memory;
- BF16 Tensor Core support;
- 300 GB/s device-memory bandwidth;
- PCIe Gen4 x16 interconnect.

A ~62 GiB BF16 model sharded ideally over TP=4 is approximately:
- **15.5 GiB raw weights per GPU**;
- **8.5 GiB raw headroom per 24 GiB L4**.

That is a useful result: **BF16 is not ruled out by raw weight bytes alone.**

It is not proof that the model fits. The remaining ~8.5 GiB/GPU must absorb Mamba state, attention KV cache, activations/temp buffers, CUDA graphs, allocator overhead and runtime structures. TP communication over the actual Kaggle topology may also dominate performance.

Official vLLM deployment-target text names H100/H200/A100/L40S/RTX and several Blackwell systems but does not explicitly name L4. Therefore L4 compatibility remains a measured gate, not an assumption.

Source:
- https://www.nvidia.com/data-center/l4/

Repo tool:
- `src/arcsolver/deployment_budget.py`
- `scripts/model_deployment_budget.py`

## 7. Throughput lower bound is at least as important as memory

The hidden competition run has 240 unseen tasks and a 12-hour notebook ceiling. A model can fit and still be useless if its reasoning traces are too long.

Using 240 output slots only as a clean planning proxy and two candidate generations per output, the **generated-token-only** lower bound is:

| generated tokens / candidate | minimum aggregate generation rate |
|---:|---:|
| 1,000 | 11.1 tok/s |
| 2,000 | 22.2 tok/s |
| 4,000 | 44.4 tok/s |
| 8,000 | 88.9 tok/s |
| 20,000 | 222.2 tok/s |
| 35,000 | 388.9 tok/s |

These are optimistic lower bounds. They exclude prompt prefill, tool execution, verification, retries, selection/scoring, startup and safety margin.

This matters because the public Nemotron ARC SFT traces can be very long. A competition-fit path likely needs a much tighter reasoning/tool budget than simply replaying the long training-trajectory distribution.

## 8. Source-faithful baseline experiment now available

If Lightning can be loaded on L4 x4, the first clean comparison should **not** be an original mechanism. It should be a bounded source-faithful baseline:

1. same Lightning checkpoint;
2. same frozen ARC development tasks;
3. transductive mode versus inductive `transform()` mode;
4. fixed candidate count and fixed inference-token budget;
5. exact pass@1/pass@2, runtime/coverage and candidate-diversity telemetry;
6. no tuning on validation/heldout.

This answers a high-information question:

> Under identical competition-fit compute, does the ARC-trained model generalize better by directly predicting grids or by inducing an executable transformation?

That experiment is prior-art reproduction/ablation, not our novelty. Any original mechanism comes only after the visibility gate.

## 9. Current decision

**PROMOTE from “interesting model” to “preferred M1/M2 feasibility probe”, still UNVALIDATED.**

Why:
- official ARC-specific training disclosure;
- official ARC/NVARC verifier/harness exists;
- official inference stack uses TP=4;
- raw BF16 memory does not immediately rule out 4xL4;
- inductive/transductive modes give a clean causal baseline comparison;
- this has substantially more information value than another correlated ~31% public Qwen/NVARC leaderboard run.

Remaining gates before asking the user for any Kaggle work:
- exact checkpoint redistribution/Kaggle attachment legality;
- practical vLLM+Lightning load on L4/Ada;
- measured memory after server initialization;
- short-prompt throughput and tool/parser correctness;
- dataset-license resolution if the SFT data itself is used rather than only the released checkpoint;
- no hidden assumption that ARC-specific post-training implies high unseen-task accuracy.
