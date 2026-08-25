# M1 Prior-Art / Novelty Boundaries

Snapshot: 2026-08-25
Status: literature boundary map only; no original competitive mechanism is disclosed here.

## Purpose

The ARC Prize Paper rubric explicitly scores **Novelty**, while the 2025 literature already contains many ideas that sound novel when described at a high level. This file exists to prevent us from accidentally rediscovering a known idea, overstating a contribution, or optimizing a mechanism before checking its closest prior art.

The rule is strict:

> A useful engineering combination is not automatically a novel scientific contribution.

Our eventual paper may use known ingredients. Novelty, if any, must be attached to a specific mechanism, theory, or empirical result that survives a closest-prior comparison and controlled ablation.

## Public ideas that are already established

### 1. Test-time training / task-specific weight adaptation

Already established by the ARChitects lineage and central to the 2024–2025 top-score systems. NVARC's 2025 winner used an improved Qwen/ARChitects task-time-adaptation pipeline.

**Do not claim novelty for:** fine-tuning a pretrained model separately on each puzzle's demonstrations.

### 2. Synthetic curricula for ARC

NVARC used large-scale synthetic puzzle generation and augmentation as a major source of performance.

**Do not claim novelty for:** synthetic ARC data, program-generated training tasks, or augmentation at scale by themselves.

### 3. Recursive neural refinement

TRM/HRM-style systems refine answer and/or latent state recurrently. TRM won the 2025 Paper Prize and demonstrated strong ARC performance with a very small network.

**Do not claim novelty for:** a recurrent network simply because it repeatedly rewrites a latent state or output canvas.

### 4. Per-puzzle learning from scratch / zero-pretraining refinement

CompressARC trains a fresh model for each puzzle under an MDL/compression framing. TRM-related work also shows small-network refinement regimes.

**Do not claim novelty for:** initializing a small network per task and optimizing it only from the visible examples.

### 5. MDL / compression objectives

CompressARC explicitly treats ARC as neural code golf / minimum-description-length optimization.

**Do not claim novelty for:** using compression, description length, simplicity penalties, or short programs as the sole claimed new idea.

### 6. Evolutionary program synthesis and iterative program repair

SOAR, Berman, Pang and related 2025 work use repeated program generation/mutation, execution, verification and refinement. The ARC Prize 2025 technical report identifies the **refinement loop** as the defining theme of the year.

**Do not claim novelty for:** generator-verifier loops, repeated Python-program repair, evolutionary search, self-improvement from search traces, or “refine until demonstrations pass” in the abstract.

### 7. 2D-aware masked diffusion and recursive self-refinement

The 2025 ARChitects system used a 2D-aware masked-diffusion language model with recursive self-refinement and perspective-based scoring.

**Do not claim novelty for:** iterative masked-grid denoising/refinement or perspective scoring at a generic level.

### 8. Multi-view / perspective ensembles

ARC systems already use rotations, transpositions, color permutations, perspective transforms and augmentation-based rescoring. Product-of-Experts work explicitly studies perspective diversity.

**Do not claim novelty for:** adding geometric/color views, voting across views, or rescoring the same candidate under multiple augmentations.

### 9. Candidate pools, rescoring and two-attempt selection

NVARC/Qwen systems generate more candidates than they submit and rank them into ARC's two allowed attempts. NVARC's own analysis showed that a candidate source can contain unique exact solves yet add little final score when the selector drops them.

**Do not claim novelty for:** generating many candidates, selecting top two, frequency voting, likelihood rescoring, or merely choosing diverse attempts.

### 10. Neuro-symbolic and object/compositional reasoning

2025 honorable-mention work explicitly explored neuro-symbolic architectures for compositional ARC reasoning, and a large broader literature uses objects, components, relations and executable transformations.

**Do not claim novelty for:** adding connected components, object graphs, symbolic transformations or a neural+symbolic hybrid at the category level.

### 11. Visual-representation emphasis

2025 work such as `ARC-AGI is a Vision Problem!` and video/visual-pretraining approaches already challenge purely token-centric framing.

**Do not claim novelty for:** treating ARC as vision, using visual encoders, or adding spatial inductive bias by itself.

## 2026 high-capability warning

Hosted 2026 systems such as Confluence and Imbue show very strong ARC-AGI-2 results from repeated executable-program refinement using online frontier models and external sandboxes. They are not directly Kaggle-valid, but they sharply narrow our novelty space.

Therefore the current project question — compressing the benefit of a refinement loop into a self-contained offline Kaggle solver — is a **research problem**, not itself a novelty claim.

## What could eventually qualify as novelty

A future candidate contribution must be stated at mechanism level, for example:

- a particular way of representing, proposing, verifying or revising hypotheses;
- a specific learned/search interface that changes candidate discovery efficiency;
- a principled method for allocating test-time compute across tasks/hypotheses;
- a selection/diversity mechanism with a defensible theory and causal evidence;
- a new empirical finding about when/why a refinement mechanism generalizes.

The examples above are categories, not endorsements of any particular direction.

## Closest-prior gate before original implementation

Before the first genuinely original mechanism is committed, create a private/internal comparison containing:

1. one-sentence mechanism claim;
2. the three closest public methods, not merely the most famous methods;
3. exact similarities and differences;
4. which difference is expected to cause improvement and why;
5. falsifiable experiment;
6. compute-matched control;
7. minimum ablation needed to attribute the effect;
8. what result would make us withdraw the novelty claim.

If we cannot write this cleanly, the idea is not ready for a Paper Prize novelty claim.

## Novelty evidence standard

For a final paper claim, aim to have all of:

- **source evidence:** closest prior implementations/papers cited accurately;
- **mechanism isolation:** remove/replace the proposed component and measure the effect;
- **generalization:** effect appears outside the continuously tuned development slice;
- **compute control:** improvement is not explained only by more search time/model calls;
- **failure analysis:** document where the mechanism does not help;
- **reproducibility:** enough detail/code to reproduce after the required open-source window.

A leaderboard gain without these controls can still be valuable for the Progress Prize, but it should not automatically be presented as scientific novelty.

## Primary sources for this boundary map

- ARC Prize 2025 Technical Report: https://arxiv.org/html/2601.10904
- NVARC: https://github.com/1ytic/NVARC
- Tiny Recursive Models: https://github.com/SamsungSAILMontreal/TinyRecursiveModels
- SOAR: https://github.com/flowersteam/SOAR
- CompressARC: https://github.com/iliao2345/CompressARC
- 2026 public Qwen mirror: https://github.com/MA-Zbida/arc2026-kaggle

This list is a starting boundary, not a claim of exhaustive literature coverage. It must be refreshed immediately before any novelty claim is frozen.
