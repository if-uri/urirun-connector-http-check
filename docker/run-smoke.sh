#!/usr/bin/env bash
# Author: Tom Sapletta · https://tom.sapletta.com
# Part of the ifURI solution.

set -euo pipefail

mkdir -p .docker-smoke

TARGET_URL="${TARGET_URL:-http://target-site/}"

echo "==> direct connector CLI"
urirun-http-check status "$TARGET_URL" --expect-status 200 > .docker-smoke/cli-result.json

echo "==> build bindings and registry"
python3 - <<'PY' > .docker-smoke/bindings.json
import json
from urirun_connector_http_check import urirun_bindings
print(json.dumps(urirun_bindings(), indent=2))
PY

urirun validate .docker-smoke/bindings.json
urirun compile .docker-smoke/bindings.json --out .docker-smoke/registry.json

echo "==> execute connector URI through urirun"
urirun run 'httpcheck://host/http/query/status' .docker-smoke/registry.json \
  --payload "{\"url\":\"$TARGET_URL\",\"expectStatus\":200,\"timeout\":5}" \
  --execute \
  --allow 'httpcheck://host/*' > .docker-smoke/urirun-result.json

echo "==> project registry to MCP tools and A2A card"
python3 -m urirun.v2_mcp tools .docker-smoke/registry.json > .docker-smoke/mcp-tools.json
python3 -m urirun.v2_mcp card .docker-smoke/registry.json \
  --name http-check-docker \
  --url http://tester/ > .docker-smoke/a2a-card.json

python3 - <<'PY'
import json
from pathlib import Path

base = Path(".docker-smoke")
cli = json.loads((base / "cli-result.json").read_text())
run = json.loads((base / "urirun-result.json").read_text())
tools = json.loads((base / "mcp-tools.json").read_text())
card = json.loads((base / "a2a-card.json").read_text())

assert cli["ok"] is True, cli
assert run["ok"] is True, run
assert any(tool["name"] == "httpcheck_host_http_query" for tool in tools["tools"]), tools
assert any("httpcheck://host/http/query/status" in skill.get("examples", []) for skill in card["skills"]), card
print(json.dumps({
    "ok": True,
    "status": cli["status"],
    "mcpTools": len(tools["tools"]),
    "a2aSkills": len(card["skills"]),
}, indent=2))
PY
