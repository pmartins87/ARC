# M1 — Lightning L4 x4 smoke protocol

Snapshot: 2026-08-25

This protocol is deliberately small. Its purpose is to decide whether the Lightning/NVARC path deserves a real frozen-development experiment. It is **not** an ARC competition submission and it is **not** a tuning loop.

## Gate A — inspect only

Run `scripts/lightning_kaggle_smoke.py` in default `inspect` mode with:
- Kaggle GPU: L4 x4;
- Internet: OFF;
- target Lightning model attached as an input if the HF→Kaggle integration succeeds.

PASS requires:
- four CUDA devices visible;
- attached local HF-style checkpoint discovered;
- enough disk/input visibility to enumerate the checkpoint;
- package inventory recorded;
- no network dependency required to discover/load local assets.

If `vllm` is missing or clearly older/incompatible with Lightning 3.5, do **not** attempt a blind large-model load. Prepare an attached dependency package/wheel first.

## Gate B — one model load + one short generation

Run `scripts/lightning_vllm_kaggle_smoke.py` only after Gate A.

First configuration:
- TP=4;
- expert parallel ON;
- BF16 weights;
- max model length = 8192;
- Mamba SSM cache = float16;
- Mamba backend = flashinfer;
- Mamba stochastic rounding ON, 5 Philox rounds;
- speculative decoding OFF;
- eager execution ON for the first compatibility test;
- GPU memory utilization target = 0.88;
- one short ARC-shaped prompt;
- max completion = 64 tokens.

These choices intentionally favor **load/compatibility diagnosis**, not production throughput.

PASS requires all of:
- vLLM health endpoint becomes ready;
- `/v1/models` exposes a model id;
- one local chat completion succeeds;
- no OOM or unsupported-kernel error;
- startup time, output tokens, generation time and GPU memory are captured.

PARTIAL:
- model loads but generation fails for a fixable parser/chat-template reason;
- a current-vLLM flag mismatch is isolated;
- the model fits only after a simple non-score-seeking compatibility change (for example disabling a parser or changing backend while preserving the same checkpoint).

FAIL / REJECT DEPLOYMENT PATH:
- BF16 cannot initialize even at reduced context because of VRAM;
- L4 lacks a required kernel/backend and no safe competition-valid fallback is available;
- startup is repeatedly unstable;
- measured throughput makes even a minimal 240-task budget clearly infeasible.

## Gate C — source-faithful frozen development ablation

Only after Gate B PASS/PARTIAL with a viable fix.

Compare on the frozen development split:
1. transductive direct-grid prompt;
2. python-inductive `transform(grid)` prompt.

Hold constant:
- checkpoint;
- task list;
- candidate count;
- generation token budget;
- temperature/sampling family;
- global runtime ceiling.

Record:
- exact pass@1 and pass@2;
- tasks/outputs reached before deadline;
- invalid-output rate;
- program execution failure rate;
- output-shape error rate;
- attempt diversity;
- runtime per solved/attempted output;
- candidate discovery vs selection if multiple candidates are generated.

No validation/heldout tuning.

## Stop rule

E0006 gets at most:
- one compatibility/load round;
- one bounded fix round if the first failure is clearly mechanical;
- one source-faithful transductive-vs-inductive development ablation.

Then classify **KEEP / REJECT / INCONCLUSIVE**. Do not let deployment debugging consume M1 indefinitely.
