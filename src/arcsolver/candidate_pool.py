from __future__ import annotations

from dataclasses import asdict, dataclass
from statistics import median
from typing import Any, Iterable, Mapping, Sequence

from .io import Grid, validate_grid

CanonicalGrid = tuple[tuple[int, ...], ...]


def canonical_grid(grid: Grid) -> CanonicalGrid:
    validate_grid(grid)
    return tuple(tuple(int(value) for value in row) for row in grid)


def _mean(values: Sequence[float]) -> float:
    if not values:
        raise ValueError("mean requires at least one value")
    return sum(values) / len(values)


def _quantile_nearest_rank(values: Sequence[int], q: float) -> int:
    if not values:
        return 0
    if not 0.0 <= q <= 1.0:
        raise ValueError("q must be between 0 and 1")
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, int((len(ordered) - 1) * q + 0.5)))
    return ordered[index]


@dataclass
class CandidateEvidence:
    solution: Grid
    votes: int
    beam_scores: list[float]
    score_aug: list[list[float]]
    first_seen: int


@dataclass(frozen=True)
class SelectorSummary:
    pass_at_2: float
    exact_hits: int
    truth_in_pool_not_top2: int
    correct_rank_median: float | None
    correct_rank_p90: int | None


@dataclass(frozen=True)
class CandidatePoolAudit:
    total_outputs: int
    processed_outputs: int
    missing_outputs: int
    raw_samples: int
    unique_candidates: int
    mean_unique_candidates_per_processed_output: float
    median_unique_candidates_per_processed_output: float
    p90_unique_candidates_per_processed_output: int
    duplicate_sample_fraction: float
    oracle_exact_hits: int
    oracle_pass_at_2: float
    selectors: dict[str, SelectorSummary]
    selector_gap: dict[str, float]
    selector_unique_rescues: dict[str, int]
    top2_disagreement_outputs: int
    top2_disagreement_rate: float
    truth_in_pool_outputs: list[str]
    missing_output_keys: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def candidate_features(samples: Iterable[Mapping[str, Any]]) -> list[CandidateEvidence]:
    """Aggregate repeated Qwen/NVARC-lineage candidate samples by exact grid.

    This mirrors the public `tune_selection.py` evidence fields: candidate vote
    count, DFS/beam score observations, and augmentation-rescoring values. The
    first-seen index is retained so score ties reproduce Python's stable-sort
    behavior from the public reference implementation.
    """
    by_grid: dict[CanonicalGrid, CandidateEvidence] = {}
    for index, sample in enumerate(samples):
        if "solution" not in sample or "beam_score" not in sample or "score_aug" not in sample:
            raise ValueError("candidate sample requires solution, beam_score and score_aug")
        solution = sample["solution"]
        validate_grid(solution)
        aug_scores = [float(value) for value in sample["score_aug"]]
        if not aug_scores:
            raise ValueError("score_aug must contain at least one score")
        key = canonical_grid(solution)
        if key not in by_grid:
            by_grid[key] = CandidateEvidence(
                solution=solution,
                votes=0,
                beam_scores=[],
                score_aug=[],
                first_seen=index,
            )
        evidence = by_grid[key]
        evidence.votes += 1
        evidence.beam_scores.append(float(sample["beam_score"]))
        evidence.score_aug.append(aug_scores)
    return list(by_grid.values())


def rank_score_kgmon(candidates: Sequence[CandidateEvidence]) -> list[Grid]:
    """Public NVARC/KGMon-style vote minus augmentation-NLL selector."""
    scored: list[tuple[float, int, Grid]] = []
    for candidate in candidates:
        sample_aug_means = [_mean(scores) for scores in candidate.score_aug]
        score = float(candidate.votes) - _mean(sample_aug_means)
        scored.append((score, candidate.first_seen, candidate.solution))
    # Stable-source semantics: score only. Python sort preserves first-seen ties.
    scored.sort(key=lambda item: item[0], reverse=True)
    return [grid for _, _, grid in scored]


def rank_score_full_probmul_3(
    candidates: Sequence[CandidateEvidence], *, baseline: float = 3.0
) -> list[Grid]:
    """Public `score_full_probmul_3` selector from the 2026 Qwen mirror."""
    scored: list[tuple[float, int, Grid]] = []
    for candidate in candidates:
        inference_score = sum(baseline - value for value in candidate.beam_scores)
        augmentation_score = _mean(
            [sum(baseline - value for value in scores) for scores in candidate.score_aug]
        )
        scored.append((inference_score + augmentation_score, candidate.first_seen, candidate.solution))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [grid for _, _, grid in scored]


SELECTORS = {
    "score_kgmon": rank_score_kgmon,
    "score_full_probmul_3": rank_score_full_probmul_3,
}


def _expected_output_keys(solutions: Mapping[str, list[Grid]]) -> list[str]:
    keys: list[str] = []
    for task_id in sorted(solutions):
        for index in range(len(solutions[task_id])):
            keys.append(f"{task_id}_{index}")
    return keys


def _truth_for_key(output_key: str, solutions: Mapping[str, list[Grid]]) -> Grid:
    try:
        task_id, index_text = output_key.rsplit("_", 1)
        index = int(index_text)
        return solutions[task_id][index]
    except (ValueError, KeyError, IndexError) as exc:
        raise ValueError(f"invalid output key for supplied solutions: {output_key}") from exc


def _rank_of_truth(ordered: Sequence[Grid], truth: Grid) -> int | None:
    truth_key = canonical_grid(truth)
    for index, guess in enumerate(ordered, start=1):
        if canonical_grid(guess) == truth_key:
            return index
    return None


