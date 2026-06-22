# urirun-connector-http-check

Small ifuri/urirun connector that checks HTTP endpoints and exposes the action
as a package, CLI and URI binding.

The route is declared once as a single `@handler(isolated=True)` Python function:
the typed signature is the JSON Schema and the body is the work. There is no argv
template, no `_exec.py` shim and no hand-written bindings file. `isolated=True`
runs the route out-of-process through the shared `python -m urirun.exec` runner,
so the binding stays registry-portable — it executes from a compiled/served
registry with only the package importable.

## Documentation

- Hub page: [connect.ifuri.com/connectors/http-check](https://connect.ifuri.com/connectors/http-check)
- Machine manifest: [connect.ifuri.com/connectors/http-check.json](https://connect.ifuri.com/connectors/http-check.json)
- Connector docs: [docs.ifuri.com/connectors.html](https://docs.ifuri.com/connectors.html)
- Authoring guide: [docs.ifuri.com/connector-authoring.html](https://docs.ifuri.com/connector-authoring.html)
- Registry model: [docs.ifuri.com/registry-and-bindings.html](https://docs.ifuri.com/registry-and-bindings.html)
- Work summary: [if-uri/docs/work-summary-2026-06-20.md](https://github.com/if-uri/docs/blob/main/work-summary-2026-06-20.md)
- Examples: [if-uri/examples](https://github.com/if-uri/examples)

## Install from GitHub

```bash
python3 -m pip install "git+https://github.com/if-uri/urirun-connector-http-check.git@v0.1.5"
```

Or install through the public connector hub:

```bash
curl -fsSL 'https://connect.ifuri.com/install?connectors=http-check' | bash
```

## CLI

```bash
urirun-http-check status https://ifuri.com --expect-status 200
urirun-http-check manifest
urirun-http-check bindings
```

When running through a virtualenv, keep the environment active or prepend
`venv/bin` to `PATH`, so `urirun` can find the installed console script.

## URI contract

Primary route:

```text
httpcheck://host/http/query/status
```

The package exposes `urirun_bindings()`, derived from a single connector-local
`@handler`. The connector id and URI scheme are declared once; the function
signature becomes the JSON Schema and the function body does the work.
`isolated=True` makes the route run out-of-process via `python -m urirun.exec`,
so the binding is registry-portable (adapter `local-function-subprocess`):

```python
import urirun

conn = urirun.connector("http-check", scheme="httpcheck")

@conn.handler("http/query/status", isolated=True, meta={"label": "Check HTTP status"})
def status(url: str, expectStatus: int = 200, timeout: float = 10.0) -> dict:
    return check_url(url, timeout=timeout, expect_status=expectStatus)
```

Generate bindings and compile them into a registry:

```bash
python - <<'PY' > bindings.json
import json
from urirun_connector_http_check import urirun_bindings
print(json.dumps(urirun_bindings(), indent=2))
PY

urirun compile bindings.json --out registry.json
urirun run httpcheck://host/http/query/status registry.json \
  --payload '{"url":"https://ifuri.com","expectStatus":200,"timeout":10}' \
  --execute \
  --allow 'httpcheck://host/*'
```

After installation, `urirun` can discover this connector automatically through
the `urirun.bindings` entry-point group:

```bash
urirun discover --out connectors.bindings.json --registry-out connectors.registry.json
urirun list --entry-points
```

Adopt the console script as a generic `cli://` route:

```bash
python -m urirun.v2_adopt add-python-package urirun-connector-http-check --out cli-bindings.json
urirun compile cli-bindings.json --out cli-registry.json
urirun run cli://urirun-connector-http-check/urirun-http-check/run cli-registry.json \
  --payload '{"args":["status","https://ifuri.com","--expect-status","200"]}' \
  --execute \
  --allow 'cli://urirun-connector-http-check/*'
```

## Public verification

The connector has been tested from a clean virtualenv by:

- installing `urirun` and this connector through `https://connect.ifuri.com/install?connectors=http-check`,
- running the direct CLI against `https://ifuri.com`,
- compiling the package bindings into a registry,
- executing `httpcheck://host/http/query/status` through `urirun run`.

## Docker verification

Run the connector in an isolated Docker network with a local nginx target:

```bash
make docker-test
```

The Docker smoke test verifies:

- direct CLI execution,
- registry compilation,
- `urirun run httpcheck://host/http/query/status`,
- MCP tools projection,
- A2A card projection.

Repository notes: [TODO.md](TODO.md) · [CHANGELOG.md](CHANGELOG.md)

## License

Released under the terms in [LICENSE](LICENSE).
