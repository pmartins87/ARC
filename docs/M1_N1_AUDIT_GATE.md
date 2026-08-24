# M1 N1 Audit Gate

Snapshot: 2026-08-24

The N1 `ARC2 vanilla exact` Version 1 local `submission.json` has been received and audited. The first assumption for this gate — that the file represented a complete 120-task public-evaluation run — was falsified by the artifact itself.

## What the artifact actually is

The local/non-rerun file contains 120 task IDs and 172 output slots, but **167/172 slots are `[[0]]` placeholders**. Only five output slots across four tasks contain generated candidates. Therefore it is a smoke artifact and cannot support a full N1 public-evaluation error taxonomy.

On those five generated outputs, exact scoring against the matching current official task outputs gives pass@1 **3/5** and pass@2 **4/5**, including one second-attempt rescue. See `experiments/E0004_20260824_n1_local_smoke_audit.md`.

## Dataset provenance issue

The current official `arcprize/ARC-AGI-2` GitHub evaluation directory and the Kaggle submission schema disagree on the number of test pairs for five task IDs. The official-data export workflow is retained as reproducible infrastructure, but a future full evaluation must pin the exact Kaggle competition dataset version rather than silently substitute the current GitHub directory.

## Revised gate

Before an original M2/M3 mechanism is selected, obtain enough evidence to distinguish generation, selection and coverage failures. Acceptable evidence is one of:
- a pinned full/frozen public-evaluation run that emits real predictions rather than placeholders;
- a richer public inference dump with candidate pools and exact dataset provenance;
- a documented PARTIAL outcome if neither can be obtained inside the M1 timebox, followed by an evidence-bounded hypothesis rather than indefinite reproduction work.

The hidden Kaggle competition rerun score remains an external reproduction gate, but it does not reveal task-level error structure by itself.

No Ryzen work is required now. Do not launch another Kaggle run until its information value is explicit.
