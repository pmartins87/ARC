# Repository Visibility Gate

Snapshot: 2026-08-25

## Current state

`pmartins87/ARC` remains **PUBLIC during M1** because current work is public-source reproduction, generic measurement infrastructure, provenance auditing and paper scaffolding.

Public visibility is useful for GitHub Actions and traceability, but it is not treated as protection for competition-sensitive ideas. A public repository can be indexed, forked and copied even with few/no followers.

## Trigger

Stop before the next public commit when any proposed change contains one or more of:

- a genuinely original competitive mechanism not already public;
- unpublished ablation evidence showing a material advantage;
- an unpublished score improvement we would not want competitors to reproduce immediately;
- a new candidate-selection/search method whose competitive value is demonstrated;
- private competition artifacts or information that should not be disclosed.

At that point the project state must explicitly say:

> **Visibility Gate atingido: não devemos publicar o próximo commit.**

## Default action after trigger

Default to private development until the competition's required open-source/writeup window, while preserving full internal provenance.

The visibility decision must never be used to hide methods beyond prize eligibility requirements. ARC Prize requires open sourcing for prize eligibility; the purpose of temporary privacy is only to avoid premature competitive disclosure during active research.

## What may remain public before the trigger

- official rules and deadline summaries;
- public literature/prior-art maps;
- reproductions of public notebooks;
- exact scorers/evaluation protocol;
- generic error/complementarity/candidate-pool tooling;
- negative results from non-novel baselines;
- paper structure and evidence requirements;
- experiment methodology that does not reveal the original mechanism.

## Re-check points

Mandatory visibility review:

1. at M1 exit before selecting/implementing the first original M2 mechanism;
2. before committing any material positive ablation from M2–M6;
3. before final open-source release / Solution Writeup / Paper submission.

## Traceability requirement

Private development must preserve the same standards as public work:

- commit history;
- experiment IDs;
- exact configs/seeds/data provenance;
- raw results where feasible;
- decisions and ablations.

Temporary privacy must not become an excuse for irreproducible research.
