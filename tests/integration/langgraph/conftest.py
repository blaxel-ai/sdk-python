"""Clients owned by the event loop of each LangGraph test class."""

import pytest
import pytest_asyncio

pytest.importorskip("langgraph")

from openai import DefaultAsyncHttpxClient  # noqa: E402


@pytest_asyncio.fixture(scope="class", loop_scope="class")
async def model_http_client():
    """Avoid LangChain's cached client surviving a closed test-class loop."""
    async with DefaultAsyncHttpxClient() as client:
        yield client
