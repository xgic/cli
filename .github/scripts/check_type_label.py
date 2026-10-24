"""Fail unless an issue or pull request has exactly one type label.

The check reads label names from ``LABELS_JSON``. It does not add a label.
"""

from __future__ import annotations

import json
import os
import sys

TYPE_LABELS = frozenset(
    {"bug", "enhancement", "documentation", "standards", "chore"}
)


def label_names(items: object) -> list[str]:
    """Return label names from a JSON list of strings or label objects."""
    if not isinstance(items, list):
        return []
    names: list[str] = []
    for item in items:
        if isinstance(item, str):
            names.append(item)
        elif isinstance(item, dict) and isinstance(item.get("name"), str):
            names.append(item["name"])
    return names


def type_label_error(names: list[str]) -> str | None:
    """Return an error when ``names`` does not contain exactly one type label."""
    found = [name for name in names if name in TYPE_LABELS]
    if len(found) == 1:
        return None
    allowed = ", ".join(sorted(TYPE_LABELS))
    if not found:
        return f"exactly one type label is required ({allowed}); found none"
    return (
        "exactly one type label is required "
        f"({allowed}); found {', '.join(found)}"
    )


def main() -> int:
    """Exit 0 for one type label and 1 otherwise."""
    try:
        payload = json.loads(os.environ.get("LABELS_JSON", "[]"))
    except json.JSONDecodeError as exc:
        print(f"LABELS_JSON is not valid JSON: {exc}", file=sys.stderr)
        return 1
    error = type_label_error(label_names(payload))
    if error is None:
        return 0
    print(error, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
