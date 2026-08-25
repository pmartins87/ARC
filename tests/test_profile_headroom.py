from __future__ import annotations

import pytest

from arcsolver.profile_headroom import assess_profile_headroom


def test_l4_vs_lightning_bf16_tp4_profile_floor() -> None:
    report = assess_profile_headroom(
        gpu_vram_gb=24.0,
        profile_min_vram_gb=20.0,
        gpu_count=4,
        profile_min_gpu_count=4,
        gpu_compute_capability=8.9,
        required_compute_capability=8.0,
    )
    assert report.memory_floor_pass is True
    assert report.gpu_count_pass is True
    assert report.architecture_pass is True
    assert report.overall_floor_pass is True
    assert report.per_gpu_headroom_gb == pytest.approx(4.0)
    assert report.per_gpu_headroom_fraction == pytest.approx(1 / 6)
    assert report.aggregate_headroom_gb == pytest.approx(16.0)


def test_below_profile_floor_fails() -> None:
    report = assess_profile_headroom(
        gpu_vram_gb=18.0,
        profile_min_vram_gb=20.0,
        gpu_count=4,
        profile_min_gpu_count=4,
        gpu_compute_capability=8.9,
        required_compute_capability=8.0,
    )
    assert report.memory_floor_pass is False
    assert report.overall_floor_pass is False


def test_architecture_floor_can_fail_independently() -> None:
    report = assess_profile_headroom(
        gpu_vram_gb=24.0,
        profile_min_vram_gb=20.0,
        gpu_count=4,
        profile_min_gpu_count=4,
        gpu_compute_capability=7.5,
        required_compute_capability=8.0,
    )
    assert report.memory_floor_pass is True
    assert report.architecture_pass is False
    assert report.overall_floor_pass is False


def test_unknown_architecture_is_reported_not_assumed() -> None:
    report = assess_profile_headroom(
        gpu_vram_gb=24.0,
        profile_min_vram_gb=20.0,
        gpu_count=4,
        profile_min_gpu_count=4,
    )
    assert report.architecture_pass is None
    assert report.overall_floor_pass is True


@pytest.mark.parametrize(
    "kwargs",
    [
        {"gpu_vram_gb": 0},
        {"profile_min_vram_gb": 0},
        {"gpu_count": 0},
        {"profile_min_gpu_count": 0},
        {"gpu_compute_capability": 0},
        {"required_compute_capability": 0},
    ],
)
def test_invalid_inputs(kwargs: dict[str, float | int]) -> None:
    base = dict(
        gpu_vram_gb=24.0,
        profile_min_vram_gb=20.0,
        gpu_count=4,
        profile_min_gpu_count=4,
        gpu_compute_capability=8.9,
        required_compute_capability=8.0,
    )
    base.update(kwargs)
    with pytest.raises(ValueError):
        assess_profile_headroom(**base)
