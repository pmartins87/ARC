# E0010 — Lightning/NVARC frozen development pilot

Status: **PENDING — blocked on E0006 Gate B deployment feasibility**

## Pre-registered question

Once Lightning can load and generate on Kaggle L4 x4, does the source-faithful NVARC **direct-grid transductive mode** or the **executable-program inductive mode** provide the better exact-answer candidate source under the same small compute budget?

This is a feasibility/diagnostic pilot, not the final M2 architecture.

## Frozen pilot set

Manifest: `experiments/e0006_dev_pilot_v1.json`

- 12 unique tasks;
- 17 visible test-output slots;
- all from the 60-task development split;
- selected solely from E0009 prompt-token counts, not from answers, known difficulty labels or solver scores;
- covers task-level max prompt lengths from **744 to 6,621 tokens** approximately across evenly spaced rank quantiles.

Validation and heldout stay sealed.

## Equal-budget rule

For each mode use the same:
- checkpoint and precision route;
- selected task/test slots;
- number of candidates per slot;
- maximum new tokens unless the output representation itself requires a predeclared different hard cap;
- temperature/sampling family;
- total wall-clock budget as closely as the representation permits.

Record candidate extraction success separately from exact correctness.

## Primary pilot outputs

Per mode:
- exact pass@1;
- exact pass@2 if two independent candidates are requested;
- valid-output / extraction rate;
- runtime per slot;
- prompt and completion tokens;
- duplicate-attempt rate;
- for inductive mode: code extraction success, transform execution success, timeout/error class;
- unique exact wins by mode.

## Decision after pilot

- **KEEP transductive** if it materially dominates exact accuracy/coverage at comparable cost.
- **KEEP inductive** if executable hypotheses materially dominate or add complementary exact wins.
- **KEEP both** only if oracle-union/complementarity justifies their combined runtime.
- **REJECT Lightning/NVARC route** if candidate quality is too low to justify a full 82-slot development pass after the already-bounded compatibility work.

Do not tune prompts task-by-task during this pilot. A single mechanical parsing/serving fix is allowed only if it applies uniformly.
