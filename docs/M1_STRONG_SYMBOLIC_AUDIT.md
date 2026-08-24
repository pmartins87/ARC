# M1 Strong Symbolic / Program-Synthesis Audit

Snapshot: 2026-08-24

## Why this audit exists

S0 established that a shallow one-step DSL is not a serious ARC-AGI-2 evaluation solver: it fitted zero exact hypotheses on the frozen 60-task development split. M1 therefore needs a stronger reference without turning baseline reproduction into an open-ended research project.

## Candidate A — CompressARC

Repository: `iliao2345/CompressARC`

Facts verified from the public project:
- MIT licensed;
- dependency surface is small (`torch`, `numpy`, `matplotlib`, `tqdm`);
- trains a fresh model on a single puzzle rather than relying on pretrained ARC data;
- public README example runs 1,500 training steps for one task;
- ARC Prize 2025 reports the method at roughly **4% ARC-AGI-2**, while its main value is the MDL/single-puzzle learning idea rather than raw competition score.

### M1 decision

**SELECT as the preferred serious symbolic/MDL reference family.**

A full 120-task reproduction is not required inside M1 if it would consume the timebox. We need enough reproduction evidence to understand the execution path, cost envelope and solved-task coverage. If full evaluation is not practical by 2026-09-02, record it as `PARTIAL` and advance.

## Candidate B — SOAR / Trelis ARC-AGI framework

Repository: `TrelisResearch/arc-agi-2025`

The current public framework is materially heavier:
- designed around an LLM generating/evolving Python programs;
- quick-start examples call an OpenAI-style endpoint or launch Runpod GPUs;
- dependency set includes model-serving/API/cloud infrastructure;
- the ARC Prize 2025 paper result is scientifically important, but the original execution path is not directly compatible with the final Kaggle no-internet environment.

### M1 decision

**REFERENCE, not primary reproduction target.**

Its evolutionary refinement/search ideas remain important for later offline adaptation, especially M4/M5, but a faithful M1 reproduction would introduce external endpoint/Runpod infrastructure that does not directly prove competition-valid execution.

## Candidate C — ARC-MDL

Repository: `sebferre/ARC-MDL`

Facts:
- explicit MDL search over descriptive grid models;
- interpretable parse/generation models;
- GPLv3;
- OCaml toolchain plus project-specific libraries.

### M1 decision

**CONCEPTUAL REFERENCE only.**

Useful for MDL/search design, but lower reproduction leverage than CompressARC for our Python/Kaggle pipeline.

## M1 bounded plan

1. Keep S0 as the dependency-light lower bound and regression harness.
2. Use CompressARC as the serious MDL/program-learning reproduction target.
3. Do not duplicate SOAR infrastructure in M1.
4. Neural/NVARC B0 and B1 remain higher priority because the competition frontier is currently around 31% and our eventual prize system will need to improve on that frontier.
5. Close M1 on 2026-09-02 even if CompressARC reproduction is `PARTIAL`; preserve evidence and move to M2 rather than consuming the project schedule.

## Forward-looking architecture implication

The three families suggest a useful separation for later milestones:
- **NVARC/TRM/Qwen:** strong learned prior / direct prediction;
- **CompressARC/MDL:** puzzle-specific adaptation and simplicity pressure;
- **SOAR-style refinement:** generate, execute, verify and improve candidate programs.

This is not yet our novel architecture. It is a source-grounded map of components that later ablations may justify combining.
