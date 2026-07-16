"""Docker Compose orchestration layer.

High-level Python interface for controlling Docker and Docker Compose via
subprocess (intentional: low deps, straightforward operations). Public methods
are the stable contract so the backend can evolve later.

Default compose file / project names match the public Payload CMS Dev
Containers template; override via constructor for other products.
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from xgic.cli.core.environment import EnvironmentContext

COMPOSE_FILE = ".devcontainer/docker-compose.yml"
DEFAULT_COMPOSE_PROJECT = "xgic-payload-cms-dev-containers"
DEFAULT_PRIMARY_SERVICE = "xgic-payload-cms-dev-containers"
DEFAULT_CONFIG_FILE = Path(".devcontainer/create-payload-config.json")


@dataclass
class DockerComposeController:
    """Controls Docker Compose services for a dev environment."""

    env: EnvironmentContext
    compose_file: str = COMPOSE_FILE
    project_name: str = DEFAULT_COMPOSE_PROJECT
    primary_service: str = DEFAULT_PRIMARY_SERVICE
    config_file: Path = DEFAULT_CONFIG_FILE

    def _run_compose(
        self,
        *args: str,
        check: bool = True,
        capture_output: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        """Run a docker compose command with consistent flags."""
        cmd = [
            "docker",
            "compose",
            "-f",
            self.compose_file,
            "-p",
            self.project_name,
            *args,
        ]
        return subprocess.run(
            cmd,
            check=check,
            capture_output=capture_output,
            text=True,
        )

    def services_running(self) -> bool:
        """Return True if the primary compose service appears to be up."""
        try:
            result = self._run_compose(
                "ps",
                "--services",
                "--filter",
                "status=running",
                capture_output=True,
            )
            return self.primary_service in result.stdout
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def up(
        self, *, build: bool = False, services: list[str] | None = None
    ) -> None:
        """Start services in detached mode with active DB profile."""
        profile = self._get_db_profile()
        args = ["--profile", profile, "up", "-d"]
        if build:
            args.append("--build")
        if services:
            args.extend(services)
        self._run_compose(*args)

    def down(self) -> None:
        """Stop services (volumes are preserved)."""
        self._run_compose("down")

    def rm_service(
        self,
        service: str,
        *,
        force: bool = True,
        stop: bool = True,
        remove_volumes: bool = False,
    ) -> None:
        """Best-effort compose rm for a single service."""
        args = ["rm"]
        if force:
            args.append("-f")
        if stop:
            args.append("-s")
        if remove_volumes:
            args.append("-v")
        args.append(service)
        self._run_compose(*args, check=False)

    def build(self, *, no_cache: bool = False) -> None:
        """Build images."""
        args = ["build"]
        if no_cache:
            args.append("--no-cache")
        self._run_compose(*args)

    def logs(self, follow: bool = True) -> None:
        """Follow logs (this blocks)."""
        args = ["logs"]
        if follow:
            args.append("-f")
        self._run_compose(*args, check=False)

    def exec(
        self, service: str, *cmd: str, check: bool = True
    ) -> subprocess.CompletedProcess[str]:
        """Run a command inside a service container."""
        return self._run_compose("exec", service, *cmd, check=check)

    def get_payload_project_name(self) -> str:
        """Return the name of the generated Payload CMS project folder."""
        if self.config_file.exists():
            try:
                with open(self.config_file, encoding="utf-8") as f:
                    data: dict[str, Any] = json.load(f)
                if name := data.get("projectName"):
                    return str(name)
            except (json.JSONDecodeError, OSError):
                pass
        return "my-payload-cms"

    def get_db_config(self) -> tuple[str, str]:
        """Return (db_name, db_user) from create-payload-config.json."""
        default_db = "payload_db"
        default_user = "payload"
        if not self.config_file.exists():
            return default_db, default_user
        try:
            with self.config_file.open(encoding="utf-8") as f:
                cfg: dict[str, Any] = json.load(f)
            db_name = cfg.get("dbName") or default_db
            db_user = cfg.get("dbUser") or default_user
            db_uri = cfg.get("dbUri") or ""
            if db_uri and (db_name == default_db or db_user == default_user):
                try:
                    if "://" in db_uri:
                        after = db_uri.split("://", 1)[1]
                        if "@" in after and db_user == default_user:
                            creds = after.split("@", 1)[0]
                            if ":" in creds:
                                db_user = creds.split(":", 1)[0] or db_user
                        if "/" in after and db_name == default_db:
                            after_host = after.split("@", 1)[-1]
                            path = after_host.split("/", 1)[-1].split("?")[0]
                            if path:
                                db_name = path or db_name
                except Exception:
                    pass
            return db_name, db_user
        except Exception:
            return default_db, default_user

    def _get_db_profile(self) -> str:
        """Return the compose profile for the active DB adapter."""
        if not self.config_file.exists():
            return "postgres"
        try:
            with self.config_file.open(encoding="utf-8") as f:
                cfg: dict[str, Any] = json.load(f)
            adapter = str(cfg.get("dbAdapter", "postgres")).lower()
            if adapter == "mongodb":
                return "mongodb"
            return "postgres"
        except Exception:
            return "postgres"

    def get_db_service(self) -> str:
        """Return the compose service name for the active DB."""
        return self._get_db_profile()

    def get_db_volume_name(self) -> str:
        """Return the named volume for the active DB data."""
        service = self.get_db_service()
        return f"{self.project_name}-{service}-data"

    def db_ready(self) -> bool:
        """Check if the active DB is accepting connections."""
        service = self.get_db_service()
        if service == "mongodb":
            try:
                result = self._run_compose(
                    "exec",
                    "-T",
                    service,
                    "mongosh",
                    "--quiet",
                    "--eval",
                    "db.runCommand({ping: 1})",
                    capture_output=True,
                    check=False,
                )
                return result.returncode == 0
            except Exception:
                return False

        _, db_user = self.get_db_config()
        try:
            result = self._run_compose(
                "exec",
                "-T",
                "postgres",
                "pg_isready",
                "-U",
                db_user,
                capture_output=True,
                check=False,
            )
            return result.returncode == 0
        except Exception:
            return False

    def remove_volume(self, volume_name: str) -> bool:
        """Attempt to remove a Docker volume via top-level docker CLI."""
        try:
            result = subprocess.run(
                ["docker", "volume", "rm", "-f", volume_name],
                check=False,
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except Exception:
            return False
