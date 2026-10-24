"""The type-label check accepts exactly one type label."""

from __future__ import annotations

import importlib.util
from pathlib import Path

_SCRIPT = (
    Path(__file__).resolve().parents[1]
    / ".github"
    / "scripts"
    / "check_type_label.py"
)
_spec = importlib.util.spec_from_file_location("check_type_label", _SCRIPT)
assert _spec is not None and _spec.loader is not None
check_type_label = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_type_label)


def test_no_type_label_fails() -> None:
    error = check_type_label.type_label_error(["good first issue"])
    assert error is not None
    assert "found none" in error


def test_two_type_labels_fail() -> None:
    error = check_type_label.type_label_error(["bug", "chore"])
    assert error is not None
    assert "bug" in error
    assert "chore" in error


def test_one_type_label_passes() -> None:
    assert check_type_label.type_label_error(["bug"]) is None
    assert (
        check_type_label.type_label_error(
            ["documentation", "good first issue"]
        )
        is None
    )


def test_label_objects_use_the_name_field() -> None:
    names = check_type_label.label_names(
        [{"name": "enhancement"}, {"name": "help wanted"}]
    )
    assert check_type_label.type_label_error(names) is None
