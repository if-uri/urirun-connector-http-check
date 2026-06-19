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
sumd_declared_file('app.doql.less', 'doql').
sumd_declared_file('testql-scenarios/generated-cli-tests.testql.toon.yaml', 'testql').
sumd_declared_file('testql-scenarios/generated-from-pytests.testql.toon.yaml', 'testql').
sumd_declared_file('project/map.toon.yaml', 'analysis').
sumd_declared_file('project/logic.pl', 'analysis').
sumd_declared_file('project/calls.toon.yaml', 'analysis').
sumd_interface('cli', 'argparse').
sumd_interface('cli', '').
sumd_workflow('test', 'manual').
sumd_workflow_step('test', 1, 'python3 -m pytest -q').
sumd_workflow('smoke', 'manual').
sumd_workflow_step('smoke', 1, 'python3 -m urirun_connector_http_check.cli status https://ifuri.com --expect-status 200').
sumd_workflow('manifest', 'manual').
sumd_workflow_step('manifest', 1, 'python3 -m urirun_connector_http_check.cli manifest').

