# M1 — Live leader evidence ladder

Snapshot: 2026-08-25

Purpose: exploit public clues from the ~70% ARC-AGI-2 leaders without turning community speculation into architecture claims.

## 1. Facts we can use

### Live scores

ARC Prize public updates report:
- `nvbanana`: **72.08%** live score;
- `rabbithole`: **70.42%**, after a reported jump from 50.42% over a weekend.

These establish the current competition capability frontier, not the mechanism used.

### nvbanana identity / compute regime

ARC Prize publicly identifies nvbanana as Jean-François Puget (`cpmpml` / JFPuget) and Darragh (`darraghdog`). Their public profiles identify both with NVIDIA affiliation/research context.

Puget publicly states that the team exceeded 70%:
- with **no internet**;
- using only **4×L4 GPUs**;
- and that the same code would run faster on H100.

A later public post from Puget describes their then-current system at about **71.5%** and roughly **$0.20 per task** in his comparison context.

This is strong evidence that ~70% is achievable inside exactly the hardware/internet regime we must target. It also argues against treating 4×L4 itself as the fundamental barrier.

Sources:
- ARC Prize public score updates, 2026-08-25
- https://www.kaggle.com/darraghdog/competitions
- public JFPuget posts captured in the research log

## 2. Facts that do NOT reveal their method

None of the public leader statements inspected here establishes:
- which checkpoint/model nvbanana uses;
- whether the final 2026 method uses Nemotron 3.5 Lightning;
- whether it uses NVIDIA's NVARC RL/SFT datasets;
- whether it uses direct-grid generation, Python induction, image generation, TTT, or a mixture;
- its candidate count, reasoning budget, selector, quantization, or runtime allocation policy.

Therefore no architecture attribution is allowed from score/employer coincidence alone.

## 3. Community clue — useful only as hypothesis generation

A Kaggle discussion participant noticed NVIDIA's public `Nemotron-SFT-ARC-AGI-v1` data and speculated that it could explain or inspire the large nvbanana gains. The same comment mentions the public ARC tools (`arc-python-executor`, augmenter, etc.) and guesses that a smaller distilled model might fit the competition.

This is **third-party speculation**, not team disclosure.

It is useful in exactly one way: it independently points toward the same public NVIDIA ARC post-training artifacts that our source audit already selected on their own merits. It does not raise the probability enough to label them “the nvbanana method.”

Source:
- Kaggle ARC Prize 2026 discussion activity by `mccocoful`, observed 2026-08-25.

## 4. Why the Nemotron/NVARC probe remains justified without the speculation

Even if nvbanana uses something entirely different, the Lightning/NVARC path deserves E0006 because public primary sources independently establish:
- Lightning has explicit ARC-specific post-training data/environment disclosure;
- NVIDIA provides a public exact ARC NVARC environment with direct-grid and executable-program modes;
- an official RL dataset exposes matching task modes/prompts/reward semantics;
- Lightning has only 3B active parameters and an official TP=4 serving reference;
- Kaggle allows freely/publicly available pretrained models;
- raw BF16 weight bytes do not immediately rule out 4×24GB L4.

Thus E0006 is evidence-driven, not leader-chasing.

## 5. Strategic inference we ARE allowed to make

From the verified compute regime plus the public model landscape:

> A 70%+ ARC-AGI-2 system does not require internet, H100s, or hardware beyond the competition allocation. The leverage must come from model capability, ARC-specific training/adaptation, representation/search/selection, inference efficiency, or some combination thereof.

This narrows M2. It does not identify the winning combination.

## 6. Anti-confirmation-bias rule

For every clue about a live leader, tag it as one of:
- **TEAM/ORGANIZER FACT** — direct statement from team or organizer;
- **PUBLIC ARTIFACT FACT** — reproducible code/model/data;
- **INFERENCE** — conclusion supported by facts but not directly stated;
- **SPECULATION** — community guess.

Only the first two can establish implementation provenance. Inference may guide experiments. Speculation may only generate bounded hypotheses.

## 7. Current decision

No change to the user workflow: wait for N1 while continuing zero-user-cost source work.

No attempt to reverse-engineer private leader code. Public evidence is used to choose higher-information experiments and to keep our competitive target realistic.
