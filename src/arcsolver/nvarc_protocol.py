from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import re
import subprocess
import sys
from typing import Any, Literal, Mapping, Sequence

Grid = list[list[int]]
AgentMode = Literal["transductive", "inductive"]

# Verbatim from NVIDIA NeMo Gym's public transductive example dataset.
TRANSDUCTIVE_SYSTEM_PROMPT = (
    "Find the common rule that maps an input grid to an output grid, given the examples below.\n"
    "After reasoning you must provide only the output and nothing else.\n"
    "Output format: \\boxed{solution} where solution is an array of rows separated by newlines, values by spaces.\n"
)

# The public HF python_inductive viewer exposes the opening wording but truncates
# the full system prompt in its table UI. We therefore keep the inductive contract
# explicit and versioned rather than pretending this string is byte-identical to
# NVIDIA's released dataset prompt. Verifier semantics below *are* source-faithful.
INDUCTIVE_SYSTEM_PROMPT_V1 = (
    "You are an expert at solving ARC-AGI (Abstraction and Reasoning Corpus) puzzles by writing Python code.\n"
    "Analyze the input-output examples and return Python code defining transform(grid).\n"
    "The transform function must accept a 2D list of integers and return the transformed 2D list.\n"
    "Return the code in a ```python fenced block.\n"
)

_BANNED_BUILTINS = frozenset(
    {
        "open",
        "input",
        "breakpoint",
        "help",
        "license",
        "credits",
        "copyright",
        "exit",
        "quit",
        "vars",
        "dir",
        "globals",
        "locals",
    }
)

_BANNED_MODULES = frozenset(
    {
        "os",
        "subprocess",
        "shutil",
        "pathlib",
        "builtins",
        "socket",
        "urllib",
        "requests",
        "http",
        "ftplib",
        "smtplib",
        "pickle",
        "shelve",
        "marshal",
        "importlib",
        "pkgutil",
        "ctypes",
        "multiprocessing",
        "threading",
        "signal",
        "tempfile",
        "fileinput",
        "codecs",
        "pty",
        "fcntl",
        "resource",
        "syslog",
        "asyncio",
        "concurrent",
    }
)


@dataclass(frozen=True)
class VerificationResult:
    mode: AgentMode
    extraction_successful: bool
    exact_match: bool
    predicted_output: Grid | None
    error: str | None = None

    @property
    def reward(self) -> float:
        return 1.0 if self.exact_match else 0.0

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["reward"] = self.reward
        return payload


def validate_grid(grid: Any) -> bool:
    if not isinstance(grid, list) or not grid:
        return False
    if not all(isinstance(row, list) and row for row in grid):
        return False
    width = len(grid[0])
    if any(len(row) != width for row in grid):
        return False
    return all(isinstance(cell, int) and 0 <= cell <= 9 for row in grid for cell in row)


def compact_grid_text(grid: Sequence[Sequence[int]]) -> str:
    """Render grids like NVIDIA's public NVARC prompt examples (one digit per cell)."""
    if not validate_grid([list(row) for row in grid]):
        raise ValueError("grid must be rectangular with integer cells 0..9")
    return "\n".join("".join(str(cell) for cell in row) for row in grid)


def render_problem_text(train: Sequence[Mapping[str, Grid]], test_input: Grid) -> str:
    """Match the public NVARC user-message layout for visible ARC examples."""
    parts = ["Please solve this ARC-AGI problem:\n"]
    for index, pair in enumerate(train, start=1):
        parts.append(
            f"\nTrain Example {index}:\n\n"
            f"Input:\n{compact_grid_text(pair['input'])}\n\n"
            f"Output:\n{compact_grid_text(pair['output'])}\n"
        )
    parts.append(f"\n\nTest Input:\n{compact_grid_text(test_input)}\n\n")
    return "".join(parts)


def build_messages(
    train: Sequence[Mapping[str, Grid]],
    test_input: Grid,
    *,
    mode: AgentMode,
) -> list[dict[str, str]]:
    if mode not in ("transductive", "inductive"):
        raise ValueError(f"unsupported mode: {mode}")
    system = TRANSDUCTIVE_SYSTEM_PROMPT if mode == "transductive" else INDUCTIVE_SYSTEM_PROMPT_V1
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": render_problem_text(train, test_input)},
    ]


