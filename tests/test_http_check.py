from __future__ import annotations

import json
import importlib

import urirun
from urirun_connector_http_check import connector_manifest, urirun_bindings
from urirun_connector_http_check.cli import main


def _compile_registry(bindings: dict):
    compile_registry = getattr(urirun, "compile_registry", None)
    list_routes = getattr(urirun, "list_routes", None)
    if compile_registry is not None and list_routes is not None:
        registry = compile_registry(bindings)
        return registry, list_routes(registry)
    v2 = importlib.import_module("urirun.v2")

    registry = v2.compile_registry(bindings)
    return registry, v2.list_routes(registry)


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
    _registry, routes = _compile_registry(bindings)
    assert any(route["uri"] == "httpcheck://host/http/query/status" for route in routes)


def test_bindings_export_only_this_connector_routes() -> None:
    @urirun.command("other://local/example/run")
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
