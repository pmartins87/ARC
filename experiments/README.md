# Experiment Ledger

Every material experiment gets a directory or record keyed by an immutable experiment ID, for example:

`E0007_20260903_symbolic_object_v2`

Record at minimum:

```yaml
id: E0007
commit: <git-sha>
dataset: arc-agi-2
split_manifest: <path-and-sha>
method: <short name>
config: <path-or-inline summary>
seeds: [0]
hardware: <cpu/gpu>
runtime_seconds: 0
pass_at_1: 0.0
pass_at_2: 0.0
correct_outputs: 0
total_outputs: 0
status: KEEP | REJECT | INCONCLUSIVE
notes: <what changed and what we learned>
```

For Kaggle submissions also record:
- notebook slug/version;
- accelerator;
- observed runtime;
- public/hidden leaderboard score as applicable;
- submission date;
- whether internet was disabled;
- all attached datasets/models and versions.

Negative results are retained. We are optimizing cumulative knowledge, not a cosmetically clean history.
