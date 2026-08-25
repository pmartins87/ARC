# M1 — Nemotron Lightning license / ARC Prize external-model gate

Snapshot: 2026-08-25

## Competition rule

ARC Prize 2026 ARC-AGI-2 explicitly allows **external data, including pre-trained models, when freely and publicly available**. The final notebook must remain offline and under the 12-hour GPU limit.

Source:
- https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/overview/code-requirements

This means a public Nemotron checkpoint is not disqualified merely because it is external to the competition dataset. It still has to be attached/packaged into the Kaggle notebook so the hidden rerun needs no internet.

## Lightning model license

The official `nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16` repository is marked **OpenMDW-1.1**.

OpenMDW-1.1 is permissive. Subject to its terms it grants permission to use, modify and redistribute Model Materials. If Model Materials are redistributed, the distribution must retain:
- the OpenMDW-1.1 agreement;
- applicable copyright/origin notices.

Sources:
- https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16
- https://openmdw.ai/faq/
- https://github.com/OpenMDW/OpenMDW/blob/main/1.1/LICENSE.OpenMDW-1.1

## Decision

**The released Lightning weights are provisionally compatible with the competition's public-external-model rule.**

This is a much cleaner gate than the separate `Nemotron-SFT-ARC-AGI-v1` dataset, whose current Hugging Face metadata/prose license signals are inconsistent. We do not need to train on or redistribute that SFT dataset merely to evaluate the already-released Lightning checkpoint.

Remaining deployment obligation:
- package the exact public checkpoint and required inference software/data into an internet-off Kaggle notebook;
- preserve license/origin notices in any redistributed model artifact;
- verify all third-party inference dependencies separately;
- comply with the open-source obligations if the final solution becomes prize eligible.

This is a research compliance note, not legal advice.
