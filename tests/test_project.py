"""Unit tests for project setup helpers (pure paths)."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from xgic.cli.core.project import (
    build_create_payload_command,
    compute_synced_project_env_content,
    ensure_payload_project,
    get_project_name,
    is_payload_project_complete,
    load_create_payload_config,
    resolve_db_connection_string,
)


class TestProjectPureHelpers:
    @pytest.mark.parametrize(
        "config_data, expected_name",
        [
            ({"projectName": "my-app"}, "my-app"),
            ({"projectName": "  spaced  "}, "spaced"),
            ({"projectName": ""}, "my-payload-cms"),
            ({"projectName": None}, "my-payload-cms"),
            ({}, "my-payload-cms"),
        ],
    )
    def test_get_project_name_variants(
        self, tmp_path: Path, config_data: dict, expected_name: str
    ) -> None:
        cfg_path = tmp_path / "cfg.json"
        cfg_path.write_text(json.dumps(config_data))
        cfg = load_create_payload_config(cfg_path)
        assert get_project_name(cfg) == expected_name

    @pytest.mark.parametrize(
        "files_present, expected_complete",
        [
            (["payload.config.ts"], True),
            (["payload.config.js"], True),
            (["src/payload.config.ts"], True),
            (["src/payload.config.js"], True),
            ([], False),
            (["README.md"], False),
        ],
    )
    def test_is_payload_project_complete_layouts(
        self,
        tmp_path: Path,
        files_present: list[str],
        expected_complete: bool,
    ) -> None:
        proj = tmp_path / "layout-test"
        proj.mkdir()
        for f in files_present:
            p = proj / f
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("// payload config")
        assert is_payload_project_complete(proj) is expected_complete

    def test_load_create_payload_config_defaults_when_missing(
        self, tmp_path: Path
    ) -> None:
        missing = tmp_path / "no-config.json"
        cfg = load_create_payload_config(missing)
        assert cfg["projectName"] == "my-payload-cms"
        assert cfg["template"] == "website"
        assert cfg["dbAdapter"] == "postgres"

    def test_load_create_payload_config_bad_json(
        self, tmp_path: Path
    ) -> None:
        bad = tmp_path / "bad.json"
        bad.write_text("{ not json }")
        cfg = load_create_payload_config(bad)
        assert cfg["projectName"] == "my-payload-cms"

    @pytest.mark.parametrize(
        "live, json_uri, expected",
        [
            ("postgres://live", "postgres://json", "postgres://live"),
            ("", "postgres://json", "postgres://json"),
            ("", "", None),
            ("live", "", "live"),
        ],
    )
    def test_resolve_db_connection_string(
        self, live: str, json_uri: str, expected: str | None
    ) -> None:
        assert resolve_db_connection_string(json_uri, live) == expected

    def test_compute_synced_project_env_content(self) -> None:
        result = compute_synced_project_env_content(
            "DATABASE_URL=old\nPAYLOAD_SECRET=old", "newdb", "newsec"
        )
        assert "DATABASE_URL=newdb" in result
        assert "PAYLOAD_SECRET=newsec" in result

    def test_build_create_payload_command_basic(self) -> None:
        cmd = build_create_payload_command(
            "website", template="website", db_adapter="postgres"
        )
        assert cmd[0:5] == [
            "pnpx",
            "create-payload-app@latest",
            "website",
            "-t",
            "website",
        ]
        assert "--use-pnpm" in cmd
        assert "--db-accept-recommended" in cmd
        assert "--no-agent" in cmd

    def test_build_create_payload_command_with_uri_and_agent(self) -> None:
        cmd = build_create_payload_command(
            "site",
            template="blank",
            db_adapter="postgres",
            db_connection_string="postgres://u:p@h:5432/db",
            agent="myagent",
        )
        assert "--db-connection-string" in cmd
        assert "postgres://u:p@h:5432/db" in cmd
        assert cmd[cmd.index("--agent") + 1] == "myagent"

    def test_ensure_payload_project_idempotent_on_complete(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        proj = tmp_path / "complete-site"
        proj.mkdir()
        (proj / "src").mkdir()
        (proj / "src" / "payload.config.ts").write_text("// ok")
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr(
            "xgic.cli.core.project.load_create_payload_config",
            lambda *a, **k: {"projectName": "complete-site"},
        )
        rc = ensure_payload_project()
        assert rc == 0

    def test_core_classes_directly_importable(self) -> None:
        from xgic.cli.core.project import load_create_payload_config

        cfg = load_create_payload_config(Path("/nonexistent-xgic-test"))
        assert cfg["projectName"] == "my-payload-cms"
        with patch("xgic.cli.core.project.subprocess.run"):
            rc = ensure_payload_project(quiet=True)
        assert rc == 0
