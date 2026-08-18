"""Regression tests for the Core integration cleanup safeguards."""

from types import SimpleNamespace

import pytest

from blaxel.core.client.models.get_workspace_features_response_200 import (
    GetWorkspaceFeaturesResponse200,
)
from tests.helpers import resource_labels
from tests.integration.core.conftest import (
    _TEST_RESOURCE_LABELS,
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
