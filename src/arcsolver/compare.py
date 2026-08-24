from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from .io import Grid, validate_grid

Submission = Mapping[str, list[Mapping[str, Grid]]]
Solutions = Mapping[str, list[Grid]]


@dataclass(frozen=True)
class SolverDiagnostics:
    name: str
    correct_outputs_pass1: int
    correct_outputs_pass2: int
    total_outputs: int
    solved_tasks_pass1: int
    solved_tasks_pass2: int
    total_tasks: int
    second_attempt_rescues: int
    duplicate_attempt_outputs: int

    @property
    def pass1(self) -> float:
        return self.correct_outputs_pass1 / self.total_outputs if self.total_outputs else 0.0

    @property
    def pass2(self) -> float:
        return self.correct_outputs_pass2 / self.total_outputs if self.total_outputs else 0.0

    @property
    def task_pass1(self) -> float:
        return self.solved_tasks_pass1 / self.total_tasks if self.total_tasks else 0.0

    @property
    def task_pass2(self) -> float:
        return self.solved_tasks_pass2 / self.total_tasks if self.total_tasks else 0.0

    @property
    def duplicate_attempt_rate(self) -> float:
        return self.duplicate_attempt_outputs / self.total_outputs if self.total_outputs else 0.0

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result.update(
            {
                "pass_at_1": self.pass1,
                "pass_at_2": self.pass2,
                "task_pass_at_1": self.task_pass1,
                "task_pass_at_2": self.task_pass2,
                "duplicate_attempt_rate": self.duplicate_attempt_rate,
            }
        )
        return result


@dataclass(frozen=True)
class Complementarity:
    solver_a: SolverDiagnostics
    solver_b: SolverDiagnostics
    both_correct_outputs: int
    only_a_correct_outputs: int
    only_b_correct_outputs: int
    neither_correct_outputs: int
    oracle_union_correct_outputs: int
    total_outputs: int
    both_solved_tasks: int
    only_a_solved_tasks: int
    only_b_solved_tasks: int
    neither_solved_tasks: int
    oracle_union_solved_tasks: int
    total_tasks: int
    first_attempt_disagreements: int

    @property
    def oracle_union_pass2(self) -> float:
        return self.oracle_union_correct_outputs / self.total_outputs if self.total_outputs else 0.0

    @property
    def oracle_union_task_pass2(self) -> float:
        return self.oracle_union_solved_tasks / self.total_tasks if self.total_tasks else 0.0

    @property
    def correct_set_jaccard(self) -> float:
        union = self.both_correct_outputs + self.only_a_correct_outputs + self.only_b_correct_outputs
        return self.both_correct_outputs / union if union else 0.0

    @property
    def marginal_union_gain_over_best(self) -> float:
        best = max(self.solver_a.correct_outputs_pass2, self.solver_b.correct_outputs_pass2)
        return (self.oracle_union_correct_outputs - best) / self.total_outputs if self.total_outputs else 0.0

    @property
    def first_attempt_disagreement_rate(self) -> float:
        return self.first_attempt_disagreements / self.total_outputs if self.total_outputs else 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "solver_a": self.solver_a.to_dict(),
            "solver_b": self.solver_b.to_dict(),
            "outputs": {
                "both_correct": self.both_correct_outputs,
                "only_a_correct": self.only_a_correct_outputs,
                "only_b_correct": self.only_b_correct_outputs,
                "neither_correct": self.neither_correct_outputs,
                "oracle_union_correct": self.oracle_union_correct_outputs,
                "total": self.total_outputs,
                "oracle_union_pass_at_2": self.oracle_union_pass2,
                "correct_set_jaccard": self.correct_set_jaccard,
                "marginal_union_gain_over_best": self.marginal_union_gain_over_best,
                "first_attempt_disagreements": self.first_attempt_disagreements,
                "first_attempt_disagreement_rate": self.first_attempt_disagreement_rate,
            },
            "tasks": {
                "both_solved": self.both_solved_tasks,
                "only_a_solved": self.only_a_solved_tasks,
                "only_b_solved": self.only_b_solved_tasks,
                "neither_solved": self.neither_solved_tasks,
                "oracle_union_solved": self.oracle_union_solved_tasks,
                "total": self.total_tasks,
                "oracle_union_task_pass_at_2": self.oracle_union_task_pass2,
            },
        }


