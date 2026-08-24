# M1 Kaggle Run Queue

Snapshot: 2026-08-24

The queue is ordered by information value per user-side run. A run is not performed merely because it was once planned; lower-value runs are skipped when a higher-value run already proves the same pipeline property.

## N1 — competitive neural frontier — FIRST PRIORITY

Notebook: `ARC2 vanilla exact`

URL: `https://www.kaggle.com/code/sorenravn/arc2-vanilla-exact`

Current public evidence:
- public score: **31.39**;
- directly copyable public Kaggle notebook;
- currently the highest score in our frozen 2026-08-24 public-code snapshot.

### Protocol

1. Copy & Edit from the public notebook.
2. Do not modify method/code for the first run.
3. Preserve attached inputs/models exactly as copied.
4. Use the accelerator required by the copied notebook.
5. Keep internet disabled for competition-compatible execution.
6. Run/save the complete version.
7. Submit to ARC Prize 2026 — ARC-AGI-2.
8. Record exact source version, copied version, accelerator, runtime, public score, warnings/errors, and all attached inputs.

### PASS

A valid submission is accepted and score/runtime are captured. Exact equality to 31.39 is not mandatory until source/input-version differences have been audited.

## N0 — BlackCat pipeline anchor — FALLBACK ONLY

Notebook: `BlackCat Stable Anchor — NVARC Guard`

URL: `https://www.kaggle.com/code/lucifer19/blackcat-stable-anchor-nvarc-guard`

Public evidence:
- current page around **26.81**;
- historical best **28.89 (V4)**;
- runtime around **24m48s** on L4 x4.

### Decision change

N0 was originally our first run. It is now a **fallback**. N1 is itself directly copyable and validates the same end-to-end Kaggle pipeline while simultaneously establishing the stronger competition baseline. If N1 completes normally, we skip N0 and save a redundant run.

Use N0 only if N1 fails for environment/input reasons that need a simpler anchor.

## C0 — CompressARC / MDL reference — SECONDARY

Notebook: `ARC-AGI Without Pretraining`

URL: `https://www.kaggle.com/code/iliao2345/arc-agi-without-pretraining`

Reference version 10/11:
- L4 x4;
- runtime **6m32s**;
- ARC-AGI-2 semi-private successful runs reported in the **1.67–4.17** range.

C0 requires adapting the historical 2025 competition attachment to the 2026 ARC-AGI-2 input while preserving the method. It is lower priority than N1 and is timeboxed; see `docs/M1_COMPRESSARC_REPRO.md`.

## After N1

Once N1 is reproduced, the next neural experiment is not another arbitrary public notebook. We first record N1's components/resources and then choose one controlled ablation or the 31.11 NVARC/TRM Evidence Cost notebook to isolate what TRM contributes.

## User-side data to send back

For each completed Kaggle run, a screenshot of the submission/result screen is sufficient if it visibly includes:
- notebook/version identity;
- public score;
- runtime/status where available.

Attached input/model names can be sent as a second screenshot if they are not visible on the result screen.
