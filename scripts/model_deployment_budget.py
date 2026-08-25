from __future__ import annotations

import argparse
import json

from arcsolver.deployment_budget import memory_budget, throughput_budget


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Compute optimistic raw-weight memory headroom and minimum generated-token "
            "throughput for a competition deployment plan."
        )
    )
    parser.add_argument("--weights-gib", type=float, required=True)
    parser.add_argument("--tp", type=int, required=True)
    parser.add_argument("--gpu-memory-gib", type=float, required=True)
    parser.add_argument("--output-slots", type=int, required=True)
    parser.add_argument("--candidates", type=int, required=True)
    parser.add_argument("--tokens-per-candidate", type=int, required=True)
    parser.add_argument("--hours", type=float, default=12.0)
    args = parser.parse_args()

    memory = memory_budget(
        total_weight_gib=args.weights_gib,
        tensor_parallel_size=args.tp,
        gpu_memory_gib=args.gpu_memory_gib,
    )
    throughput = throughput_budget(
        output_slots=args.output_slots,
        candidates_per_output=args.candidates,
        generated_tokens_per_candidate=args.tokens_per_candidate,
        wallclock_hours=args.hours,
    )
    print(
        json.dumps(
            {"memory": memory.to_dict(), "throughput_lower_bound": throughput.to_dict()},
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
