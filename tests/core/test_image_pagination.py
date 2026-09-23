"""Exercise generated image clients through the HTTP transport boundary."""

import httpx
import pytest

from blaxel.core.client.api.compute import list_sandboxes
from blaxel.core.client.api.images import get_image, list_image_tags, list_images
from blaxel.core.client.client import Client
from blaxel.core.client.models.list_image_tags_sort import ListImageTagsSort
from blaxel.core.client.models.status import Status
from blaxel.core.common.settings import settings

SUMMARY = {
    "metadata": {
        "name": "python",
        "status": "BUILT",
        "lastDeployedAt": "2026-09-22T10:00:00Z",
    },
    "spec": {"size": 4096, "tagCount": 10000},
}


def make_client(monkeypatch):
    monkeypatch.delenv("BL_API_VERSION", raising=False)
    requests = []

    def handle(request):
        requests.append(request)
        assert request.headers["Blaxel-Version"] == "2026-09-22"
        path = request.url.path
        if path.endswith("/tags"):
            assert request.url.params["sourceWorkspace"] == "source-workspace"
            assert request.url.params["name"] == "release"
            assert request.url.params["sort"] == "name:desc"
            return httpx.Response(
                200,
                json={"data": [{"name": "release", "size": 4096}], "meta": {"hasMore": False}},
            )
        if path == "/images/sandbox/python":
            return httpx.Response(200, json=SUMMARY)
        if path == "/sandboxes":
            return httpx.Response(200, json={"data": [], "meta": {"hasMore": False}})
        assert path == "/images"
        assert request.url.params["limit"] == "1"
        assert request.url.params["q"] == "py"
        assert request.url.params["sort"] == "name:asc"
        if "cursor" in request.url.params:
            assert request.url.params["cursor"] == "opaque+/cursor="
            return httpx.Response(200, json={"data": [], "meta": {"hasMore": False}})
        return httpx.Response(
            200,
            json={"data": [SUMMARY], "meta": {"hasMore": True, "nextCursor": "opaque+/cursor="}},
        )

    return Client(
        base_url="https://api.test",
        headers={"Blaxel-Version": settings.api_version},
        httpx_args={"transport": httpx.MockTransport(handle)},
    ), requests


def assert_summary(summary):
    assert summary.metadata.status == Status.BUILT
    assert summary.metadata.last_deployed_at == "2026-09-22T10:00:00Z"
    assert summary.spec.size == 4096
    assert summary.spec.tag_count == 10000
    assert "tags" not in summary.spec.to_dict()


def test_sync_image_catalog_and_separate_tags(monkeypatch):
    client, requests = make_client(monkeypatch)
    with client:
        page = list_images.sync(client=client, limit=1, q="py", sort="name:asc")
        assert_summary(page.data[0])
        assert page.meta.has_more
        # Fetching summaries never implicitly fetches 10,000 tags.
        assert len(requests) == 1
        last = list_images.sync(
            client=client, limit=1, q="py", sort="name:asc", cursor=page.meta.next_cursor
        )
        assert last.data == []
        assert not last.meta.has_more
        assert_summary(get_image.sync("sandbox", "python", client=client))
        tags = list_image_tags.sync(
            "sandbox",
            "python",
            client=client,
            limit=1,
            name="release",
            sort=ListImageTagsSort.NAMEDESC,
            source_workspace="source-workspace",
        )
        assert tags.data[0].name == "release"
        assert not tags.meta.has_more
        assert list_sandboxes.sync(client=client).data == []


@pytest.mark.asyncio
async def test_async_image_catalog_and_separate_tags(monkeypatch):
    client, requests = make_client(monkeypatch)
    async with client:
        page = await list_images.asyncio(client=client, limit=1, q="py", sort="name:asc")
        assert_summary(page.data[0])
        assert len(requests) == 1
        last = await list_images.asyncio(
            client=client, limit=1, q="py", sort="name:asc", cursor=page.meta.next_cursor
        )
        assert last.data == []
        assert not last.meta.has_more
        assert_summary(await get_image.asyncio("sandbox", "python", client=client))
        tags = await list_image_tags.asyncio(
            "sandbox",
            "python",
            client=client,
            limit=1,
            name="release",
            sort=ListImageTagsSort.NAMEDESC,
            source_workspace="source-workspace",
        )
        assert tags.data[0].name == "release"
        assert not tags.meta.has_more
        assert (await list_sandboxes.asyncio(client=client)).data == []


def wrapper_client(monkeypatch):
    from blaxel.core.image import image as image_module

    calls = []

    def handle(request):
        calls.append(request)
        params = request.url.params
        assert params["limit"] == "1"
        if request.url.path.endswith("/tags"):
            assert params["sort"] == "name:desc"
            assert params["q"] == "rel"
            assert params["name"] == "release"
            assert params["sourceWorkspace"] == "owner"
            item = {"name": "release"}
        else:
            assert params["sort"] == "name:asc"
            assert params["q"] == "py"
            item = SUMMARY
        return httpx.Response(
            200,
            json={
                "data": [item],
                "meta": {"hasMore": "cursor" not in params, "nextCursor": "next"},
            },
        )

    client = Client(
        base_url="https://api.test", httpx_args={"transport": httpx.MockTransport(handle)}
    )
    monkeypatch.setattr(image_module, "client", client)
    return client, calls


def test_image_helpers_fetch_only_explicit_next_pages(monkeypatch):
    from blaxel.core.image import ImageInstance

    client, calls = wrapper_client(monkeypatch)
    with client:
        page = ImageInstance.list(limit=1, q="py")
        assert len(calls) == 1
        assert_summary(page[0])
        last = page.next_page()
        assert len(calls) == 2
        assert not last.has_more
        assert not last.next_page()
        assert len(calls) == 2
        tags = ImageInstance.list_tags(
            "sandbox",
            "python",
            limit=1,
            sort=ListImageTagsSort.NAMEDESC,
            q="rel",
            name="release",
            source_workspace="owner",
        )
        assert len(calls) == 3
        assert [tag.name for tag in tags.auto_paging_iter()] == ["release", "release"]
        assert len(calls) == 4


@pytest.mark.asyncio
async def test_async_image_helpers_fetch_only_explicit_next_pages(monkeypatch):
    from blaxel.core.image import ImageInstance

    client, calls = wrapper_client(monkeypatch)
    async with client:
        page = await ImageInstance.list_async(limit=1, q="py")
        assert len(calls) == 1
        assert_summary(page[0])
        last = await page.next_page()
        assert len(calls) == 2
        assert not last.has_more
        assert not await last.next_page()
        assert len(calls) == 2
        tags = await ImageInstance.list_tags_async(
            "sandbox",
            "python",
            limit=1,
            sort=ListImageTagsSort.NAMEDESC,
            q="rel",
            name="release",
            source_workspace="owner",
        )
        assert len(calls) == 3
        assert [tag.name async for tag in tags.auto_paging_iter()] == ["release", "release"]
        assert len(calls) == 4
