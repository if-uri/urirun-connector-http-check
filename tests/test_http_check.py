from __future__ import annotations

from urirun_connector_http_check import connector_manifest, urirun_bindings
from urirun_connector_http_check.cli import main


def test_manifest_shape() -> None:
    manifest = connector_manifest()
    assert manifest["id"] == "http-check"
    assert "httpcheck://host/http/query/status" in manifest["routes"]


def test_bindings_shape() -> None:
    bindings = urirun_bindings()
    assert bindings["version"] == "urirun.bindings.v2"
    assert "httpcheck://host/http/query/status" in bindings["bindings"]


def test_cli_manifest(capsys) -> None:
    assert main(["manifest"]) == 0
    assert '"id": "http-check"' in capsys.readouterr().out
