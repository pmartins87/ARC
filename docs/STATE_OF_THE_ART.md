# State of the Art Map — ARC-AGI-2

Snapshot updated 2026-08-24. Reported scores belong to their cited authors unless explicitly reproduced in this repository.

## Comparability rule

Every score must be labeled by:
- dataset: training / public evaluation / semi-private / Kaggle public / Kaggle private;
- pass@1 or pass@2 where known;
- hardware/runtime;
- internet/API availability;
- whether the result is ours or third-party reported.

A hosted-agent 95% public-evaluation result and a 30% offline Kaggle score are different engineering regimes and must not be treated as directly comparable.

## Competition-comparable reference: ARC Prize 2025

ARC Prize reported 1,455 teams and 15,154 submissions in 2025. The winning private ARC-AGI-2 score was 24.03% under the competition constraints.

### NVARC — 2025 high-score winner

Architecture:
- multi-stage synthetic data generation;
- improved ARChitects/Qwen3 4B task-time adaptation;
- improved Tiny Recursive Models;
- ensemble/candidate selection.

NVARC's public repository describes roughly 103k synthetic puzzles and 3.2M augmented puzzles. The important 2025 lesson is not simply “add TRM”: the team reported cases where TRM had non-zero standalone accuracy but added little to a strong Qwen run because solved-task overlap and candidate selection limited marginal value.

**Implication for this project:** measure exact complementarity, second-attempt rescues and oracle-union gain before keeping an ensemble member.

Sources:
- https://arcprize.org/blog/arc-prize-2025-results-analysis
- https://github.com/1ytic/NVARC

### ARChitects — 2025 second place

ARC Prize describes a 2D-aware masked-diffusion language-model approach with recursive self-refinement and perspective-based scoring.

Key lesson: iterative refinement and candidate scoring matter; ARC output generation need not be a one-shot autoregressive decode.

Source:
- https://arcprize.org/blog/arc-prize-2025-results-analysis

### MindsAI — 2025 third place

Test-time fine-tuning, augmentation ensembles, tokenizer dropout and pretraining improvements.

Key lesson: task-time adaptation remains competitive, but the value of each added component must be measured against the fixed Kaggle runtime/memory budget.

Source:
- https://arcprize.org/blog/arc-prize-2025-results-analysis

## 2025 Paper Prize lines

### Tiny Recursive Model (TRM)

Paper Prize 1st place. ARC Prize reports a roughly 7M-parameter recursive model with iterative latent/answer refinement.

The NVARC reproduction material shows that serious ARC-AGI-2 TRM use is not “tiny compute”: their pretraining used a large augmented corpus and multi-H100 training, while competition-time adaptation was engineered for four GPUs.

Sources:
- https://arcprize.org/blog/arc-prize-2025-results-analysis
- https://github.com/SamsungSAILMontreal/TinyRecursiveModels
- https://github.com/1ytic/NVARC

### SOAR

Paper Prize 2nd place. Evolutionary program synthesis in which an LLM proposes and refines executable Python programs using search feedback.

Key lesson: the program space itself can be searched/refined rather than relying on a fixed hand-written shallow DSL.

Current Trelis reproduction infrastructure uses external OpenAI-style model endpoints and/or Runpod, so it is a scientific reference rather than a directly Kaggle-offline M1 baseline.

Sources:
- https://github.com/flowersteam/SOAR
- https://github.com/TrelisResearch/arc-agi-2025

### CompressARC

Paper Prize 3rd place. Per-puzzle learning from scratch with an MDL/compression framing and no cross-task pretraining.

The public implementation is MIT licensed, trains a fresh model per puzzle, and has a historical L4 x4 Kaggle template. Its reported ARC-AGI-2 scores are far below the current ~31% offline neural frontier, but its puzzle-specific adaptation/compression mechanism is materially different and therefore useful as a complementarity reference.

Source:
- https://github.com/iliao2345/CompressARC

## 2026 competition-valid public frontier

At the 2026-08-24 Kaggle Code snapshot:
- `ARC2 vanilla exact`: **31.39** public score;
- `ARC 2026 NVARC TRM Evidence Cost V1`: **31.11**;
- `ARC 2026 NVARC TRM Aggressive Cost Order`: **31.11**;
- `ARC AGI2 Minimal Augmentation Specialist`: **28.89**.

These notebooks run under the actual no-internet Kaggle competition regime and are therefore more relevant to prize engineering than much higher API-hosted public-evaluation numbers.

Current project target N1 is an unchanged reproduction of `ARC2 vanilla exact`; no reported public score is counted as ours until reproduced.

Source:
- https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/code

## 2026 frontier reasoning capability outside the Kaggle sandbox

### Gemini 3.7 Flash

