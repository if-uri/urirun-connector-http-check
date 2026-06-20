# Author: Tom Sapletta · https://tom.sapletta.com
# Part of the ifURI solution.

from __future__ import annotations

import sys

import urirun

from .core import check_url, connector_manifest, urirun_bindings


def register(sub) -> None:
    status = sub.add_parser("status", help="Check an HTTP URL and emit JSON")
    status.add_argument("url")
    status.add_argument("--timeout", type=float, default=10.0)
    status.add_argument("--expect-status", type=int)


def dispatch(args) -> int:
    if args.command == "status":
        result = check_url(args.url, timeout=args.timeout, expect_status=args.expect_status)
        urirun.connector_emit(result)
        return 0 if result["ok"] else 2
    return 1


def main(argv: list[str] | None = None) -> int:
    return urirun.connector_cli(
        "urirun-http-check",
        manifest=connector_manifest,
        bindings=urirun_bindings,
        register=register,
        dispatch=dispatch,
        argv=argv,
    )


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
