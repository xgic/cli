"""Environment detection and context.

Robust detection of the execution environment (host machine, VS Code
Dev Container, generic container, etc.). Frozen dataclass for safe sharing
across CLI modules and library callers.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from enum import Enum, auto


class EnvironmentType(Enum):
    """Detected execution environment."""

    HOST = auto()
    DEV_CONTAINER = auto()
    GENERIC_CONTAINER = auto()
    UNKNOWN = auto()


@dataclass(frozen=True)
class EnvironmentContext:
    """Rich context object describing the current execution environment."""

    env_type: EnvironmentType
    is_remote: bool = False
    project_root: str | None = None

    @classmethod
    def detect(cls) -> EnvironmentContext:
        """Detect the current environment using reliable signals."""
        remote_containers = os.environ.get("REMOTE_CONTAINERS")
        codespaces = os.environ.get("CODESPACES")
        xg_host_type = os.environ.get("XG_AIS_HOST_TYPE")

        if (
            remote_containers == "true"
            or codespaces == "true"
            or xg_host_type == "xgic-devcontainer"
        ):
            env_type = EnvironmentType.DEV_CONTAINER
        elif os.path.exists("/.dockerenv"):
            env_type = EnvironmentType.GENERIC_CONTAINER
        else:
            env_type = EnvironmentType.HOST

        is_remote = bool(remote_containers or codespaces)

        cwd = os.getcwd()
        project_root = (
            cwd if os.path.exists(os.path.join(cwd, ".devcontainer")) else None
        )

        return cls(
            env_type=env_type,
            is_remote=is_remote,
            project_root=project_root,
        )

    def is_host_only_command_safe(self) -> bool:
        """Return True if safe to run host-only commands (Docker etc.)."""
        return self.env_type in (EnvironmentType.HOST, EnvironmentType.UNKNOWN)

    def describe(self) -> str:
        """Human-friendly description for logging / UI."""
        if self.env_type == EnvironmentType.DEV_CONTAINER:
            return "Inside Dev Container (VS Code)"
        if self.env_type == EnvironmentType.GENERIC_CONTAINER:
            return "Inside generic container"
        if self.is_remote:
            return "Remote session"
        return "Local host"
