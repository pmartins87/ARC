import pytest

from arcsolver.deployment_budget import memory_budget, throughput_budget


def test_memory_budget_is_raw_weight_lower_bound():
    result = memory_budget(total_weight_gib=62.0, tensor_parallel_size=4, gpu_memory_gib=24.0)
    assert result.weight_shard_gib == 15.5
    assert result.raw_headroom_gib == 8.5
    assert result.raw_headroom_fraction == pytest.approx(8.5 / 24.0)


def test_memory_budget_can_reject_obvious_raw_weight_mismatch():
    result = memory_budget(total_weight_gib=120.0, tensor_parallel_size=4, gpu_memory_gib=24.0)
    assert result.raw_headroom_gib == -6.0


def test_throughput_budget_turns_reasoning_length_into_rate():
    result = throughput_budget(
        output_slots=240,
        candidates_per_output=2,
        generated_tokens_per_candidate=4000,
        wallclock_hours=12.0,
    )
    assert result.total_generated_tokens == 1_920_000
    assert result.required_output_slots_per_hour == 20.0
    assert result.required_generated_tokens_per_second == pytest.approx(44.4444444444)


def test_throughput_budget_exposes_long_trace_cost():
    short = throughput_budget(
        output_slots=240,
        candidates_per_output=2,
        generated_tokens_per_candidate=4000,
        wallclock_hours=12.0,
    )
    long = throughput_budget(
        output_slots=240,
        candidates_per_output=2,
        generated_tokens_per_candidate=20_000,
        wallclock_hours=12.0,
    )
    assert long.required_generated_tokens_per_second == pytest.approx(
        5 * short.required_generated_tokens_per_second
    )


def test_invalid_budgets_fail_closed():
    with pytest.raises(ValueError):
        memory_budget(total_weight_gib=0, tensor_parallel_size=4, gpu_memory_gib=24)
    with pytest.raises(ValueError):
        throughput_budget(
            output_slots=0,
            candidates_per_output=2,
            generated_tokens_per_candidate=100,
            wallclock_hours=12,
        )
