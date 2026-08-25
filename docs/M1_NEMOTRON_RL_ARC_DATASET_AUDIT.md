# M1 — Nemotron-RL-ARC-AGI-v1 audit

Snapshot: 2026-08-25

## Executive finding

NVIDIA's official `Nemotron-RL-ARC-AGI-v1` release is a public semantic counterpart to the NeMo Gym NVARC environment we already audited. It exposes both of the same high-level task modes used by the upstream NVARC verifier:

- `transductive`: predict the final ARC grid directly;
- `python_inductive`: emit a Python `transform(grid)` function, execute it with a 30-second timeout, and exact-match the resulting grid.

This is important because the NeMo Gym repository config points to NVARC train/validation paths that are not committed, while the Hugging Face release makes an official NVIDIA ARC RL dataset with matching modes, prompts, exact-reward semantics and agent references publicly inspectable.

**Provenance guard:** this audit does not claim that the Hugging Face files are byte-identical to the uncommitted NeMo Gym paths. Treat them as an official semantic/formatted counterpart until file hashes or an NVIDIA source explicitly establish identity.

Official dataset:
- https://huggingface.co/datasets/nvidia/Nemotron-RL-ARC-AGI-v1

## 1. Exact released structure

The official card states that both variants are single-step: one model response per ARC problem.

Each variant uses the same:
- **10,000 training problems**;
- **514 validation problems**.

The 514 validation problems are described as the union of ARC-AGI-1 evaluation (400) and ARC-AGI-2 evaluation (120), deduplicated. All validation problem IDs are blacklisted from the training sample.

Released counts:

| subset | split | rows | disk reported by card |
|---|---:|---:|---:|
| transductive | train | 10,000 | 272 MB |
| transductive | validation | 514 | 8.4 MB |
| python_inductive | train | 10,000 | 297 MB |
| python_inductive | validation | 514 | 9.5 MB |
| total | | **21,028** | ~587 MB card accounting |

Hugging Face also reports total downloadable file size around 443 MB; converted Parquet artifacts may have different storage totals. Record the representation/version whenever bytes are used.

## 2. Exact task semantics

### Transductive

The system prompt asks the model to infer the input-output rule and return only a grid in `\\boxed{...}` format. The parsed grid receives binary reward 1 only when it exactly equals `expected_output`.

### Python-inductive

The prompt casts ARC as code induction: infer the transformation and create a Python `transform` function. The verifier:
- extracts Python;
- executes it on the test input;
- applies a **30-second timeout**;
- exact-matches the produced grid against `expected_output`;
- awards no partial credit.

These semantics align directly with the public NeMo Gym NVARC resource server already recorded in `docs/M1_NVIDIA_NVARC_HARNESS_AUDIT.md`.

## 3. Row-level provenance signals

The official viewer exposes fields including:
- `responses_create_params.input`;
- demonstrations in `train`;
- `test_input` and `expected_output`;
- `problem_id` / `task_id`;
- `variant`;
- difficulty score/bucket;
- augmentation metadata;
- `original_problem`;
- model/source `metadata`;
- `agent_ref`;
- `used_in`.

Observed `python_inductive` rows carry:
- `agent_ref.name = nvarc_inductive_simple_agent`;
- `used_in = ["ultra_v3"]` in the current viewer;
- generating/source metadata examples such as `gpt-oss-120b`.

This is strong evidence that the release belongs to NVIDIA's NVARC/Nemotron post-training ecosystem, but it still does not prove that every released row was used to train Nemotron 3.5 Lightning specifically. Keep model-specific training claims tied to the Lightning model card/disclosure, not inferred from this field alone.

## 4. Sampling and leakage controls

The card says the 10K training problems are sampled uniformly from roughly **66K eligible problems**, with:
- at most five training examples per problem;
- all 514 validation IDs excluded;
- no released augmentation variants (one row per problem).

Seed sources are stated as:
- ARC-AGI-2;
- NVARC Augmented Puzzles;
- `arc-dataset-collection` community subsets.

This is materially cleaner for a causal transductive-vs-inductive baseline than mixing unknown task pools, because both variants use the **same 10,000 train + 514 validation problem identities** and differ primarily in prompt/output/verifier mode.

## 5. Difficulty distribution

The official card reports the 10K training sample as:
- easy: **1,201 (12.0%)**;
- medium: **3,591 (35.9%)**;
- hard: **5,208 (52.1%)**.

This makes difficulty-conditioned analysis possible later without inventing our own labels. Do not use the 514 validation answers for iterative tuning; difficulty metadata can be used only as a reporting stratifier under our frozen protocol.

## 6. Licensing contradiction remains

The Hugging Face repository currently displays metadata license **`pending-legal-review`**, while the prose dataset card states **CC BY 4.0** plus Apache 2.0 / MIT additional information.

Therefore:
- source inspection and methodology audit: acceptable for research planning;
- final prize-critical redistribution or training dependency on these dataset bytes: **gated** until license metadata is cleanly resolved or a controlling NVIDIA license source is identified.

This does not block evaluation of the already-released Lightning checkpoint under its separate OpenMDW-1.1 license.

## 7. Consequence for E0006

The strongest source-faithful baseline is now better specified:

1. released Nemotron 3.5 Lightning checkpoint;
2. frozen ARC development tasks;
3. NVIDIA-style transductive prompt/verification contract;
4. NVIDIA-style python-inductive `transform()` contract;
5. same checkpoint, same tasks and fixed generation/runtime budget;
6. exact pass@1/pass@2, runtime/coverage, shape/error taxonomy and diversity;
7. compare the two modes before any original mechanism.

The comparison asks a clean question:

> Does an ARC-post-trained model generalize better under a direct output representation or an executable transformation representation when task identities and inference budget are controlled?

This is prior-art reproduction/ablation, not a novelty claim.

## 8. Decision

**RETAIN — high-information public baseline resource, with license gate on dataset reuse.**

The new evidence further reduces the value of blindly running another correlated ~31% Qwen notebook. If Lightning passes the 4xL4 deployment gate, a source-faithful transductive-vs-inductive experiment is the preferred next controlled neural experiment.
