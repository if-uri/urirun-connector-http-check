# http-check connector — examples

HTTP status, latency and header checks.

## Install
```bash
urirun install urirun-connector-http-check
```
`urirun install` resolves catalog ids via connect.ifuri.com; `--catalog <url>` points at a
local/on-prem registry; a full package name / git URL / path falls back to `pip install`.

## Run
```bash
# HTTP status, latency and header checks (read)
urirun run 'httpcheck://host/http/query/status' --payload '{"url": "https://example.com"}' --execute --allow 'httpcheck://*'

# preview without running (dry-run): drop --execute
urirun run 'httpcheck://host/http/query/status' --payload '{"url": "https://example.com"}' --allow 'httpcheck://*'
```

## Inspect the runtime (no path — like error:// / log://)
```bash
urirun list | grep 'httpcheck://'                                   # this connector's routes
urirun run 'registry://local/routes/query/list' --payload '{"scheme":"httpcheck"}' --allow 'registry://*'
urirun run 'registry://local/bindings/query/show' --payload '{"uri":"httpcheck://host/http/query/status"}' --allow 'registry://*'   # full typed contract
urirun errors                                                      # recent runtime errors (error://)
```

## Generate a client / API surface from the binding
```bash
urirun discover | urirun gen openapi - --out openapi.json   # OpenAPI 3 (one path per route)
urirun discover | urirun gen proto   - --out service.proto  # protobuf + gRPC (typed rpc per route)
urirun discover | urirun gen client  - --out client.py      # typed Python client
```
