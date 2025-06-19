"""Tests for jobs functionality."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from blaxel.core.jobs import bl_job


@pytest.mark.asyncio
async def test_bl_job_creation():
    """Test job creation."""
    job = bl_job("test-job")
    assert job.name == "test-job"
    assert str(job) == "Job test-job"


@pytest.mark.asyncio
async def test_bl_job_url_properties():
    """Test job URL properties."""
    job = bl_job("myjob")

    # Test that URL properties are accessible
    assert hasattr(job, "url")
    assert hasattr(job, "external_url")
    assert hasattr(job, "internal_url")
    assert hasattr(job, "forced_url")
    assert hasattr(job, "fallback_url")


@pytest.mark.asyncio
@patch("blaxel.core.jobs.client")
async def test_bl_job_run(mock_client):
    """Test job run functionality."""
    # Mock the HTTP client properly
    mock_httpx_client = MagicMock()
    mock_async_httpx_client = MagicMock()

    # Mock sync response
    mock_sync_response = MagicMock()
    mock_sync_response.status_code = 200
    mock_sync_response.text = "Job completed successfully"
    mock_httpx_client.post.return_value = mock_sync_response

    # Mock async response
    mock_async_response = MagicMock()
    mock_async_response.status_code = 200
    mock_async_response.text = "Job completed successfully"
    mock_async_httpx_client.post = AsyncMock(return_value=mock_async_response)

    mock_client.get_httpx_client.return_value = mock_httpx_client
    mock_client.get_async_httpx_client.return_value = mock_async_httpx_client

    job = bl_job("test-job")

    # Test sync run
    result = job.run([{"name": "charlou", "age": 25}])
    assert result == "Job completed successfully"

    # Test async run
    result = await job.arun([{"name": "charlou", "age": 25}])
    assert result == "Job completed successfully"


@pytest.mark.asyncio
async def test_bl_job_methods():
    """Test job has required methods."""
    job = bl_job("test-job")

    # Test that core methods exist
    assert hasattr(job, "run")
    assert hasattr(job, "arun")
    assert hasattr(job, "call")
    assert hasattr(job, "acall")


@pytest.mark.asyncio
async def test_bl_job_representation():
    """Test job string representation."""
    job = bl_job("test-job")

    # Test string representation
    assert str(job) == "Job test-job"
    assert repr(job) == "Job test-job"
