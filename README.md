# ARC Prize 2026 Research Project

Research and competition repository for the **ARC Prize 2026 — ARC-AGI-2** and the linked **Paper Track**.

## Primary objective

Maximize the probability of earning a monetary prize in ARC Prize 2026 while preserving scientific rigor, reproducibility, and competition-rule compliance.

## Tracks

- **ARC-AGI-2:** primary competitive track.
- **Paper Track:** second prize path using the same research, experiments, and code.

## Working principles

1. **Source-first:** distinguish official ARC/Kaggle facts from our own hypotheses.
2. **No evaluation leakage:** public evaluation tasks are treated as a sealed benchmark for architecture decisions.
3. **Measured progress:** every material change must be evaluated against fixed validation/held-out splits.
4. **Reproducibility:** configs, seeds, scores, runtimes, hardware, and commit SHA are recorded for meaningful experiments.
5. **Ablations before claims:** scientific claims require controlled comparisons.
6. **Prize-oriented engineering:** optimize for exact-task accuracy under Kaggle compute/runtime limits, not elegance alone.
7. **Open-source readiness:** prize-eligible artifacts must be publishable and reproducible.

## Initial research direction

The first hypothesis family is a hybrid verified-reasoning solver that combines:

- pixel/grid representation;
- object/relation representation;
- short program synthesis over a compact DSL;
- exact verification against all demonstrations;
- deliberate diversity between the two allowed test attempts;
- learned or heuristic search guidance only when it produces measurable gains.

This is a **research hypothesis, not yet a novelty claim**. Prior work from ARC Prize 2025 already includes test-time training, recursive refinement, evolutionary program synthesis, MDL-style approaches, and neuro-symbolic systems. Novelty must be established empirically and against the literature.

## Repository map

- `docs/STATUS.md` — current project state and next gate.
- `docs/ROADMAP.md` — competition-oriented milestones.
- `docs/RESEARCH_PROTOCOL.md` — leakage controls, split policy, metrics, and experiment rules.
- `docs/STATE_OF_THE_ART.md` — source-backed prior-art map.
- `experiments/README.md` — experiment ledger format.
- `src/` — solver code (introduced after baseline audit).

## External official sources

- ARC Prize 2026 ARC-AGI-2: https://arcprize.org/competitions/2026/arc-agi-2
- ARC Prize 2026 Paper Prize: https://arcprize.org/competitions/2026/paper
- ARC-AGI-2 dataset: https://github.com/arcprize/ARC-AGI-2

## Status

Repository initialized on 2026-08-24. Baseline/state-of-the-art audit is the active gate before implementation.
