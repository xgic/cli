"""Console entrypoint for the ``xgic`` command."""

from __future__ import annotations

import argparse
import sys

from xgic.cli import __version__


def build_parser() -> argparse.ArgumentParser:
    """Build the top-level argument parser for XGIC CLI."""
    parser = argparse.ArgumentParser(
        prog="xgic",
        description=(
            "XGIC CLI — modular command-line framework for XGIC tools "
            "and environment orchestration."
        ),
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "command",
        nargs="?",
        help="Subcommand (plugins will register here in later releases).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the XGIC CLI entrypoint.

    Args:
        argv: Optional argument list (defaults to ``sys.argv[1:]``).

    Returns:
        Process exit code.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    parser.error(
        f"unknown command {args.command!r}; "
        "domain modules will provide subcommands in future releases "
        "(see https://github.com/xgic/ai/blob/main/docs/adr/0005-modular-xgic-cli-and-retirement-of-xde.md)"
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
