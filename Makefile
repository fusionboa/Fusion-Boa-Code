# FusionBoa Language Makefile
# Common tasks for development and testing.
# Usage: make <target>

.PHONY: help test run build clean version

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

version: ## Show FusionBoa version
	python fusionboa.py version

test: ## Run all 207 unit tests
	python fusionboa_lang/codegen/test_codegens.py

test-all: ## Run unit tests + 23-target complete test
	python fusionboa_lang/codegen/test_codegens.py
	@echo ""
	python tests/complete_test_runner.py

build: ## Build complete_test.fusboa (23 targets -> Desktop folder)
	python fusionboa.py build complete_test.fusboa

run: ## Run complete_test.fusboa (Python section)
	python fusionboa.py run complete_test.fusboa

run-js: ## Run complete_test.fusboa (JavaScript section)
	python fusionboa.py run complete_test.fusboa -t js

clean: ## Remove generated build outputs
	rm -rf complete_test_output/
	rm -f complete_test.py complete_test.js complete_test.ts complete_test.rb
	rm -f complete_test.go complete_test.rs complete_test.cpp complete_test.java
	rm -f complete_test.kt complete_test.swift complete_test.cs complete_test.lua
	rm -f complete_test.jl complete_test.r complete_test.jsx
	rm -f complete_test.html complete_test.css complete_test.json
	rm -f complete_test.yaml complete_test.toml complete_test.xml
	rm -f complete_test.md complete_test.ini
	@echo "Cleaned up build outputs."

init: ## Create a new FusionBoa project
	python fusionboa.py init my_project

targets: ## List all 23 compilation targets
	python fusionboa.py targets

format: ## Format all .fusboa files
	python fusionboa.py format complete_test.fusboa
	python fusionboa.py format fusionboa_lang/examples/all_in_one.fusboa

