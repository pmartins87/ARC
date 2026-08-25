# ARC Prize 2026 Paper — Evidence-First Outline

Status: scaffold only; no unsupported novelty claims.

## Working title

TBD after M3. Do not name a mechanism before evidence supports it.

## Abstract

Fill only after the final contribution and quantitative effect are known.

Required content:
- problem;
- specific contribution;
- evaluation protocol;
- principal quantitative result;
- why the result matters beyond one leaderboard.

## 1. Introduction

- What ARC-AGI-2 measures.
- Why exact generalization from demonstrations remains difficult.
- Competition constraint: self-contained offline inference and only two output attempts.
- Gap addressed by our final method.
- Contributions, each tied to a result or ablation.

## 2. Prior Work

Organize by mechanism, not chronology:
- pretrained grid-language / sequence models;
- test-time adaptation;
- candidate search and rescoring;
- recursive/iterative refinement;
- symbolic / program-synthesis approaches;
- ensembles and complementary candidate sources.

For every claimed distinction record an exact source in the literature matrix.

## 3. Evaluation Protocol

- ARC-AGI-2 dataset roles.
- Frozen 60/30/30 public-evaluation development/validation/heldout protocol.
- Exact pass@1/pass@2.
- Two-attempt policy.
- No answer leakage.
- Kaggle hidden rerun as external competition evidence.
- Hardware/runtime reporting.

## 4. Baselines

- S0 compact symbolic baseline and negative result.
- N1 public Qwen/TTT frontier reproduction.
- One bounded alternative/complementary reference if M1 obtains comparable predictions.

Keep public-source baselines clearly separated from our modifications.

## 5. Method

TBD after visibility gate and M3 mechanism freeze.

Must include:
- algorithm-level description;
- candidate generation;
- verification/refinement if applicable;
- final two-attempt selection;
- runtime budget behavior;
- what is learned versus deterministic.

## 6. Results

Minimum table set:
- development / validation / heldout exact pass@2;
- Kaggle public/semi-private score where available;
- runtime and hardware;
- pass@1 versus pass@2;
- duplicate-attempt rate;
- shape-changing versus same-shape performance where meaningful.

## 7. Ablations

Each major method component needs a remove/replace/control experiment.

Priority ablations:
- candidate-generation gain versus selector gain;
- refinement iterations / stopping policy;
- diversity policy for attempt 2;
- learned guidance versus unguided search if applicable;
- compute/runtime trade-off.

## 8. Error Analysis

Separate:
- wrong output dimensions;
- correct dimensions, wrong content;
- correct candidate discovered but not selected;
- failures caused by timeouts/coverage;
- second-attempt rescues.

## 9. Theory / Interpretation

Explain why the final mechanism should generalize. Avoid retrofitted storytelling: claims must be compatible with ablations and failure cases.

## 10. Limitations

Include compute limits, benchmark-specific assumptions, remaining failure classes and uncertainty about generality.

## 11. Conclusion

State only contributions demonstrated by the experiments.

## Reproducibility Appendix

- commit/tag;
- notebook version;
- datasets/checkpoints and licenses;
- seeds;
- hardware;
- runtime;
- commands/configs;
- experiment IDs.
