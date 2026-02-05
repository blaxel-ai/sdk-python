"""Pytest configuration for integration tests."""

import pytest
import pytest_asyncio


@pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
async def reset_client():
    """Reset the global client's async httpx client for each test class.

    This ensures each test class gets a fresh httpx.AsyncClient bound to
    its own event loop, preventing "Event loop is closed" errors.
    """
    from blaxel.core.client.client import client

    # Reset at the start of each test class
    client._async_client = None

    yield

    # Reset at the end (the event loop will close after this)
    client._async_client = None


# Mark all tests in this module as integration tests
def pytest_collection_modifyitems(config, items):
    """Add integration marker to all tests in this directory."""
    for item in items:
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
