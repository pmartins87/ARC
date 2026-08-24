# ARC-AGI-2 2026 Frontier — What Matters for Our Prize Strategy

Snapshot: 2026-08-24

This document separates **benchmark capability** from **Kaggle-eligible execution**. High public/semiprivate ARC scores do not automatically translate into a legal ARC Prize 2026 submission because the competition reruns one self-contained notebook with no internet and a fixed compute budget.

## 1. Frontier reasoning models are no longer the main scientific bottleneck

ARC Prize's verified result page reports Gemini 3.7 Flash at:
- 84.6% ARC-AGI-2 Semi-Private at high effort;
- 63.7% at medium effort;
- 52.9% at low effort.

This is far above the current public Kaggle notebook frontier (~31%). The competition gap is therefore increasingly about **how much capable reasoning can be packaged into the allowed offline notebook**, not whether modern models can conceptually solve ARC-AGI-2.

## 2. Iterative code/program refinement is extremely strong

### Confluence Labs

Public repository `confluence-labs/arc-agi-2` reports **97.92%** on the public evaluation set using a Gemini-CLI program-synthesis solver.

Published reproduction defaults:
- 12 agents per test input;
- up to 10 refinement iterations per agent;
- concurrency up to 132 sandboxes;
- 12-hour wall-clock budget;
- Gemini API + E2B sandbox keys.

This is important architectural evidence, but **not Kaggle-eligible as-is** because the evaluation notebook has no internet and cannot call Gemini/E2B.

### Imbue code evolution

Imbue reports the same evolutionary harness improving several base models on public ARC-AGI-2:
- Kimi K2.5: 12.1% -> **34.0%**;
- Gemini 3 Flash: 34.0% -> **61.4%**;
- Gemini 3.1 Pro: 88.1% -> **95.1%**.

The method represents a candidate solution as Python code, repeatedly mutates/evaluates a population, and stops when sufficiently strong solutions are found. Published fitness heavily weights demonstration correctness and also adds transfer/simplicity signals. Results use up to 16 evolution iterations.

Again, the published system depends on external LLM inference and therefore is not directly valid for the Kaggle rerun.

## 3. Open weights can exceed the current Kaggle notebook frontier — but may not fit

ARC Prize reports **Inkling-Small** at **40.1% ARC-AGI-2 Semi-Private**, currently a strong open-weight result.

However, Thinking Machines' official model card says:
- 276B total / 12B active parameters;
- BF16 requires at least ~600 GB aggregate VRAM;
- NVFP4 requires at least ~180 GB aggregate VRAM.

Our competition L4 x4 pool exposes about 96 GB aggregate VRAM. Therefore the official Inkling-Small checkpoints **do not fit the competition GPU envelope directly**. Community ultra-low-bit/offload variants may exist, but they are not yet a validated prize path and could sacrifice the reasoning quality that makes the model interesting.

## 4. Consequence for this project

The evidence changes what a high-value original contribution looks like.

Low-value direction:
- keep adding hand-written primitives to a shallow symbolic DSL;
- stack many correlated public notebooks;
- try to fit a frontier 180+ GB model into a 96 GB environment by brute force without proving preserved ARC accuracy.

High-value direction to test later:
- retain a small/medium competition-fit learned prior (NVARC/TRM/Qwen family or successor);
- make it **generate/refine verifiable hypotheses or programs**, not merely one-shot pixels;
- use exact demonstration execution as a hard verifier;
- allocate inference-time search adaptively by task difficulty;
- preserve diversity for ARC's second attempt;
- distill insights from expensive/online frontier methods into a self-contained offline procedure.

This is **not yet a claim of novelty or our frozen architecture**. It is a source-grounded design pressure to revisit after M1 reproduces the competition-valid neural frontier.

## 5. Research gates created by this frontier

Before any novel implementation:
1. reproduce N1 (~31% public Kaggle frontier);
2. inventory its model/resources/runtime headroom;
3. determine whether it already performs test-time refinement/program search;
4. measure where a bounded MDL/program-learning reference differs;
5. only then freeze an original hypothesis and trigger the repository-visibility decision.

The prize target is not to reproduce 97.9% online. It is to capture as much of the **refinement-loop advantage** as possible inside the Kaggle sandbox.
