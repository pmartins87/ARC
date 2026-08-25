Current milestone: **M1 — Baselines / feasibility**, due 2026-09-02.

- N1 `ARC2 vanilla exact` hidden Kaggle rerun: **PENDING / IN PROGRESS**; no user action while it runs.
- S0 shallow symbolic: **REJECT standalone** (0/82 exact dev outputs).
- Candidate-pool, selector, diversity, runtime/coverage and dataset-provenance instrumentation: **READY on main**.
- Live-prize frontier correction: public/copyable N1 ~31% is an open anchor, while organizer-reported live leaders are ~70%+; M2 must seek step-change leverage.
- N2 correlated ~31% TRM sibling: **CONDITIONAL**, not worth a run for score alone.
- New preferred feasibility probe: **Nemotron 3.5 Lightning + NVIDIA NeMo Gym NVARC**. Official public sources provide ARC-specific post-training disclosure, an Apache-2.0 ARC verifier with transductive and executable-`transform()` modes, vLLM support and a TP=4 reference. BF16 raw weights are not ruled out by 4x24GB L4 capacity, but L4 startup, peak VRAM and throughput remain unverified.
- E0006: **PENDING_DEPLOYMENT_FEASIBILITY**. No competition submission or Ryzen work has been launched.
- Paper Prize path remains active from the same evidence stream.
- Before any original competitive mechanism is committed publicly, trigger `docs/VISIBILITY_GATE.md`.
