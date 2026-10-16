"""Workspace secrets integration tests (write-only values, versioned on the backend)."""

import pytest
import pytest_asyncio

from blaxel.core import SecretInstance, SyncSecretInstance
from blaxel.core.client.client import client
from blaxel.core.client.types import UNSET
from blaxel.core.errors import BlaxelError
from tests.helpers import unique_name

# Workspace secrets are behind the "workspace-secrets" feature flag (403 when off,
# 404 on environments that predate controlplane#5736): skip unless the workspace has them.
pytestmark = pytest.mark.skipif(
    client.get_httpx_client().get("/secrets").status_code in (403, 404),
    reason="workspace secrets not enabled for this workspace/environment",
)


def _secret_name(prefix: str) -> str:
    return unique_name(prefix).replace(".", "-")


def _by_name(secrets: list[SecretInstance], name: str) -> list[SecretInstance]:
    return [s for s in secrets if s.name == name]


@pytest.mark.asyncio(loop_scope="class")
class TestSecrets:
    created: list[str] = []

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def cleanup(self, request):
        request.cls.created = []
        yield
        for name in request.cls.created:
            try:
                await SecretInstance.delete(name)
            except BlaxelError:
                pass

    async def test_set_list_rotate_delete(self):
        name = _secret_name("sdk-test-secret")
        self.created.append(name)

        created = await SecretInstance.set(name, "first-value", ["api.stripe.com"])
        assert created.name == name
        assert created.destinations == ["api.stripe.com"]
        assert created.secret.value is UNSET, "the value must never be echoed back"

        listed = _by_name(await SecretInstance.list(), name)
        assert len(listed) == 1
        assert listed[0].destinations == ["api.stripe.com"]
        assert listed[0].created_at is not None
        assert listed[0].updated_at is not None
        assert listed[0].secret.value is UNSET

        rotated = await SecretInstance.set(
            name, "second-value", ["api.stripe.com", "api.example.com/v1/*"]
        )
        assert rotated.destinations == ["api.stripe.com", "api.example.com/v1/*"]
        listed_rotated = _by_name(await SecretInstance.list(), name)
        assert len(listed_rotated) == 1, "rotation must not create a second entry"
        assert listed_rotated[0].destinations == ["api.stripe.com", "api.example.com/v1/*"]
        assert listed_rotated[0].created_at == listed[0].created_at
        assert listed_rotated[0].updated_at >= listed[0].updated_at
        assert listed_rotated[0].secret.value is UNSET

        deleted = await SecretInstance.delete(name)
        assert deleted.name == name
        self.created.remove(name)
        assert _by_name(await SecretInstance.list(), name) == []

    async def test_delete_unknown_secret_is_idempotent(self):
        await SecretInstance.delete(_secret_name("sdk-test-secret-missing"))

    async def test_invalid_name_rejected(self):
        with pytest.raises(BlaxelError):
            await SecretInstance.set("not a valid name!", "value", ["api.stripe.com"])

    async def test_empty_destinations_rejected(self):
        with pytest.raises(BlaxelError):
            await SecretInstance.set(_secret_name("sdk-test-secret-nodest"), "value", [])

    async def test_wildcard_destination_rejected(self):
        with pytest.raises(BlaxelError):
            await SecretInstance.set(_secret_name("sdk-test-secret-wild"), "value", ["*"])


class TestSyncSecrets:
    def test_sync_set_list_delete(self):
        name = _secret_name("sdk-test-secret-sync")
        try:
            created = SyncSecretInstance.set(name, "value", ["api.stripe.com"])
            assert created.name == name
            assert created.destinations == ["api.stripe.com"]
            assert name in {s.name for s in SyncSecretInstance.list()}
        finally:
            SyncSecretInstance.delete(name)
        assert name not in {s.name for s in SyncSecretInstance.list()}
