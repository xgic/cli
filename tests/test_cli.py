"""Tests for the XGIC CLI entrypoint and framework."""

from __future__ import annotations

import argparse

import pytest

from xgic.cli import __version__
from xgic.cli.app import CommandContext, _call_handler, build_parser, main
from xgic.cli.core.environment import EnvironmentContext


def test_version_constant() -> None:
    assert __version__ == "0.2.3rc1"


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


def test_namespace_handler_receives_parsed_arguments() -> None:
    seen: dict[str, object] = {}

    def restore(args: argparse.Namespace) -> int:
        seen["archive"] = args.archive
        seen["yes"] = args.yes
        return 4

    parsed = argparse.Namespace(archive="/tmp/a.tar.zst", yes=True)
    ctx = CommandContext(env=EnvironmentContext.detect(), args=parsed)
    assert _call_handler(restore, ctx, parsed) == 4
    assert seen == {"archive": "/tmp/a.tar.zst", "yes": True}


def test_context_handler_receives_command_context() -> None:
    seen: dict[str, str] = {}

    def info(ctx: CommandContext) -> int:
        seen["type"] = type(ctx).__name__
        return 0

    parsed = argparse.Namespace()
    ctx = CommandContext(env=EnvironmentContext.detect(), args=parsed)
    assert _call_handler(info, ctx, parsed) == 0
    assert seen["type"] == "CommandContext"


def test_info_command(capsys: pytest.CaptureFixture[str]) -> None:
    rc = main(["info"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "Environment" in out or "Local host" in out or "Dev Container" in out


def test_help_has_no_architecture_epilogue(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main([]) == 0
    out = capsys.readouterr().out
    assert "usage: xgic" in out
    assert "Available commands" in out or "COMMAND" in out
    assert "xgic.cli.commands" not in out
    assert "retirement-of-xde" not in out
    parser = build_parser(include_plugins=False)
    assert parser.epilog in (None, "")
