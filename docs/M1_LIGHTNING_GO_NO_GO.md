# M1 — Nemotron 3.5 Lightning GO / NO-GO gate

Status: **FEASIBILITY ACTIVE — no user run yet**

Goal: decide whether Nemotron 3.5 Lightning deserves the next scarce Kaggle L4x4 experiment after N1, without confusing model fit with model accuracy.

## Gate A — public-source prerequisites

| Check | State | Evidence / rule |
|---|---|---|
| ARC-specific checkpoint relevance | PASS | Official Lightning post-training disclosure contains ARC-specific data/environment sources |
| Public ARC-native harness exists | PASS | NVIDIA NeMo Gym `nvarc` provides transductive + inductive modes |
| Exact verifier exists | PASS | Both modes use binary exact-grid reward |
| Program execution path exists | PASS | Inductive mode executes `transform(input_grid)` in sandbox |
| Model is freely/publicly available | PASS | Official Hugging Face checkpoint |
| Competition allows public external pretrained models | PASS | ARC Prize 2026 code requirements explicitly allow them |
| Model license permits use/redistribution with notices | PASS-PROVISIONAL | OpenMDW-1.1; preserve license/origin notices |
| Full NVARC train/validation dataset public | FAIL/PARTIAL | paths configured but not committed; not required for checkpoint-only inference |

## Gate B — 4xL4 deployment

| Check | State | Pass condition |
|---|---|---|
| BF16 raw weight capacity | NOT-RULED-OUT | ~62 GB model, official TP=4 reference; conservative raw shard leaves useful headroom on 24 GB ranks |
| vLLM architecture support | PASS upstream | day-0 Lightning support exists |
| TP=4 support | PASS upstream | official eval configuration validates TP=4 |
| L4/Ada startup | UNVERIFIED | model server initializes on Kaggle L4x4 without OOM/kernel failure |
| Short ARC prompt generation | UNVERIFIED | valid non-empty response under offline notebook |
| `nemotron_v3` reasoning parser | UNVERIFIED ON L4 | parser works in target runtime |
| `qwen3_coder` tool parser if used | UNVERIFIED ON L4 | tool calls parse correctly |
| Peak VRAM headroom | UNVERIFIED | enough memory remains for chosen short context/concurrency |
| Measured throughput | UNVERIFIED | compatible with hidden-run token budget plus safety margin |

A single **load/smoke notebook version** can eventually answer most Gate B items. It should not be submitted to the competition leaderboard.

## Gate C — ARC value

Run only after Gate B passes.

Frozen development comparison, same checkpoint and compute budget:
1. direct-grid/transductive baseline;
2. executable-program/inductive baseline;
3. identical task set and fixed inference budget;
4. exact pass@1/pass@2;
5. runtime/coverage;
6. attempt/candidate diversity;
7. shape/error taxonomy;
8. unique exact wins versus N1 where provenance permits comparison.

### Promotion threshold

Promote Lightning into M2 if at least one is true:
- materially stronger exact development score than N1-compatible evidence;
- substantial unique exact coverage that could complement N1;
- inductive mode gives a reproducible generalization gain at controlled compute;
- model exposes a high candidate-pool oracle with a fixable selection gap;
- clear large-step mechanism evidence worth an M2 ablation even before leaderboard superiority.

### Reject/defer threshold

Reject/defer if:
- L4x4 cannot load it reliably;
- realistic throughput cannot cover the hidden run;
- useful ARC accuracy collapses under the only deployment precision that fits;
- no meaningful exact/unique coverage appears on frozen dev;
- the next fix would require large off-platform training that cannot plausibly be reproduced before the project freeze.

## User-effort policy

Do not ask the user to upload/download tens of GB or create a new Kaggle asset until public-source work is exhausted and N1 is no longer occupying the submission pipeline. The next manual action, if needed, should be one bounded Kaggle notebook setup, not a multi-step local environment build.
