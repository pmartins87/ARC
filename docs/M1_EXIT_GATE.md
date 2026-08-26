# M1 Exit Gate — Baseline to Research Hypothesis

Snapshot: 2026-08-26
Status: decision protocol; no original competitive mechanism is disclosed here.

## Purpose

M1 ends on **2026-09-02** whether every desired diagnostic is perfect or not. The goal is to leave baseline reproduction with enough evidence to choose one bounded M2/M3 research hypothesis, not to collect public notebooks indefinitely.

## Evidence buckets

### A. Competition-valid anchor — COMPLETE

Minimum acceptable:
- N1 notebook/version identity;
- L4 x4 runtime evidence;
- accepted competition rerun or documented failure/timeout;
- hidden/public competition score if returned.

Current state:
- N1 `ARC2 vanilla exact` frozen;
- clean run **25m29s on L4 x4**;
- competition rerun **Succeeded**;
- Public Score **29.72**;
- source snapshot reference **31.39**;
- reproduction delta **-1.67pp**.

Bucket A is complete. Do not reopen it by rerunning N1 for score alone.

### B. Public/frozen error structure — PARTIAL

Preferred:
- exact pass@1/pass@2 on pinned evaluation-development tasks;
- shape/content error taxonomy;
- attempt-2 rescue and duplicate rate;
- processed/missing task coverage.

Current state:
- exact scorer and evaluation split v2 are frozen;
- diversity/attempt telemetry infrastructure is ready;
- a full trusted N1/P33 task-level artifact set has not yet been ingested.

P33 (`Failed in AIMO`, public score 33.89) exposes **44 public output files** and is now the first no-run artifact source to inspect. If those outputs do not expose usable task-level evidence within the M1 timebox, keep this bucket `PARTIAL`; do not spend a leaderboard run merely to make the bucket look complete.

### C. Candidate discovery versus selection — PARTIAL / INFRA READY

Preferred:
- candidate-pool oracle;
- selected pass@2 from same pool;
- oracle-selector gap;
- correct-candidate rank distribution;
- timeout/missing coverage.

Current state:
- candidate-pool/selector instrumentation is ready;
- safe artifact inventory now fingerprints NVARC-style extensionless **BZ2** candidate files without deserializing them;
- public NVARC prior art confirms its decoder reads BZ2-compressed pickle candidate artifacts from `inference_outputs`;
- no full trusted candidate pool from N1/P33 has yet been audited.

If P33 exposes compatible BZ2 artifacts, provenance-check them before invoking the trusted-pickle audit path. If compatible candidate artifacts remain unavailable, keep `PARTIAL` and make the first M2 experiment emit its own telemetry.

### D. Complementary alternative — PARTIAL / E0006 ACTIVE

Preferred:
- one materially different candidate source with comparable task-level predictions;
- exact unique wins and oracle-union gain relative to N1.

Current state:
- correlated N2 remains skipped by default;
- P33 is likely related to the Qwen/NVARC family and therefore is evidence/provenance first, not automatically a complementary source;
- E0006 Nemotron 3.5 Lightning is the active materially different open-weight feasibility route;
- E0006 mirror completion is pending verification before Gate A.

A second leaderboard number without task/candidate artifacts does not satisfy this bucket.

### E. Prior-art / novelty boundary — READY FOR CATEGORY SELECTION

Required before original work:
- broad categories already known are documented;
- first specific hypothesis has three closest prior methods;
- claimed difference and causal prediction can be stated cleanly.

Current state:
- broad boundaries are frozen;
- public diversity/refinement/selection prior art is documented;
- the specific M2 mechanism is intentionally not selected until B/C/D evidence is as complete as the M1 timebox permits.

### F. Paper traceability — ACTIVE

Required:
- evidence matrix active;
- negative results preserved;
- method/ablation/result placeholders linked to experiment IDs.

Current state: active. E0006 deployment evidence, P33 public-frontier evidence, split correction and rejected attachment paths are all traceable negative/positive evidence streams.

## M1 classification

### PASS

Use when A is complete and enough of B/C/D is available to choose the next mechanism from measured evidence rather than intuition.

### PARTIAL

Use when N1 competition evidence exists but one or more task/candidate-level diagnostics remain unavailable despite bounded attempts. M2 then starts with the smallest experiment that resolves the most important remaining uncertainty.

### FAIL

Reserve for infrastructure/provenance failure severe enough that no competition-valid baseline or trustworthy evaluation protocol exists. Current evidence makes this unlikely.

## Current provisional classification

**PARTIAL, trending toward PASS.**

Reason:
- A is complete;
- B/C are instrumented but still waiting for a trusted full artifact set;
- D has a materially different route in E0006 but no comparable task-level result yet.

This provisional classification does not justify extending M1 beyond 2026-09-02.

## Hypothesis-selection rubric

Score each candidate research hypothesis from 0–3 on each dimension **before** implementation:

| Dimension | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Expected exact-score leverage | no causal path | weak/speculative | plausible measured bottleneck | directly targets dominant measured loss |
| Novelty headroom | essentially known | small implementation variation | meaningful mechanism distinction | clear closest-prior gap worth testing |
| Attribution | many confounders | difficult | bounded control possible | clean causal ablation |
| Kaggle fit | unlikely <12h/L4x4 | risky | feasible with optimization | comfortably feasible |
| Information per run | mostly leaderboard signal | limited | answers one strong question | decisively separates hypotheses |
| Paper value if negative | none | minor | useful boundary | strong falsifiable scientific result |

Maximum = 18.

The first M2 hypothesis should normally score **>=12/18** and must have no zero in Kaggle fit or attribution. This threshold is a project triage rule, not a scientific theorem.

## Candidate M2 categories — do not choose yet

These categories are kept distinct until current evidence resolves the bottleneck:

1. **candidate discovery/search** — favored if candidate oracle itself is low;
2. **selection / two-attempt allocation** — favored if truth is often in pool but outside top two;
3. **runtime/coverage** — favored if meaningful tasks/outputs are missed because the fixed sandbox budget expires;
4. **representation / ARC-post-trained model route** — favored if E0006 produces materially different exact coverage;
5. **diversity-preserving generation/refinement** — only if trajectory evidence shows useful hypotheses are being collapsed.

The logit-transfer optimization in `docs/M1_LOGIT_TRANSFER_OPTIMIZATION.md` is mechanical engineering evidence, not by itself an M2 reasoning hypothesis.

## Tie-breakers

When two hypotheses score similarly, prefer in order:

1. lower compute / faster falsification;
2. stronger intermediate diagnostic signal;
3. larger expected unique exact coverage rather than cosmetic diversity;
4. cleaner comparison to closest prior art;
5. reusable infrastructure for later ensemble/pass@2 work.

## Mandatory visibility decision

Immediately before the chosen specific M2 mechanism is implemented, re-check `docs/VISIBILITY_GATE.md`.

If the mechanism is genuinely original or competition-sensitive, stop public commits and state:

> **Visibility Gate atingido: não devemos publicar o próximo commit.**

## Exit output

M1 closes with exactly one short decision record containing:

- `PASS` or `PARTIAL`;
- N1 competition result/status;
- strongest measured bottleneck;
- evidence still missing;
- selected first M2 hypothesis category;
- hypothesis rubric score;
- visibility decision;
- first experiment ID and timebox.

This prevents M1 from becoming an open-ended survey phase.
