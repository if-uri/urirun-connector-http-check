#!/usr/bin/env bash
# http-check: install once, then run — auto-discovered, no registry path.
set -euo pipefail
urirun install urirun-connector-http-check            # local dev: pip install -e .
urirun run 'httpcheck://host/http/query/status' --payload '{"url": "https://example.com"}' --execute --allow 'httpcheck://*'
