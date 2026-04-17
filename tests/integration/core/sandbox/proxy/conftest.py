"""Pytest fixtures local to the proxy integration tests."""

from __future__ import annotations

import asyncio
import os

import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance


async def _safe_delete(name: str) -> None:
    try:
        await SandboxInstance.delete(name)
    except Exception:
        pass


@pytest_asyncio.fixture(loop_scope="module", scope="module")
async def created_sandboxes():
    """Module-scoped bag of sandbox names to delete on teardown.

    Mirrors the ``proxyCleanup(createdSandboxes)`` pattern from the TS suite:
    each test appends the names it creates and they are all deleted in parallel
    once the module finishes. Set ``SKIP_CLEANUP=1`` to keep resources around.
    """
    names: list[str] = []
    yield names
    if os.environ.get("SKIP_CLEANUP") == "1":
        print("SKIP_CLEANUP=1: skipping teardown. Resources to clean up manually:")
        print(f"  Sandboxes: {names}")
        return
    await asyncio.gather(*(_safe_delete(n) for n in names))
