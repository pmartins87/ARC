# State of the Art Map — ARC-AGI-2

Snapshot updated 2026-08-25. Reported scores belong to their cited authors unless explicitly reproduced in this repository.

## Comparability rule

Every score must be labeled by:
- dataset: training / public evaluation / semi-private / Kaggle public leaderboard / Kaggle final-private;
- pass@1 or pass@2 where known;
- hardware/runtime;
- internet/API availability;
- whether the result is ours or third-party reported;
- whether code is public and reproducible under the 2026 competition sandbox.

Three frontiers must remain separate:

1. **public-code Kaggle frontier** — inspectable/copyable notebooks, currently around 31%;
2. **live Kaggle competition frontier** — private team methods, currently above 70%;
3. **hosted/verified capability frontier** — API/agent systems that can exceed 80–90% but are not directly competition-valid.

A 95% hosted public-evaluation result, a 72% live no-internet competition score and a 31% public notebook are different evidence regimes.

## Competition-comparable reference: ARC Prize 2025

ARC Prize reported 1,455 teams and 15,154 submissions in 2025. The winning private ARC-AGI-2 score was 24.03% under the competition constraints.

### NVARC — 2025 high-score winner

Architecture:
- multi-stage synthetic data generation;
- improved ARChitects/Qwen3 4B task-time adaptation;
- improved Tiny Recursive Models;
- ensemble/candidate selection.

NVARC's public repository describes roughly 103k synthetic puzzles and 3.2M augmented puzzles. The important 2025 lesson is not simply “add TRM”: the team reported cases where TRM had non-zero standalone accuracy but added little to a strong Qwen run because solved-task overlap and candidate selection limited marginal value.

**Implication:** measure exact complementarity, second-attempt rescues and oracle-union gain before keeping an ensemble member.

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

Current public reproductions use external OpenAI-style endpoints and/or Runpod, so SOAR is a scientific reference rather than a directly Kaggle-offline M1 baseline.

Sources:
- https://github.com/flowersteam/SOAR
- https://github.com/TrelisResearch/arc-agi-2025

### CompressARC

Paper Prize 3rd place. Per-puzzle learning from scratch with an MDL/compression framing and no cross-task pretraining.

The public implementation is MIT licensed, trains a fresh model per puzzle, and has a historical L4 x4 Kaggle template. Its historical ARC-AGI-2 scores are far below the current public-code Qwen frontier, but its puzzle-specific adaptation/compression mechanism is materially different and therefore useful as a complementarity reference.

Source:
- https://github.com/iliao2345/CompressARC

## 2026 public-code Kaggle frontier

At the 2026-08-24/25 Kaggle Code snapshot:
- `ARC2 vanilla exact`: **31.39** public score;
- `ARC 2026 NVARC TRM Evidence Cost V1`: **31.11**;
- `ARC 2026 NVARC TRM Aggressive Cost Order`: **31.11**;
- `ARC2 champion E48`: **29.86**;
- `ARC-AGI-2 Public Frontier Perfpatch Evidence Lab`: **29.03**;
- `ARC AGI2 Minimal Augmentation Specialist`: **28.89**.

These notebooks are valuable because they expose inspectable competition-fit code/resources. They should be described as the **public-code frontier**, not the live competition frontier.

Current project N1 is an unchanged reproduction of `ARC2 vanilla exact`; no source score is counted as ours until our hidden rerun returns.

Source:
- https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/code

## 2026 live Kaggle competition frontier

Fresh ARC Prize public updates on 2026-08-25 report:

- **nvbanana — 72.08%** current high score;
- **rabbithole — 70.42%** current second place, up from 50.42% over the preceding weekend.

ARC Prize President Greg Kamradt publicly described the race as nvbanana appearing locked around 72% before rabbithole jumped roughly +20 percentage points, and suggested that multiple teams might reach 85%.

This is the key competitive reset for our project. A 31.39% public notebook is a reproduction anchor, not a near-prize frontier. A 35–40% result would be meaningful progress relative to public baselines but, based on the current live leaders, should not be presented as a realistic prize target by itself.

The exact current **8th-place score is not yet verified** in this repository. Do not infer or invent it.

Sources captured 2026-08-25:
- https://ngntipkolamrenang.twstalker.com/arcprize
- https://instalker.org/GregKamradt
- https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/leaderboard

## Competition hidden-set regime

Kaggle states that submitted notebooks are rerun on **240 unseen tasks**. Most have one test input; a small number have two. The public leaderboard uses approximately half the hidden test data and final standings use the other half.

This means a large live score cannot be explained away as merely fitting the visible 120 public evaluation tasks. It is evidence of strong competition-fit generalization, although final/private rank can still differ from public rank.

Source:
- https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/data

## 2026 hosted / verified capability outside the Kaggle sandbox

### Frontier models

ARC Prize's verified model/harness results now include systems far beyond the public-code Kaggle baseline. These demonstrate raw ARC capability but may rely on online APIs, different inference budgets or hardware and must not be conflated with Kaggle competition scores.

### Confluence Labs iterative program synthesis

The public Confluence system reports **97.92%** on the 120-task public evaluation set using multiple Gemini agents, repeated refinement and external sandbox execution.

