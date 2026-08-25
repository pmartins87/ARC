from __future__ import annotations

import argparse
import json

from arcsolver.profile_headroom import assess_profile_headroom


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare target GPUs against a vendor-published deployment profile floor."
    )
    parser.add_argument("--gpu-vram-gb", type=float, required=True)
    parser.add_argument("--profile-min-vram-gb", type=float, required=True)
    parser.add_argument("--gpu-count", type=int, required=True)
    parser.add_argument("--profile-min-gpu-count", type=int, required=True)
    parser.add_argument("--gpu-compute-capability", type=float)
    parser.add_argument("--required-compute-capability", type=float)
    args = parser.parse_args()

    report = assess_profile_headroom(
        gpu_vram_gb=args.gpu_vram_gb,
        profile_min_vram_gb=args.profile_min_vram_gb,
        gpu_count=args.gpu_count,
        profile_min_gpu_count=args.profile_min_gpu_count,
        gpu_compute_capability=args.gpu_compute_capability,
        required_compute_capability=args.required_compute_capability,
    )
    print(json.dumps(report.to_dict(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