ARC Prize reports **84.6% ARC-AGI-2 Semi-Private** at high effort, with lower-effort settings also far above the current Kaggle public-code frontier.

This demonstrates that the scientific capability to solve ARC-AGI-2 has advanced much faster than what can currently be packaged into the self-contained competition notebook.

Source:
- ARC Prize verified model results / Gemini 3.7 Flash announcement

### Confluence Labs iterative program synthesis

The public Confluence system reports **97.92%** on the 120-task public evaluation set using multiple Gemini agents, repeated refinement and external sandbox execution.

Its published reproduction path uses Gemini API access and E2B sandboxes, so it is **not competition-valid as-is**. It is nevertheless strong evidence that iterative executable-program refinement can close a large part of the ARC gap when inference resources are abundant.

Source:
- https://github.com/confluence-labs/arc-agi-2

### Imbue code evolution

Imbue reports the same evolutionary code framework improving several base models on public ARC-AGI-2, including approximately:
- Kimi K2.5: 12.1% -> 34.0%;
- Gemini 3 Flash: 34.0% -> 61.4%;
- Gemini 3.1 Pro: 88.1% -> 95.1%.

The important mechanism is repeated generation/mutation/execution/selection of Python solutions, with fitness dominated by demonstration correctness and augmented by transfer/simplicity signals.

Again, online LLM inference makes the published path non-Kaggle-valid, but the refinement-loop effect is directly relevant to later offline architecture design.

Source:
- Imbue ARC-AGI-2 code-evolution research, 2026

## 2026 open-weight frontier and hardware reality

### Inkling-Small

ARC Prize reports **40.1% ARC-AGI-2 Semi-Private**, a strong open-weight result.

The official model is a 276B-total / 12B-active MoE. Thinking Machines states approximate aggregate VRAM requirements of at least:
- ~600 GB for BF16;
- ~180 GB for NVFP4.

ARC Prize 2026 Kaggle L4 x4 exposes roughly 96 GB aggregate VRAM. Therefore the official Inkling-Small checkpoints are **not a direct competition-fit path**. A future community quantization/offload variant would need ARC accuracy and runtime validation before it deserves project time.

Sources:
- ARC Prize verified model results
- Thinking Machines Inkling-Small model card

## Current direct-grid caution: VRM V1.1

`quyen123ab/VRM` is a 2026 audited research artifact exploring recurrent output-canvas rewriting with direct cross-attention to support demonstrations.

Reported probe results include:
- substantial training-task shape capacity;
- **0.00% exact decoded grids on unseen episodes** in the declared V1.1 capacity probe;
- support-path dependence on training tasks but no detected transferable support-mapping use on unseen tasks.

The associated CompressARC audit found pairing-sensitive behavior and a bounded 3/10 exact-grid readout under its local protocol, while carefully refusing to promote this into a benchmark solver claim.

**Implication:** simply giving a recurrent neural state direct access to support pairs is not evidence that the model learns the support input-output transformation. Later architecture work needs causal/ablation checks, not only a higher training fit.

Source:
- https://github.com/quyen123ab/VRM

## What the evidence says about promising directions

The project should test, rather than assume, a competition-fit combination of:
1. a learned prior small enough for L4 x4;
2. puzzle-specific adaptation or search;
3. generation of verifiable hypotheses/programs rather than only one-shot pixels;
4. exact execution against all demonstrations as a hard constraint or strong scoring signal;
5. iterative refinement with strict runtime allocation;
6. deliberate use of ARC's second attempt for genuinely different hypotheses;
7. ensemble/routing decisions based on measured unique wins, not standalone score alone.

None of these ingredients is individually novel. Potential Paper Track novelty must be a specific mechanism, theory or empirical result supported by controlled ablations.

## M1 reproduction order after evidence update

1. infrastructure/scorer — DONE;
2. shallow symbolic S0 — measured 0.0%, REJECT as serious standalone solver;
3. **N1 `ARC2 vanilla exact` ~31.39 public frontier — next external gate**;
4. one controlled NVARC/TRM comparison after N1;
5. bounded CompressARC/MDL reference C0 if it remains clean within the M1 timebox;
6. complementarity/error map;
7. freeze the first evidence-based original hypothesis and trigger repository-visibility review.

## Competitive thesis for later milestones

The current gap is no longer well described as “invent enough primitive transformations.” Strong hosted systems show the value of iterative program refinement, while the Kaggle competition forbids the APIs that make those systems easy to deploy. The high-value research question is therefore:

> **How much of the refinement-loop advantage can be compressed into a self-contained, offline, <12-hour L4 x4 solver without sacrificing generalization?**

This is a research direction, not yet our novelty claim. M1 must first establish the competition-valid baseline and error evidence.