Its published reproduction path uses Gemini API access and E2B sandboxes, so it is **not competition-valid as-is**. It remains evidence that executable hypothesis/program search can close a large part of the ARC gap when inference resources are abundant.

Source:
- https://github.com/confluence-labs/arc-agi-2

### Imbue code evolution

Imbue reports the same evolutionary harness improving several base models on public ARC-AGI-2, including approximately:
- Kimi K2.5: 12.1% -> 34.0%;
- Gemini 3 Flash: 34.0% -> 61.4%;
- Gemini 3.1 Pro: 88.1% -> 95.1%.

The method represents a candidate solution as Python code, repeatedly mutates/evaluates a population, and uses demonstration correctness plus transfer/simplicity signals.

Online LLM inference makes the published path non-Kaggle-valid, but the search/refinement effect is scientifically relevant.

## Johan Land 2026 — diversity + holistic trace judging

Paper: **Modality-Driven Search with Holistic Trace Judging for ARC-AGI-2** (2026).

Reported results:
- **72.9%** ARC-AGI-2 semi-private at **$38.99/task**;
- **76.1%** public evaluation at **$19.69/task**.

Public solver description uses:
- independent candidate generation across text, image and code modalities;
- long-horizon/multi-step reasoning;
- agentic code generation/execution;
- multiple frontier models;
- logic and consistency judges;
- holistic comparison of complete reasoning traces.

The paper's most important negative result for our project is that **prescriptive prompting templates and iterative refinement systematically reduced hypothesis diversity and degraded performance** in the tested setting. The correct answer can be a minority hypothesis, making majority/frequency alone a weak selector.

This updates the 2025 “refinement loop” lesson:

> refinement can be powerful, but preserving independent hypotheses and selecting minority-correct candidates can be equally important.

The published system is not directly Kaggle-valid because it relies on frontier APIs and far greater cost. Its mechanisms are also now **prior art**: modality-driven candidate diversity and holistic trace judging cannot later be claimed as our novelty at a broad level.

Sources:
- https://arxiv.org/abs/2606.31543
- https://github.com/beetree/ARC-AGI

## 2026 open-weight / hardware reality

Some strong open-weight systems exceed the public-code baseline but official checkpoints may require substantially more memory than 4xL4. Earlier audits found examples requiring more aggregate VRAM than Kaggle provides.

The 70%+ live competition scores change the interpretation: the main question is no longer whether 4xL4 can support strong performance in principle. It demonstrably can. The unresolved question is which efficient combination of learned prior, adaptation/search, representation, candidate generation, selection and runtime allocation produces that performance.

Community speculation about the leaders' exact models/resources is not accepted as evidence until it comes from the teams or reproducible artifacts.

## Current direct-grid caution: VRM V1.1

`quyen123ab/VRM` explores recurrent output-canvas rewriting with direct cross-attention to support demonstrations.

Reported probe results include:
- substantial training-task shape capacity;
- **0.00% exact decoded grids on unseen episodes** in its declared V1.1 capacity probe;
- support-path dependence on training tasks but no detected transferable support-mapping use on unseen tasks.

**Implication:** simply giving a recurrent neural state direct access to support pairs is not evidence that the model learns the support input-output transformation. Architecture work needs causal/ablation checks, not only higher training fit.

Source:
- https://github.com/quyen123ab/VRM

## What the evidence now says about promising directions

The project should test, not assume:

1. a competition-fit learned prior;
2. puzzle-specific adaptation/search;
3. rich candidate generation rather than only one-shot pixels;
4. verification against all demonstrations;
5. refinement that does **not collapse hypothesis diversity**;
6. deliberate use of the second attempt for genuinely distinct, evidence-supported hypotheses;
7. selector/routing decisions based on unique exact wins and candidate-pool oracle gaps, not frequency alone;
8. runtime allocation that increases coverage without being mislabeled as reasoning progress.

None of these categories is individually novel. Paper Prize novelty must come from a specific mechanism/theory/result supported by controlled ablations and closest-prior comparison.

## Revised M1 order

1. infrastructure/scorer — DONE;
2. shallow symbolic S0 — 0.0%, REJECT standalone;
3. N1 `ARC2 vanilla exact` — hidden competition rerun ACTIVE;
4. candidate-pool / selector / runtime / provenance instrumentation — DONE at infrastructure level;
5. one controlled alternative only if it yields task/candidate information, not merely another leaderboard score;
6. retrieve/track credible public evidence from 70%+ competition teams as it becomes available;
7. close M1 PASS/PARTIAL by 2026-09-02;
8. score M2 hypotheses by step-change leverage, attribution, Kaggle fit, information/run and Paper value;
9. trigger visibility gate before original competitive implementation.

## Competitive thesis — provisional, not novelty

The gap is no longer adequately described as “add more primitive transformations” or simply “add iterative refinement.” The stronger provisional research question is:

> **How can an offline 4xL4 solver generate and evaluate sufficiently diverse, verifiable hypotheses under a hard runtime and two-attempt budget without collapsing onto the same wrong mode?**

This is a design pressure, not our frozen method and not a novelty claim. N1 and candidate/runtime evidence still determine which bottleneck M2 should attack first.
