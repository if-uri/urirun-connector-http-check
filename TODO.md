# TODO

## Next connector improvements

- [ ] Add a stable `urirun` entry-point group once core supports
  `urirun connectors list/install`.
- [ ] Add a GitHub Actions workflow that runs tests, `make docker-test`, builds a wheel and proves
  installation from `git+https://github.com/if-uri/urirun-connector-http-check.git@v0.1.5`.
- [ ] Add this connector to IFURI-016 full host-node Docker matrix with
      `httpcheck://` routes executed from both host and node contexts.
- [ ] Add more URI routes for common website checks, for example response time
  thresholds, TLS expiry and required text checks.
- [ ] Add example flows that combine `httpcheck://` with `planfile://` task
      updates and `log://` routes.
- [ ] Add an example flow that runs `httpcheck://` from a host against a node in
      `if-uri/examples/11-novnc_lan_flow`.
- [ ] Keep the hub manifest and package manifest in sync through a small CI
      check.
- [ ] Publish route schemas and response examples on the connector detail page.

Current cross-repository status:
https://github.com/if-uri/docs/blob/main/work-summary-2026-06-20.md
