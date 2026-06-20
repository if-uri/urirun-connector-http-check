# Changelog

## [Unreleased]

### Added
- Add structure-audit follow-up tasks for IFURI-016 matrix coverage and richer
  connector contract documentation.
- Link README and TODO to the current cross-repository work summary and examples
  repository.
- Add a TODO for host/node example coverage using `httpcheck://`.
- Expose `urirun_bindings()` through the `urirun.bindings` entry-point group
  and document `urirun discover` / `urirun list --entry-points`.

### Changed
- Point active runtime dependency and docs links at `github.com/if-uri/urirun`.
- Update the README GitHub install command to the current `v0.1.5` tag.

## [0.1.5] - 2026-06-20

### Changed
- Require `urirun` `v0.3.14` so connector installs use the runtime with stable
  unique MCP/A2A tool names.

## [0.1.4] - 2026-06-20

### Changed
- Use `urirun.connector(...)` in connector code and docs so connector id,
  default URI target and binding export are declared once.
- Require `urirun` `v0.3.13`, where the connector helper is available.

## [0.1.3] - 2026-06-20

### Changed
- Prefer the public `@urirun.command(...)` decorator in connector code and docs.
- Require `urirun` `v0.3.12`, where the top-level decorator API is available.

## [0.1.2] - 2026-06-20

### Changed
- Pin the urirun runtime dependency to the corrected release tag `v0.3.11`.

## [0.1.1] - 2026-06-20

### Changed
- Generate the `httpcheck://host/http/query/status` binding from a
  `@urirun.v2.uri_command` decorated function instead of maintaining a
  hand-written `urirun.bindings.v2.json` file.
- Use `urirun.v2.connector_bindings()` as the shared connector binding exporter.
- Declare `urirun` as an explicit package dependency so the connector can be
  installed and used directly from GitHub.

### Documentation
- Link the connector README to the public hub page, machine manifest and central
  docs.
- Document the public `connect.ifuri.com` installer path and verified
  end-to-end `urirun run` flow.

## [0.1.10] - 2026-06-19

### Fixed
- Fix relative-imports issues (ticket-50e66a13)
- Fix unused-imports issues (ticket-d1e33090)
- Fix unused-imports issues (ticket-a6b9e487)
- Fix relative-imports issues (ticket-1a31691b)
- Fix unused-imports issues (ticket-edc92277)
- Fix ai-boilerplate issues (ticket-0bac07a7)
- Fix duplicate-imports issues (ticket-467454ba)
- Fix unused-imports issues (ticket-ad4ca1eb)
- Fix relative-imports issues (ticket-0d6c2658)
- Fix unused-imports issues (ticket-1cb86b50)
- Fix duplicate-imports issues (ticket-9adceca0)
- Fix unused-imports issues (ticket-e4e6851c)
- Fix relative-imports issues (ticket-66fd4e6a)
- Fix unused-imports issues (ticket-ad907185)
- Fix ai-boilerplate issues (ticket-ae3ab1a8)
