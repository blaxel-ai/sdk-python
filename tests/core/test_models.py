"""Tests for models functionality."""

from unittest.mock import AsyncMock, patch

import pytest

from blaxel.core.models import bl_model


@pytest.mark.asyncio
async def test_bl_model_creation():
    """Test model creation."""
    model = bl_model("gpt-4o-mini")
    assert model.model_name == "gpt-4o-mini"
    assert isinstance(model.kwargs, dict)


@pytest.mark.asyncio
@patch("blaxel.core.models.get_model")
async def test_bl_model_get_parameters(mock_get_model):
    """Test model parameter retrieval."""
    # Mock the model response
    mock_model_data = AsyncMock()
    mock_model_data.spec.runtime.type_ = "openai"
    mock_model_data.spec.runtime.model = "gpt-4o-mini"
    mock_get_model.asyncio.return_value = mock_model_data

    model = bl_model("gpt-4o-mini")

    # Test that get_parameters method exists
    assert hasattr(model, "get_parameters")


@pytest.mark.asyncio
async def test_bl_model_with_kwargs():
    """Test model creation with additional kwargs."""
    kwargs = {"temperature": 0.7, "max_tokens": 100}
    model = bl_model("gpt-4o-mini", **kwargs)

    assert model.model_name == "gpt-4o-mini"
    assert model.kwargs == kwargs


@pytest.mark.asyncio
async def test_bl_model_different_models():
    """Test different model names."""
    models = [
        "gpt-4o-mini",
        "claude-3-5-sonnet",
        "xai-grok-beta",
        "cohere-command-r-plus",
        "gemini-2-0-flash",
        "deepseek-chat",
        "mistral-large-latest",
        "cerebras-llama-4-scout-17b",
    ]

    for model_name in models:
        model = bl_model(model_name)
        assert model.model_name == model_name


@pytest.mark.asyncio
async def test_bl_model_cache():
    """Test model caching functionality."""
    model = bl_model("gpt-4o-mini")

    # Test that models class attribute exists for caching
    assert hasattr(model, "models")
    assert isinstance(model.models, dict)


@pytest.mark.asyncio
async def test_bl_model_metadata_method():
    """Test model metadata retrieval method."""
    model = bl_model("gpt-4o-mini")

    # Test that _get_model_metadata method exists
    assert hasattr(model, "_get_model_metadata")
    assert callable(getattr(model, "_get_model_metadata"))


# Note: Framework conversion methods (to_langchain, to_llamaindex, etc.)
# are available in the framework-specific modules, not in the core model
