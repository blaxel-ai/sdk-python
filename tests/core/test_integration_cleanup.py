"""Regression tests for the Core integration cleanup safeguards."""

from types import SimpleNamespace

import httpx
import pytest

from blaxel.core.client.api.volumes.get_volume import _parse_response
from blaxel.core.client.models.get_workspace_features_response_200 import (
    GetWorkspaceFeaturesResponse200,
)
from blaxel.core.volume import volume as volume_module
from blaxel.core.volume.volume import VolumeAPIError, VolumeInstance
from tests.helpers import resource_labels
from tests.integration.core.conftest import (
    _TEST_RESOURCE_LABELS,
    _is_already_deleted,
    _is_test_resource,
)
from tests.integration.core.sandbox import test_volumes


def test_lite_volume_without_labels_is_not_treated_as_a_test_resource():
    listed_volume = SimpleNamespace(metadata=SimpleNamespace(name="volume-from-list"))

    assert resource_labels(listed_volume) == {}
    assert _is_test_resource(listed_volume) is False


def test_cleanup_requires_all_exact_test_labels():
    exact_match = SimpleNamespace(
        metadata=SimpleNamespace(
            labels={
                **_TEST_RESOURCE_LABELS,
                "extra": "allowed",
            }
        )
    )
    partial_labels = _TEST_RESOURCE_LABELS.copy()
    partial_labels.pop("created-by")
    partial_match = SimpleNamespace(metadata=SimpleNamespace(labels=partial_labels))

    assert _is_test_resource(exact_match) is True
    assert _is_test_resource(partial_match) is False


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("status", "body", "expected"),
    [
        (404, {"code": 404, "error": "Volume not found"}, True),
        (404, {"error": "Volume not found"}, True),
        (500, {"code": 500, "error": "Internal error"}, False),
    ],
)
async def test_cleanup_skips_a_volume_its_test_already_deleted(monkeypatch, status, body, expected):
    async def get_volume(*, volume_name, client):
        return _parse_response(client=client, response=httpx.Response(status, json=body))

    monkeypatch.setattr(volume_module, "get_volume", get_volume)

    with pytest.raises(VolumeAPIError) as caught:
        await VolumeInstance.get("volume-delete-test")

    assert _is_already_deleted(caught.value) is expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("features", "expected"),
    [
        ({}, False),
        ({"generation_mk31": True}, True),
    ],
)
async def test_workspace_feature_detection_uses_the_live_feature_map(
    monkeypatch, features, expected
):
    response = GetWorkspaceFeaturesResponse200.from_dict({"features": features})

    async def get_features(*, client):
        return response

    monkeypatch.setattr(test_volumes, "get_workspace_features", get_features)

    assert await test_volumes._workspace_feature_enabled("generation_mk31") is expected
