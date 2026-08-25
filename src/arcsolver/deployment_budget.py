from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class MemoryBudget:
    total_weight_gib: float
    tensor_parallel_size: int
    gpu_memory_gib: float
    weight_shard_gib: float
    raw_headroom_gib: float
    raw_headroom_fraction: float

    def to_dict(self) -> dict[str, float | int]:
        return asdict(self)


@dataclass(frozen=True)
class ThroughputBudget:
    output_slots: int
    candidates_per_output: int
    generated_tokens_per_candidate: int
    wallclock_hours: float
    total_generated_tokens: int
    required_output_slots_per_hour: float
    required_candidates_per_second: float
    required_generated_tokens_per_second: float

    def to_dict(self) -> dict[str, float | int]:
        return asdict(self)


def memory_budget(
    *, total_weight_gib: float, tensor_parallel_size: int, gpu_memory_gib: float
) -> MemoryBudget:
    """Compute a deliberately optimistic raw-weight memory bound.

    This assumes weights shard evenly across tensor-parallel ranks and excludes
    runtime memory (Mamba/KV state, activations, CUDA graphs, allocator overhead,
    temporary buffers, tokenizer/model metadata, etc.). Therefore positive
    headroom means only "not ruled out by raw weight bytes"; it is not proof
    that a model will load or run.
    """
    if total_weight_gib <= 0:
        raise ValueError("total_weight_gib must be positive")
    if tensor_parallel_size <= 0:
        raise ValueError("tensor_parallel_size must be positive")
    if gpu_memory_gib <= 0:
        raise ValueError("gpu_memory_gib must be positive")

    shard = total_weight_gib / tensor_parallel_size
    headroom = gpu_memory_gib - shard
    return MemoryBudget(
        total_weight_gib=total_weight_gib,
        tensor_parallel_size=tensor_parallel_size,
        gpu_memory_gib=gpu_memory_gib,
        weight_shard_gib=shard,
        raw_headroom_gib=headroom,
        raw_headroom_fraction=headroom / gpu_memory_gib,
    )


def throughput_budget(
    *,
    output_slots: int,
    candidates_per_output: int,
    generated_tokens_per_candidate: int,
    wallclock_hours: float,
) -> ThroughputBudget:
    """Convert a candidate-generation plan into a minimum aggregate token rate.

    The result ignores prompt-prefill cost, verification/tool execution, retries,
    model startup, scoring, serialization and safety margin. It is therefore a
    lower bound on required end-to-end serving throughput.
    """
    if output_slots <= 0:
        raise ValueError("output_slots must be positive")
    if candidates_per_output <= 0:
        raise ValueError("candidates_per_output must be positive")
    if generated_tokens_per_candidate < 0:
        raise ValueError("generated_tokens_per_candidate must be non-negative")
    if wallclock_hours <= 0:
        raise ValueError("wallclock_hours must be positive")

    candidates = output_slots * candidates_per_output
    total_tokens = candidates * generated_tokens_per_candidate
    seconds = wallclock_hours * 3600.0
    return ThroughputBudget(
        output_slots=output_slots,
        candidates_per_output=candidates_per_output,
        generated_tokens_per_candidate=generated_tokens_per_candidate,
        wallclock_hours=wallclock_hours,
        total_generated_tokens=total_tokens,
        required_output_slots_per_hour=output_slots / wallclock_hours,
        required_candidates_per_second=candidates / seconds,
        required_generated_tokens_per_second=total_tokens / seconds,
    )
