# Blaxel SDK Tests

This directory contains the comprehensive test suite for the Blaxel SDK v0.2.0. The tests are organized into logical categories to ensure good coverage and maintainability.

## Test Structure

### Core Tests (`tests/core/`)
- **`test_agents.py`** - Tests for agent functionality (`bl_agent`)
- **`test_jobs.py`** - Tests for job functionality (`bl_job`)
- **`test_models.py`** - Tests for model functionality (`bl_model`)
- **`test_tools.py`** - Tests for tools functionality (`bl_tools`)
- **`test_environment.py`** - Tests for environment variables and settings
- **`test_hash.py`** - Tests for hash functions and utilities

### Sandbox Tests (`tests/sandbox/`)
- **`test_sandbox.py`** - Comprehensive sandbox functionality tests

### MCP Tests (`tests/mcp/`)
- **`test_mcp_client.py`** - Model Control Protocol client tests

### Integration Tests (`tests/integration/`)
- **`test_fastapi_integration.py`** - FastAPI framework integration tests

### Framework Tests (`tests/frameworks/`)
- **`test_framework_agents.py`** - Tests for framework-specific agent implementations

### Agent Tests (`tests/agents/`)
- Existing agent tests for different frameworks (inherited from v0.1.0)

### API Tests (`tests/api/`)
- Existing API tests (inherited from v0.1.0)

### Utilities (`tests/utils/`)
- **`test_utils.py`** - Common test utilities and helpers

## Running Tests

### Run All Tests
```bash
# Using the test runner
python tests/run_tests.py

# Using pytest directly
pytest tests/

# With coverage
pytest tests/ --cov=src/blaxel --cov-report=term-missing
```

### Run Specific Test Categories
```bash
# Core functionality tests
pytest tests/core/

# Sandbox tests
pytest tests/sandbox/

# MCP tests
pytest tests/mcp/

# Integration tests
pytest tests/integration/

# Framework tests
pytest tests/frameworks/
```

### Run Specific Tests
```bash
# Run tests matching a pattern
python tests/run_tests.py "test_agent"

# Run a specific test file
pytest tests/core/test_agents.py

# Run a specific test function
pytest tests/core/test_agents.py::test_bl_agent_creation
```

## Test Dependencies

Install test dependencies:
```bash
# Using uv (recommended)
uv sync --group test

# Using pip
pip install pytest pytest-asyncio pytest-cov pytest-mock coverage
```

## Test Configuration

- **`conftest.py`** - Shared pytest configuration and fixtures
- **`pyproject.toml`** - Test configuration in `[tool.pytest.ini_options]`

## Test Categories

### Unit Tests
- Test individual components in isolation
- Use mocking for external dependencies
- Fast execution

### Integration Tests
- Test component interactions
- May require optional dependencies
- Use `pytest.skip()` for missing dependencies

### Framework Tests
- Test framework-specific integrations
- Gracefully handle missing optional dependencies
- Verify adapter patterns work correctly

## Key Testing Patterns

### Async Testing
All tests use `pytest.mark.asyncio` for async/await support.

### Mocking
External dependencies are mocked using `unittest.mock`:
- HTTP clients
- WebSocket connections
- File system operations
- Environment variables

### Environment Isolation
Tests use fixtures to:
- Set up clean test environments
- Restore original environment after tests
- Avoid test pollution

### Optional Dependencies
Framework tests gracefully skip when optional dependencies are not available:
```python
try:
    from some_optional_framework import Component
    # Test code here
except ImportError as e:
    pytest.skip(f"Optional dependency not available: {e}")
```

## Migrated from v0.1.0

These tests were migrated and reorganized from the v0.1.0 integration tests:
- `integrationtest/bl_agents.py` → `tests/core/test_agents.py`
- `integrationtest/bl_jobs.py` → `tests/core/test_jobs.py`
- `integrationtest/bl_models.py` → `tests/core/test_models.py`
- `integrationtest/bl_tools.py` → `tests/core/test_tools.py`
- `integrationtest/sandbox*.py` → `tests/sandbox/test_sandbox.py`
- `integrationtest/mcp_*.py` → `tests/mcp/test_mcp_client.py`
- `integrationtest/fastapi_*.py` → `tests/integration/test_fastapi_integration.py`
- `integrationtest/agent_*.py` → `tests/frameworks/test_framework_agents.py`

## Coverage Goals

- **Core functionality**: >90% coverage
- **Framework integrations**: Basic import and method existence tests
- **Error handling**: Test error paths and edge cases
- **Environment handling**: Test configuration and settings