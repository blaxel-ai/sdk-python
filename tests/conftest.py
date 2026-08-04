"""Pytest configuration and shared fixtures."""

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from dotenv import load_dotenv

# Load .env file from the sdk-python directory
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment variables."""
    # Set test environment variables
    test_env = {
        "BL_WORKSPACE": "test-workspace",
        "BL_TYPE": "test",
        "BL_NAME": "test-component",
        "BL_ENV": "test",
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
    """Mock the Blaxel client.

    Pre-configures get_httpx_client().request() and get_async_httpx_client().request()
    to return responses with integer status_code values, preventing ValueError when
    auto-generated API code calls HTTPStatus(response.status_code).
    """
    with patch("blaxel.core.client.client") as mock:
        # Configure default response for sync httpx client
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"{}"
        mock_response.headers = {}
        mock_response.json.return_value = {}
        mock.get_httpx_client.return_value.request.return_value = mock_response

        # Configure default response for async httpx client
        mock_async_response = MagicMock()
        mock_async_response.status_code = 200
        mock_async_response.content = b"{}"
        mock_async_response.headers = {}
        mock_async_response.json.return_value = {}
        mock.get_async_httpx_client.return_value.request.return_value = mock_async_response

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
