"""Pytest fixtures local to the custom domain integration tests."""

from __future__ import annotations

import asyncio
import os

import pytest_asyncio

from blaxel.core.client.api.customdomains.delete_custom_domain import (
    asyncio as delete_custom_domain,
)
from blaxel.core.client.client import client


async def _safe_delete(name: str) -> None:
    try:
        await delete_custom_domain(name, client=client)
    except Exception:
        pass


@pytest_asyncio.fixture(loop_scope="module", scope="module")
async def created_domains():
    """Module-scoped bag of custom domain names to delete on teardown.

    Each test appends the names it creates (including the ones it expects the
    API to reject, in case it accepts them) and they are all deleted once the
    module finishes. Set ``SKIP_CLEANUP=1`` to keep resources around.
    """
    names: list[str] = []
    yield names
    if os.environ.get("SKIP_CLEANUP") == "1":
        print("SKIP_CLEANUP=1: skipping teardown. Resources to clean up manually:")
        print(f"  Custom domains: {names}")
        return
    await asyncio.gather(*(_safe_delete(n) for n in names))
