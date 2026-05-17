from __future__ import annotations

import json
from types import SimpleNamespace

import spark.cli as spark_cli


def test_redact_git_remote_removes_credentials_and_suffix():
    assert (
        spark_cli._redact_git_remote("https://token@example.com/vibeforge1111/repo.git")
        == "example.com/vibeforge1111/repo"
    )
    assert (
        spark_cli._redact_git_remote("git@github.com:vibeforge1111/vibeship-spark-intelligence.git")
        == "github.com/vibeforge1111/vibeship-spark-intelligence"
    )
    assert spark_cli._redact_git_remote("/Users/example/private/repo") == "local"


def test_cmd_os_compile_json(monkeypatch, capsys, tmp_path):
    expected = {
        "schema": "spark.os.compile.v1",
        "capability": {"cli": "spark"},
        "repo_board": {"root_name": "project"},
    }
    seen = {}

    def fake_build(project_root):
        seen["project_root"] = project_root
        return expected

    monkeypatch.setattr(spark_cli, "_build_os_compile_snapshot", fake_build)

    spark_cli.cmd_os(
        SimpleNamespace(os_cmd="compile", json=True, project=str(tmp_path))
    )

    assert seen["project_root"] == tmp_path
    assert json.loads(capsys.readouterr().out) == expected


def test_main_accepts_os_compile_json(monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(
        spark_cli,
        "_build_os_compile_snapshot",
        lambda project_root: {"schema": "spark.os.compile.v1", "project": str(project_root)},
    )
    monkeypatch.setattr(
        spark_cli.sys,
        "argv",
        ["spark", "os", "compile", "--json", "--project", str(tmp_path)],
    )

    spark_cli.main()

    payload = json.loads(capsys.readouterr().out)
    assert payload["schema"] == "spark.os.compile.v1"
    assert payload["project"] == str(tmp_path)
