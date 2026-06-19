from __future__ import annotations

import json

from urirun import v2
from urirun_connector_http_check import connector_manifest, urirun_bindings
from urirun_connector_http_check.cli import main


def test_manifest_shape() -> None:
    manifest = connector_manifest()
    assert manifest["id"] == "http-check"
    assert "httpcheck://host/http/query/status" in manifest["routes"]


def test_bindings_shape() -> None:
    bindings = urirun_bindings()
    assert bindings["version"] == "urirun.bindings.v2"
    route = bindings["bindings"]["httpcheck://host/http/query/status"]
    assert route["argv"] == [
        "urirun-http-check",
        "status",
        "{url}",
        "--expect-status",
        "{expectStatus}",
        "--timeout",
        "{timeout}",
    ]
    assert route["inputSchema"]["required"] == ["url"]
    assert route["inputSchema"]["properties"]["expectStatus"]["default"] == 200


def test_bindings_are_json_serializable_and_compile() -> None:
    bindings = urirun_bindings()
    json.dumps(bindings)
    registry = v2.compile_registry(bindings)
    routes = v2.list_routes(registry)
    assert any(route["uri"] == "httpcheck://host/http/query/status" for route in routes)


def test_bindings_export_only_this_connector_routes() -> None:
    @v2.uri_command("other://local/example/run")
    def other_command(name: str) -> list[str]:
        return ["echo", "{name}"]

    bindings = urirun_bindings()
    assert "httpcheck://host/http/query/status" in bindings["bindings"]
    assert "other://local/example/run" not in bindings["bindings"]


def test_cli_manifest(capsys) -> None:
    assert main(["manifest"]) == 0
    assert '"id": "http-check"' in capsys.readouterr().out


def test_cli_bindings_are_generated(capsys) -> None:
    assert main(["bindings"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert "httpcheck://host/http/query/status" in output["bindings"]
