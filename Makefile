.PHONY: install test lint format check-style check-types docs clean

# Variables
PYTHON = python
PIP = pip
PYTEST = pytest
BLACK = black
ISORT = isort
FLAKE8 = flake8
MYPY = mypy
SPHINX_BUILD = sphinx-build

# Directories
SRC = autopm
TESTS = tests
DOCS = docs
BUILD = build
DIST = dist

# Install dependencies
install:
	$(PIP) install -e .
	$(PIP) install -r requirements-dev.txt

# Install pre-commit hooks
install-hooks:
	pre-commit install

# Run tests
test:
	$(PYTEST) $(TESTS) -v --cov=$(SRC) --cov-report=term-missing

# Run linter
lint:
	$(FLAKE8) $(SRC) $(TESTS)

# Format code
format:
	$(BLACK) $(SRC) $(TESTS) setup.py
	$(ISORT) $(SRC) $(TESTS) setup.py

# Check code style
check-style:
	$(BLACK) --check $(SRC) $(TESTS) setup.py
	$(ISORT) --check-only $(SRC) $(TESTS) setup.py

# Check types
check-types:
	$(MYPY) $(SRC) $(TESTS)

# Build documentation
docs:
	$(SPHINX_BUILD) -b html $(DOCS) $(BUILD)/docs

# Build distribution
build:
	$(PYTHON) setup.py sdist bdist_wheel

# Clean build artifacts
clean:
	rm -rf $(BUILD) $(DIST) *.egg-info
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type f -name '*.py[co]' -delete

# Run all checks
check: check-style check-types lint test

# Default target
all: install check docs build
