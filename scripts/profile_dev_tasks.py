from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def shape(grid: list[list[int]]) -> tuple[int, int]:
    return len(grid), len(grid[0])


def colors(grid: list[list[int]]) -> set[int]:
    return {value for row in grid for value in row}


def load_manifest(path: Path, split: str) -> list[str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return list(payload["splits"][split])


def classify_pair(inp: list[list[int]], out: list[list[int]]) -> dict[str, Any]:
    ih, iw = shape(inp)
    oh, ow = shape(out)
    in_colors = colors(inp)
    out_colors = colors(out)
    return {
        "same_shape": (ih, iw) == (oh, ow),
        "output_smaller_area": oh * ow < ih * iw,
        "output_larger_area": oh * ow > ih * iw,
        "height_ratio_integer_up": oh >= ih and oh % ih == 0,
        "width_ratio_integer_up": ow >= iw and ow % iw == 0,
        "height_ratio_integer_down": ih >= oh and ih % oh == 0,
        "width_ratio_integer_down": iw >= ow and iw % ow == 0,
        "same_color_set": in_colors == out_colors,
        "output_colors_subset_input": out_colors <= in_colors,
        "introduces_new_colors": bool(out_colors - in_colors),
        "removes_colors": bool(in_colors - out_colors),
        "input_color_count": len(in_colors),
        "output_color_count": len(out_colors),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate structural profile of an ARC split using train pairs only.")
    parser.add_argument("task_directory", type=Path)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--split", default="development", choices=("development", "validation", "heldout"))
    parser.add_argument("--json-out", type=Path, required=True)
    args = parser.parse_args()

    task_ids = load_manifest(args.manifest, args.split)
    pair_flags: Counter[str] = Counter()
    task_flags: Counter[str] = Counter()
    shape_signatures: Counter[str] = Counter()
    color_delta_hist: Counter[str] = Counter()
    total_pairs = 0

    for task_id in task_ids:
        task = json.loads((args.task_directory / f"{task_id}.json").read_text(encoding="utf-8"))
        profiles = [classify_pair(pair["input"], pair["output"]) for pair in task["train"]]
        total_pairs += len(profiles)

        bool_keys = [key for key, value in profiles[0].items() if isinstance(value, bool)]
        for profile in profiles:
            for key in bool_keys:
                pair_flags[key] += int(profile[key])
            delta = profile["output_color_count"] - profile["input_color_count"]
            color_delta_hist[str(delta)] += 1

        for key in bool_keys:
            if all(profile[key] for profile in profiles):
                task_flags[f"all_{key}"] += 1

        signatures = []
        for pair in task["train"]:
            ih, iw = shape(pair["input"])
            oh, ow = shape(pair["output"])
            signatures.append((ih, iw, oh, ow))
        relation = []
        for ih, iw, oh, ow in signatures:
            relation.append(
                (
                    "same" if ih == oh else ("up" if oh > ih else "down"),
                    "same" if iw == ow else ("up" if ow > iw else "down"),
                )
            )
        if len(set(relation)) == 1:
            shape_signatures[str(relation[0])] += 1
        else:
            shape_signatures["mixed"] += 1

    report = {
        "split": args.split,
        "tasks": len(task_ids),
        "train_pairs": total_pairs,
        "pair_flag_counts": dict(sorted(pair_flags.items())),
        "task_flag_counts": dict(sorted(task_flags.items())),
        "task_shape_relation_counts": dict(sorted(shape_signatures.items())),
        "pair_color_count_delta_histogram": dict(sorted(color_delta_hist.items(), key=lambda item: int(item[0]))),
        "note": "Profiles use training demonstrations only; no test outputs are consulted.",
    }

    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
