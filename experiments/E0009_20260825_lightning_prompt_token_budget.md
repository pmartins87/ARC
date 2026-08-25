# E0009 — Lightning/NVARC visible prompt-token budget

Status: **PASS — 8K is sufficient for the frozen development gate**

```yaml
id: E0009
date: 2026-08-25
workflow_run: 32849612257
workflow_artifact: lightning-prompt-token-budget
artifact_sha256: e7b482f6cd8f7e538af82bf68405f19b16d354a6b9b5e10fd7e57d1084815624
model: nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16
model_revision: a9904d24bcc1d289a1950fa9d2b978c47cf903b9
visible_public_evaluation_slots: 167
split_manifest: experiments/evaluation_split_v2.json
method: exact tokenizer apply_chat_template on public NVARC-style messages
hardware: GitHub Actions ubuntu-latest CPU
status: PASS
```

## Question

Is the conservative **8,192-token** E0006 L4 compatibility context large enough for evaluation-shaped ARC prompts, or would the first GPU load experiment be invalidated by prompt truncation?

## Leakage guard

The profiler constructs each prompt from:
- public training demonstration inputs;
- public training demonstration outputs;
- the current test **input**.

It never copies or reads the test output into the prompt-slot record. No ARC score is computed.

## Measured results

### Transductive public NVARC prompt

| Metric | Tokens |
|---|---:|
| Slots | 167 |
| Minimum | 689 |
| Median | 2,321 |
| Mean | 2,586.6 |
| P90 | 4,161 |
| P95 | 4,752 |
| Maximum | 8,490 |
| >4,096 | 17 / 167 (10.18%) |
| >8,192 | **1 / 167 (0.60%)** |
| >16,384 | 0 |

Frozen development split:
- 82 visible output slots;
- median **2,281**;
- P95 **4,752**;
- maximum **6,621**;
- therefore **0 development slots exceed 8,192**.

Validation has the single >8K slot: `981571dc[0]`, **8,490** tokens. Heldout maximum is **4,481**.

### Inductive controlled-v1 prompt

The inductive system prompt is only 16 tokens longer under this tokenizer, so the distribution is nearly identical:
- median **2,337**;
- P95 **4,768**;
- maximum **8,506**;
- exactly one slot >8,192, again `981571dc[0]` in validation;
- frozen development maximum **6,637**.

## Decision

**KEEP `--max-model-len 8192` for E0006 Gate B and the first Gate C development ablation.**

This is now evidence-based rather than arbitrary: every frozen-development prompt fits with at least ~1,555 tokens of context headroom before generation on the worst visible dev slot.

Do not infer that 8K is sufficient for every future validation/competition task. Before opening validation, either raise the context ceiling beyond 8,506 if memory permits or implement a predeclared prompt-budget fallback that is validated without inspecting task answers.

## Consequence for deployment

The first Lightning load smoke can optimize for **VRAM compatibility** at 8K without sacrificing any frozen-development task. Therefore a failure at Gate B cannot be excused as a known development-prompt context mismatch.
