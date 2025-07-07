# Makefile for Renault Intelligence Agent

.PHONY: test test-simple test-unit test-integration test-coverage clean setup help

# Default target
help:
	@echo "Available targets:"
	@echo "  test          - Run all tests"
	@echo "  test-simple   - Run simple tests only"
	@echo "  test-unit     - Run unit tests"
	@echo "  test-coverage - Run tests with coverage"
	@echo "  clean         - Clean up test artifacts"
	@echo "  setup         - Set up test environment"
	@echo "  help          - Show this help"

# Set up test environment
setup:
	@echo "Setting up test environment..."
	python -m pip install --upgrade pip
	python -m pip install pytest pytest-cov pytest-mock
	@echo "Test environment ready!"

# Run simple tests (no external dependencies)
test-simple:
	@echo "Running simple tests..."
	cd tests && python test_simple.py

# Run all tests using unittest
test-unit:
	@echo "Running unit tests..."
	cd tests && python -m unittest discover -v

# Run tests using pytest if available
test-pytest:
	@echo "Running tests with pytest..."
	cd tests && python -m pytest -v

# Run tests with coverage
test-coverage:
	@echo "Running tests with coverage..."
	cd tests && python -m pytest --cov=../src/app --cov-report=html --cov-report=term

# Run all tests (fallback to simple if pytest not available)
test:
	@echo "Running all tests..."
	@if command -v pytest >/dev/null 2>&1; then \
		make test-pytest; \
	else \
		make test-simple; \
	fi

# Clean up test artifacts
clean:
	@echo "Cleaning up test artifacts..."
	rm -rf tests/__pycache__/
	rm -rf tests/.pytest_cache/
	rm -rf tests/htmlcov/
	rm -rf tests/.coverage
	rm -f tests/graph.png
	@echo "Clean up complete!"

# Install test dependencies
install-test-deps:
	@echo "Installing test dependencies..."
	python -m pip install pytest pytest-cov pytest-mock

# Run specific test file
test-file:
	@if [ -z "$(FILE)" ]; then \
		echo "Usage: make test-file FILE=test_filename.py"; \
	else \
		cd tests && python $(FILE); \
	fi

# Run tests in verbose mode
test-verbose:
	@echo "Running tests in verbose mode..."
	cd tests && python test_simple.py -v

# Check test environment
check-env:
	@echo "Checking test environment..."
	@python -c "import sys; print('Python version:', sys.version)"
	@python -c "import unittest; print('unittest: OK')"
	@python -c "import importlib; print('pytest: OK' if importlib.util.find_spec('pytest') else 'pytest: Not available')"
	@echo "Test environment check complete!"
