"""Unit tests for DockerComposeController (mocked subprocess)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from xgic.cli.core.docker import DockerComposeController
from xgic.cli.core.environment import EnvironmentContext, EnvironmentType


@pytest.fixture
def mock_env() -> EnvironmentContext:
    return EnvironmentContext(env_type=EnvironmentType.HOST)


@pytest.fixture
def controller(mock_env: EnvironmentContext) -> DockerComposeController:
    return DockerComposeController(env=mock_env)


class TestDockerComposeController:
    def test_services_running_returns_true_on_running_service(
        self, controller: DockerComposeController
    ) -> None:
        with patch.object(controller, "_run_compose") as mock_run:
            mock_result = MagicMock()
            mock_result.stdout = "xgic-payload-cms-dev-containers\nother"
            mock_run.return_value = mock_result
            assert controller.services_running() is True
            mock_run.assert_called_once()

    def test_services_running_returns_false_on_no_services(
        self, controller: DockerComposeController
    ) -> None:
        with patch.object(controller, "_run_compose") as mock_run:
            mock_result = MagicMock()
            mock_result.stdout = ""
            mock_run.return_value = mock_result
            assert controller.services_running() is False

    def test_up_calls_compose_with_detach(
        self, controller: DockerComposeController, tmp_path: Path
    ) -> None:
        cfg = tmp_path / "cfg.json"
        cfg.write_text('{"dbAdapter": "postgres"}')
        controller.config_file = cfg
        with patch.object(controller, "_run_compose") as mock_run:
            controller.up()
            mock_run.assert_called_with("--profile", "postgres", "up", "-d")
            controller.up(build=True)
            mock_run.assert_called_with(
                "--profile", "postgres", "up", "-d", "--build"
            )

    def test_down_calls_compose_down(
        self, controller: DockerComposeController
    ) -> None:
        with patch.object(controller, "_run_compose") as mock_run:
            controller.down()
            mock_run.assert_called_with("down")

    def test_db_ready_uses_pg_isready(
        self, controller: DockerComposeController, tmp_path: Path
    ) -> None:
        cfg = tmp_path / "cfg.json"
        cfg.write_text('{"dbAdapter": "postgres"}')
        controller.config_file = cfg
        with patch.object(controller, "_run_compose") as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_run.return_value = mock_result
            assert controller.db_ready() is True
            args = mock_run.call_args[0]
            assert "exec" in args
            assert "postgres" in args
            assert "pg_isready" in args

    def test_remove_volume_calls_docker_volume_rm(
        self, controller: DockerComposeController
    ) -> None:
        with patch("xgic.cli.core.docker.subprocess.run") as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_run.return_value = mock_result
            assert controller.remove_volume("test-volume") is True
            called_cmd = mock_run.call_args[0][0]
            assert called_cmd[0:4] == ["docker", "volume", "rm", "-f"]
            assert "test-volume" in called_cmd

    def test_up_with_services_targets_only_those(
        self, controller: DockerComposeController, tmp_path: Path
    ) -> None:
        cfg = tmp_path / "cfg.json"
        cfg.write_text('{"dbAdapter": "postgres"}')
        controller.config_file = cfg
        with patch.object(controller, "_run_compose") as mock_run:
            controller.up(services=["postgres"])
            mock_run.assert_called_with(
                "--profile", "postgres", "up", "-d", "postgres"
            )

    def test_rm_service_passes_expected_flags(
        self, controller: DockerComposeController
    ) -> None:
        with patch.object(controller, "_run_compose") as mock_run:
            controller.rm_service(
                "postgres", force=True, stop=True, remove_volumes=False
            )
            mock_run.assert_called_with(
                "rm", "-f", "-s", "postgres", check=False
            )

    def test_get_payload_project_name_falls_back(
        self, controller: DockerComposeController, tmp_path: Path
    ) -> None:
        controller.config_file = tmp_path / "nope.json"
        assert controller.get_payload_project_name() == "my-payload-cms"

    def test_get_db_config_returns_values_from_config(
        self, controller: DockerComposeController, tmp_path: Path
    ) -> None:
        cfg = tmp_path / "cfg.json"
        cfg.write_text('{"dbName": "mydb", "dbUser": "me"}')
        controller.config_file = cfg
        assert controller.get_db_config() == ("mydb", "me")

    def test_get_db_config_falls_back_safely(
        self, controller: DockerComposeController, tmp_path: Path
    ) -> None:
        controller.config_file = tmp_path / "no.json"
        assert controller.get_db_config() == ("payload_db", "payload")
