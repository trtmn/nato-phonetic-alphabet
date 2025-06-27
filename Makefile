.PHONY: help install install-dev test format lint clean

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the package in development mode
	pip install -e .

install-dev: ## Install development dependencies
	pip install -r requirements-dev.txt

test: ## Run tests with coverage
	python -m pytest tests/ -v --cov=src/nato_phonetic --cov-report=term-missing

format: ## Format code with black
	black src/ tests/

lint: ## Run linting with flake8
	flake8 src/ tests/

type-check: ## Run type checking with mypy
	mypy src/

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
	nato-phonetic list
	@echo ""
	nato-phonetic lookup A
	@echo ""
	nato-phonetic spell "HELLO" 