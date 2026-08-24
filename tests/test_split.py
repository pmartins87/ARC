from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "make_split.py"
spec = spec_from_file_location("make_split", MODULE_PATH)
assert spec and spec.loader
make_split = module_from_spec(spec)
spec.loader.exec_module(make_split)


def test_evaluation_profile_exact_counts_for_120_tasks():
    task_ids = [f"task_{i:03d}" for i in range(120)]
    result = make_split.split_ids(task_ids, "evaluation", "seed")
    assert len(result["development"]) == 60
    assert len(result["validation"]) == 30
    assert len(result["heldout"]) == 30
    assert len(set().union(*map(set, result.values()))) == 120


def test_training_profile_exact_counts_for_1000_tasks():
    task_ids = [f"task_{i:04d}" for i in range(1000)]
    result = make_split.split_ids(task_ids, "training", "seed")
    assert len(result["development"]) == 700
    assert len(result["validation"]) == 150
    assert len(result["heldout"]) == 150


def test_split_is_deterministic_and_input_order_independent():
    task_ids = [f"task_{i:03d}" for i in range(120)]
    a = make_split.split_ids(task_ids, "evaluation", "arc-2026-v1")
    b = make_split.split_ids(list(reversed(task_ids)), "evaluation", "arc-2026-v1")
    assert a == b


def test_seed_changes_assignment():
    task_ids = [f"task_{i:03d}" for i in range(120)]
    a = make_split.split_ids(task_ids, "evaluation", "a")
    b = make_split.split_ids(task_ids, "evaluation", "b")
    assert a != b
