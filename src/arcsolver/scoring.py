from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .io import Grid, validate_grid


@dataclass(frozen=True)
class Score:
    correct_outputs: int
    total_outputs: int

    @property
    def accuracy(self) -> float:
        return self.correct_outputs / self.total_outputs if self.total_outputs else 0.0


def _same_grid(a: Grid, b: Grid) -> bool:
    return a == b


def score_submission(
    submission: Mapping[str, list[Mapping[str, Grid]]],
    solutions: Mapping[str, list[Grid]],
    *,
    validate: bool = True,
) -> Score:
    """Score ARC-AGI-2 predictions using the official pass@2 semantics.

    For each task test output, either ``attempt_1`` or ``attempt_2`` must match
    the ground-truth grid exactly. Accuracy is averaged over task test outputs,
    not merely over task IDs.
    """
    if set(submission) != set(solutions):
        missing = sorted(set(solutions) - set(submission))
        extra = sorted(set(submission) - set(solutions))
        raise ValueError(f"task-id mismatch: missing={missing[:5]} extra={extra[:5]}")

    correct = 0
    total = 0
    for task_id, truth_outputs in solutions.items():
        predictions = submission[task_id]
        if len(predictions) != len(truth_outputs):
            raise ValueError(
                f"{task_id}: expected {len(truth_outputs)} test outputs, "
                f"got {len(predictions)}"
            )
        for index, (prediction, truth) in enumerate(zip(predictions, truth_outputs)):
            if "attempt_1" not in prediction or "attempt_2" not in prediction:
                raise ValueError(f"{task_id}[{index}]: both attempts are required")
            a1 = prediction["attempt_1"]
            a2 = prediction["attempt_2"]
            if validate:
                validate_grid(a1)
                validate_grid(a2)
                validate_grid(truth)
            correct += int(_same_grid(a1, truth) or _same_grid(a2, truth))
            total += 1

    return Score(correct_outputs=correct, total_outputs=total)


def make_identity_submission(challenges: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    """Create a schema-valid identity baseline for infrastructure smoke tests."""
    result: dict[str, Any] = {}
    for task_id, task in challenges.items():
        outputs = []
        for test_pair in task["test"]:
            grid = test_pair["input"]
            outputs.append({"attempt_1": grid, "attempt_2": grid})
        result[task_id] = outputs
    return result
