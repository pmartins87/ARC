import pytest

from arcsolver.scoring import make_identity_submission, score_submission


def test_second_attempt_can_score():
    solutions = {"task": [[[1, 2], [3, 4]]]}
    submission = {
        "task": [
            {
                "attempt_1": [[0, 0], [0, 0]],
                "attempt_2": [[1, 2], [3, 4]],
            }
        ]
    }
    score = score_submission(submission, solutions)
    assert score.correct_outputs == 1
    assert score.total_outputs == 1
    assert score.accuracy == 1.0


def test_accuracy_is_per_test_output():
    solutions = {"task": [[[1]], [[2]]]}
    submission = {
        "task": [
            {"attempt_1": [[1]], "attempt_2": [[0]]},
            {"attempt_1": [[0]], "attempt_2": [[0]]},
        ]
    }
    score = score_submission(submission, solutions)
    assert score.correct_outputs == 1
    assert score.total_outputs == 2
    assert score.accuracy == 0.5


def test_requires_both_attempts():
    with pytest.raises(ValueError, match="both attempts"):
        score_submission({"task": [{"attempt_1": [[1]]}]}, {"task": [[[1]]]})


def test_identity_submission_shape():
    challenges = {
        "task": {
            "train": [],
            "test": [{"input": [[1, 2]]}, {"input": [[3], [4]]}],
        }
    }
    submission = make_identity_submission(challenges)
    assert len(submission["task"]) == 2
    assert submission["task"][0]["attempt_1"] == [[1, 2]]
    assert submission["task"][1]["attempt_2"] == [[3], [4]]
