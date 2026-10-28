"""Tests for models functionality."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from blaxel.core.client.models import Error, Model
from blaxel.core.errors import BlaxelError, ModelNotFoundError
from blaxel.core.models import BLModel, bl_model


@pytest.fixture(autouse=True)
def _clear_model_cache():
    """BLModel.models is a shared class attribute; isolate it between tests."""
    BLModel.models.clear()
    yield
    BLModel.models.clear()


def _error_response(status_code: int) -> Error:
    """Build a modeled ``Error`` carrying an HTTP response, like ``get_model`` does."""
    error = Error(error="boom")
    error._response = httpx.Response(status_code, content=b'{"error":"boom"}')
    return error


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


@pytest.mark.asyncio
@patch("blaxel.core.models.find_from_cache", new_callable=AsyncMock)
@patch("blaxel.core.models.get_model")
async def test_get_model_metadata_returns_model(mock_get_model, mock_cache):
    """A 200 response (a real ``Model``) is returned unchanged."""
    mock_cache.return_value = None
    model_obj = Model.__new__(Model)  # isinstance check only; attrs are not touched
    mock_get_model.asyncio = AsyncMock(return_value=model_obj)

    assert await bl_model("some-model")._get_model_metadata() is model_obj


@pytest.mark.asyncio
@patch("blaxel.core.models.find_from_cache", new_callable=AsyncMock)
@patch("blaxel.core.models.get_model")
async def test_get_model_metadata_treats_404_error_as_not_found(mock_get_model, mock_cache):
    """A documented 404 deserializes to an ``Error``; treat it as "not found"."""
    mock_cache.return_value = None
    mock_get_model.asyncio = AsyncMock(return_value=_error_response(404))

    assert await bl_model("missing-model")._get_model_metadata() is None


@pytest.mark.asyncio
@patch("blaxel.core.models.find_from_cache", new_callable=AsyncMock)
@patch("blaxel.core.models.get_model")
async def test_get_model_metadata_surfaces_non_404_error(mock_get_model, mock_cache):
    """A non-404 documented status is surfaced, not masked as "not found"."""
    mock_cache.return_value = None
    mock_get_model.asyncio = AsyncMock(return_value=_error_response(500))

    with pytest.raises(BlaxelError) as excinfo:
        await bl_model("boom-model")._get_model_metadata()

    assert not isinstance(excinfo.value, ModelNotFoundError)
    assert excinfo.value.status == 500


@pytest.mark.asyncio
@patch("blaxel.core.models.find_from_cache", new_callable=AsyncMock)
@patch("blaxel.core.models.get_model")
async def test_get_model_metadata_propagates_transient_error(mock_get_model, mock_cache):
    """Transient/network failures propagate instead of becoming a false "not found"."""
    mock_cache.return_value = None
    mock_get_model.asyncio = AsyncMock(side_effect=httpx.ConnectError("connection reset"))

    with pytest.raises(httpx.ConnectError):
        await bl_model("transient-model")._get_model_metadata()


@pytest.mark.asyncio
@patch.object(BLModel, "_get_model_metadata", new_callable=AsyncMock)
async def test_get_parameters_raises_model_not_found(mock_meta):
    """A missing model raises a catchable ``ModelNotFoundError`` (not a bare Exception)."""
    mock_meta.return_value = None

    with pytest.raises(ModelNotFoundError, match="Model ghost-model not found"):
        await bl_model("ghost-model").get_parameters()


@pytest.mark.asyncio
@patch("blaxel.core.models.find_from_cache", new_callable=AsyncMock)
@patch("blaxel.core.models.get_model")
async def test_get_parameters_on_404_raises_model_not_found(mock_get_model, mock_cache):
    """Regression: a 404 ``Error`` must become ModelNotFoundError, not AttributeError."""
    mock_cache.return_value = None
    mock_get_model.asyncio = AsyncMock(return_value=_error_response(404))

    with pytest.raises(ModelNotFoundError, match="Model sandbox-openai not found"):
        await bl_model("sandbox-openai").get_parameters()


@pytest.mark.asyncio
@patch.object(BLModel, "_get_model_metadata", new_callable=AsyncMock)
async def test_get_parameters_returns_runtime_parameters(mock_meta):
    """The happy path returns (url, type, model) from the model runtime."""
    runtime = MagicMock()
    runtime.type_ = "openai"
    runtime.model = "gpt-4o-mini"
    model_data = MagicMock()
    model_data.spec.runtime = runtime
    mock_meta.return_value = model_data

    url, model_type, model_name = await bl_model("gpt-4o-mini").get_parameters()

    assert model_type == "openai"
    assert model_name == "gpt-4o-mini"
    assert url.endswith("/models/gpt-4o-mini")


@pytest.mark.asyncio
@patch.object(BLModel, "_get_model_metadata", new_callable=AsyncMock)
async def test_get_parameters_raises_when_model_has_no_runtime(mock_meta):
    """A model without a runtime raises ModelNotFoundError rather than a bare Exception."""
    model_data = MagicMock()
    model_data.spec.runtime = None
    mock_meta.return_value = model_data

    with pytest.raises(ModelNotFoundError, match="has no runtime"):
        await bl_model("runtimeless-model").get_parameters()


# Note: Framework conversion methods (to_langchain, to_llamaindex, etc.)
# are available in the framework-specific modules, not in the core model
