"""XGIC CLI core package (modular framework).

Namespace: ``xgic.cli``
Distribution: ``xgic-cli``
Console entry: ``xgic``

Shared core lives under ``xgic.cli.core`` (environment, docker, project).
Domain modules register via entry point group ``xgic.cli.commands``.
"""

__version__ = "0.2.0"

__all__ = ["__version__"]
