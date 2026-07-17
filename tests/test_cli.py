"""Tests for the XGIC CLI entrypoint and framework."""

from __future__ import annotations

import pytest

from xgic.cli import __version__
from xgic.cli.app import build_parser, main


def test_version_constant() -> None:
    assert __version__ == "0.2.0rc1"


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
    assert build_parser(include_plugins=False).prog == "xgic"


def test_info_command(capsys: pytest.CaptureFixture[str]) -> None:
    rc = main(["info"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "Environment" in out or "Local host" in out or "Dev Container" in out


def test_help_mentions_domain_modules(capsys: pytest.CaptureFixture[str]) -> None:
    main([])
    out = capsys.readouterr().out
    assert "xgic.cli.commands" in out or "entry points" in out.lower() or "Domain" in out
