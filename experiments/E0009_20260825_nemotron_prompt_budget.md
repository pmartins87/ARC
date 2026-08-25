# E0009 — Nemotron 3.5 Lightning exact prompt-token budget

Status: **PASS — 8k is suitable for the load smoke but not a safe full evaluation context**

```yaml
id: E0009
date: 2026-08-25
model: nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16
tokenizer_runtime: transformers 4.57.6 / released model tokenizer+chat template
prompt_contract: nvidia_public_transductive
split_manifest: experiments/evaluation_split_v2.json
public_output_slots_profiled: 167
workflow_run: 32816692011
artifact_name: nemotron-prompt-budget
artifact_sha256: 58d701c4ef1da61edb16fea06da46b31911f8396ecc8ceebc680367df703ff57
status: PASS
```

## Question

How much of the model context is already consumed by source-faithful visible ARC prompt material before any reasoning/output tokens are generated?

This matters because the first L4 feasibility smoke intentionally uses `max_model_len=8192` to minimize memory risk. A successful 8k load does not prove that realistic ARC prompts leave enough room for useful reasoning.

## Leakage guard

The profiler reads:

- training inputs;
- training outputs;
- public test **inputs**.

It never reads public test outputs. The adopted v2 manifest is used only to report split-local distributions.

## Exact tokenizer result

All 167 public-evaluation output prompts, under the released Lightning tokenizer and chat template:

| prompt tokens | value |
|---|---:|
| minimum | 689 |
| median | 2,321 |
| mean | 2,586.6 |
| p90 | 4,161 |
| p95 | 4,752 |
| maximum | **8,490** |
| >4,096 | 17 / 167 |
| >8,192 | **1 / 167** |
| >16,384 | 0 / 167 |

By split:

| split | outputs | median | p90 | p95 | max | >4k | >8k |
|---|---:|---:|---:|---:|---:|---:|---:|
| development | 82 | 2,281 | 3,711 | 4,752 | **6,621** | 6 | 0 |
| validation | 42 | 2,229.5 | 4,752 | 7,719 | **8,490** | 5 | 1 |
| heldout | 43 | 2,813 | 4,179 | 4,401 | **4,481** | 6 | 0 |

The tokenizer is `PreTrainedTokenizerFast`. The public evaluation prompts contain a median of 2,097 visible grid cells and a maximum of 8,100.

## Consequence

`max_model_len=8192` remains correct for the **first load + short-generation smoke**. It is deliberately a mechanical gate, not an evaluation setting.

For a meaningful development probe:

- the largest development prompt is 6,621 tokens;
- a 2,048-token generation allowance would require at least **8,669** context tokens;
- therefore 8,192 would truncate/fail on the largest development prompt even though the prompt itself fits;
- 12,288 gives ~5,667 tokens of headroom on the largest development prompt;
- 16,384 gives ~9,763 tokens of headroom on the largest development prompt and ~7,894 on the largest public-evaluation prompt.

So the post-load context gate should be **12k/16k**, preferably 16,384 if L4 startup/VRAM remains healthy.

This still does not make the released long-trace training distribution competition-efficient. Public SFT disclosures report much longer average successful ARC traces, so generation-length/runtime compression remains a real research constraint even though input prompts themselves are manageable.

## Decision

- KEEP 8,192 for the first minimal L4 load smoke.
- After load PASS, restart at **16,384** for one bounded context/generation smoke if memory permits.
- Do not run the full 60-task development set until startup VRAM and short-generation throughput are measured.
- Record prompt tokens and generated tokens separately in every E0006 run.
