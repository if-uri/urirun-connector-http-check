# urirun-connector-http-check

Small ifuri/urirun connector that checks HTTP endpoints and exposes the action
as a package, CLI and URI binding.

## Install from GitHub

```bash
python3 -m pip install "git+https://github.com/if-uri/urirun-connector-http-check.git@main"
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

The package also ships `urirun.bindings.v2.json`, so `urirun scan` or
`python -m urirun.v2_adopt add-python-package urirun-connector-http-check` can
adopt the console script into a registry.

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