def audit_candidate_pools(
    pools: Mapping[str, Sequence[Mapping[str, Any]]],
    solutions: Mapping[str, list[Grid]],
    *,
    selector_names: Sequence[str] = ("score_kgmon", "score_full_probmul_3"),
) -> CandidatePoolAudit:
    """Measure candidate-discovery ceiling separately from two-attempt selection.

    Missing inference-output keys are counted as misses, so timeout/coverage loss
    remains visible in the final denominator instead of being silently dropped.
    Extra keys are rejected because they indicate dataset/provenance mismatch.
    """
    unknown_selectors = [name for name in selector_names if name not in SELECTORS]
    if unknown_selectors:
        raise ValueError(f"unknown selectors: {unknown_selectors}")
    if not selector_names:
        raise ValueError("at least one selector is required")

    expected = _expected_output_keys(solutions)
    expected_set = set(expected)
    extra = sorted(set(pools) - expected_set)
    if extra:
        raise ValueError(f"candidate dump contains unknown output keys: {extra[:5]}")

    total_outputs = len(expected)
    selector_hits = {name: 0 for name in selector_names}
    selector_missed_pool_truth = {name: 0 for name in selector_names}
    selector_ranks: dict[str, list[int]] = {name: [] for name in selector_names}
    selector_hit_sets: dict[str, set[str]] = {name: set() for name in selector_names}
    selector_top2: dict[str, dict[str, set[CanonicalGrid]]] = {
        name: {} for name in selector_names
    }

    oracle_hits = 0
    processed_outputs = 0
    raw_samples = 0
    unique_candidates = 0
    candidate_counts: list[int] = []
    truth_in_pool_outputs: list[str] = []
    missing_output_keys: list[str] = []

    for output_key in expected:
        samples = list(pools.get(output_key, []))
        truth = _truth_for_key(output_key, solutions)
        validate_grid(truth)
        if not samples:
            missing_output_keys.append(output_key)
            continue

        processed_outputs += 1
        raw_samples += len(samples)
        candidates = candidate_features(samples)
        unique_candidates += len(candidates)
        candidate_counts.append(len(candidates))

        truth_key = canonical_grid(truth)
        truth_in_pool = any(canonical_grid(candidate.solution) == truth_key for candidate in candidates)
        if truth_in_pool:
            oracle_hits += 1
            truth_in_pool_outputs.append(output_key)

        for name in selector_names:
            ordered = SELECTORS[name](candidates)
            top2 = ordered[:2]
            selector_top2[name][output_key] = {canonical_grid(grid) for grid in top2}
            rank = _rank_of_truth(ordered, truth)
            if rank is not None:
                selector_ranks[name].append(rank)
            if rank is not None and rank <= 2:
                selector_hits[name] += 1
                selector_hit_sets[name].add(output_key)
            elif truth_in_pool:
                selector_missed_pool_truth[name] += 1

    selector_summaries: dict[str, SelectorSummary] = {}
    selector_gap: dict[str, float] = {}
    for name in selector_names:
        ranks = selector_ranks[name]
        pass_at_2 = selector_hits[name] / total_outputs if total_outputs else 0.0
        selector_summaries[name] = SelectorSummary(
            pass_at_2=pass_at_2,
            exact_hits=selector_hits[name],
            truth_in_pool_not_top2=selector_missed_pool_truth[name],
            correct_rank_median=float(median(ranks)) if ranks else None,
            correct_rank_p90=_quantile_nearest_rank(ranks, 0.90) if ranks else None,
        )
        selector_gap[name] = (oracle_hits / total_outputs if total_outputs else 0.0) - pass_at_2

    selector_unique_rescues: dict[str, int] = {}
    for name in selector_names:
        other_hits: set[str] = set()
        for other_name in selector_names:
            if other_name != name:
                other_hits |= selector_hit_sets[other_name]
        selector_unique_rescues[name] = len(selector_hit_sets[name] - other_hits)

    disagreement_outputs = 0
    if len(selector_names) >= 2:
        first = selector_names[0]
        for output_key in expected:
            if output_key not in selector_top2[first]:
                continue
            baseline_top2 = selector_top2[first][output_key]
            if any(
                selector_top2[other].get(output_key, set()) != baseline_top2
                for other in selector_names[1:]
            ):
                disagreement_outputs += 1

    candidate_mean = (
        sum(candidate_counts) / len(candidate_counts) if candidate_counts else 0.0
    )
    duplicate_fraction = (
        1.0 - unique_candidates / raw_samples if raw_samples else 0.0
    )
    oracle_pass = oracle_hits / total_outputs if total_outputs else 0.0

    return CandidatePoolAudit(
        total_outputs=total_outputs,
        processed_outputs=processed_outputs,
        missing_outputs=total_outputs - processed_outputs,
        raw_samples=raw_samples,
        unique_candidates=unique_candidates,
        mean_unique_candidates_per_processed_output=candidate_mean,
        median_unique_candidates_per_processed_output=(
            float(median(candidate_counts)) if candidate_counts else 0.0
        ),
        p90_unique_candidates_per_processed_output=_quantile_nearest_rank(candidate_counts, 0.90),
        duplicate_sample_fraction=duplicate_fraction,
        oracle_exact_hits=oracle_hits,
        oracle_pass_at_2=oracle_pass,
        selectors=selector_summaries,
        selector_gap=selector_gap,
        selector_unique_rescues=selector_unique_rescues,
        top2_disagreement_outputs=disagreement_outputs,
        top2_disagreement_rate=(
            disagreement_outputs / processed_outputs if processed_outputs else 0.0
        ),
        truth_in_pool_outputs=truth_in_pool_outputs,
        missing_output_keys=missing_output_keys,
    )
