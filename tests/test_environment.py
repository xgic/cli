"""Unit tests for EnvironmentContext detection logic."""

from __future__ import annotations

import os
from unittest.mock import patch

from xgic.cli.core.environment import EnvironmentContext, EnvironmentType


class TestEnvironmentDetection:
    """Tests for EnvironmentContext.detect()."""

    def test_detects_dev_container_via_remote_containers(self) -> None:
        with patch.dict(os.environ, {"REMOTE_CONTAINERS": "true"}, clear=True):
            ctx = EnvironmentContext.detect()
            assert ctx.env_type == EnvironmentType.DEV_CONTAINER
            assert ctx.is_remote is True

    def test_detects_dev_container_via_codespaces(self) -> None:
        with patch.dict(os.environ, {"CODESPACES": "true"}, clear=True):
            ctx = EnvironmentContext.detect()
            assert ctx.env_type == EnvironmentType.DEV_CONTAINER
            assert ctx.is_remote is True

    def test_detects_host_when_no_container_markers(
        self, tmp_path, monkeypatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=True):
            ctx = EnvironmentContext.detect()
            assert ctx.env_type == EnvironmentType.HOST
            assert ctx.is_remote is False

    def test_is_host_only_command_safe_on_host(self) -> None:
        ctx = EnvironmentContext(env_type=EnvironmentType.HOST)
        assert ctx.is_host_only_command_safe() is True

    def test_is_host_only_command_safe_in_dev_container(self) -> None:
        ctx = EnvironmentContext(env_type=EnvironmentType.DEV_CONTAINER)
        assert ctx.is_host_only_command_safe() is False

    def test_describe_returns_human_readable_string(self) -> None:
        ctx = EnvironmentContext(env_type=EnvironmentType.DEV_CONTAINER)
        assert "Dev Container" in ctx.describe()
