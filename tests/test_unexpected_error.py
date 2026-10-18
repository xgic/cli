"""Unexpected errors name their type even when the message is empty."""

from xgic.cli.app import unexpected_error_text


def test_memory_error_names_its_type() -> None:
    text = unexpected_error_text(MemoryError())
    assert text.startswith("Unexpected error: MemoryError:")
