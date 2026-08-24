from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import combinations
from typing import Any, Mapping

from .compare import Solutions, Submission, diagnose_submission

OutputKey = tuple[str, int]


@dataclass(frozen=True)
class SolverCoverage:
    name: str
    correct_outputs: int
    total_outputs: int
    unique_outputs_vs_rest: int
    leave_one_out_union_loss: int
    runtime_seconds: float | None

    @property
    def pass_at_2(self) -> float:
        return self.correct_outputs / self.total_outputs if self.total_outputs else 0.0

    @property
    def unique_gain(self) -> float:
        return self.unique_outputs_vs_rest / self.total_outputs if self.total_outputs else 0.0

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result.update(
            {
                "pass_at_2": self.pass_at_2,
                "unique_gain": self.unique_gain,
            }
        )
        return result


@dataclass(frozen=True)
class GreedyStep:
    rank: int
    solver: str
    newly_covered_outputs: int
    cumulative_covered_outputs: int
    cumulative_runtime_seconds: float | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class BudgetChoice:
    budget_seconds: float
    solvers: tuple[str, ...]
    runtime_seconds: float
    covered_outputs: int
    total_outputs: int

    @property
    def oracle_pass_at_2(self) -> float:
        return self.covered_outputs / self.total_outputs if self.total_outputs else 0.0

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["oracle_pass_at_2"] = self.oracle_pass_at_2
        return result


@dataclass(frozen=True)
class PortfolioReport:
    solvers: tuple[SolverCoverage, ...]
    oracle_union_correct_outputs: int
    total_outputs: int
    greedy_order: tuple[GreedyStep, ...]
    budget_choices: tuple[BudgetChoice, ...]

    @property
    def oracle_union_pass_at_2(self) -> float:
        return self.oracle_union_correct_outputs / self.total_outputs if self.total_outputs else 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "solvers": [solver.to_dict() for solver in self.solvers],
            "oracle_union_correct_outputs": self.oracle_union_correct_outputs,
            "total_outputs": self.total_outputs,
            "oracle_union_pass_at_2": self.oracle_union_pass_at_2,
            "greedy_order": [step.to_dict() for step in self.greedy_order],
            "budget_choices": [choice.to_dict() for choice in self.budget_choices],
        }


def _correct_set(submission: Submission, solutions: Solutions) -> set[OutputKey]:
    # diagnose_submission performs strict task/output/grid validation first.
    diagnose_submission("solver", submission, solutions)
    result: set[OutputKey] = set()
    for task_id, truths in solutions.items():
        for index, (prediction, truth) in enumerate(zip(submission[task_id], truths)):
            if prediction["attempt_1"] == truth or prediction["attempt_2"] == truth:
                result.add((task_id, index))
    return result


def _total_outputs(solutions: Solutions) -> int:
    return sum(len(outputs) for outputs in solutions.values())


def _normalize_runtimes(
    names: tuple[str, ...], runtimes_seconds: Mapping[str, float] | None
) -> dict[str, float] | None:
    if runtimes_seconds is None:
        return None
    if set(runtimes_seconds) != set(names):
        missing = sorted(set(names) - set(runtimes_seconds))
        extra = sorted(set(runtimes_seconds) - set(names))
        raise ValueError(f"runtime-name mismatch: missing={missing} extra={extra}")
    normalized = {name: float(runtimes_seconds[name]) for name in names}
    if any(value < 0 for value in normalized.values()):
        raise ValueError("runtime values must be non-negative")
    return normalized


