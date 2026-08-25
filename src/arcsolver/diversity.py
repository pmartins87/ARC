from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import combinations
from typing import Any, Iterable, Sequence

from .io import Grid, validate_grid


def grid_shape(grid: Grid) -> tuple[int, int]:
    validate_grid(grid)
    return len(grid), len(grid[0])


def color_signature(grid: Grid) -> tuple[int, ...]:
    validate_grid(grid)
    return tuple(sorted({int(value) for row in grid for value in row}))


def exact_duplicate(a: Grid, b: Grid) -> bool:
    validate_grid(a)
    validate_grid(b)
    return a == b


def normalized_cell_disagreement(a: Grid, b: Grid) -> float | None:
    """Fraction of unequal cells for same-shape grids; None when shapes differ."""
    validate_grid(a)
    validate_grid(b)
    if grid_shape(a) != grid_shape(b):
        return None
    total = len(a) * len(a[0])
    different = sum(
        1
        for row_a, row_b in zip(a, b)
        for value_a, value_b in zip(row_a, row_b)
        if value_a != value_b
    )
    return different / total


@dataclass(frozen=True)
class PairDiversity:
    exact_duplicate: bool
    same_shape: bool
    same_color_signature: bool
    normalized_cell_disagreement: float | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def compare_grids(a: Grid, b: Grid) -> PairDiversity:
    return PairDiversity(
        exact_duplicate=exact_duplicate(a, b),
        same_shape=grid_shape(a) == grid_shape(b),
        same_color_signature=color_signature(a) == color_signature(b),
        normalized_cell_disagreement=normalized_cell_disagreement(a, b),
    )


@dataclass(frozen=True)
class CandidateDiversitySummary:
    candidates: int
    unique_exact_candidates: int
    exact_duplicate_fraction: float
    distinct_shapes: int
    modal_shape_fraction: float
    distinct_color_signatures: int
    modal_color_signature_fraction: float
    same_shape_pair_fraction: float
    mean_same_shape_cell_disagreement: float | None
    median_same_shape_cell_disagreement: float | None
    near_duplicate_pair_fraction: float | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _median(values: Sequence[float]) -> float:
    ordered = sorted(values)
    n = len(ordered)
    mid = n // 2
    if n % 2:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2.0


def _modal_fraction(values: Sequence[Any]) -> float:
    if not values:
        return 0.0
    counts: dict[Any, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return max(counts.values()) / len(values)


def summarize_candidate_diversity(
    grids: Iterable[Grid], *, near_duplicate_threshold: float = 0.10
) -> CandidateDiversitySummary:
    """Describe candidate diversity without assuming that diversity is beneficial.

    `near_duplicate_threshold` is applied only to same-shape pairs. A value of
    0.10 means pairs differing in at most 10% of cells count as near-duplicates.
    The summary is diagnostic only and deliberately contains no ranking policy.
    """
    if not 0.0 <= near_duplicate_threshold <= 1.0:
        raise ValueError("near_duplicate_threshold must be in [0, 1]")

    candidates = list(grids)
    for grid in candidates:
        validate_grid(grid)

    count = len(candidates)
    if count == 0:
        return CandidateDiversitySummary(
            candidates=0,
            unique_exact_candidates=0,
            exact_duplicate_fraction=0.0,
            distinct_shapes=0,
            modal_shape_fraction=0.0,
            distinct_color_signatures=0,
            modal_color_signature_fraction=0.0,
            same_shape_pair_fraction=0.0,
            mean_same_shape_cell_disagreement=None,
            median_same_shape_cell_disagreement=None,
            near_duplicate_pair_fraction=None,
        )

    canonical = [tuple(tuple(row) for row in grid) for grid in candidates]
    unique_exact = len(set(canonical))
    duplicate_fraction = 1.0 - unique_exact / count
    shapes = [grid_shape(grid) for grid in candidates]
    colors = [color_signature(grid) for grid in candidates]

    pair_count = 0
    same_shape_pairs = 0
    same_shape_disagreements: list[float] = []
    near_duplicates = 0
    for left, right in combinations(candidates, 2):
        pair_count += 1
        disagreement = normalized_cell_disagreement(left, right)
        if disagreement is None:
            continue
        same_shape_pairs += 1
        same_shape_disagreements.append(disagreement)
        if disagreement <= near_duplicate_threshold:
            near_duplicates += 1

    return CandidateDiversitySummary(
        candidates=count,
        unique_exact_candidates=unique_exact,
        exact_duplicate_fraction=duplicate_fraction,
        distinct_shapes=len(set(shapes)),
        modal_shape_fraction=_modal_fraction(shapes),
        distinct_color_signatures=len(set(colors)),
        modal_color_signature_fraction=_modal_fraction(colors),
        same_shape_pair_fraction=(same_shape_pairs / pair_count if pair_count else 0.0),
        mean_same_shape_cell_disagreement=(
            sum(same_shape_disagreements) / len(same_shape_disagreements)
            if same_shape_disagreements
            else None
        ),
        median_same_shape_cell_disagreement=(
            _median(same_shape_disagreements) if same_shape_disagreements else None
        ),
        near_duplicate_pair_fraction=(
            near_duplicates / same_shape_pairs if same_shape_pairs else None
        ),
    )


@dataclass(frozen=True)
class AttemptDiversitySummary:
    outputs: int
    exact_duplicate_outputs: int
    exact_duplicate_rate: float
    different_shape_outputs: int
    different_shape_rate: float
    same_shape_outputs: int
    mean_same_shape_cell_disagreement: float | None
    median_same_shape_cell_disagreement: float | None
    different_color_signature_outputs: int
    different_color_signature_rate: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def summarize_attempt_pairs(pairs: Iterable[tuple[Grid, Grid]]) -> AttemptDiversitySummary:
    """Aggregate how different attempt_1 and attempt_2 are across outputs."""
    pair_list = list(pairs)
    comparisons = [compare_grids(left, right) for left, right in pair_list]
    outputs = len(comparisons)
    exact_duplicates = sum(item.exact_duplicate for item in comparisons)
    different_shapes = sum(not item.same_shape for item in comparisons)
    same_shape = outputs - different_shapes
    disagreements = [
        item.normalized_cell_disagreement
        for item in comparisons
        if item.normalized_cell_disagreement is not None
    ]
    different_colors = sum(not item.same_color_signature for item in comparisons)

    return AttemptDiversitySummary(
        outputs=outputs,
        exact_duplicate_outputs=exact_duplicates,
        exact_duplicate_rate=(exact_duplicates / outputs if outputs else 0.0),
        different_shape_outputs=different_shapes,
        different_shape_rate=(different_shapes / outputs if outputs else 0.0),
        same_shape_outputs=same_shape,
        mean_same_shape_cell_disagreement=(
            sum(disagreements) / len(disagreements) if disagreements else None
        ),
        median_same_shape_cell_disagreement=(
            _median(disagreements) if disagreements else None
        ),
        different_color_signature_outputs=different_colors,
        different_color_signature_rate=(different_colors / outputs if outputs else 0.0),
    )
