# ARC Prize 2026 — Finite Roadmap

## Mission

Build the strongest prize-eligible ARC-AGI-2 system we can before the competition deadline, and use the same research record for the ARC Prize 2026 Paper Track.

**Outcome target:** win prize money.

**Operational definition of DONE:** the project is complete when:
1. the final ARC-AGI-2 code submission has been accepted by Kaggle;
2. the exact submitted system is reproducible from a tagged commit/artifact set;
3. the required open-source/writeup obligations have been satisfied;
4. the Paper Track submission has been sent;
5. the experiment ledger and final result are archived.

Winning is the outcome target, but it is not a condition for ending research: after the final deadlines we stop active R&D, await judging, and only perform organizer/prize administration or a short postmortem.

## Hard calendar boundaries

- ARC-AGI-2 entry/team deadline: **2026-10-26 23:59 UTC**.
- ARC-AGI-2 final code deadline: **2026-11-02 23:59 UTC**.
- Paper Track deadline: **2026-11-09 23:59 UTC**.
- Winners announcement: **2026-12-04**.

There will be **no open-ended research after 2026-11-02 for ARC-AGI-2** and **no open-ended paper work after 2026-11-09**.

## Project state machine

Every status report must identify exactly one active milestone:

`M0 Foundation -> M1 Baselines -> M2 Error Map/Structural Solver -> M3 Novel Core -> M4 Pass@2 -> M5 Hybrid Guidance -> M6 Ensemble/Freeze -> M7 Final Submission -> M8 Paper/Release -> M9 Closeout`

A milestone can be `NOT_STARTED`, `ACTIVE`, `PASS`, `PARTIAL`, or `STOPPED`.

If a milestone misses its gate by its timebox, we record `PARTIAL`, keep the best working artifact, and move on. A weak phase is not allowed to consume the rest of the project.

---

## M0 — Foundation and rules freeze

**Timebox:** 2026-08-24.

**Status:** PASS.

Deliverables:
- repository/project scaffold;
- exact pass@2 scorer and schema validation;
- research/leakage protocol;
- experiment ledger contract;
- initial state-of-the-art map;
- competition mechanics/deadline snapshot.

**Gate:** scoring, schema, evaluation policy, source map, and reproducible experiment format exist and have been checked.

---

## M1 — Reproduce competitive baselines

**Timebox:** 2026-08-24 through 2026-09-02.

**Purpose:** establish the real 2026 public frontier before we spend time inventing architecture.

Required evidence:
1. B0: unchanged public NVARC-derived Kaggle anchor;
2. B1: one public ~31% frontier notebook reproduced or explained if irreproducible;
3. one TRM-family result with runtime/score recorded;
4. one symbolic/program-synthesis baseline, even if much weaker;
5. solved-task overlap and runtime table where outputs are available.

**Gate:** we have a reproducible score/runtime table with at least one serious neural baseline and one symbolic baseline, plus a clear error/complementarity map.

**Failure rule:** if a public notebook cannot be reproduced after two controlled attempts, record the blocker and move to the next baseline.

---

## M2 — Error map and structural solver

**Timebox:** 2026-09-03 through 2026-09-12.

**Purpose:** build only symbolic capabilities that attack measured baseline failures.

Candidate capabilities:
- background/color hypotheses;
- 4/8-connected components;
- object masks, bounding boxes, holes, symmetry;
- containment/adjacency/alignment relations;
- geometric and color transforms;
- crop/extraction/composition;
- line/ray/region operations;
- compact DSL and exact demonstration verifier.

**Gate:** the structural solver adds measurable held-out coverage or complementary exact solves versus M1. Mere code volume is not success.

**Stop rule:** primitives with no demonstrated coverage after controlled tests are frozen rather than endlessly expanded.

---

## M3 — Novel competitive core

**Timebox:** 2026-09-13 through 2026-09-22.

**Purpose:** test our first genuinely original hypothesis derived from M1/M2 evidence.

Possible directions include dual grid/object representations, verified program generation, refinement loops, search-budget adaptation, or another mechanism justified by the failure map.

**Gate:** at least one original mechanism shows a positive, reproducible ablation on validation/held-out data or provides a strong Paper Track result.

**Idea budget:** an idea gets at most two serious implementation/ablation cycles before KEEP / REJECT / INCONCLUSIVE. A third cycle requires specific evidence that the next test can change the decision.

---

## M4 — Two-attempt inference (pass@2)

**Timebox:** 2026-09-23 through 2026-10-02.

**Purpose:** exploit the competition's two attempts deliberately rather than returning correlated guesses.

Test:
- top-2 score ranking;
- semantic/program diversity;
- representation diversity;
- uncertainty-conditioned attempt 2;
- consensus/ensemble candidate selection.

**Gate:** credible pass@2 improvement with no material pass@1 degradation under the same evaluation protocol.

**Failure rule:** if diversity does not improve pass@2, revert to the best simple top-2 strategy and close M4.

