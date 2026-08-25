# E0006 — Nemotron 3.5 Lightning / NVIDIA NVARC feasibility

Status: **PENDING — source gates partially passed, no GPU run**

```yaml
id: E0006
date_opened: 2026-08-25
method: source-faithful Nemotron 3.5 Lightning + NVIDIA NeMo Gym NVARC feasibility
checkpoint: nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16
checkpoint_license: OpenMDW-1.1
upstream_harness: NVIDIA-NeMo/Gym resources_servers/nvarc
upstream_harness_commit_origin: fb99c89e0a68f3f89f1e18fe1a8a6f1c8cfbb54c
hardware_target: Kaggle L4 x4
competition_submission: NOT_STARTED
status: PENDING_DEPLOYMENT_FEASIBILITY
```

## Question

Can a released ARC-post-trained, 30B-total/3B-active Nemotron model be deployed within ARC Prize 2026's offline 4xL4 envelope, and if so, under a controlled budget does NVIDIA's public direct-grid or executable-program ARC interface generalize better?

## Evidence already established without compute

- official Lightning checkpoint is public and OpenMDW-1.1;
- ARC Prize permits freely/publicly available external pre-trained models;
- NVIDIA NeMo Gym contains a public NVARC exact verifier with transductive and inductive `transform()` modes;
- official Lightning evaluation uses vLLM and TP=4;
- official base-evaluation documentation reports ~62 GB BF16 weights;
- L4 provides 24 GB/GPU and BF16 support;
- raw weights alone therefore do not rule out TP=4;
- L4-specific startup/runtime and end-to-end throughput remain unmeasured;
- no official Lightning ARC-AGI-2 score has been established.

## Planned evidence sequence

1. finish public-source deployment audit;
2. no-leaderboard L4x4 load/smoke only if still justified;
3. freeze exact checkpoint/runtime/software provenance;
4. frozen development evaluation with controlled generation budget;
5. transductive-vs-inductive ablation;
6. exact score, candidate/attempt diversity, runtime/coverage and error taxonomy;
7. KEEP / REJECT / INCONCLUSIVE decision.

## Guardrails

- no score inferred from ARC-specific training data;
- no attribution of current 70%+ leaders to Nemotron without team evidence;
- no use of validation/heldout for iterative tuning;
- no original competitive mechanism committed publicly before visibility review;
- no extra competition submission merely to test whether the model loads.
