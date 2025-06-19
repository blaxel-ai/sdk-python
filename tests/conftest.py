"""Pytest configuration and shared fixtures."""

import os
from unittest.mock import patch

import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment variables."""
    # Set test environment variables
    test_env = {
        "BL_WORKSPACE": "test-workspace",
        "BL_TYPE": "test",
        "BL_NAME": "test-component",
        "BL_DEBUG_TELEMETRY": "false",
        "BL_ENABLE_OPENTELEMETRY": "false",
    }

    # Store original values
    original_env = {}
    for key, value in test_env.items():
        original_env[key] = os.environ.get(key)
        os.environ[key] = value

    yield

    # Restore original values
    for key, original_value in original_env.items():
        if original_value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = original_value


@pytest.fixture
def mock_client():
    """Mock the Blaxel client."""
    with patch("blaxel.core.client.client") as mock:
        yield mock


@pytest.fixture
def mock_sandbox_client():
    """Mock the sandbox client."""
    with patch("blaxel.core.sandbox.client") as mock:
        yield mock


@pytest.fixture
def mock_websocket_client():
    """Mock the websocket client for MCP."""
    with patch("blaxel.core.mcp.websocket_client") as mock:
        yield mock


@pytest.fixture
def clean_environment():
    """Clean environment fixture that removes test-specific env vars."""
    env_vars_to_clean = [
        "BL_FUNCTION_TEST_URL",
        "BL_AGENT_TEST_URL",
        "BL_JOB_TEST_URL",
        "BL_SANDBOX_TEST_URL",
    ]

    # Store original values
    original_values = {}
    for var in env_vars_to_clean:
        original_values[var] = os.environ.get(var)
        if var in os.environ:
            del os.environ[var]

    yield

    # Restore original values
    for var, original_value in original_values.items():
        if original_value is not None:
            os.environ[var] = original_value


# Mark all tests as asyncio by default
pytestmark = pytest.mark.asyncio
