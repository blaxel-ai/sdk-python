"""Unit tests for sandbox.fetch() and SandboxNetwork / SyncSandboxNetwork."""

import json
from unittest.mock import patch

import httpx
import pytest

from blaxel.core.client.models import Metadata, Sandbox, SandboxSpec
from blaxel.core.sandbox import SandboxInstance, SyncSandboxInstance
from blaxel.core.sandbox._network import SANDBOX_API_PORT


def _make_sandbox(cls):
    return cls(
        Sandbox(
            metadata=Metadata(name="test-sandbox", url="https://sandbox.test"),
            spec=SandboxSpec(),
        )
    )


@pytest.mark.parametrize("path", ["/", "/health", "health"])
async def test_async_fetch_rejects_sandbox_api_port_without_sending_request(path):
    sandbox = _make_sandbox(SandboxInstance)
    with patch.object(sandbox.network, "get_client") as mock_get_client:
        with pytest.raises(ValueError, match=rf"{SANDBOX_API_PORT}.*sandbox-api"):
            await sandbox.fetch(SANDBOX_API_PORT, path)
        with pytest.raises(ValueError, match=rf"{SANDBOX_API_PORT}.*sandbox-api"):
            await sandbox.network.fetch(SANDBOX_API_PORT, path)
    mock_get_client.assert_not_called()


@pytest.mark.parametrize("path", ["/", "/health", "health"])
def test_sync_fetch_rejects_sandbox_api_port_without_sending_request(path):
    sandbox = _make_sandbox(SyncSandboxInstance)
    with patch.object(sandbox.network, "get_client") as mock_get_client:
        with pytest.raises(ValueError, match=rf"{SANDBOX_API_PORT}.*sandbox-api"):
            sandbox.fetch(SANDBOX_API_PORT, path)
        with pytest.raises(ValueError, match=rf"{SANDBOX_API_PORT}.*sandbox-api"):
            sandbox.network.fetch(SANDBOX_API_PORT, path)
    mock_get_client.assert_not_called()


@pytest.mark.parametrize(
    ("path", "expected_path"),
    [
        ("/", "/port/3000/"),
        ("/health", "/port/3000/health"),
        ("health", "/port/3000/health"),
        ("", "/port/3000/"),
    ],
)
async def test_async_fetch_proxies_non_reserved_ports_and_forwards_kwargs(path, expected_path):
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(200, text="OK")

    sandbox = _make_sandbox(SandboxInstance)
    client = httpx.AsyncClient(
        base_url="https://sandbox.test",
        transport=httpx.MockTransport(handler),
    )
    try:
        with patch.object(sandbox.network, "get_client", return_value=client):
            response = await sandbox.fetch(
                3000,
                path,
                method="POST",
                headers={"X-Custom": "1"},
                json={"ok": True},
            )
    finally:
        await client.aclose()

    assert response.status_code == 200
    assert response.text == "OK"
    assert len(captured) == 1
    assert captured[0].method == "POST"
    assert captured[0].url.path == expected_path
    assert captured[0].headers["X-Custom"] == "1"
    assert json.loads(captured[0].content) == {"ok": True}


@pytest.mark.parametrize(
    ("path", "expected_path"),
    [
        ("/", "/port/3000/"),
        ("/health", "/port/3000/health"),
        ("health", "/port/3000/health"),
        ("", "/port/3000/"),
    ],
)
def test_sync_fetch_proxies_non_reserved_ports_and_forwards_kwargs(path, expected_path):
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(201, text="CREATED")

    sandbox = _make_sandbox(SyncSandboxInstance)

    def make_client() -> httpx.Client:
        return httpx.Client(
            base_url="https://sandbox.test",
            transport=httpx.MockTransport(handler),
        )

    with patch.object(sandbox.network, "get_client", side_effect=make_client):
        response = sandbox.fetch(
            3000,
            path,
            method="PUT",
            headers={"X-Custom": "2"},
            json={"sync": True},
        )

    assert response.status_code == 201
    assert response.text == "CREATED"
    assert len(captured) == 1
    assert captured[0].method == "PUT"
    assert captured[0].url.path == expected_path
    assert captured[0].headers["X-Custom"] == "2"
    assert json.loads(captured[0].content) == {"sync": True}
