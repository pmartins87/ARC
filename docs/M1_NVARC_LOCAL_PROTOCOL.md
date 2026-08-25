# M1 — Local NVARC compatibility protocol

Status: **PUBLIC-SOURCE INFRASTRUCTURE — no competitive mechanism**

Purpose: remove evaluator/prompt ambiguity before the first Lightning L4 smoke so a successful model load can immediately feed a controlled direct-grid vs executable-program development experiment.

## Primary public sources

NVIDIA NeMo Gym:

- `resources_servers/nvarc/app.py`
- `resources_servers/nvarc/problem.py`
- `resources_servers/nvarc/configs/transductive.yaml`
- `resources_servers/nvarc/configs/inductive.yaml`
- `resources_servers/nvarc/data/example.jsonl`

NVIDIA Hugging Face dataset:

- `nvidia/Nemotron-RL-ARC-AGI-v1`

The released Gym code is Apache-2.0. The HF dataset metadata currently displays `pending-legal-review`; we use it here only as public protocol/provenance evidence, not as new training material.

## What is source-faithful

`src/arcsolver/nvarc_protocol.py` mirrors the public verifier contract:

- `transductive`: strip complete `<think>...</think>` blocks, extract/parse the final grid through the integer-palette text contract, exact match;
- `inductive`: strip thinking, extract the last fenced `python` block (then generic fence, then raw text containing `def transform`), execute `transform(test_input)` in a subprocess, validate a rectangular ARC grid, exact match;
- banned builtins/modules track the public NVIDIA sandbox list;
- reward is binary 1/0 with no partial credit;
- the default inductive transform timeout remains 30 seconds.

The local subprocess is a compatibility sandbox, **not a hardened hostile-code security boundary**. Competition runs should use the same controlled model-output context and should never execute arbitrary third-party code through this helper.

## Prompt fidelity

### Transductive

The system prompt is copied verbatim from NVIDIA's public NVARC example record. The user-message layout also follows the released example:

- `Please solve this ARC-AGI problem:`
- numbered `Train Example` blocks;
- compact digit rows for input/output grids;
- final `Test Input` block.

### Inductive

The public `Nemotron-RL-ARC-AGI-v1` viewer confirms the opening wording:

> You are an expert at solving ARC-AGI ... puzzles by writing Python code.

and states that the model must emit `transform(grid)`. The table viewer truncates the rest of the system message in the source we can programmatically inspect here. Therefore `INDUCTIVE_SYSTEM_PROMPT_V1` is deliberately labeled a **local controlled prompt**, not a byte-identical NVIDIA prompt.

Before calling a future inductive run a strict source reproduction, pin the exact released `responses_create_params.input` from the public dataset artifact and hash it. Until then, comparisons using the local prompt must be labeled `controlled_inductive_v1`, not `nvidia_exact_prompt`.

## Why preserve the apparently odd direct-grid parser

NVIDIA's public prompt **inputs** are rendered as compact digit rows, while its system instruction tells the model to return output values separated by spaces. The public verifier parses whitespace-separated integer tokens. We preserve that behavior rather than silently adding a permissive compact-output fallback, because parser changes can create fake model gains.

Any later parser robustness experiment must be an explicit ablation.

## Planned use after E0006 load PASS

1. Run a tiny transductive sanity set with the exact public transductive prompt contract.
2. Run the same development identities with `controlled_inductive_v1` only if the model/runtime budget makes long code traces plausible.
3. Store raw model responses before parsing.
4. Record extraction success separately from exact solution success.
5. Keep token count/runtime/candidate count fixed when comparing modes.
6. Feed successful outputs/candidates into the existing candidate-pool, diversity and selector diagnostics.

No Kaggle leaderboard submission is needed for this experiment.
