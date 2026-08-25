# E0006 — Nemotron 3.5 Lightning / NVIDIA NVARC feasibility

Status: **PENDING L4 SMOKE — public-source hardware floor passed, no GPU run**

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
status: PENDING_L4_SMOKE
```

## Question

Can a released ARC-post-trained, 30B-total/3B-active Nemotron model be deployed within ARC Prize 2026's offline 4xL4 envelope, and if so, under a controlled budget does NVIDIA's public direct-grid or executable-program ARC interface generalize better?

## Evidence established without compute

### Checkpoint relevance

- official Lightning checkpoint is public and OpenMDW-1.1;
- official model card: 30B total / 3B active, hybrid Mamba-2 + MoE + Attention;
- post-training cutoff is May 2026;
- the released model card explicitly lists **ARC-AGI Gym Environment** in its post-training sources;
- the same disclosure lists **Synthetic ARC-AGI Ultra Data — 192,016 records**, sourced from ARC-AGI-2 plus the ARC dataset collection;
- it also lists another synthetic agentic-reasoning blend whose seed sources include ARC-AGI-2;
- therefore Lightning has direct ARC-specific post-training provenance, not just generic reasoning capability;
- no official Lightning ARC-AGI-2 exact score has been established, so no score is inferred from training provenance.

Primary source:
- https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16

### Public ARC task contracts

NVIDIA NeMo Gym contains a public Apache-2.0 NVARC verifier with:
- `transductive`: direct final grid;
- `python_inductive`: executable Python `transform(grid)`;
- binary exact-match reward;
- 30-second transform timeout for the inductive mode.

The companion public `Nemotron-RL-ARC-AGI-v1` dataset confirms the same two variants over matched tasks and states:
- 10,000 training problems per variant;
- 514 validation problems per variant;
- validation = ARC-AGI-1 evaluation union ARC-AGI-2 evaluation, deduplicated;
- all validation IDs blacklisted from the released 10k training sample.

Sources:
- https://github.com/NVIDIA-NeMo/Gym/tree/main/resources_servers/nvarc
- https://huggingface.co/datasets/nvidia/Nemotron-RL-ARC-AGI-v1

### SFT scale and runtime warning

The public `Nemotron-SFT-ARC-AGI-v1` card reports very large successful ARC trajectory pools and curated blends with mean output traces around ~20.9k to ~35.1k tokens. That supports our existing concern that replaying the long-trace training distribution naively is incompatible with an efficient 240-task / 12-hour competition run.

The dataset card says ARC-AGI / ARC-AGI-2 evaluation IDs were blacklisted from the SFT construction pool.

Source:
- https://huggingface.co/datasets/nvidia/Nemotron-SFT-ARC-AGI-v1

License caveat: Hugging Face metadata currently shows `pending-legal-review` while the card text says CC BY 4.0 plus upstream Apache/MIT lineage. Raw-dataset redistribution or further training remains **license clarification required**. This does not alter the model checkpoint's separately published OpenMDW-1.1 license.

### Deployment feasibility — vendor profile floor now passed

NVIDIA's current NIM support matrix publishes a stronger bound than our earlier raw-weight estimate. For `nemotron-3.5-lightning-30b-a3b`, **BF16 TP4 / PP1** it reports:
- minimum VRAM per GPU: **20 GB**;
- minimum GPU count: **4**;
- architecture requirement: **Ampere or newer, SM 8.0+**.

NVIDIA lists L4 as:
- **24 GB** GPU memory;
- Ada Lovelace architecture;
- CUDA compute capability **8.9**;
- BF16 support.

Therefore the target L4 x4 passes the published profile floor:
- +4 GB/GPU nominal headroom above the NIM floor;
- +16 GB aggregate nominal floor headroom;
- 4 GPUs = required count;
- SM 8.9 > SM 8.0 requirement.

This materially upgrades feasibility, but **NIM profile fit is not proof of bare-vLLM Kaggle fit**. The NIM matrix warns its floor does not cover arbitrary additional KV-cache/context/concurrency headroom, and Kaggle's L4 topology/kernel/package stack remains unmeasured.

Sources:
- https://docs.nvidia.com/nim/large-language-models/latest/reference/support-matrix.html
- https://www.nvidia.com/data-center/l4/
- https://developer.nvidia.com/cuda/gpus

Repo calculation:
- `src/arcsolver/profile_headroom.py`
- `scripts/check_profile_headroom.py`
- `docs/M1_LIGHTNING_NIM_PROFILE_BOUND.md`

### Serving path

- official Lightning evaluation uses vLLM;
- NVIDIA's evaluation recipe defaults to tensor parallel size **4** and expert parallelism;
- NVIDIA's current model card documents vLLM `v0.27.1`;
- the memory-constrained recipe uses Mamba backend `flashinfer`, Mamba SSM cache `float16`, stochastic rounding and reduced context as needed;
- our first smoke disables speculative decoding and uses reduced context to isolate compatibility rather than optimize final throughput.

Sources:
- https://github.com/NVIDIA-NeMo/Nemotron/blob/main/docs/nemotron/lightning35/evaluate.md
- https://github.com/NVIDIA-NeMo/Nemotron/blob/main/src/nemotron/recipes/lightning35/stage3_eval/config/default.yaml
- official Lightning model card above.

### Kaggle L4/vLLM precedent

Public Kaggle notebooks demonstrate that vLLM and FlashInfer have run successfully on **L4 x4** in earlier competitions, including 72B AWQ/multi-model examples. Historical competition discussion also documents successful vLLM execution on Kaggle L4 x4 after environment-specific setup.

This is useful platform precedent, not evidence that current Lightning/vLLM 0.27 kernels work unchanged.

Examples:
- https://www.kaggle.com/code/abdullahmeda/load-72b-awq-model-using-vllm-on-l4-x4
- https://www.kaggle.com/code/rsmits/vllm-load-multiple-models

### Kaggle attachment path

Current Kaggle documentation says Hugging Face models can be linked into Kaggle Models through the **Use this model → Kaggle** integration, and attached Models can then be added to notebooks as inputs. Kaggle documents up to 100 GB per model variation.

This gives a preferred path that avoids routing ~60+ GB through the user's PC. It still must be verified that the linked Lightning model materializes as a local attached input usable with Internet OFF.

Sources:
- https://www.kaggle.com/docs/models
- https://www.kaggle.com/docs/notebooks
- https://www.kaggle.com/product-announcements/470613

## Prepared measurement harness

Merged repository tooling provides two layers:

1. `scripts/lightning_kaggle_smoke.py`
   - inspect-only mode by default;
   - local model discovery;
   - Python/package/GPU inventory;
   - optional Transformers load fallback.

2. `scripts/lightning_vllm_kaggle_smoke.py`
   - offline local-model path only;
   - vLLM server launched as a subprocess;
   - TP=4 + expert-parallel configuration;
   - reduced context for the first feasibility test;
   - health check + `/v1/models` + one short chat generation;
   - startup latency, output-token throughput and `nvidia-smi` memory snapshots;
   - structured failure classes and server log tail;
   - machine-readable JSON result;
   - server terminated automatically unless explicitly kept alive.

Pure command construction, model discovery and profile-floor logic have CI tests.

## Planned evidence sequence

1. N1 hidden rerun continues independently;
2. use the Hugging Face → Kaggle linkage path rather than local 60+ GB upload if possible;
3. run **inspect-only** on L4 x4 with Internet OFF, no competition submission;
4. if package/model discovery passes, run vLLM load + one short generation only;
5. freeze exact checkpoint/runtime/software/topology/VRAM provenance;
6. if load+throughput are plausible, run a bounded frozen-development comparison:
   - direct-grid transductive;
   - executable-program inductive;
   - fixed candidate count;
   - fixed token/runtime budget;
7. measure exact pass@1/pass@2, coverage, candidate diversity and failures;
8. KEEP / REJECT / INCONCLUSIVE decision.

## Guardrails

- no score inferred from ARC-specific training data;
- no attribution of current 70%+ leaders to Nemotron without team evidence;
- no use of validation/heldout for iterative tuning;
- no original competitive mechanism committed publicly before visibility review;
- no extra competition submission merely to test whether the model loads;
- no manual 60+ GB user-PC upload while a lower-friction Kaggle/HF path remains available;
- raw NVIDIA ARC datasets are not used for new training until their displayed license inconsistency is resolved;
- NIM profile floors are used only as deployment evidence, never substituted for direct Kaggle measurement.
