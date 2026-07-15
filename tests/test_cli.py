"""Tests for the XGIC CLI scaffold entrypoint."""

from __future__ import annotations

import pytest

from xgic.cli import __version__
from xgic.cli.__main__ import build_parser, main


def test_version_constant() -> None:
    assert __version__ == "0.1.0"


def test_help_exits_zero() -> None:
    assert main([]) == 0


def test_version_flag(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    out = capsys.readouterr().out
    assert "xgic" in out
    assert __version__ in out


def test_unknown_command_errors() -> None:
    with pytest.raises(SystemExit) as exc:
        main(["not-a-command"])
    assert exc.value.code == 2


def test_parser_prog() -> None:
    assert build_parser().prog == "xgic"