---

## M5 — Learned guidance / hybrid refinement

**Timebox:** 2026-10-03 through 2026-10-14.

**Purpose:** use learned models only where M1-M4 telemetry shows they can guide search, ranking, or refinement.

Candidate families:
- TRM/recursive-model guidance;
- learned primitive/operator proposal;
- learned object-role prediction;
- synthetic curriculum;
- test-time refinement constrained by exact demonstration verification.

**Gate:** positive ablation against the same search/runtime budget, or a clearly complementary set of exact solves that improves an ensemble.

**Stop rule:** no large retraining project is allowed unless compute, time-to-result, and expected marginal gain are documented first.

---

## M6 — Ensemble and feature freeze

**Timebox:** 2026-10-15 through 2026-10-23.

**Purpose:** convert research components into one competition system under Kaggle constraints.

Optimize:
- solver routing;
- time allocation by difficulty;
- early stopping;
- shared cache/perception;
- candidate normalization;
- final two-attempt selection;
- runtime/VRAM margin.

**Gate:** the full offline notebook runs within the Kaggle 12-hour limit with safe margin and beats the selected M1 baseline on our strongest legitimate evaluation evidence.

**Hard freeze:** after **2026-10-23**, no new architecture family enters the final system. Only bug fixes, parameter choices already in the experiment plan, packaging, and reliability work are allowed.

---

## M7 — Prize submission hardening

**Timebox:** 2026-10-24 through 2026-11-02.

Tasks:
- dependency/model freeze;
- deterministic offline packaging;
- zero-missing-output validator;
- repeated full dry runs;
- failure-safe `submission.json` generation;
- runtime margin checks;
- final Kaggle submissions;
- tag the exact final source/artifacts.

**Gate:** Kaggle accepts the final submission, and the exact submitted version can be reproduced.

**Hard stop:** ARC-AGI-2 R&D ends at the final submission deadline.

---

## M8 — Paper Track and open-source release

**Timebox:** evidence collection occurs throughout the project; finalization is 2026-11-03 through 2026-11-09.

Deliverables:
- competition writeup;
- Paper Track submission;
- method diagram;
- ablation/result tables;
- reproducibility instructions;
- limitations and negative results;
- required public repository/notebook artifacts;
- links from claims to experiment records/commits.

**Gate:** Paper Track submission accepted before the deadline and release obligations satisfied.

**Hard stop:** research/paper production ends at the Paper Track deadline.

---

## M9 — Outcome and project closeout

**Timebox:** 2026-11-10 through winner announcement on 2026-12-04.

No active model research. Activities are limited to:
- respond to organizer verification requests;
- preserve/release requested artifacts;
- record leaderboard/final judging outcome;
- prize administration if applicable;
- short postmortem and explicit project closure.

**Gate:** final outcome recorded and project marked `CLOSED`.

---

## Repository visibility policy

**Decision for the current phase: keep the repository PUBLIC through M1.**

Reason:
- M0/M1 contain infrastructure, published methods, baseline reproduction, and public research methodology;
- public CI is convenient during this phase;
- there is little competitive value in hiding already-public baselines.

Follower count is not a security boundary: public repositories can be found through search/indexing even with no followers.

**Automatic privacy trigger:** before committing the first genuinely original competitive mechanism, unpublished ablation result, or materially improved system that we would not want competitors to copy, reassess visibility. Default action at that trigger is to make the repository private until the required prize/open-source window.

GitHub Actions convenience is not allowed to override protection of a genuinely valuable competitive advantage. Heavy ARC compute should run on Kaggle/appropriate compute anyway; Actions is primarily CI/reproducibility infrastructure here.

---

## Project-wide decision rules

1. Score/evidence beats elegance.
2. Every material experiment gets an ID, commit, config, runtime, metrics, and KEEP/REJECT/INCONCLUSIVE conclusion.
3. Prefer complementary exact solves over highly correlated models with similar headline scores.
4. Leaderboard movement that fails internal validation is suspect.
5. No task-ID-specific rules or evaluation-set hand fitting.
6. Every new idea has a time/iteration budget.
7. Missing a milestone gate does not extend the project indefinitely; record PARTIAL and advance with the best known artifact.
8. No new architecture after M6 freeze.
9. Final submission reliability takes priority over late speculative score gains.
10. After the final deadlines, the project is finished regardless of prize outcome; judging/admin is M9, not continued R&D.

## Status-report contract

Whenever asked `onde estamos?`, report in this format:

- **Current milestone:** Mx — name / status.
- **Completed:** milestones with PASS.
- **Current gate:** exact condition we are trying to satisfy.
- **Evidence so far:** latest reproducible scores/results.
- **Blocker:** if any.
- **Next action:** one concrete next step.
- **Timebox remaining:** calendar deadline for the current milestone.
- **Project end:** ARC-AGI-2 2026-11-02; Paper Track 2026-11-09; closeout after results.
