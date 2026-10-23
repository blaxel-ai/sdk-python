"""Generated models read an empty optional enum as unset.

The API has sent "" for optional enums such as a model's spec.runtime.generation
(the default model on a new workspace) and spec.runtime.type. "" is not a member
of those enums, so the generated from_dict used to raise ValueError and the whole
model failed to load.
"""

from http import HTTPStatus
from unittest.mock import AsyncMock, patch

import pytest

from blaxel.core.client.models import Error, Model, ModelRuntime
from blaxel.core.client.models.model_runtime_generation import ModelRuntimeGeneration
from blaxel.core.client.models.model_runtime_type import ModelRuntimeType
from blaxel.core.client.types import UNSET, Response
from blaxel.core.models import bl_model

DEFAULT_MODEL = {
    "metadata": {"name": "sandbox-openai"},
    "spec": {
        "runtime": {
            "model": "gpt-4o-mini",
            "type": "openai",
            "organization": "",
            "endpointName": "",
            "generation": "",
        }
    },
}


def test_model_runtime_reads_empty_generation_as_unset():
    runtime = ModelRuntime.from_dict({"generation": ""})

    assert runtime.generation is UNSET
    assert "generation" not in runtime.to_dict()


def test_model_runtime_reads_empty_type_as_unset():
    runtime = ModelRuntime.from_dict({"model": "gpt-4o-mini", "type": ""})

    assert runtime.type_ is UNSET
    assert runtime.model == "gpt-4o-mini"


def test_model_runtime_keeps_valid_values():
    runtime = ModelRuntime.from_dict({"generation": "mk3", "type": "openai"})

    assert runtime.generation == ModelRuntimeGeneration.MK3
    assert runtime.type_ == ModelRuntimeType.OPENAI


def test_model_runtime_still_rejects_unknown_values():
    with pytest.raises(ValueError):
        ModelRuntime.from_dict({"generation": "mk9"})


def test_default_model_payload_parses():
    model = Model.from_dict(DEFAULT_MODEL)

    assert model.spec.runtime.generation is UNSET
    assert model.spec.runtime.type_ == ModelRuntimeType.OPENAI


def _response(status: HTTPStatus, parsed):
    return Response(status_code=status, content=b"", headers={}, parsed=parsed)


@pytest.mark.asyncio
@patch("blaxel.core.models.find_from_cache", new=AsyncMock(return_value=None))
@patch("blaxel.core.models.get_model")
async def test_bl_model_loads_default_model(mock_get_model):
    mock_get_model.asyncio_detailed = AsyncMock(
        return_value=_response(HTTPStatus.OK, Model.from_dict(DEFAULT_MODEL))
    )

    url, type_, model = await bl_model("empty-enum-default").get_parameters()

    assert url.endswith("/models/empty-enum-default")
    assert type_ == ModelRuntimeType.OPENAI
    assert model == "gpt-4o-mini"


@pytest.mark.asyncio
@patch("blaxel.core.models.find_from_cache", new=AsyncMock(return_value=None))
@patch("blaxel.core.models.get_model")
async def test_bl_model_reports_missing_model(mock_get_model):
    mock_get_model.asyncio_detailed = AsyncMock(
        return_value=_response(HTTPStatus.NOT_FOUND, Error(error="Model not found"))
    )

    with pytest.raises(Exception, match="Model empty-enum-missing not found"):
        await bl_model("empty-enum-missing").get_parameters()


@pytest.mark.asyncio
@patch("blaxel.core.models.find_from_cache", new=AsyncMock(return_value=None))
@patch("blaxel.core.models.get_model")
async def test_bl_model_does_not_report_other_errors_as_missing(mock_get_model):
    mock_get_model.asyncio_detailed = AsyncMock(
        return_value=_response(
            HTTPStatus.FORBIDDEN, Error(error="forbidden", message="No access to this model")
        )
    )

    with pytest.raises(Exception, match=r"HTTP 403\): No access to this model"):
        await bl_model("empty-enum-forbidden").get_parameters()


@pytest.mark.asyncio
@patch("blaxel.core.models.find_from_cache", new=AsyncMock(return_value=None))
@patch("blaxel.core.models.get_model")
async def test_bl_model_surfaces_unexpected_errors(mock_get_model):
    mock_get_model.asyncio_detailed = AsyncMock(side_effect=ValueError("boom"))

    with pytest.raises(ValueError, match="boom"):
        await bl_model("empty-enum-unexpected").get_parameters()
