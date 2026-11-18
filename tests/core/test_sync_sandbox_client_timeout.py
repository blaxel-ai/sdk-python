"""The sync sandbox HTTP client must use a generous timeout, like the async one.

Regression test for SDK-PYTHON-13T: the sync client omitted a ``timeout``, so
httpx fell back to its 5s default and large/slow sandbox writes raised
``httpx.WriteTimeout`` ("The write operation timed out").
"""

import httpx

from blaxel.core.client.models import Metadata, Sandbox, SandboxSpec
from blaxel.core.common.settings import Settings
from blaxel.core.sandbox.default.action import SandboxAction
from blaxel.core.sandbox.sync.action import SyncSandboxAction
from blaxel.core.sandbox.types import SandboxConfiguration

# httpx's default when no timeout is passed; the value the bug fell back to.
HTTPX_DEFAULT_TIMEOUT = 5.0
EXPECTED_RW_TIMEOUT = 300.0
EXPECTED_CONNECT_TIMEOUT = 10.0


def _config(force_url: str | None = None) -> SandboxConfiguration:
    return SandboxConfiguration(
        sandbox=Sandbox(metadata=Metadata(name="timeout-test"), spec=SandboxSpec()),
        force_url=force_url,
    )


def _assert_generous_timeout(timeout: httpx.Timeout) -> None:
    assert timeout.connect == EXPECTED_CONNECT_TIMEOUT
    assert timeout.read == EXPECTED_RW_TIMEOUT
    # The write timeout is the one that raised WriteTimeout at the 5s default.
    assert timeout.write == EXPECTED_RW_TIMEOUT
    assert timeout.write != HTTPX_DEFAULT_TIMEOUT
    assert timeout.pool == EXPECTED_RW_TIMEOUT


def test_sync_client_uses_generous_timeout_with_force_url():
    action = SyncSandboxAction(_config(force_url="https://example.test"))
    client = action.get_client()
    try:
        _assert_generous_timeout(client.timeout)
    finally:
        client.close()


def test_sync_client_uses_generous_timeout_without_force_url(monkeypatch):
    # Avoid the auth/workspace lookup the default URL path would otherwise do:
    # replace the read-only ``headers`` property with a plain empty mapping.
    monkeypatch.setattr(Settings, "headers", {})
    config = _config()
    config.sandbox.metadata.url = "https://sandbox.example.test"
    action = SyncSandboxAction(config)
    client = action.get_client()
    try:
        _assert_generous_timeout(client.timeout)
    finally:
        client.close()


def test_sync_and_async_clients_share_the_same_timeout():
    sync_action = SyncSandboxAction(_config(force_url="https://example.test"))
    async_action = SandboxAction(_config(force_url="https://example.test"))
    sync_client = sync_action.get_client()
    async_client = async_action.get_client()
    try:
        assert sync_client.timeout == async_client.timeout
    finally:
        sync_client.close()
