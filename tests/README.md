# Test Guide - Renault Intelligence Agent

## Overview
This project includes unit tests for the Renault Intelligence Agent. The tests verify that each module and functionality of the project works correctly.

## Test Structure

```
tests/
├── conftest.py          # pytest configuration and fixtures
├── test_simple.py       # Simple unit tests (no external dependencies)
├── test_main_safe.py    # Safe main module tests (concept-based)
├── test_utils.py        # Utility function tests
├── tools.py             # Tool module tests
├── test_config.py       # Test configuration and environment
├── run_tests.py         # Test execution script
├── test_main.py.disabled # Disabled test file (import issues)
└── README.md            # This file
```

## How to Run Tests

### 1. Basic Test Execution
```bash
# Run simple tests (recommended)
make test-simple

# Or run directly
cd tests && python test_simple.py
```

### 2. Run All Tests
```bash
# Using Makefile
make test

# Or using unittest
make test-unit
```

### 3. Run Specific Test File
```bash
# Test specific file
make test-file FILE=test_simple.py

# Or run directly
cd tests && python test_simple.py
```

### 4. Test Environment Setup
```bash
# Initial test environment setup
make setup

# Check test environment
make check-env
```

## Test Types

### 1. Unit Tests
- **TestStockAPI**: Stock API related functionality tests
- **TestDateTool**: Date tool functionality tests
- **TestGraphCreator**: Graph creation functionality tests
- **TestRetriever**: Document retrieval functionality tests
- **TestErrorHandling**: Error handling functionality tests
- **TestStateManagement**: State management functionality tests

### 2. Integration Tests
- **TestIntegration**: Module interaction tests
- **TestWorkflow**: Complete workflow tests
- **TestMainIntegration**: Main module integration tests (concept-based)
- **TestMainModule**: Core main module functionality tests (safe implementation)

## Test Result Interpretation

### Successful Test Results
```
test_date_format_default (test_simple.TestDateTool.test_date_format_default)
Test default date format ... ok

----------------------------------------------------------------------
Ran 39 tests in 0.022s

OK
```

### Failed Test Results
```
test_example (__main__.TestExample.test_example)
Test example functionality ... FAIL

======================================================================
FAIL: test_example (__main__.TestExample.test_example)
----------------------------------------------------------------------
AssertionError: Expected 'expected_value' but got 'actual_value'
```

## Test Writing Guide

### 1. Adding New Tests
```python
class TestNewFeature(unittest.TestCase):
    """Tests for new functionality"""
    
    def test_new_functionality(self):
        """Test new functionality"""
        # Arrange
        input_data = "test_input"
        expected_output = "expected_output"
        
        # Act
        result = new_function(input_data)
        
        # Assert
        self.assertEqual(result, expected_output)
```

### 2. Using Mocks
```python
@patch('module.external_function')
def test_with_mock(self, mock_external):
    """Test with external dependencies using Mock"""
    mock_external.return_value = "mocked_result"
    
    result = function_using_external()
    
    self.assertEqual(result, "expected_result")
    mock_external.assert_called_once()
```

## Test Best Practices

### 1. Test Naming Convention
- Test methods should start with `test_`
- Use names that clearly describe what is being tested
- Examples: `test_stock_data_structure`, `test_error_handling`

### 2. Test Structure (AAA Pattern)
```python
def test_example(self):
    # Arrange - Prepare test data
    input_data = "test_input"
    
    # Act - Execute the target function
    result = target_function(input_data)
    
    # Assert - Verify the results
    self.assertEqual(result, expected_result)
```

### 3. Maintaining Independence
- Each test should be executable independently
- Do not share state between tests
- Utilize `setUp()` and `tearDown()` methods

## Coverage Check

### Running Test Coverage
```bash
# Run tests with coverage
make test-coverage
```

### Checking Coverage Results
```bash
# Generate HTML report (tests/htmlcov/index.html)
# Check coverage percentage in terminal
```

## Troubleshooting

### 1. Import Errors
```bash
# Run from project root
cd /Users/suyeoncho/Documents/data_science/renault_intelligence_agent
make test-simple
```

### 2. Dependency Errors
```bash
# Install test dependencies
pip install -r requirements-test.txt
```

### 3. Environment Variable Setup
```bash
# Set test environment variables
export TESTING=1
export PYTHONPATH="/Users/suyeoncho/Documents/data_science/renault_intelligence_agent/src/app:$PYTHONPATH"
```

## Continuous Integration (CI)

Tests are automatically executed in the following situations:
- When code changes are made
- When Pull Requests are created
- Before deployment

## Additional Information

### Related Files
- `Makefile`: Test execution commands
- `requirements-test.txt`: Test dependencies
- `conftest.py`: pytest configuration

### Useful Commands
```bash
# Clean up test results
make clean

# Run tests in verbose mode
make test-verbose

# Check test environment
make check-env
```

## Contributing

When adding new features:
1. Write tests for the new functionality
2. Ensure existing tests still pass
3. Maintain code coverage

---

**Note**: This test suite minimizes external dependencies to ensure fast and stable test execution.
