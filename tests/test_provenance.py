from arcsolver.provenance import (
    compare_fingerprints,
    fingerprint_challenges,
    submission_schema_fingerprint,
)


def _task(test_count, marker=0):
    return {
        "train": [{"input": [[marker]], "output": [[marker]]}],
        "test": [{"input": [[marker]]} for _ in range(test_count)],
    }


def test_fingerprint_is_order_independent_but_content_sensitive():
    a = {"bbbb0000": _task(2, 1), "aaaa0000": _task(1, 2)}
    b = {"aaaa0000": _task(1, 2), "bbbb0000": _task(2, 1)}
    c = {"aaaa0000": _task(1, 9), "bbbb0000": _task(2, 1)}

    fa = fingerprint_challenges(a)
    fb = fingerprint_challenges(b)
    fc = fingerprint_challenges(c)

    assert fa == fb
    assert fa.task_count == 2
    assert fa.output_slots == 3
    assert fa.test_counts == {"aaaa0000": 1, "bbbb0000": 2}
    assert fa.task_ids_sha256 == fc.task_ids_sha256
    assert fa.test_count_signature_sha256 == fc.test_count_signature_sha256
    assert fa.canonical_challenges_sha256 != fc.canonical_challenges_sha256


def test_compare_catches_same_task_ids_with_changed_test_counts():
    reference = fingerprint_challenges(
        {"aaaa0000": _task(1), "bbbb0000": _task(2)}
    )
    candidate = fingerprint_challenges(
        {"aaaa0000": _task(2), "bbbb0000": _task(1)}
    )

    diff = compare_fingerprints(reference, candidate)

    assert diff.task_ids_match
    assert diff.output_slots_match
    assert not diff.compatible_schema
    assert diff.test_count_mismatches == {
        "aaaa0000": (1, 2),
        "bbbb0000": (2, 1),
    }


def test_compare_reports_missing_and_extra_ids():
    reference = fingerprint_challenges(
        {"aaaa0000": _task(1), "bbbb0000": _task(1)}
    )
    candidate = fingerprint_challenges(
        {"bbbb0000": _task(1), "cccc0000": _task(1)}
    )

    diff = compare_fingerprints(reference, candidate)

    assert not diff.task_ids_match
    assert diff.missing_task_ids == ("aaaa0000",)
    assert diff.extra_task_ids == ("cccc0000",)
    assert not diff.compatible_schema


def test_submission_schema_fingerprint_matches_challenge_test_counts():
    challenges = {
        "aaaa0000": _task(1),
        "bbbb0000": _task(2),
    }
    submission = {
        "aaaa0000": [{"attempt_1": [[0]], "attempt_2": [[0]]}],
        "bbbb0000": [
            {"attempt_1": [[0]], "attempt_2": [[0]]},
            {"attempt_1": [[0]], "attempt_2": [[0]]},
        ],
    }

    challenge_fp = fingerprint_challenges(challenges)
    submission_fp = submission_schema_fingerprint(submission)
    diff = compare_fingerprints(challenge_fp, submission_fp)

    assert diff.compatible_schema
    assert challenge_fp.task_ids_sha256 == submission_fp.task_ids_sha256
    assert (
        challenge_fp.test_count_signature_sha256
        == submission_fp.test_count_signature_sha256
    )
    # Full content hashes should differ because submission schema has no inputs/training pairs.
    assert not diff.canonical_hash_match


def test_invalid_empty_inputs_fail_closed():
    for value in ({}, []):
        try:
            fingerprint_challenges(value)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid challenges should fail closed")

    try:
        submission_schema_fingerprint({"aaaa0000": []})
    except ValueError:
        pass
    else:
        raise AssertionError("empty submission outputs should fail closed")
