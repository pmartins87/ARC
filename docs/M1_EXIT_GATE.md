# M1 Exit Gate — Baseline to Research Hypothesis

Snapshot: 2026-08-25
Status: decision protocol; no original competitive mechanism is disclosed here.

## Purpose

M1 ends on **2026-09-02** whether every desired diagnostic is perfect or not. The goal is to leave baseline reproduction with enough evidence to choose one bounded M2/M3 research hypothesis, not to collect public notebooks indefinitely.

## Evidence buckets

### A. Competition-valid anchor

Minimum acceptable:
- N1 notebook/version identity;
- L4 x4 runtime evidence;
- accepted competition rerun or documented failure/timeout;
- hidden/public competition score if returned.

Current state: runtime/submission path captured; hidden rerun pending.

### B. Public/frozen error structure

Preferred:
- exact pass@1/pass@2 on pinned evaluation-development tasks;
- shape/content error taxonomy;
- attempt-2 rescue and duplicate rate;
- processed/missing task coverage.

If exact full N1 public artifacts cannot be obtained within M1, mark this bucket `PARTIAL`; do not substitute smoke-only evidence as full-set evidence.

### C. Candidate discovery versus selection

Preferred:
- candidate-pool oracle;
- selected pass@2 from same pool;
- oracle-selector gap;
- correct-candidate rank distribution;
- timeout/missing coverage.

Instrumentation is ready. If compatible candidate artifacts remain unavailable, mark `PARTIAL` and choose the first M2 experiment so that it generates its own telemetry.

### D. Complementary alternative

Preferred:
- one materially different candidate source with comparable task-level predictions;
- exact unique wins and oracle-union gain relative to N1.

N2 is conditional. A second ~31% leaderboard number without task/candidate artifacts does not satisfy this bucket.

### E. Prior-art / novelty boundary

Required before original work:
- broad categories already known are documented;
- first specific hypothesis has three closest prior methods;
- claimed difference and causal prediction can be stated cleanly.

Current state: broad boundaries frozen; specific hypothesis intentionally not selected yet.

### F. Paper traceability

Required:
- evidence matrix active;
- negative results preserved;
- method/ablation/result placeholders linked to experiment IDs.

Current state: active.

## M1 classification

### PASS

Use when A is complete and enough of B/C/D is available to choose the next mechanism from measured evidence rather than intuition.

### PARTIAL

Use when N1 competition evidence exists but one or more task/candidate-level diagnostics remain unavailable despite bounded attempts. M2 then starts with the smallest experiment that resolves the most important remaining uncertainty.

### FAIL

Reserve for infrastructure/provenance failure severe enough that no competition-valid baseline or trustworthy evaluation protocol exists. Current evidence makes this unlikely.

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
