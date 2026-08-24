# M1 N1 Audit Gate

Snapshot: 2026-08-24

The N1 `ARC2 vanilla exact` Version 1 public-evaluation submission artifact has been received out-of-band from the Kaggle run. Before selecting any original mechanism, M1 will score and classify that artifact against the current official 120-task ARC-AGI-2 evaluation set.

This gate exports the official public evaluation task files as a reproducible GitHub Actions artifact. It does not contain user-private or novel solver material and exists only to make the N1 error audit source-grounded and repeatable.

Required analysis:
- exact pass@1/pass@2;
- second-attempt rescues and duplicate attempts;
- wrong-shape vs right-shape/content-wrong failures;
- same-shape vs shape-changing target groups;
- solved task IDs;
- frozen 60/30/30 split metrics;
- candidate-selection implications for M2/M3.

No Kaggle rerun and no Ryzen work is required for this gate.
