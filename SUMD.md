# urirun-connector-http-check

HTTP status check connector for ifuri and urirun

## Contents

- [Metadata](#metadata)
- [Architecture](#architecture)
- [Interfaces](#interfaces)
- [Workflows](#workflows)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Makefile Targets](#makefile-targets)
- [Code Analysis](#code-analysis)
- [Call Graph](#call-graph)
- [Test Contracts](#test-contracts)
- [Intent](#intent)

## Metadata

- **name**: `urirun-connector-http-check`
- **version**: `0.1.0`
- **python_requires**: `>=3.10`
- **license**: Apache-2.0
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: pyproject.toml, Makefile, testql(2), app.doql.less, project/(3 analysis files)

## Architecture

```
SUMD (description) → DOQL/source (code) → taskfile (automation) → testql (verification)
```

### DOQL Application Declaration (`app.doql.less`)

```less markpact:doql path=app.doql.less
// LESS format — define @variables here as needed

app {
  name: urirun-connector-http-check;
  version: 0.1.0;
}

interface[type="cli"] {
  framework: argparse;
}
interface[type="cli"] page[name="urirun-http-check"] {
  entry: urirun_connector_http_check.cli:main;
}

workflow[name="test"] {
  trigger: manual;
  step-1: run cmd=python3 -m pytest -q;
}

workflow[name="smoke"] {
  trigger: manual;
  step-1: run cmd=python3 -m urirun_connector_http_check.cli status https://ifuri.com --expect-status 200;
}

workflow[name="manifest"] {
  trigger: manual;
  step-1: run cmd=python3 -m urirun_connector_http_check.cli manifest;
}

deploy {
  target: makefile;
}

environment[name="local"] {
  runtime: python;
  python_version: >=3.10;
}
```

## Interfaces

### CLI Entry Points

- `urirun-http-check`

### testql Scenarios

#### `testql-scenarios/generated-cli-tests.testql.toon.yaml`

```toon markpact:testql path=testql-scenarios/generated-cli-tests.testql.toon.yaml
# SCENARIO: CLI Command Tests
# TYPE: cli
# GENERATED: true

CONFIG[2]{key, value}:
  cli_command, python -m urirun-connector-http-check
  timeout_ms, 10000

# Test 1: CLI help command
SHELL "python -m urirun-connector-http-check --help" 5000
ASSERT_EXIT_CODE 0
ASSERT_STDOUT_CONTAINS "usage"

# Test 2: CLI version command
SHELL "python -m urirun-connector-http-check --version" 5000
ASSERT_EXIT_CODE 0

# Test 3: CLI main workflow (dry-run)
SHELL "python -m urirun-connector-http-check --help" 10000
ASSERT_EXIT_CODE 0
```

#### `testql-scenarios/generated-from-pytests.testql.toon.yaml`

```toon markpact:testql path=testql-scenarios/generated-from-pytests.testql.toon.yaml
# SCENARIO: Auto-generated from Python Tests
# TYPE: integration
# GENERATED: true

CONFIG[2]{key, value}:
  base_url, ${api_url:-http://localhost:8101}
  timeout_ms, 10000

# Converted 6 assertions from pytest
ASSERT[6]{field, operator, expected}:
  manifest.id, ==, "http-check"
  bindings.version, ==, "urirun.bindings.v2"
  main(.manifest), ==, 0
  manifest.id, ==, "http-check"
  bindings.version, ==, "urirun.bindings.v2"
  main(.manifest), ==, 0
```

## Workflows

## Configuration

```yaml
project:
  name: urirun-connector-http-check
  version: 0.1.0
  env: local
```

## Deployment

```bash markpact:run
pip install urirun-connector-http-check

# development install
pip install -e .[dev]
```

## Makefile Targets

- `help`
- `test`
- `smoke`
- `manifest`

## Code Analysis

### `project/map.toon.yaml`

```toon markpact:analysis path=project/map.toon.yaml
# urirun-connector-http-check | 7f 240L | python:4,shell:2,less:1 | 2026-06-19
# stats: 9 func | 0 cls | 7 mod | CC̄=2.8 | critical:0 | cycles:0
# alerts[5]: CC check_url=6; CC main=5; CC test_manifest_shape=3; CC test_bindings_shape=3; CC test_cli_manifest=3
# hotspots[5]: check_url fan=10; main fan=9; _json_resource fan=6; test_cli_manifest fan=2; emit fan=2
# evolution: baseline
# Keys: M=modules, D=details, i=imports, e=exports, c=classes, f=functions, m=methods
M[7]:
  app.doql.less,38
  project.sh,63
  tests/test_http_check.py,22
  tree.sh,2
  urirun_connector_http_check/__init__.py,6
  urirun_connector_http_check/cli.py,42
  urirun_connector_http_check/core.py,67
D:
  tests/test_http_check.py:
    e: test_manifest_shape,test_bindings_shape,test_cli_manifest
    test_manifest_shape()
    test_bindings_shape()
    test_cli_manifest(capsys)
  urirun_connector_http_check/__init__.py:
  urirun_connector_http_check/cli.py:
    e: emit,main
    emit(payload)
    main(argv)
  urirun_connector_http_check/core.py:
    e: _json_resource,connector_manifest,urirun_bindings,check_url
    _json_resource(name)
    connector_manifest()
    urirun_bindings()
    check_url(url;timeout;expect_status)
```

### `project/logic.pl`

```prolog markpact:analysis path=project/logic.pl
% ── Project Metadata ─────────────────────────────────────
project_metadata('urirun-connector-http-check', '0.1.0', 'python').

% ── Project Files ────────────────────────────────────────
project_file('app.doql.less', 38, 'less').
project_file('project.sh', 63, 'shell').
project_file('tests/test_http_check.py', 22, 'python').
project_file('tree.sh', 2, 'shell').
project_file('urirun_connector_http_check/__init__.py', 6, 'python').
project_file('urirun_connector_http_check/cli.py', 42, 'python').
project_file('urirun_connector_http_check/core.py', 67, 'python').

% ── Python Functions ─────────────────────────────────────
python_function('tests/test_http_check.py', 'test_manifest_shape', 0, 3, 1).
python_function('tests/test_http_check.py', 'test_bindings_shape', 0, 3, 1).
python_function('tests/test_http_check.py', 'test_cli_manifest', 1, 3, 2).
python_function('urirun_connector_http_check/cli.py', 'emit', 1, 1, 2).
python_function('urirun_connector_http_check/cli.py', 'main', 1, 5, 9).
python_function('urirun_connector_http_check/core.py', '_json_resource', 1, 2, 6).
python_function('urirun_connector_http_check/core.py', 'connector_manifest', 0, 1, 1).
python_function('urirun_connector_http_check/core.py', 'urirun_bindings', 0, 1, 1).
python_function('urirun_connector_http_check/core.py', 'check_url', 3, 6, 10).

% ── Python Classes ───────────────────────────────────────

% ── Dependencies ─────────────────────────────────────────

% ── Makefile Targets ─────────────────────────────────────
makefile_target('help', '').
makefile_target('test', '').
makefile_target('smoke', '').
makefile_target('manifest', '').

% ── Taskfile Tasks ───────────────────────────────────────

% ── Environment Variables ────────────────────────────────

% ── TestQL Scenarios ─────────────────────────────────────
testql_scenario('generated-cli-tests.testql.toon.yaml', 'cli').
testql_scenario('generated-from-pytests.testql.toon.yaml', 'integration').

% ── Semantic Facts from SUMD.md ──────────────────────────
```

## Call Graph

*5 nodes · 3 edges · 2 modules · CC̄=2.7*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `check_url` *(in urirun_connector_http_check.core)* | 6 | 1 | 19 | **20** |
| `main` *(in urirun_connector_http_check.cli)* | 5 | 0 | 15 | **15** |
| `_json_resource` *(in urirun_connector_http_check.core)* | 2 | 2 | 6 | **8** |
| `connector_manifest` *(in urirun_connector_http_check.core)* | 1 | 1 | 1 | **2** |
| `urirun_bindings` *(in urirun_connector_http_check.core)* | 1 | 1 | 1 | **2** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/if-uri/urirun-connector-http-check
# generated in 0.00s
# nodes: 5 | edges: 3 | modules: 2
# CC̄=2.7

HUBS[20]:
  urirun_connector_http_check.core.check_url
    CC=6  in:1  out:19  total:20
  urirun_connector_http_check.cli.main
    CC=5  in:0  out:15  total:15
  urirun_connector_http_check.core._json_resource
    CC=2  in:2  out:6  total:8
  urirun_connector_http_check.core.connector_manifest
    CC=1  in:1  out:1  total:2
  urirun_connector_http_check.core.urirun_bindings
    CC=1  in:1  out:1  total:2

MODULES:
  urirun_connector_http_check.cli  [1 funcs]
    main  CC=5  out:15
  urirun_connector_http_check.core  [4 funcs]
    _json_resource  CC=2  out:6
    check_url  CC=6  out:19
    connector_manifest  CC=1  out:1
    urirun_bindings  CC=1  out:1

EDGES:
  urirun_connector_http_check.cli.main → urirun_connector_http_check.core.check_url
  urirun_connector_http_check.core.connector_manifest → urirun_connector_http_check.core._json_resource
  urirun_connector_http_check.core.urirun_bindings → urirun_connector_http_check.core._json_resource
```

## Test Contracts

*Scenarios as contract signatures — what the system guarantees.*

### Cli (1)

**`CLI Command Tests`**

### Integration (1)

**`Auto-generated from Python Tests`**

## Intent

HTTP status check connector for ifuri and urirun
