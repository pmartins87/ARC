from __future__ import annotations

from arcsolver.nvarc_protocol import (
    TRANSDUCTIVE_SYSTEM_PROMPT,
    build_messages,
    execute_transform,
    extract_python_code,
    parse_transductive_grid,
    render_problem_text,
    strip_thinking,
    verify_response,
)


def sample_train():
    return [
        {"input": [[0, 1], [0, 0]], "output": [[1, 0], [0, 0]]},
        {"input": [[0, 0, 1]], "output": [[1, 0, 0]]},
    ]


def test_public_transductive_prompt_layout() -> None:
    user = render_problem_text(sample_train(), [[0, 0], [1, 0]])
    assert user.startswith("Please solve this ARC-AGI problem:\n\nTrain Example 1:\n\nInput:\n01\n00")
    assert "\nOutput:\n10\n00\n" in user
    assert user.endswith("\n\nTest Input:\n00\n10\n\n")
    messages = build_messages(sample_train(), [[0, 0], [1, 0]], mode="transductive")
    assert messages[0] == {"role": "system", "content": TRANSDUCTIVE_SYSTEM_PROMPT}
    assert messages[1]["content"] == user


def test_strip_thinking_matches_public_verifier_behavior() -> None:
    assert strip_thinking("before<think>hidden\ntrace</think>after") == "beforeafter"


def test_parse_boxed_whitespace_grid() -> None:
    text = "<think>reasoning</think>\\boxed{1 0\n0 1}"
    assert parse_transductive_grid(text) == [[1, 0], [0, 1]]


def test_parse_rejects_ragged_and_compact_response() -> None:
    assert parse_transductive_grid("\\boxed{1 0\n1}") is None
    # NVIDIA's released response parser expects whitespace-separated integer tokens.
    assert parse_transductive_grid("\\boxed{10\n01}") is None


def test_extract_python_code_prefers_last_python_block() -> None:
    text = """
```python
def transform(grid):
    return [[0]]
```
noise
```python
def transform(grid):
    return grid
```
"""
    assert extract_python_code(text) == "def transform(grid):\n    return grid"


def test_execute_transform_success() -> None:
    code = "def transform(grid):\n    return [row[::-1] for row in grid]"
    predicted, error = execute_transform(code, [[1, 2], [3, 4]], timeout_seconds=2)
    assert error is None
    assert predicted == [[2, 1], [4, 3]]


def test_execute_transform_blocks_banned_import() -> None:
    code = "import os\ndef transform(grid):\n    return grid"
    predicted, error = execute_transform(code, [[1]], timeout_seconds=2)
    assert predicted is None
    assert error is not None
    assert "not allowed" in error


def test_execute_transform_requires_transform() -> None:
    predicted, error = execute_transform("x = 1", [[1]], timeout_seconds=2)
    assert predicted is None
    assert error is not None
    assert "transform" in error


def test_verify_transductive_exact_reward() -> None:
    result = verify_response(
        "\\boxed{1 0\n0 1}",
        test_input=[[0, 0], [0, 0]],
        expected_output=[[1, 0], [0, 1]],
        mode="transductive",
    )
    assert result.extraction_successful
    assert result.exact_match
    assert result.reward == 1.0


def test_verify_inductive_exact_reward() -> None:
    result = verify_response(
        "```python\ndef transform(grid):\n    return [[9]]\n```",
        test_input=[[1]],
        expected_output=[[9]],
        mode="inductive",
        timeout_seconds=2,
    )
    assert result.extraction_successful
    assert result.exact_match
    assert result.reward == 1.0


def test_wrong_valid_output_has_zero_reward_without_extraction_error() -> None:
    result = verify_response(
        "\\boxed{0}",
        test_input=[[1]],
        expected_output=[[1]],
        mode="transductive",
    )
    assert result.extraction_successful
    assert not result.exact_match
    assert result.reward == 0.0
