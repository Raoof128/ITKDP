.PHONY: help install install-dev test test-coverage lint format clean build docker run docs

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
PIP := $(PYTHON) -m pip
PYTEST := $(PYTHON) -m pytest
BLACK := $(PYTHON) -m black
ISORT := $(PYTHON) -m isort
FLAKE8 := $(PYTHON) -m flake8
MYPY := $(PYTHON) -m mypy
DOCKER := docker
DOCKER_COMPOSE := docker-compose
IMAGE_NAME := impossible-travel-detector
CONTAINER_NAME := itd-container

help: ## Show this help message
	@echo "Impossible Travel Detection Engine - Makefile Commands"
	@echo "======================================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

install-dev: ## Install development dependencies
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-cov black flake8 mypy isort pylint safety bandit

setup: install-dev ## Complete development environment setup
	@echo "Development environment ready!"

test: ## Run unit tests
	$(PYTEST) tests/ -v

test-coverage: ## Run tests with coverage report
	$(PYTEST) tests/ -v --cov=. --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/index.html"

test-watch: ## Run tests in watch mode
	$(PYTEST) tests/ -v --watch

lint: ## Run all linters (flake8, black, isort, mypy)
	@echo "Running Flake8..."
	$(FLAKE8) . --count --select=E9,F63,F7,F82 --show-source --statistics
	@echo "\nChecking Black formatting..."
	$(BLACK) --check --diff .
	@echo "\nChecking isort..."
	$(ISORT) --check-only --diff .
	@echo "\nRunning MyPy type checking..."
	$(MYPY) . --ignore-missing-imports || true

format: ## Auto-format code with black and isort
	@echo "Formatting with Black..."
	$(BLACK) .
	@echo "Sorting imports with isort..."
	$(ISORT) .
	@echo "Code formatting complete!"

security: ## Run security checks (safety, bandit)
	@echo "Checking dependencies for vulnerabilities..."
	safety check || true
	@echo "\nScanning code for security issues..."
	bandit -r . -f json || true

clean: ## Remove build artifacts and cache files
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/ htmlcov/ .coverage
	rm -f impossible_travel.csv full_analysis.csv report.md
	@echo "Cleanup complete!"

build: clean ## Build Python package
	$(PYTHON) -m build
	@echo "Package built successfully in dist/"

build-check: build ## Build and verify package
	twine check dist/*

install-local: build ## Install package locally in development mode
	$(PIP) install -e .

# Docker Commands
docker-build: ## Build Docker image
	$(DOCKER) build -t $(IMAGE_NAME):latest .
	@echo "Docker image built: $(IMAGE_NAME):latest"

docker-run: ## Run Docker container with sample data
	$(DOCKER) run --rm \
		-v $(PWD)/sample_logins.csv:/data/logins.csv:ro \
		-v $(PWD)/output:/output \
		$(IMAGE_NAME):latest /data/logins.csv --output-dir /output

docker-shell: ## Open shell in Docker container
	$(DOCKER) run --rm -it \
		-v $(PWD):/app \
		$(IMAGE_NAME):latest /bin/bash

docker-compose-up: ## Start services with docker-compose
	$(DOCKER_COMPOSE) up

docker-compose-down: ## Stop docker-compose services
	$(DOCKER_COMPOSE) down

docker-clean: ## Remove Docker images and containers
	$(DOCKER) rmi $(IMAGE_NAME):latest || true
	$(DOCKER) system prune -f

# Analysis Commands
run: ## Run analysis on sample data
	$(PYTHON) main.py sample_logins.csv

run-verbose: ## Run analysis with verbose logging
	$(PYTHON) main.py sample_logins.csv --verbose

run-custom: ## Run analysis with custom threshold (usage: make run-custom THRESHOLD=1200)
	$(PYTHON) main.py sample_logins.csv --speed-threshold $(THRESHOLD)

# Development Commands
dev-setup: install-dev ## Setup complete development environment
	pre-commit install || echo "pre-commit not installed, skipping hooks setup"
	@echo "Development environment configured!"

watch-tests: ## Watch for changes and run tests automatically
	$(PYTEST) tests/ -v --watch

profile: ## Profile code performance
	$(PYTHON) -m cProfile -o profile.stats main.py sample_logins.csv
	@echo "Profile saved to profile.stats"

# Documentation Commands
docs: ## Generate documentation (placeholder)
	@echo "Documentation generation coming soon..."

docs-serve: ## Serve documentation locally (placeholder)
	@echo "Documentation server coming soon..."

# Release Commands
version: ## Show current version
	@echo "Current version: $$(grep -oP "version = \"\K[^\"]*" pyproject.toml)"

changelog: ## Show recent changelog
	@head -n 20 CHANGELOG.md || echo "CHANGELOG.md not found"

# Quality Assurance
qa: lint test security ## Run all quality checks
	@echo "\nAll quality checks complete!"

ci: qa ## Run full CI pipeline locally
	@echo "\nCI pipeline complete! Ready for commit."

# Database setup (for real GeoIP database)
setup-geoip: ## Instructions for setting up GeoIP database
	@echo "To use real GeoIP database:"
	@echo "1. Create MaxMind account: https://www.maxmind.com/en/geolite2/signup"
	@echo "2. Download GeoLite2-City.mmdb"
	@echo "3. Place in project root"
	@echo "4. Run with: python main.py --geo-db GeoLite2-City.mmdb logins.csv"

# Utility Commands
example: ## Generate example output files
	$(PYTHON) main.py sample_logins.csv
	@echo "\nExample files generated:"
	@ls -lh impossible_travel.csv full_analysis.csv report.md

tree: ## Show project structure
	tree -I '__pycache__|*.pyc|venv|.venv|.git|htmlcov' -L 3

status: ## Show git status and project info
	@echo "Git Status:"
	@git status -s || echo "Not a git repository"
	@echo "\nProject Info:"
	@echo "Python: $$($(PYTHON) --version)"
	@echo "Dependencies: $$($(PIP) list | wc -l) packages installed"

# Complete workflow
all: clean install-dev qa build ## Run complete build pipeline
	@echo "\nComplete build pipeline finished successfully!"
