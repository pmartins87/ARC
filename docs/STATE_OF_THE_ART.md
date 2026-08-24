# State of the Art Map — ARC-AGI-2

Snapshot started 2026-08-24. Reported scores belong to their cited authors unless reproduced in this repository.

## Competition-comparable reference: ARC Prize 2025

ARC Prize reported 1,455 teams and 15,154 submissions in 2025. The winning private ARC-AGI-2 score was 24.03% under the competition constraints.

### NVARC — 2025 high-score winner

Reported architecture:
- multi-stage synthetic data generation;
- improved ARChitects-style test-time-trained Qwen3 4B component;
- improved Tiny Recursive Model components;
- ensemble across complementary systems.

Key lesson: synthetic-data scale, augmentation, task-time adaptation, and ensemble complementarity were competitive. A 2026 system should reproduce/measure this family before claiming progress.

Sources:
- https://arcprize.org/blog/arc-prize-2025-results-analysis
- https://github.com/1ytic/NVARC

### ARChitects — 2025 second place

ARC Prize describes a 2D-aware masked-diffusion language-model approach with recursive self-refinement and perspective-based scoring.

Key lesson: output generation need not be strictly autoregressive, and iterative refinement/perspective scoring can materially improve ARC behavior.

Source:
- https://arcprize.org/blog/arc-prize-2025-results-analysis

### MindsAI — 2025 third place

ARC Prize describes test-time fine-tuning, augmentation ensembles, tokenizer dropout, and pretraining improvements.

Key lesson: engineering around task-time adaptation remains strong, but gains must be weighed against Kaggle runtime and memory constraints.

Source:
- https://arcprize.org/blog/arc-prize-2025-results-analysis

## 2025 Paper Prize lines

### Tiny Recursive Model (TRM)

Paper Prize 1st place. ARC Prize reports a ~7M parameter recursive model with iterative latent/answer refinement, ~45% ARC-AGI-1 and ~8% ARC-AGI-2 in the paper setting.

Important caution: independent reproductions report that matching the published score can be difficult and compute-intensive. Do not assume the headline number is a cheap baseline.

Sources:
- https://arcprize.org/blog/arc-prize-2025-results-analysis
- https://github.com/SamsungSAILMontreal/TinyRecursiveModels

### SOAR

Paper Prize 2nd place. Evolutionary program synthesis in which an LLM learns from its own search traces and improves proposal/refinement operators.

Key lesson: program synthesis and learning can be coupled; a fixed human-written DSL is not the only path.

Source:
- https://github.com/flowersteam/SOAR

### CompressARC

Paper Prize 3rd place. Per-puzzle learning from scratch with a Minimum Description Length / compression framing and no pretraining.

Key lesson: task-specific optimization can act as a program-learning substrate, but inference cost and candidate selection matter.

Source:
- https://github.com/iliao2345/CompressARC

## Relevant 2026 public work

### Pure program synthesis

`Ag3497120/verantyx-arc-agi2` reports 74/1000 (7.4%) on the public training set using program synthesis without neural networks or LLMs.

This is useful as a symbolic reference point, but training-set coverage is not directly comparable to private competition accuracy.

Source:
- https://github.com/Ag3497120/verantyx-arc-agi2

### Hosted-agent very-high public scores

Some 2026 systems report >95% on the 120-task public evaluation using hosted frontier models, agent orchestration, APIs, and/or external sandboxes. Example: Confluence Labs reports 97.92% using Gemini CLI agents and external API/sandbox infrastructure.

These results are scientifically informative but **not directly competition-comparable** because ARC-AGI-2 Kaggle reruns require no internet and a self-contained notebook under the runtime limit.

Source:
- https://github.com/confluence-labs/arc-agi-2

### ARC-GEN

Google's ARC-GEN provides procedural generation machinery and expanded support for ARC-AGI-2 tasks. It is relevant to synthetic curricula and leakage-aware generation.

Source:
- https://github.com/google/ARC-GEN

## Current hypothesis space

The project should investigate a hybrid only after reproducing baselines:

1. multi-view perception (grid + objects/relations);
2. verified program synthesis;
3. search guidance learned from synthetic/task traces;
4. recursive refinement where it is cost-effective;
5. explicit optimization of the second allowed attempt;
6. ensemble routing based on complementary error profiles.

None of these ingredients is individually new. Potential Paper Track novelty would need to arise from a specific mechanism, demonstrated generality, or a new empirical/theoretical result.

## Baseline reproduction order

1. exact scorer/schema and trivial baseline;
2. symbolic/program-synthesis baseline;
3. public NVARC-derived Kaggle baseline compatible with 2026 hardware;
4. TRM-family baseline or inference component;
5. CompressARC/MDL baseline if runtime permits;
6. controlled hybrid experiments.

## Competitive comparability rule

Always label a reported score with:
- dataset (training/public evaluation/private/Kaggle hidden);
- pass@1 or pass@2;
- hardware/runtime;
- internet/API availability;
- whether the result is ours or reported by a third party.

A 97% hosted-API public-eval score and a 24% offline private competition score are answers to different engineering constraints and must never be compared as if they were the same benchmark setting.
