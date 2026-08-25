Current milestone: **M1 — Baselines / feasibility**, due 2026-09-02.

- N1 `ARC2 vanilla exact` hidden Kaggle rerun: **PENDING / IN PROGRESS**; no user action while it runs.
- S0 shallow symbolic: **REJECT standalone** (0/82 exact dev outputs).
- Candidate-pool, selector, diversity, runtime/coverage and dataset-provenance instrumentation: **READY on main**.
- Public-code frontier refresh: the strongest public-notebook score currently verified in our audit is **31.81** (`ARC Baseline Rebuild`, best Version 73). N1's public **31.39** remains our controlled reproduction anchor. The +0.42pp public update does **not** justify another run by score alone.
- Live-prize frontier remains a separate regime: organizer-reported leaders are ~70%+; M2 must seek step-change leverage rather than incremental public-notebook tuning.
- N2 correlated ~31% TRM sibling: **CONDITIONAL**, not worth a run for score alone.
- Preferred feasibility probe: **Nemotron 3.5 Lightning + NVIDIA NeMo Gym NVARC**. Official public sources provide ARC-specific post-training disclosure, an Apache-2.0 exact verifier with direct-grid and executable-`transform()` modes, vLLM support and TP=4 serving references.
- Deployment evidence materially strengthened: NVIDIA's current NIM support matrix reports the Lightning **BF16 TP4** profile floor as **20 GB/GPU, minimum 4 GPUs, Ampere-or-newer / SM 8.0+**. NVIDIA lists L4 as **24 GB, Ada Lovelace, compute capability 8.9**, so Kaggle L4 x4 passes the published profile floor with nominal **4 GB/GPU** headroom. This is stronger than raw-weight arithmetic but still does not prove bare-vLLM Kaggle compatibility or sufficient throughput.
- The offline no-leaderboard L4 smoke harness is **READY on main**: inspect-only first, then bounded TP4 vLLM load + one short generation, structured OOM/kernel/version failure classes, startup latency, memory snapshots and token throughput. One compatibility round + one bounded mechanical fix max.
- NVIDIA's official `Nemotron-RL-ARC-AGI-v1` gives a source-faithful public prompt/reward baseline for both NVARC modes: matched transductive and Python-inductive tasks, binary exact reward, 30s Python execution. Dataset metadata still says `pending-legal-review`, so checkpoint-only evaluation is cleaner than new training on those bytes.
- Kaggle/Hugging Face integration provides the preferred low-manual-work model attachment path; do **not** route ~60+ GB through the user's PC unless lower-friction attachment/import paths fail.
- E0006: **PENDING_L4_SMOKE**. No competition submission or Ryzen work has been launched for it.
- Paper Prize path remains active from the same evidence stream. Current organizer pages disagree by one day: Kaggle submission host says **2026-11-09 23:59 UTC**, ARC Prize overview says Nov 8. Project rule: operational external deadline Nov 9, **internal safety deadline Nov 8** until re-verified.
- Before any original competitive mechanism is committed publicly, trigger `docs/VISIBILITY_GATE.md`.
