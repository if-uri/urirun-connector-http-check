# Author: Tom Sapletta · https://tom.sapletta.com
# Part of the ifURI solution.
"""Route contracts for the http-check connector — single read-only status check."""
from __future__ import annotations

from urirun_connectors_toolkit.contract_gate import Contract

CONTRACTS: dict[str, Contract] = {
    "http/query/status": Contract(
        version="v1",
        effect="query",
        reversible=False,
        inp={"url": "str", "expectStatus": "?int", "timeout": "?num"},
        out={"ok": "bool", "url": "str", "finalUrl": "?str", "status": "?int",
             "expectedStatus": "?int", "contentType": "?str",
             "elapsedMs": "num", "sampleBytes": "?int", "error": "?str"},
        errors=("unreachable",),
        examples=(
            {
                "payload": {"url": "https://example.com"},
                "result": {
                    "ok": True,
                    "connector": "http-check",
                    "url": "https://example.com",
                    "finalUrl": "https://example.com/",
                    "status": 200,
                    "expectedStatus": 200,
                    "contentType": "text/html",
                    "elapsedMs": 42.5,
                    "sampleBytes": 256,
                    "error": None,
                },
            },
            {
                "payload": {"url": "http://10.0.0.99:9999", "timeout": 1.0},
                "result": {
                    "ok": False,
                    "connector": "http-check",
                    "url": "http://10.0.0.99:9999",
                    "finalUrl": None,
                    "status": None,
                    "expectedStatus": 200,
                    "elapsedMs": 1000.0,
                    "error": "Connection refused",
                },
            },
        ),
    ),
}
