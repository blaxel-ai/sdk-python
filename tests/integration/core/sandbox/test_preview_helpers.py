"""Small base-image preview helper checks (async and sync), no scheduler waits."""

import asyncio
import inspect
import logging
from datetime import datetime, timedelta, timezone
from typing import Any

import httpx
import pytest
import pytest_asyncio

from blaxel.core import SandboxInstance, SyncSandboxInstance
from tests.helpers import default_image, default_labels, unique_name


async def call(fn, *args, **kwargs):
    result = fn(*args, **kwargs)
    return await result if inspect.isawaitable(result) else result


async def _wait_for_http(
    client: httpx.AsyncClient,
    url: str,
    status: int,
    params: dict[str, str] | None = None,
) -> httpx.Response:
    loop = asyncio.get_running_loop()
    deadline = loop.time() + 10
    last_status = None
    while True:
        try:
            response = await client.get(url, params=params, timeout=2)
            last_status = response.status_code
            if last_status == status:
                return response
        except httpx.TransportError:
            pass
        if loop.time() >= deadline:
            # Do not include the credential-bearing request URL in failure output.
            pytest.fail(f"Preview did not reach HTTP {status}; last status: {last_status}")
        await asyncio.sleep(0.25)


@pytest.mark.asyncio(loop_scope="class")
class TestPreviewHelpers:
    sandbox: Any

    @pytest_asyncio.fixture(
        autouse=True,
        scope="class",
        loop_scope="class",
        params=[SandboxInstance, SyncSandboxInstance],
        ids=["async", "sync"],
    )
    async def cleanup(self, request):
        cls = request.param
        name = unique_name("preview-helpers")
        failed_before = request.session.testsfailed
        setup_failed = False
        try:
            request.cls.sandbox = await call(
                cls.create,
                {
                    "name": name,
                    "image": default_image,
                    "memory": 512,
                    "region": "us-was-1",
                    "ports": [{"target": 3000}],
                    "labels": default_labels,
                },
            )
            await call(
                self.sandbox.process.exec,
                {
                    "command": 'node -e \'require("http").createServer((req,res)=>res.end("pm-523-ok")).listen(3000,"0.0.0.0")\'',
                    "wait_for_ports": [3000],
                },
            )
            yield
        except BaseException:
            setup_failed = True
            raise
        finally:
            try:
                await call(cls.delete, name)
            except Exception as error:
                if setup_failed or request.session.testsfailed > failed_before:
                    logging.getLogger(__name__).error(
                        "Preview helper cleanup failed (%s); preserving original failure",
                        type(error).__name__,
                    )
                else:
                    raise

    async def test_private_reuse_short_ceiling_and_legacy(self):
        preview = await call(self.sandbox.previews.create_if_not_exists, {"port": 3000})
        assert preview.name == "preview-3000" and preview.spec.public is False
        assert preview.url and not preview.spec.prefix_url
        token = await call(preview.tokens.create_if_expired)
        assert token.value and token.name
        raw_expiry = token.preview_token.spec.expires_at
        expiry = datetime.fromisoformat(raw_expiry.replace("Z", "+00:00"))
        assert (
            timedelta(hours=23, minutes=59)
            < expiry - datetime.now(timezone.utc)
            <= timedelta(hours=24)
        )
        async with httpx.AsyncClient(timeout=15) as client:
            denied = await _wait_for_http(client, preview.url, 401)
            allowed = await _wait_for_http(
                client,
                preview.url,
                200,
                params={"bl_preview_token": token.value},
            )
        assert denied.status_code == 401
        assert allowed.status_code == 200 and allowed.text == "pm-523-ok"
        again = await call(self.sandbox.previews.create_if_not_exists, {"port": 3000})
        reused = await call(again.tokens.create_if_expired)
        assert (again.url, again.name) == (preview.url, preview.name)
        assert (reused.value, reused.name) == (token.value, token.name)
        short = await call(
            preview.tokens.create_if_expired,
            datetime.now(timezone.utc) + timedelta(minutes=30),
            timedelta(minutes=5),
        )
        assert short.value != token.value and short.name != token.name
        public = await call(
            self.sandbox.previews.create, {"port": 3000, "name": "public-app", "public": True}
        )
        assert public.name == "public-app" and public.spec.public is True
        full = await call(
            self.sandbox.previews.create,
            {
                "metadata": {"name": "legacy-app"},
                "spec": {"port": 3000, "public": False},
            },
        )
        assert full.name == "legacy-app" and full.url
        await call(preview.tokens.delete, token.name)
