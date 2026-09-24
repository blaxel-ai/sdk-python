"""Read-only pagination contract checks against the configured API workspace."""

import asyncio

import pytest

from blaxel.core import ImageInstance
from blaxel.core.client.types import UNSET


@pytest.mark.asyncio(loop_scope="class")
class TestImagePagination:
    async def test_image_and_tag_pages(self):
        # Bound requests and duration even in a workspace with many images/tags.
        await asyncio.wait_for(self._check_pages(), timeout=45)

    async def _check_pages(self):
        images = await ImageInstance.list_async(limit=1)
        assert images.meta is not UNSET
        assert len(images) <= 1
        if images.has_more:
            assert images.next_cursor
            next_images = await images.next_page()
            assert len(next_images) <= 1
            assert next_images.meta is not UNSET

        if not images:
            return
        image = images[0]
        # Zero-valued optional aggregates may be omitted for an unbuilt image.
        if image.spec is not None:
            assert "tags" not in image.spec.to_dict()
        tags = await ImageInstance.list_tags_async(
            image.metadata.resource_type,
            image.metadata.name,
            limit=1,
            source_workspace=image.metadata.source_workspace or None,
        )
        assert tags.meta is not UNSET
        assert len(tags) <= 1
        if tags.has_more:
            assert tags.next_cursor
            next_tags = await tags.next_page()
            assert len(next_tags) <= 1
            assert next_tags.meta is not UNSET
