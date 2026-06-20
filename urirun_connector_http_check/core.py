# Author: Tom Sapletta · https://tom.sapletta.com
# Part of the ifURI solution.

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from importlib import resources
from typing import Any

import urirun


ROUTE_HTTP_STATUS = "httpcheck://host/http/query/status"
CONNECTOR_ID = "http-check"
CONNECTOR = urirun.connector(CONNECTOR_ID, scheme="httpcheck")


def _json_resource(name: str) -> dict[str, Any]:
    text = resources.files(__package__).joinpath(name).read_text(encoding="utf-8")
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"{name} must contain a JSON object")
    return data


def connector_manifest() -> dict[str, Any]:
    return _json_resource("connector.manifest.json")


@CONNECTOR.command("http/query/status", meta={"label": "Check HTTP status"})
def status_command(url: str, expectStatus: int = 200, timeout: float = 10.0) -> list[str]:
    """Declare the URI binding once, using the function signature as schema."""
    return [
        "urirun-http-check",
        "status",
        "{url}",
        "--expect-status",
        "{expectStatus}",
        "--timeout",
        "{timeout}",
    ]


def urirun_bindings() -> dict[str, Any]:
    return CONNECTOR.bindings()


def check_url(url: str, timeout: float = 10.0, expect_status: int | None = None) -> dict[str, Any]:
    started = time.perf_counter()
    request = urllib.request.Request(url, method="GET", headers={"User-Agent": "urirun-http-check/0.1"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = int(response.status)
            final_url = response.geturl()
            content_type = response.headers.get("content-type")
            body = response.read(256)
            error = None
    except urllib.error.HTTPError as exc:
        status = int(exc.code)
        final_url = exc.geturl()
        content_type = exc.headers.get("content-type") if exc.headers else None
        body = exc.read(256)
        error = str(exc)
    except Exception as exc:  # noqa: BLE001 - CLI reports network failures as JSON.
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        return {
            "ok": False,
            "url": url,
            "status": None,
            "expectedStatus": expect_status,
            "elapsedMs": elapsed_ms,
            "error": str(exc),
        }

    elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
    expected_ok = expect_status is None or status == int(expect_status)
    return {
        "ok": error is None and expected_ok,
        "url": url,
        "finalUrl": final_url,
        "status": status,
        "expectedStatus": expect_status,
        "contentType": content_type,
        "elapsedMs": elapsed_ms,
        "sampleBytes": len(body),
        "error": error,
    }
