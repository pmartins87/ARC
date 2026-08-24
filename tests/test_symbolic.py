from arcsolver.symbolic import fit_hypotheses, solve_task


def test_global_rotation_is_inferred():
    task = {
        "train": [
            {
                "input": [[1, 0, 0], [0, 0, 0]],
                "output": [[0, 1], [0, 0], [0, 0]],
            },
            {
                "input": [[0, 2, 0], [0, 0, 0]],
                "output": [[0, 0], [0, 2], [0, 0]],
            },
        ],
        "test": [{"input": [[0, 0, 3], [0, 0, 0]]}],
    }
    predictions, hypotheses = solve_task(task)
    assert hypotheses
    assert predictions[0]["attempt_1"] == [[0, 0], [0, 0], [0, 3]]


def test_crop_non_background_is_inferred():
    task = {
        "train": [
            {
                "input": [[0, 0, 0, 0], [0, 2, 2, 0], [0, 2, 2, 0]],
                "output": [[2, 2], [2, 2]],
            },
            {
                "input": [[0, 3, 0], [0, 3, 0], [0, 0, 0]],
                "output": [[3], [3]],
            },
        ],
        "test": [{"input": [[0, 0, 4, 0], [0, 0, 4, 0], [0, 0, 4, 0]]}],
    }
    predictions, _ = solve_task(task)
    assert predictions[0]["attempt_1"] == [[4], [4], [4]]


def test_largest_component_is_inferred():
    task = {
        "train": [
            {
                "input": [[2, 0, 0, 3, 3], [0, 0, 0, 3, 3]],
                "output": [[3, 3], [3, 3]],
            },
            {
                "input": [[4, 4, 4, 0, 5], [4, 4, 4, 0, 0]],
                "output": [[4, 4, 4], [4, 4, 4]],
            },
        ],
        "test": [{"input": [[6, 0, 7, 7], [0, 0, 7, 7], [0, 0, 7, 7]]}],
    }
    predictions, hypotheses = solve_task(task)
    assert any(hypothesis.family == "component" for hypothesis in hypotheses)
    assert predictions[0]["attempt_1"] == [[7, 7], [7, 7], [7, 7]]


def test_cell_scaling_is_inferred():
    task = {
        "train": [
            {"input": [[1, 2]], "output": [[1, 1, 2, 2], [1, 1, 2, 2]]},
            {"input": [[3], [4]], "output": [[3, 3], [3, 3], [4, 4], [4, 4]]},
        ],
        "test": [{"input": [[5, 6], [7, 8]]}],
    }
    predictions, _ = solve_task(task)
    assert predictions[0]["attempt_1"] == [
        [5, 5, 6, 6],
        [5, 5, 6, 6],
        [7, 7, 8, 8],
        [7, 7, 8, 8],
    ]


def test_constant_output_is_available_as_a_fallback_hypothesis():
    task = {
        "train": [
            {"input": [[1, 0]], "output": [[9]]},
            {"input": [[0, 2]], "output": [[9]]},
        ],
        "test": [{"input": [[3, 4]]}],
    }
    hypotheses = fit_hypotheses(task)
    assert any(hypothesis.family == "constant" for hypothesis in hypotheses)
    predictions, _ = solve_task(task)
    assert [[9]] in (predictions[0]["attempt_1"], predictions[0]["attempt_2"])
