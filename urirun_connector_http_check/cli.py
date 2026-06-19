from __future__ import annotations

import argparse
import json
import sys

from .core import check_url, connector_manifest, urirun_bindings


def emit(payload: dict) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="urirun-http-check")
    sub = parser.add_subparsers(dest="command", required=True)

    status = sub.add_parser("status", help="Check an HTTP URL and emit JSON")
    status.add_argument("url")
    status.add_argument("--timeout", type=float, default=10.0)
    status.add_argument("--expect-status", type=int)

    sub.add_parser("manifest", help="Emit connect.ifuri.com connector manifest")
    sub.add_parser("bindings", help="Emit urirun v2 bindings")

    args = parser.parse_args(argv)
    if args.command == "status":
        result = check_url(args.url, timeout=args.timeout, expect_status=args.expect_status)
        emit(result)
        return 0 if result["ok"] else 2
    if args.command == "manifest":
        emit(connector_manifest())
        return 0
    if args.command == "bindings":
        emit(urirun_bindings())
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