def _validate_submission(submission: Submission, solutions: Solutions) -> None:
    if set(submission) != set(solutions):
        missing = sorted(set(solutions) - set(submission))
        extra = sorted(set(submission) - set(solutions))
        raise ValueError(f"task-id mismatch: missing={missing[:5]} extra={extra[:5]}")

    for task_id, truth_outputs in solutions.items():
        predictions = submission[task_id]
        if len(predictions) != len(truth_outputs):
            raise ValueError(
                f"{task_id}: expected {len(truth_outputs)} test outputs, got {len(predictions)}"
            )
        for index, (prediction, truth) in enumerate(zip(predictions, truth_outputs)):
            if set(prediction) < {"attempt_1", "attempt_2"}:
                raise ValueError(f"{task_id}[{index}]: both attempts are required")
            validate_grid(prediction["attempt_1"])
            validate_grid(prediction["attempt_2"])
            validate_grid(truth)


def _output_flags(prediction: Mapping[str, Grid], truth: Grid) -> tuple[bool, bool, bool]:
    a1 = prediction["attempt_1"] == truth
    a2 = prediction["attempt_2"] == truth
    return a1, a1 or a2, prediction["attempt_1"] == prediction["attempt_2"]


def diagnose_submission(name: str, submission: Submission, solutions: Solutions) -> SolverDiagnostics:
    _validate_submission(submission, solutions)

    correct_pass1 = 0
    correct_pass2 = 0
    solved_tasks_pass1 = 0
    solved_tasks_pass2 = 0
    rescues = 0
    duplicates = 0
    total_outputs = 0

    for task_id, truth_outputs in solutions.items():
        task_pass1 = True
        task_pass2 = True
        for prediction, truth in zip(submission[task_id], truth_outputs):
            p1, p2, duplicate = _output_flags(prediction, truth)
            correct_pass1 += int(p1)
            correct_pass2 += int(p2)
            rescues += int((not p1) and p2)
            duplicates += int(duplicate)
            total_outputs += 1
            task_pass1 &= p1
            task_pass2 &= p2
        solved_tasks_pass1 += int(task_pass1)
        solved_tasks_pass2 += int(task_pass2)

    return SolverDiagnostics(
        name=name,
        correct_outputs_pass1=correct_pass1,
        correct_outputs_pass2=correct_pass2,
        total_outputs=total_outputs,
        solved_tasks_pass1=solved_tasks_pass1,
        solved_tasks_pass2=solved_tasks_pass2,
        total_tasks=len(solutions),
        second_attempt_rescues=rescues,
        duplicate_attempt_outputs=duplicates,
    )


def compare_submissions(
    name_a: str,
    submission_a: Submission,
    name_b: str,
    submission_b: Submission,
    solutions: Solutions,
) -> Complementarity:
    diag_a = diagnose_submission(name_a, submission_a, solutions)
    diag_b = diagnose_submission(name_b, submission_b, solutions)

    both = only_a = only_b = neither = disagreements = 0
    both_tasks = only_a_tasks = only_b_tasks = neither_tasks = 0

    for task_id, truth_outputs in solutions.items():
        task_a = True
        task_b = True
        for pred_a, pred_b, truth in zip(
            submission_a[task_id], submission_b[task_id], truth_outputs
        ):
            _, pass2_a, _ = _output_flags(pred_a, truth)
            _, pass2_b, _ = _output_flags(pred_b, truth)
            if pass2_a and pass2_b:
                both += 1
            elif pass2_a:
                only_a += 1
            elif pass2_b:
                only_b += 1
            else:
                neither += 1
            disagreements += int(pred_a["attempt_1"] != pred_b["attempt_1"])
            task_a &= pass2_a
            task_b &= pass2_b

        if task_a and task_b:
            both_tasks += 1
        elif task_a:
            only_a_tasks += 1
        elif task_b:
            only_b_tasks += 1
        else:
            neither_tasks += 1

    return Complementarity(
        solver_a=diag_a,
        solver_b=diag_b,
        both_correct_outputs=both,
        only_a_correct_outputs=only_a,
        only_b_correct_outputs=only_b,
        neither_correct_outputs=neither,
        oracle_union_correct_outputs=both + only_a + only_b,
        total_outputs=diag_a.total_outputs,
        both_solved_tasks=both_tasks,
        only_a_solved_tasks=only_a_tasks,
        only_b_solved_tasks=only_b_tasks,
        neither_solved_tasks=neither_tasks,
        oracle_union_solved_tasks=both_tasks + only_a_tasks + only_b_tasks,
        total_tasks=len(solutions),
        first_attempt_disagreements=disagreements,
    )
