# TODO

## Next connector improvements

- [ ] Add a stable `urirun` entry-point group once core supports
  `urirun connectors list/install`.
- [ ] Add a GitHub Actions workflow that runs tests, `make docker-test`, builds a wheel and proves
  installation from `git+https://github.com/if-uri/urirun-connector-http-check.git@v0.1.4`.
- [ ] Add more URI routes for common website checks, for example response time
  thresholds, TLS expiry and required text checks.
- [ ] Add example flows that combine `httpcheck://` with `planfile://` task
  updates and `log://` routes.
- [ ] Keep the hub manifest and package manifest in sync through a small CI
  check.
