.PHONY: help install install-dev test format lint clean build hatch-build hatch-clean bump-patch bump-minor bump-major

# Use virtual environment Python and pip explicitly
PYTHON := .venv/bin/python
PIP := .venv/bin/pip

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the package in development mode
	$(PIP) install -e .

install-dev: ## Install development dependencies
	$(PIP) install -r requirements-dev.txt

test: ## Run tests with coverage
	$(PYTHON) -m pytest tests/ -v --cov=src/nato_phonetic --cov-report=term-missing

format: ## Format code with black
	$(PYTHON) -m black src/ tests/

lint: ## Run linting with flake8
	$(PYTHON) -m flake8 src/ tests/

type-check: ## Run type checking with mypy
	$(PYTHON) -m mypy src/

check: format lint type-check test ## Run all checks (format, lint, type-check, test)

clean: ## Clean up build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -f .coverage
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

demo: ## Run a quick demo of the CLI
	phonetic list
	@echo ""
	phonetic lookup A
	@echo ""
	phonetic spell "HELLO"

# Version bumping commands
bump-patch: ## Bump patch version (0.1.0 -> 0.1.1)
	.venv/bin/bump-my-version bump patch

bump-minor: ## Bump minor version (0.1.0 -> 0.2.0)
	.venv/bin/bump-my-version bump minor

bump-major: ## Bump major version (0.1.0 -> 1.0.0)
	.venv/bin/bump-my-version bump major

# Hatch commands
hatch-build: ## Build package using Hatch
	$(PYTHON) -m hatch build

hatch-clean: ## Clean Hatch build artifacts
	$(PYTHON) -m hatch clean

hatch-publish: ## Publish package using Hatch (if configured)
	$(PYTHON) -m hatch publish

build: hatch-build ## Build package (alias for hatch-build) 