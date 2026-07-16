"""Console entrypoint for the ``xgic`` command."""

from __future__ import annotations

import sys

from xgic.cli.app import build_parser, main

__all__ = ["build_parser", "main"]


if __name__ == "__main__":
    sys.exit(main())
