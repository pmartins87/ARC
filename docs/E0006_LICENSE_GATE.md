# E0006 — model-license eligibility gate

Snapshot: 2026-08-26
Status: **OPEN / must resolve before any prize-eligible leaderboard submission that depends on these weights**.

## Why this exists

E0006 is currently a no-leaderboard feasibility experiment, so deployment can be investigated without claiming prize eligibility. If Nemotron 3.5 Lightning becomes part of an official ARC-AGI-2 submission, its model license must be checked against the competition's open-source requirements before that submission is relied on for a prize.

## Checkpoint license

`nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4` is currently published under **OpenMDW-1.1**.

OpenMDW's own current documentation describes v1.1 as a permissive model license and states that, subject to its terms, it grants unrestricted royalty-free permission to use, copy, modify and distribute Model Materials without field-of-use restrictions. Redistribution requires preserving the OpenMDW-1.1 license text plus applicable copyright/origin notices.

Therefore the mirror must retain the upstream `LICENSE` and notices exactly; the project must not relabel the weights as Apache-2.0, MIT, CC0 or another license.

## Competition-rule interaction

The current Kaggle competition rules require qualifying solutions to be open sourced and state that open-source code used in the model must satisfy the competition's licensing requirements. ARC Prize's 2026 overview also requires third-party code/methods to be available under a license that permits public sharing.

OpenMDW-1.1 appears permissive and explicitly permits redistribution/commercial use, but the project has **not established that OpenMDW-1.1 is OSI-approved**. OpenMDW's own FAQ says v1.1 is not presently on the SPDX License List and describes OSI/Open Source Definition conformance as an intended property, while public OSI discussion shows the license has been under community review.

That distinction may or may not matter for model weights under the exact competition wording. Do not guess.

## Gate rule

Before any official ARC-AGI-2 submission that materially depends on the Nemotron weights is treated as prize-eligible, obtain a grounded answer from one of these sources, in order:

1. explicit ARC Prize/Kaggle rule or organizer clarification covering third-party **model weights** under OpenMDW-1.1;
2. current OSI approval status for OpenMDW-1.1 if the rules require OSI approval for weights;
3. if ambiguity remains, ask the competition organizers publicly on the Kaggle competition forum so the answer is available to all participants and complies with the no-private-sharing spirit.

Until then classify:

- E0006 Gate A/B feasibility: **ALLOWED TO TEST**;
- development ablation using the checkpoint: **ALLOWED TO TEST**, subject to normal data rules;
- prize-eligibility assumption: **UNRESOLVED**;
- release/mirror provenance: **retain OpenMDW-1.1 license and notices**.

This gate is separate from `docs/VISIBILITY_GATE.md`.
