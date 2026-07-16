"""XGIC CLI application framework (parser, plugins, dispatch)."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from importlib.metadata import entry_points

from xgic.cli import __version__
from xgic.cli.core.environment import EnvironmentContext
from xgic.cli.utils.output import print_error, print_info, print_panel

CommandFunc = Callable[..., int | None]
ENTRY_POINT_GROUP = "xgic.cli.commands"


@dataclass(frozen=True)
class CommandContext:
    """Runtime context passed to registered command handlers.

    Domain modules (``xgic.cli.dev``, ``xgic.cli.payload``, …) may attach
    their own controllers after loading; core only guarantees environment.
    """

    env: EnvironmentContext
    args: argparse.Namespace


def _run_info(ctx: CommandContext) -> int:
    """Built-in: show environment detection summary."""
    env = ctx.env
    body = (
        f"Environment: {env.describe()}\n"
        f"Type: {env.env_type.name}\n"
        f"Remote: {env.is_remote}\n"
        f"Project root: {env.project_root or '(not detected)'}\n"
        f"Host-only commands safe: {env.is_host_only_command_safe()}"
    )
    print_panel("XGIC CLI environment", body)
    return 0


def register_builtin_commands(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Register built-in core commands (not domain modules)."""
    info = subparsers.add_parser(
        "info",
        help="Show detected execution environment (core diagnostic)",
    )
    info.set_defaults(func=_run_info)


def load_plugin_commands(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Load optional domain modules via entry points ``xgic.cli.commands``."""
    try:
        selected = entry_points(group=ENTRY_POINT_GROUP)
    except TypeError:  # pragma: no cover
        eps = entry_points()
        selected = eps.get(ENTRY_POINT_GROUP, [])  # type: ignore[attr-defined]

    for ep in selected:
        try:
            register = ep.load()
            register(subparsers)
        except Exception as exc:  # pragma: no cover - plugin isolation
            print_error(f"Failed to load plugin {ep.name!r}: {exc}")


def build_parser(
    *,
    include_plugins: bool = True,
) -> argparse.ArgumentParser:
    """Build the top-level argument parser for XGIC CLI."""
    parser = argparse.ArgumentParser(
        prog="xgic",
        description=(
            "XGIC CLI - modular command-line framework for XGIC tools "
            "and environment orchestration."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Domain modules register subcommands via entry points "
            f"({ENTRY_POINT_GROUP}). "
            "Dev Container: xgic/dev-cli · Payload CMS: xgic/payload-cms-cli. "
            "Architecture: "
            "https://github.com/xgic/ai/blob/main/docs/adr/0005-modular-xgic-cli-and-retirement-of-xde.md"
        ),
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Re-raise unexpected errors with full traceback",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
        metavar="COMMAND",
    )
    register_builtin_commands(subparsers)
    if include_plugins:
        load_plugin_commands(subparsers)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the XGIC CLI entrypoint."""
    argv_list = list(argv) if argv is not None else None
    parser = build_parser()
    args = parser.parse_args(argv_list)

    if args.command is None:
        parser.print_help()
        return 0

    func: CommandFunc | None = getattr(args, "func", None)
    if func is None:
        parser.error(f"unknown command {args.command!r}")
        return 2

    try:
        env = EnvironmentContext.detect()
        ctx = CommandContext(env=env, args=args)

        # Handlers may accept CommandContext or (args, env=...)
        try:
            result = func(ctx)
        except TypeError:
            result = func(args, env=env)

        if result is None:
            return 0
        return int(result)
    except KeyboardInterrupt:
        print_info("Interrupted by user")
        return 130
    except Exception as exc:
        print_error(f"Unexpected error: {exc}")
        if getattr(args, "debug", False) or "--debug" in (
            argv_list or sys.argv
        ):
            raise
        return 1
