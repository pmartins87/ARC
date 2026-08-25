# M1 Kaggle Run Queue

Snapshot: 2026-08-25

The queue is ordered by information value per user-side run. A run is not performed merely because it was once planned; lower-value runs are skipped when a higher-value run already proves the same pipeline property.

## N1 — `ARC2 vanilla exact` — COMPLETE

Source: `https://www.kaggle.com/code/sorenravn/arc2-vanilla-exact`

Our Version 1:
- clean `Save & Run All`: **25m29s** on **L4 x4**;
- Internet OFF;
- competition rerun: **Succeeded**;
- Kaggle Public Score: **29.72**;
- frozen source snapshot reference: **31.39**;
- delta: **-1.67pp**.

Decision: **KEEP as end-to-end neural baseline anchor.** Do not spend quota rerunning N1 or a correlated ~30–32% notebook merely to chase the aggregate score.

Experiment: `experiments/E0001_20260825_n1_arc2_vanilla_exact.md`.

## E0006 — Lightning + NVIDIA NVARC feasibility — NEXT HIGH-INFORMATION GPU GATE

Purpose: determine whether Nemotron 3.5 Lightning can be deployed competition-validly on Kaggle **L4 x4** and whether the public NVIDIA ARC environment is worth a frozen-development experiment.

Preferred checkpoint:
- `nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4`;
- L4 should use the supported W4A16 fallback execution path rather than native Blackwell NVFP4 arithmetic.

BF16 remains a fallback/reference, not the first attachment attempt.

This is **not a competition submission**. It should not consume leaderboard quota.

### Gate A — inspect only — CURRENT

1. Import `notebooks/E0006_lightning_gate_a_kaggle.ipynb`.
2. Attach the preferred NVFP4 Lightning checkpoint as a Kaggle Model/Input using the lowest-friction HF→Kaggle path.
3. GPU **L4 x4**; Internet **OFF**.
4. `Save Version -> Save & Run All`.
5. Return `/kaggle/working/e0006_gate_a_inspect.json`.

PASS requires environment/model attachment only. It does not prove the model loads.

### Gate B — one bounded model load + one short generation — PREPARED

Only after Gate A is reviewed and compatible.

Standalone notebook:
`notebooks/E0006_lightning_gate_b_kaggle.ipynb`

It reuses the same attached checkpoint, auto-detects the NVFP4 ModelOpt quantization path, attempts TP4 vLLM load, performs one short local generation, records startup/runtime/GPU memory, writes JSON/log, then terminates the server.

PASS requires a TP4 model load and one local generation without OOM/unsupported-kernel failure, with startup/runtime/memory evidence captured.

Stop rule: one compatibility round plus one bounded mechanical fix round maximum.

### Gate C — development ablation

Only after a viable Gate B. Compare source-faithful:
- transductive direct-grid output;
- inductive executable `transform(grid)` output;

on the frozen **development** split only, with equal candidate/token/runtime budgets. Validation/heldout remain sealed.

## N2 — correlated TRM/NVARC notebook — CONDITIONAL

Public evidence around **31.11**. Skip by default now that N1 is complete. Launch only if it answers a concrete complementarity/provenance question or exposes useful candidate artifacts.

## N0 — BlackCat — RETIRED FALLBACK

N1 validated the end-to-end Kaggle path. N0 is no longer useful unless a future environment regression specifically requires a simpler public anchor.

## C0 — CompressARC / MDL — RETAIN AS DISTINCT REFERENCE, NO ROUTINE RUN

Methodologically useful, but current artifact provenance does not match the 2026 public evaluation set closely enough to justify a user-side leaderboard run in M1.

## User-side evidence

For E0006 we prefer machine-readable smoke artifacts over screenshots. A screenshot is enough only for a UI/setup failure. Target files:
- Gate A: `e0006_gate_a_inspect.json`;
- Gate B: `e0006_gate_b_smoke.json`;
- Gate B: `e0006_gate_b_vllm.log`.
