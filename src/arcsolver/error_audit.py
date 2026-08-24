from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from typing import Any, Mapping

from .compare import Solutions, Submission, diagnose_submission
from .io import Grid

TaskInputs = Mapping[str, list[Grid]]


def _shape(grid: Grid) -> tuple[int, int]:
    return len(grid), len(grid[0])


def _colors(grid: Grid) -> set[int]:
    return {value for row in grid for value in row}


@dataclass(frozen=True)
class StructuralAudit:
    solver: str
    total_outputs: int
    correct_outputs_pass2: int
    same_shape_targets: int
    different_shape_targets: int
    correct_same_shape_targets: int
    correct_different_shape_targets: int
    at_least_one_attempt_right_shape: int
    both_attempts_wrong_shape: int
    shape_right_but_content_wrong: int
    output_color_subset_of_input: int
    output_introduces_color: int
    correct_subset_color_targets: int
    correct_color_introducing_targets: int
    second_attempt_rescues: int
    duplicate_attempt_outputs: int
    solved_task_ids: tuple[str, ...]
    unsolved_task_ids: tuple[str, ...]
    failure_reason_counts: tuple[tuple[str, int], ...]

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result.update(
            {
                "pass_at_2": self.correct_outputs_pass2 / self.total_outputs
                if self.total_outputs
                else 0.0,
                "same_shape_pass_at_2": self.correct_same_shape_targets / self.same_shape_targets
                if self.same_shape_targets
                else 0.0,
                "different_shape_pass_at_2": self.correct_different_shape_targets
                / self.different_shape_targets
                if self.different_shape_targets
                else 0.0,
                "subset_color_pass_at_2": self.correct_subset_color_targets
                / self.output_color_subset_of_input
                if self.output_color_subset_of_input
                else 0.0,
                "color_introducing_pass_at_2": self.correct_color_introducing_targets
                / self.output_introduces_color
                if self.output_introduces_color
                else 0.0,
                "right_shape_candidate_rate": self.at_least_one_attempt_right_shape / self.total_outputs
                if self.total_outputs
                else 0.0,
                "failure_reason_counts": dict(self.failure_reason_counts),
            }
        )
        return result


def audit_submission_structure(
    name: str,
    submission: Submission,
    solutions: Solutions,
    test_inputs: TaskInputs,
) -> StructuralAudit:
    diagnostics = diagnose_submission(name, submission, solutions)
    if set(test_inputs) != set(solutions):
        missing = sorted(set(solutions) - set(test_inputs))
        extra = sorted(set(test_inputs) - set(solutions))
        raise ValueError(f"test-input task-id mismatch: missing={missing[:5]} extra={extra[:5]}")

    same_shape = different_shape = 0
    correct_same = correct_different = 0
    right_shape_candidate = wrong_shape_both = shape_right_content_wrong = 0
    subset_color = introduces_color = 0
    correct_subset = correct_introduces = 0
    second_rescues = 0
    duplicate_attempts = 0
    solved_task_ids: list[str] = []
    unsolved_task_ids: list[str] = []
    failure_reasons: Counter[str] = Counter()

    for task_id, truths in solutions.items():
        inputs = test_inputs[task_id]
        predictions = submission[task_id]
        if len(inputs) != len(truths):
            raise ValueError(
                f"{task_id}: expected {len(truths)} test inputs, got {len(inputs)}"
            )

        task_solved = True
        for input_grid, truth, prediction in zip(inputs, truths, predictions):
            attempt1 = prediction["attempt_1"]
            attempt2 = prediction["attempt_2"]
            pass1 = attempt1 == truth
            pass2 = pass1 or attempt2 == truth
            second_rescues += int((not pass1) and attempt2 == truth)
            duplicate_attempts += int(attempt1 == attempt2)
            task_solved &= pass2

            input_shape = _shape(input_grid)
            truth_shape = _shape(truth)
            target_same_shape = input_shape == truth_shape
            same_shape += int(target_same_shape)
            different_shape += int(not target_same_shape)
            correct_same += int(pass2 and target_same_shape)
            correct_different += int(pass2 and not target_same_shape)

            candidate_shape_match = _shape(attempt1) == truth_shape or _shape(attempt2) == truth_shape
            right_shape_candidate += int(candidate_shape_match)
            wrong_shape_both += int(not candidate_shape_match)
            shape_right_content_wrong += int(candidate_shape_match and not pass2)

            input_colors = _colors(input_grid)
            truth_colors = _colors(truth)
            is_subset = truth_colors <= input_colors
            subset_color += int(is_subset)
            introduces_color += int(not is_subset)
            correct_subset += int(pass2 and is_subset)
            correct_introduces += int(pass2 and not is_subset)

            if not pass2:
                if not candidate_shape_match:
                    failure_reasons["both_attempts_wrong_shape"] += 1
                else:
                    failure_reasons["shape_right_content_wrong"] += 1

        (solved_task_ids if task_solved else unsolved_task_ids).append(task_id)

    return StructuralAudit(
        solver=name,
        total_outputs=diagnostics.total_outputs,
        correct_outputs_pass2=diagnostics.correct_outputs_pass2,
        same_shape_targets=same_shape,
        different_shape_targets=different_shape,
        correct_same_shape_targets=correct_same,
        correct_different_shape_targets=correct_different,
        at_least_one_attempt_right_shape=right_shape_candidate,
        both_attempts_wrong_shape=wrong_shape_both,
        shape_right_but_content_wrong=shape_right_content_wrong,
        output_color_subset_of_input=subset_color,
        output_introduces_color=introduces_color,
        correct_subset_color_targets=correct_subset,
        correct_color_introducing_targets=correct_introduces,
        second_attempt_rescues=second_rescues,
        duplicate_attempt_outputs=duplicate_attempts,
        solved_task_ids=tuple(sorted(solved_task_ids)),
        unsolved_task_ids=tuple(sorted(unsolved_task_ids)),
        failure_reason_counts=tuple(sorted(failure_reasons.items())),
    )