def _greedy_coverage_order(
    correct_sets: Mapping[str, set[OutputKey]],
    runtimes: Mapping[str, float] | None,
) -> tuple[GreedyStep, ...]:
    remaining = set(correct_sets)
    covered: set[OutputKey] = set()
    elapsed = 0.0
    steps: list[GreedyStep] = []

    while remaining:
        ranked: list[tuple[float, int, str]] = []
        for name in remaining:
            new_count = len(correct_sets[name] - covered)
            if runtimes is None:
                utility = float(new_count)
            else:
                cost = runtimes[name]
                utility = float("inf") if cost == 0 and new_count else (new_count / cost if cost else 0.0)
            ranked.append((utility, new_count, name))

        # Maximize utility, then raw new coverage; use lexical name as deterministic tie-break.
        best_utility = max(item[0] for item in ranked)
        utility_tied = [item for item in ranked if item[0] == best_utility]
        best_new = max(item[1] for item in utility_tied)
        name = min(item[2] for item in utility_tied if item[1] == best_new)

        new_outputs = correct_sets[name] - covered
        covered |= correct_sets[name]
        if runtimes is not None:
            elapsed += runtimes[name]
        steps.append(
            GreedyStep(
                rank=len(steps) + 1,
                solver=name,
                newly_covered_outputs=len(new_outputs),
                cumulative_covered_outputs=len(covered),
                cumulative_runtime_seconds=elapsed if runtimes is not None else None,
            )
        )
        remaining.remove(name)

    return tuple(steps)


def best_subset_under_budget(
    correct_sets: Mapping[str, set[OutputKey]],
    runtimes_seconds: Mapping[str, float],
    budget_seconds: float,
    total_outputs: int,
) -> BudgetChoice:
    if budget_seconds < 0:
        raise ValueError("budget must be non-negative")
    names = tuple(sorted(correct_sets))
    if len(names) > 20:
        raise ValueError("exact budget optimizer is limited to 20 solver components")

    best_names: tuple[str, ...] = ()
    best_runtime = 0.0
    best_covered: set[OutputKey] = set()

    for count in range(len(names) + 1):
        for subset in combinations(names, count):
            runtime = sum(runtimes_seconds[name] for name in subset)
            if runtime > budget_seconds:
                continue
            covered: set[OutputKey] = set()
            for name in subset:
                covered |= correct_sets[name]

            candidate_key = (len(covered), -runtime, -len(subset), tuple(reversed(subset)))
            best_key = (
                len(best_covered),
                -best_runtime,
                -len(best_names),
                tuple(reversed(best_names)),
            )
            if candidate_key > best_key:
                best_names = subset
                best_runtime = runtime
                best_covered = covered

    return BudgetChoice(
        budget_seconds=float(budget_seconds),
        solvers=best_names,
        runtime_seconds=best_runtime,
        covered_outputs=len(best_covered),
        total_outputs=total_outputs,
    )


def analyze_portfolio(
    submissions: Mapping[str, Submission],
    solutions: Solutions,
    *,
    runtimes_seconds: Mapping[str, float] | None = None,
    budgets_seconds: tuple[float, ...] = (),
) -> PortfolioReport:
    if not submissions:
        raise ValueError("at least one solver submission is required")

    names = tuple(sorted(submissions))
    runtimes = _normalize_runtimes(names, runtimes_seconds)
    if budgets_seconds and runtimes is None:
        raise ValueError("budget analysis requires runtimes_seconds")

    correct_sets = {name: _correct_set(submissions[name], solutions) for name in names}
    total = _total_outputs(solutions)
    union_all: set[OutputKey] = set().union(*correct_sets.values())

    coverage_rows: list[SolverCoverage] = []
    for name in names:
        union_rest: set[OutputKey] = set()
        for other in names:
            if other != name:
                union_rest |= correct_sets[other]
        unique = correct_sets[name] - union_rest
        leave_one_out_loss = len(union_all) - len(union_rest)
        coverage_rows.append(
            SolverCoverage(
                name=name,
                correct_outputs=len(correct_sets[name]),
                total_outputs=total,
                unique_outputs_vs_rest=len(unique),
                leave_one_out_union_loss=leave_one_out_loss,
                runtime_seconds=runtimes[name] if runtimes is not None else None,
            )
        )

    budget_choices: list[BudgetChoice] = []
    if runtimes is not None:
        for budget in sorted(set(float(value) for value in budgets_seconds)):
            budget_choices.append(
                best_subset_under_budget(correct_sets, runtimes, budget, total)
            )

    return PortfolioReport(
        solvers=tuple(coverage_rows),
        oracle_union_correct_outputs=len(union_all),
        total_outputs=total,
        greedy_order=_greedy_coverage_order(correct_sets, runtimes),
        budget_choices=tuple(budget_choices),
    )
