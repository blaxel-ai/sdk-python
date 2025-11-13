import asyncio
from datetime import datetime, timedelta, timezone

import httpx

from blaxel.core.common.settings import settings
from blaxel.core.sandbox import SandboxInstance


async def test_preview_public(sandbox: SandboxInstance):
    print("🔧 [preview] public: create/list/get/url/health")
    name = "preview-test-public"
    try:
        await sandbox.previews.create(
            {
                "metadata": {"name": name},
                "spec": {"port": 443, "prefixUrl": "prefix-python", "public": True},
            }
        )
        previews = await sandbox.previews.list()
        if len(previews) < 1:
            raise AssertionError("No previews found")

        preview = await sandbox.previews.get(name)
        if preview.name != name:
            raise AssertionError("Preview name is not correct")

        url = preview.spec.url if preview.spec else None
        if not url:
            raise AssertionError("Preview URL is not correct")

        workspace = settings.workspace
        if settings.env == "dev":
            expected = f"https://prefix-python-{workspace}.preview.blaxel.dev"
        else:
            expected = f"https://prefix-python-{workspace}.preview.bl.run"

        if url != expected:
            raise AssertionError(f"Preview URL is not correct => {url}")

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{url}/health", timeout=15.0)
            if response.status_code != 200:
                raise AssertionError(
                    f"Preview is not working => {response.status_code}:{response.text}"
                )
        print("✅ [preview] public healthy")
    finally:
        try:
            await sandbox.previews.delete(name)
        except Exception:
            pass


async def test_preview_token(sandbox: SandboxInstance):
    print("🔧 [preview] private: create/token/list/url/health")
    name = "preview-test-private"
    try:
        preview = await sandbox.previews.create(
            {
                "metadata": {"name": name},
                "spec": {"port": 443, "public": False},
            }
        )

        url = preview.spec.url if preview.spec else None
        if not url:
            raise AssertionError("Preview URL is not correct")

        retrieved = await sandbox.previews.get(name)
        token = await retrieved.tokens.create(datetime.now(timezone.utc) + timedelta(minutes=10))
        tokens = await retrieved.tokens.list()
        if len(tokens) < 1:
            raise AssertionError("No tokens found")
        if not any(t.value == token.value for t in tokens):
            raise AssertionError("Token not found in list")

        async with httpx.AsyncClient() as client:
            r_no_token = await client.get(f"{url}/health", timeout=15.0)
            if r_no_token.status_code != 401:
                raise AssertionError(
                    f"Preview is not protected by token, response => {r_no_token.status_code}"
                )
            r_with_token = await client.get(
                f"{url}/health?bl_preview_token={token.value}", timeout=15.0
            )
            if r_with_token.status_code != 200:
                raise AssertionError(
                    f"Preview is not working with token, response => {r_with_token.status_code}"
                    f"url={url}/health?bl_preview_token={token.value}"
                )
        print("✅ [preview] private healthy with token")
    finally:
        try:
            # await sandbox.previews.delete(name)
            pass
        except Exception:
            pass


async def main():
    print("🚀 [previews] starting")
    sandbox = await SandboxInstance.create()
    await asyncio.sleep(10)
    try:
        await test_preview_public(sandbox)
        await test_preview_token(sandbox)
    finally:
        try:
            md = getattr(sandbox, "metadata", None)
            sbx_name = getattr(md, "name", None) if md else None
            if sbx_name:
                await SandboxInstance.delete(sbx_name)
        except Exception:
            pass
    print("🎉 [previews] done")


if __name__ == "__main__":
    asyncio.run(main())


