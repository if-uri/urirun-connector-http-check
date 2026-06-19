# urirun-connector-http-check

SUMD - Structured Unified Markdown Descriptor for AI-aware project refactorization

## Contents

- [Metadata](#metadata)
- [Architecture](#architecture)
- [Workflows](#workflows)
- [Call Graph](#call-graph)
- [Test Contracts](#test-contracts)
- [Refactoring Analysis](#refactoring-analysis)
- [Intent](#intent)

## Metadata

- **name**: `urirun-connector-http-check`
- **version**: `0.1.0`
- **python_requires**: `>=3.10`
- **license**: Apache-2.0
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: pyproject.toml, Makefile, testql(2), app.doql.less, project/(5 analysis files)

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

## Workflows

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

## Refactoring Analysis

*Pre-refactoring snapshot — use this section to identify targets. Generated from `project/` toon files.*

### Call Graph & Complexity (`project/calls.toon.yaml`)

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

### Code Analysis (`project/analysis.toon.yaml`)

```toon markpact:analysis path=project/analysis.toon.yaml
# code2llm | 9f 317L | python:3,shell:2,json:2,toml:1 | 2026-06-19
# generated in 0.00s
# CC̅=2.7 | critical:0/6 | dups:0 | cycles:0

HEALTH[0]: ok

REFACTOR[0]: none needed

PIPELINES[1]:
  [1] Src [main]: main → check_url
      PURITY: 100% pure

LAYERS:
  urirun_connector_http_check/    CC̄=2.7    ←in:0  →out:0
  │ core                        66L  0C    4m  CC=6      ←1
  │ connector.manifest.json     56L  0C    0m  CC=0.0    ←0
  │ urirun.bindings.v2.json     43L  0C    0m  CC=0.0    ←0
  │ cli                         41L  0C    2m  CC=5      ←0
  │ __init__                     5L  0C    0m  CC=0.0    ←0
  │
  ./                              CC̄=0.0    ←in:0  →out:0
  │ project.sh                  63L  0C    0m  CC=0.0    ←0
  │ pyproject.toml              27L  0C    0m  CC=0.0    ←0
  │ Makefile                    15L  0C    0m  CC=0.0    ←0
  │ tree.sh                      1L  0C    0m  CC=0.0    ←0
  │

COUPLING: no cross-package imports detected

EXTERNAL:
  validation: run `vallm batch .` → validation.toon
  duplication: run `redup scan .` → duplication.toon
```

### Duplication (`project/duplication.toon.yaml`)

```toon markpact:analysis path=project/duplication.toon.yaml
# redup/duplication | 0 groups | 3f 112L | 2026-06-19

SUMMARY:
  files_scanned: 3
  total_lines:   112
  dup_groups:    0
  dup_fragments: 0
  saved_lines:   0
  scan_ms:       3408
```

### Evolution / Churn (`project/evolution.toon.yaml`)

```toon markpact:analysis path=project/evolution.toon.yaml
# code2llm/evolution | 6 func | 2f | 2026-06-19
# generated in 0.00s

NEXT[0]: no refactoring needed

RISKS[0]: none

METRICS-TARGET:
  CC̄:          2.7 → ≤1.9
  max-CC:      6 → ≤3
  god-modules: 0 → 0
  high-CC(≥15): 0 → ≤0
  hub-types:   0 → ≤0

PATTERNS (language parser shared logic):
  _extract_declarations() in base.py — unified extraction for:
    - TypeScript: interfaces, types, classes, functions, arrow funcs
    - PHP: namespaces, traits, classes, functions, includes
    - Ruby: modules, classes, methods, requires
    - C++: classes, structs, functions, #includes
    - C#: classes, interfaces, methods, usings
    - Java: classes, interfaces, methods, imports
    - Go: packages, functions, structs
    - Rust: modules, functions, traits, use statements

  Shared regex patterns per language:
    - import: language-specific import/require/using patterns
    - class: class/struct/trait declarations with inheritance
    - function: function/method signatures with visibility
    - brace_tracking: for C-family languages ({ })
    - end_keyword_tracking: for Ruby (module/class/def...end)

  Benefits:
    - Consistent extraction logic across all languages
    - Reduced code duplication (~70% reduction in parser LOC)
    - Easier maintenance: fix once, apply everywhere
    - Standardized FunctionInfo/ClassInfo models

HISTORY:
  (first run — no previous data)
```

## Intent

HTTP status check connector for ifuri and urirun
