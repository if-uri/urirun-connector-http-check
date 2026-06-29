# Author: Tom Sapletta · https://tom.sapletta.com
# Part of the ifURI solution.

"""http-check connector: one isolated @handler route. The binding is
registry-portable (runs out-of-process via ``python -m urirun.exec``); it
executes from a serialized -> compiled registry, and ``check_url`` stays a
reusable in-process helper."""
from __future__ import annotations

import json

import urirun
from urirun import v2
from urirun_connector_http_check import (
    check_url,
    connector_manifest,
    core,
    main,
    status,
    urirun_bindings,
)

ROUTE = "httpcheck://host/http/query/status"


def test_status_calls_check_url(monkeypatch) -> None:
    monkeypatch.setattr(
        core,
        "check_url",
        lambda url, timeout=10.0, expect_status=None: {"ok": True, "url": url, "status": expect_status},
    )
    out = status(url="https://x", expectStatus=200, timeout=5.0)
    assert out == {"ok": True, "url": "https://x", "status": 200}


def test_check_url_reports_network_error() -> None:
    r = check_url("http://127.0.0.1:9/never", timeout=0.2)
    assert r["ok"] is False and r["status"] is None and r["error"]


def test_bindings_are_isolated_handler() -> None:
    b = urirun_bindings()["bindings"][ROUTE]
    # registry-portable: runs out-of-process via urirun.exec
    assert b["adapter"] == "local-function-subprocess"
    assert b["python"]["module"] == "urirun_connector_http_check.core"
    assert b["python"]["export"] == "status"
    assert "argv" not in b
    json.dumps(urirun_bindings())  # serializable: no live ref leaks


def test_runtime_executes_from_compiled_registry() -> None:
    # the whole point: a serialized->compiled registry still runs the route, with the
    # handler hydrated from python:{module,export} and executed OUT-OF-PROCESS via
    # ``python -m urirun.exec`` — no argv shim, no _exec.py. We target an unroutable
    # host so the subprocess returns a structured network-error result instead of
    # touching the real network; the route itself still ran (env ok, exitCode 0).
    registry = urirun.compile_registry(json.loads(json.dumps(urirun_bindings())))
    env = v2.run(
        ROUTE,
        registry,
        payload={"url": "http://127.0.0.1:9/never", "expectStatus": 200, "timeout": 0.5},
        mode="execute",
        policy=urirun.policy(allow=["httpcheck://*"]),
    )
    assert env["ok"] is True  # route dispatched + ran out-of-process
    assert env["adapter"] == "local-function-subprocess"
    assert env["result"]["isolated"] is True and env["result"]["exitCode"] == 0
    data = urirun.result_data(env)
    # ok:true (or ok:false network-error) — either way it's a structured check_url result
    assert data["ok"] is False and data["status"] is None and data["error"]
    assert data["url"] == "http://127.0.0.1:9/never"


def test_manifest_prose_plus_derived() -> None:
    m = connector_manifest()
    assert m["id"] == "http-check"
    assert m["routes"] == [ROUTE]
    assert m["uriSchemes"] == ["httpcheck"]
    assert m["summary"]  # prose preserved


def test_cli_bindings_and_manifest(capsys) -> None:
    assert main(["bindings"]) == 0
    assert ROUTE in json.loads(capsys.readouterr().out)["bindings"]
    assert main(["manifest"]) == 0
    assert json.loads(capsys.readouterr().out)["id"] == "http-check"


def test_contract_output_shape() -> None:
    """Live output from a network-error call must satisfy the declared out-schema."""
    import importlib.util, sys
    sys.path.insert(0, "/home/tom/github/if-uri/urirun-contract")
    from urirun_connectors_toolkit.contract_gate import validate_output
    spec = importlib.util.spec_from_file_location(
        "contracts_http_check",
        "/home/tom/github/if-uri/urirun-connector-http-check/urirun_connector_http_check/contracts.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # Use an unreachable address so no real network is required; error path is enough.
    result = check_url("http://127.0.0.1:9/never", timeout=0.2)
    validate_output(mod.CONTRACTS["http/query/status"], result)
