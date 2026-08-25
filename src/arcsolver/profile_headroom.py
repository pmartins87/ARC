from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ProfileHeadroom:
    gpu_vram_gb: float
    profile_min_vram_gb: float
    gpu_count: int
    profile_min_gpu_count: int
    gpu_compute_capability: float | None
    required_compute_capability: float | None
    per_gpu_headroom_gb: float
    per_gpu_headroom_fraction: float
    aggregate_headroom_gb: float
    memory_floor_pass: bool
    gpu_count_pass: bool
    architecture_pass: bool | None
    overall_floor_pass: bool

    def to_dict(self) -> dict[str, float | int | bool | None]:
        return asdict(self)


def assess_profile_headroom(
    *,
    gpu_vram_gb: float,
    profile_min_vram_gb: float,
    gpu_count: int,
    profile_min_gpu_count: int,
    gpu_compute_capability: float | None = None,
    required_compute_capability: float | None = None,
) -> ProfileHeadroom:
    """Compare hardware against a vendor-published deployment-profile floor.

    This is deliberately a *floor* check, not an inference-capacity estimator.
    Vendor profile minima can include runtime allocations but still exclude
    additional headroom needed for long context, large KV caches, high
    concurrency, temporary buffers, allocator fragmentation, or a different
    serving stack. Passing this function never proves that deployment will fit.
    """
    if gpu_vram_gb <= 0:
        raise ValueError("gpu_vram_gb must be positive")
    if profile_min_vram_gb <= 0:
        raise ValueError("profile_min_vram_gb must be positive")
    if gpu_count <= 0:
        raise ValueError("gpu_count must be positive")
    if profile_min_gpu_count <= 0:
        raise ValueError("profile_min_gpu_count must be positive")
    if gpu_compute_capability is not None and gpu_compute_capability <= 0:
        raise ValueError("gpu_compute_capability must be positive when provided")
    if required_compute_capability is not None and required_compute_capability <= 0:
        raise ValueError("required_compute_capability must be positive when provided")

    per_gpu_headroom_gb = gpu_vram_gb - profile_min_vram_gb
    memory_floor_pass = per_gpu_headroom_gb >= 0
    gpu_count_pass = gpu_count >= profile_min_gpu_count

    architecture_pass: bool | None
    if gpu_compute_capability is None or required_compute_capability is None:
        architecture_pass = None
    else:
        architecture_pass = gpu_compute_capability >= required_compute_capability

    overall = memory_floor_pass and gpu_count_pass and architecture_pass is not False

    return ProfileHeadroom(
        gpu_vram_gb=gpu_vram_gb,
        profile_min_vram_gb=profile_min_vram_gb,
        gpu_count=gpu_count,
        profile_min_gpu_count=profile_min_gpu_count,
        gpu_compute_capability=gpu_compute_capability,
        required_compute_capability=required_compute_capability,
        per_gpu_headroom_gb=per_gpu_headroom_gb,
        per_gpu_headroom_fraction=per_gpu_headroom_gb / gpu_vram_gb,
        aggregate_headroom_gb=per_gpu_headroom_gb * gpu_count,
        memory_floor_pass=memory_floor_pass,
        gpu_count_pass=gpu_count_pass,
        architecture_pass=architecture_pass,
        overall_floor_pass=overall,
    )
