# M1 Public Qwen / NVARC-Derived Pipeline Audit

Date: 2026-08-24
Status: public-source architecture audit; no original competitive mechanism is disclosed here.

## Why this audit exists

N1 (`ARC2 vanilla exact`) is a Qwen3-4B task-time-adaptation pipeline in the NVARC/ARChitects lineage. Before changing it, M1 needs to separate four distinct sources of score:

1. **task-time adaptation quality**;
2. **candidate generation / search coverage**;
3. **candidate selection into the two allowed attempts**;
4. **wall-clock coverage under Kaggle's 12-hour limit**.

A score change cannot be interpreted correctly unless we know which layer changed.

## Public source basis

The exact N1 Kaggle notebook is not mirrored in this repository. We therefore use a pinned 2026 public mirror from `MA-Zbida/arc2026-kaggle` plus the NVARC 2025 sources to audit the same family of mechanisms. Claims below are about that public lineage unless explicitly labeled N1 UI evidence.

Pinned public mirror commit:

`MA-Zbida/arc2026-kaggle@4a3d6f33816807eacb7ea49846fadbca042abd69`

Relevant files:
- `arc_solver.py`
- `arc_decoder.py`
- `starter.py`
- `tune_selection.py`

N1 UI evidence from the public Kaggle page indicates a Qwen3-4B grid checkpoint, L4x4, task-time training, inference augmentations and the same `turbo_dfs` / `calc_scores` hot paths. The public score snapshot is 31.39%.

## Layer 1 — puzzle-specific adaptation

The public mirror:
- loads a local Qwen3 4B grid checkpoint in bfloat16;
- adds a high-rank LoRA adapter (`r=256`) across attention, MLP, embeddings and LM head;
- restores the same default adapter state before every puzzle;
- trains separately on each puzzle's visible demonstrations plus augmentations;
- uses AdamW, cosine scheduling and a fixed random seed;
- switches the adapted model back to inference mode before candidate search.

This is **test-time training (TTT)**: the shared pretrained model supplies priors, but each puzzle receives its own temporary adaptation.

### Measurement implication

A TTT modification must be evaluated separately from decoding changes. If adaptation improves the likelihood landscape but the true grid never enters the candidate pool, the failure is search/decoding. If the truth is in the pool but not submitted, the failure is selection.

## Layer 2 — augmentation and multi-view inference

The public mirror creates transformed views of each puzzle for both training and inference. Inference batches cover rotations, transpositions and color permutations; generated grids are inverted back to the canonical orientation before candidate aggregation.

The current family therefore already has a multi-view prior. Merely adding another rotation/flip is not a novel research direction and is unlikely to be high leverage by itself.

### Measurement implication

For each canonical candidate we should eventually record:
- how many independent views generated it;
- which transformation families generated it;
- whether it survives across TTT randomness / seeds;
- score dispersion across views.

Those quantities are available conceptually before inventing a new neural model.

## Layer 3 — DFS candidate generation

`turbo_dfs` searches only the ARC output vocabulary and prunes expansions above an NLL threshold. The public mirror:
- obtains prefix KV cache once;
- recursively extends candidates token-by-token;
- ranks expansions by accumulated NLL;
- terminates on EOS or token-length limit;
- has explicit time ceilings;
- decodes multiple transformed views.

This is not ordinary greedy generation. It is a bounded candidate-search process around the adapted model.

### Critical distinction

The **candidate pool oracle** can be better than the submitted score. If the exact output exists anywhere in the decoded pool, generation succeeded even if final pass@2 failed.

That distinction is now a project-wide invariant.

## Layer 4 — canonical candidate aggregation

After inversion of augmentation transforms, candidates are deduplicated by canonical grid. The public mirror retains for each grid:
- DFS / beam score observations;
- augmentation-rescoring values;
- effective vote/frequency through repeated generation.

This creates a rich candidate evidence table before the final two outputs are chosen.

## Layer 5 — final selection

Two public selectors are explicit in `arc_decoder.py` / `tune_selection.py`:

### `score_kgmon`

Combines:
- candidate occurrence count / votes;
- mean augmentation NLL.

### `score_full_probmul_3`

Combines:
- accumulated transformed DFS evidence;
- accumulated augmentation-rescoring evidence;
- a fixed baseline constant.

The public tuning utility computes:
- candidate-pool oracle pass@2;
- selected pass@2 for each selector;
- the **oracle-selection gap**;
- rank of the correct candidate when present but not top-2;
- candidate counts;
- runtime / timeout information when available;
- accuracy split by whether output size differs from input size.

This confirms that candidate selection is a first-class optimization surface in this code family, not a speculative concern introduced by our project.

## Layer 6 — wall-clock coverage

The public mirror uses four GPU workers and explicit end-time checks. A separate public NVARC fork documents a major failure mode of earlier baselines: per-task caps and scheduling could leave many puzzles undecoded before the global 12-hour deadline.

Therefore every future run should distinguish:
- tasks fully processed;
- tasks partially decoded;
- tasks never started / timed out;
- average and tail runtime per task.

A score improvement obtained solely by processing more tasks is useful for the competition, but it should not be confused with a reasoning improvement in the Paper Track.

## What N1 Version 1 already tells us

Our clean N1 local execution produced:
- valid `submission.json`;
- 25m29s notebook runtime;
- L4 x4 execution;
- no environment failure.

This proves the local public-evaluation pipeline works. The competition rerun score remains the external generalization gate.

## M1 measurement contract for this family

Before modifying the backbone, obtain as many of the following as the public artifacts permit:

- exact pass@1/pass@2 on our frozen 60-task development split;
- task IDs / outputs solved;
- shape-change vs same-shape error rates;
- duplicate-attempt rate;
- candidate-pool oracle pass@2;
- selection gap;
- correct-candidate rank distribution;
- number of unique canonical candidates per output;
- per-task runtime / timeout coverage.

If only `submission.json` is available, we can still recover the first four and construct an error taxonomy. Candidate-oracle metrics require the richer inference dump.

## Current decision pressure

Public evidence makes three broad routes distinguishable:

1. **Backbone/TTT changes** — potentially powerful but expensive and hard to attribute.
2. **Candidate search / refinement changes** — target the probability that the truth enters the pool.
3. **Selection/diversity changes** — target the gap between a good pool and the two submitted attempts.

M1 does **not** choose an original mechanism yet. The first M2/M3 hypothesis must be selected only after N1 task-level error evidence is available. That is also the repository-visibility trigger: the specific original mechanism should not be committed publicly before the privacy decision.

## Immediate data needed

The highest-information low-cost artifact is the 23 KB `submission.json` produced by N1 Version 1 on the public evaluation set. With that single file, the project can score N1 locally against the official 120-task public evaluation, restrict analysis to the frozen 60-task development split, and classify exact errors without another GPU run.
