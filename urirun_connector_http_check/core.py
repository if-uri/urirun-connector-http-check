# Author: Tom Sapletta · https://tom.sapletta.com
# Part of the ifURI solution.

"""http-check route for urirun.

One typed ``@handler`` declares the route, its input schema (from the signature)
and its implementation — no argv template, no ``_exec.py``, no ``run_route``
dispatcher, no ``@command`` stub. ``isolated=True`` runs the route out-of-process
through the shared ``python -m urirun.exec`` runner, so the binding stays
**registry-portable**: it executes from a compiled/served registry
(``urirun run``/``urirun node serve``, examples 12/19) with only the package
importable — no console-script install and no per-connector shim.
"""

from __future__ import annotations

import time
import urllib.error
import urllib.request
from typing import Any

import urirun

CONNECTOR_ID = "http-check"
conn = urirun.connector(CONNECTOR_ID, scheme="httpcheck")


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
    except Exception as exc:  # noqa: BLE001 - report network failures as JSON.
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        return urirun.fail(str(exc), url=url, status=None, expectedStatus=expect_status, elapsedMs=elapsed_ms)

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


@conn.handler("http/query/status", isolated=True, meta={"label": "Check HTTP status"})
def status(url: str, expectStatus: int = 200, timeout: float = 10.0) -> dict[str, Any]:
    """Check that ``url`` responds, optionally with an expected status code."""
    return check_url(url, timeout=timeout, expect_status=expectStatus)


def urirun_bindings() -> dict[str, Any]:
    """Serializable v2 bindings for this connector (entry point: urirun.bindings)."""
    return conn.bindings()


def connector_manifest() -> dict[str, Any]:
    """Full manifest: prose (connector.manifest.json) + routes/uriSchemes/
    adapterKinds/examples derived from the handler."""
    return conn.manifest(urirun.load_manifest(__package__))


def main(argv: list[str] | None = None) -> int:
    """Console-script entry point: subcommands + dispatch derived from the handler."""
    return conn.cli(argv, manifest_prose=urirun.load_manifest(__package__))


if __name__ == "__main__":
    import sys

    raise SystemExit(main())
