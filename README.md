# urirun-connector-http-check

Small ifuri/urirun connector that checks HTTP endpoints and exposes the action
as a package, CLI and URI binding.

The URI binding is generated from a decorated Python function, so the command
template and JSON Schema stay in one place instead of being duplicated in a
hand-written bindings file.

## Documentation

- Hub page: [connect.ifuri.com/connectors/http-check](https://connect.ifuri.com/connectors/http-check)
- Machine manifest: [connect.ifuri.com/connectors/http-check.json](https://connect.ifuri.com/connectors/http-check.json)
- Connector docs: [docs.ifuri.com/connectors.html](https://docs.ifuri.com/connectors.html)
- Registry model: [docs.ifuri.com/registry-and-bindings.html](https://docs.ifuri.com/registry-and-bindings.html)

## Install from GitHub

```bash
python3 -m pip install "git+https://github.com/if-uri/urirun-connector-http-check.git@v0.1.1"
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

The package exposes `urirun_bindings()`, generated from `@urirun.v2.uri_command`.
The function signature becomes the JSON Schema and the function body returns the
argv template:

```python
from urirun import v2

@v2.uri_command("httpcheck://host/http/query/status")
def status_command(url: str, expectStatus: int = 200, timeout: float = 10.0):
    return [
        "urirun-http-check", "status", "{url}",
        "--expect-status", "{expectStatus}",
        "--timeout", "{timeout}",
    ]
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
