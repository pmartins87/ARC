# M1 — Lightning L4 x4 smoke protocol

Snapshot: 2026-08-25

This protocol is deliberately small. Its purpose is to decide whether the Lightning/NVARC path deserves a real frozen-development experiment. It is **not** an ARC competition submission and it is **not** a tuning loop.

## Gate A — inspect only

Run `notebooks/E0006_lightning_gate_a_kaggle.ipynb` with:
- Kaggle GPU: L4 x4;
- Internet: OFF;
- preferred checkpoint: `nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4` attached as a Kaggle Model/Input.

PASS requires:
- four CUDA devices visible;
- attached local HF-style checkpoint discovered;
- enough disk/input visibility to enumerate the checkpoint;
- package inventory recorded;
- no network dependency required to discover/load local assets.

If `vllm` is missing or clearly older/incompatible with Lightning 3.5, do **not** attempt a blind large-model load. Prepare an attached dependency package/wheel first.

## Checkpoint order

1. **NVFP4 preferred.** On L4 this is expected to execute through the documented W4A16 fallback path rather than native Blackwell NVFP4 arithmetic. It gives substantially more memory headroom for the feasibility test.
2. **BF16 fallback/reference.** Use only if the quantized checkpoint cannot be materialized or the quantized execution path is mechanically unsupported while BF16 remains plausible.

Do not change checkpoint between Gate A and Gate B unless the Gate A review explicitly records the reason.

## Gate B — one model load + one short generation

Run `notebooks/E0006_lightning_gate_b_kaggle.ipynb` only after Gate A is reviewed and passes.

The standalone notebook mirrors the repository smoke harness and requires no repo clone. First configuration:
- TP=4;
- expert parallel ON;
- same checkpoint validated by Gate A;
- quantization auto-detected (`modelopt_fp4` for the NVFP4 checkpoint);
- compute dtype = BF16;
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

Expected artifacts:
- `/kaggle/working/e0006_gate_b_smoke.json`;
- `/kaggle/working/e0006_gate_b_vllm.log`.

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
- the selected checkpoint cannot initialize even at reduced context because of VRAM;
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
