"""Unit tests for the workspace secrets wrapper (destinations and delivery status)."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from blaxel.core.client.models import Secret, SecretStatus
from blaxel.core.secret.secret import SecretInstance, SyncSecretInstance


def test_upsert_body_carries_destinations():
    body = Secret(name="stripe-key", value="sk", destinations=["api.stripe.com"]).to_dict()
    assert body == {"name": "stripe-key", "value": "sk", "destinations": ["api.stripe.com"]}


def test_response_exposes_destinations_and_status():
    secret = SecretInstance(
        Secret.from_dict(
            {
                "name": "stripe-key",
                "destinations": ["api.stripe.com", "api.example.com/v1/*"],
                "status": "PENDING",
                "createdAt": "2026-11-21T00:00:00Z",
                "updatedAt": "2026-11-21T00:00:00Z",
            }
        )
    )
    assert secret.destinations == ["api.stripe.com", "api.example.com/v1/*"]
    assert secret.status == SecretStatus.PENDING


def test_delivered_secret_has_no_status():
    secret = SecretInstance(Secret.from_dict({"name": "k", "destinations": ["api.stripe.com"]}))
    assert secret.status is None


def test_deleted_secret_has_no_destinations():
    # a tombstone keeps no destinations; the API sends them as null
    secret = SecretInstance(
        Secret.from_dict({"name": "k", "destinations": None, "status": "DELETING"})
    )
    assert secret.destinations == []
    assert secret.status == SecretStatus.DELETING


@pytest.mark.asyncio
async def test_set_sends_destinations():
    response = Secret(name="k", destinations=["api.stripe.com"])
    with patch(
        "blaxel.core.secret.secret.upsert_secret", new=AsyncMock(return_value=response)
    ) as upsert:
        secret = await SecretInstance.set("k", "v", ["api.stripe.com"])
    body = upsert.call_args.kwargs["body"]
    assert body.to_dict() == {"name": "k", "value": "v", "destinations": ["api.stripe.com"]}
    assert secret.destinations == ["api.stripe.com"]


def test_sync_set_sends_destinations():
    response = Secret(name="k", destinations=["api.stripe.com"])
    with patch(
        "blaxel.core.secret.secret.upsert_secret_sync", new=MagicMock(return_value=response)
    ) as upsert:
        secret = SyncSecretInstance.set("k", "v", ["api.stripe.com"])
    body = upsert.call_args.kwargs["body"]
    assert body.to_dict() == {"name": "k", "value": "v", "destinations": ["api.stripe.com"]}
    assert isinstance(secret, SyncSecretInstance)
