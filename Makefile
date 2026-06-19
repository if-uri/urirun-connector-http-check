.PHONY: help
help:
	@grep -E "^[a-zA-Z_-]+:.*?## .*$$" $(MAKEFILE_LIST) | awk "BEGIN{FS=\":.*?## \"}{printf \"  %-12s %s\\n\",\$$1,\$$2}"

.PHONY: test
test: ## Run connector tests
	python3 -m pytest -q

.PHONY: smoke
smoke: ## Run CLI smoke check against ifuri.com
	python3 -m urirun_connector_http_check.cli status https://ifuri.com --expect-status 200

.PHONY: manifest
manifest: ## Print connector manifest
	python3 -m urirun_connector_http_check.cli manifest