def strip_thinking(text: str) -> str:
    """Mirror NVIDIA NVARC: remove complete <think>...</think> blocks."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def parse_transductive_grid(text: str) -> Grid | None:
    """Mirror NVIDIA's integer-palette Board.from_text path.

    This intentionally expects whitespace-separated integer tokens in the model
    response, as the released NVARC system prompt instructs. Prompt inputs are
    compact digit rows; response parsing is a separate contract.
    """
    text = strip_thinking(text)
    boxed_match = re.search(r"\\boxed\{(.+)\}", text, re.DOTALL)
    if boxed_match:
        text = boxed_match.group(1)

    text = re.sub(r"[^\s\w]", "", text)
    allowed = {str(i) for i in range(10)}
    text = re.sub(r"\b\w+\b", lambda match: match.group(0) if match.group(0) in allowed else "", text)

    board: Grid = []
    try:
        for line in text.split("\n"):
            if line.strip():
                board.append([int(token) for token in line.split()])
    except ValueError:
        return None
    return board if validate_grid(board) else None


def extract_python_code(text: str) -> str | None:
    """Mirror NVIDIA NVARC's code-extraction precedence."""
    text = strip_thinking(text)
    blocks = re.findall(r"```python\s*\n(.*?)```", text, re.DOTALL)
    if blocks:
        return blocks[-1].strip()
    blocks = re.findall(r"```\s*\n(.*?)```", text, re.DOTALL)
    if blocks:
        return blocks[-1].strip()
    if "def transform" in text:
        return text.strip()
    return None


def _sandbox_script(code: str, input_grid: Grid) -> str:
    """Build a compact subprocess sandbox derived from NVIDIA NeMo Gym NVARC.

    It is a compatibility sandbox, not a hardened hostile-code isolation layer.
    The outer process timeout remains the final mechanical guard.
    """
    banned_builtins = repr(sorted(_BANNED_BUILTINS))
    banned_modules = repr(sorted(_BANNED_MODULES))
    return f'''
import json
import sys

_BANNED_BUILTINS = frozenset({banned_builtins})
_BANNED_MODULES = frozenset({banned_modules})
_original_import = __builtins__["__import__"] if isinstance(__builtins__, dict) else __builtins__.__import__

def _restricted_import(name, globals=None, locals=None, fromlist=(), level=0):
    if name.split(".")[0] in _BANNED_MODULES:
        raise ImportError(f"Import of {{name!r}} is not allowed in sandbox")
    return _original_import(name, globals, locals, fromlist, level)

if isinstance(__builtins__, dict):
    _safe = {{k: v for k, v in __builtins__.items() if k not in _BANNED_BUILTINS}}
else:
    _safe = {{k: getattr(__builtins__, k) for k in dir(__builtins__) if k not in _BANNED_BUILTINS and not k.startswith("_")}}
_safe["__import__"] = _restricted_import
_safe["__builtins__"] = _safe

try:
    namespace = {{"__builtins__": _safe}}
    exec({code!r}, namespace)
    if "transform" not in namespace or not callable(namespace["transform"]):
        raise ValueError("No callable 'transform' function defined in code")
    result = namespace["transform"]({json.dumps(input_grid)})
    if hasattr(result, "detach") and hasattr(result, "cpu"):
        result = result.detach().cpu().tolist()
    elif hasattr(result, "tolist"):
        result = result.tolist()
    print(json.dumps({{"success": True, "result": result}}))
except Exception as exc:
    print(json.dumps({{"success": False, "error": f"{{type(exc).__name__}}: {{str(exc)[:500]}}"}}))
'''


def execute_transform(code: str, input_grid: Grid, *, timeout_seconds: float = 30.0) -> tuple[Grid | None, str | None]:
    if not validate_grid(input_grid):
        return None, "invalid input grid"
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive")

    try:
        completed = subprocess.run(
            [sys.executable, "-I", "-c", _sandbox_script(code, input_grid)],
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None, "TimeoutError: transform execution exceeded timeout"

    if completed.returncode != 0:
        return None, f"SubprocessError: returncode={completed.returncode}"
    output = completed.stdout.strip()
    if not output:
        return None, "SubprocessError: empty stdout"
    try:
        payload = json.loads(output.splitlines()[-1])
    except json.JSONDecodeError:
        return None, "SubprocessError: non-JSON stdout"
    if not payload.get("success"):
        return None, str(payload.get("error") or "transform failed")
    result = payload.get("result")
    return (result, None) if validate_grid(result) else (None, "InvalidGrid: transform returned invalid grid")


def verify_response(
    response_text: str,
    *,
    test_input: Grid,
    expected_output: Grid,
    mode: AgentMode,
    timeout_seconds: float = 30.0,
) -> VerificationResult:
    if not validate_grid(expected_output):
        raise ValueError("expected_output must be a valid ARC grid")

    if mode == "transductive":
        predicted = parse_transductive_grid(response_text)
        error = None if predicted is not None else "grid extraction failed"
    elif mode == "inductive":
        code = extract_python_code(response_text)
        if code is None:
            predicted, error = None, "python extraction failed"
        else:
            predicted, error = execute_transform(code, test_input, timeout_seconds=timeout_seconds)
    else:
        raise ValueError(f"unsupported mode: {mode}")

    extracted = predicted is not None
    return VerificationResult(
        mode=mode,
        extraction_successful=extracted,
        exact_match=bool(extracted and predicted == expected_output),
        predicted_output=predicted,
        error=error,
    )
