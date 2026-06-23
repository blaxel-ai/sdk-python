"""Tests for the Pydantic AI tools wrapper."""

import pytest

from blaxel.pydantic import tools as pydantic_tools


class _DummyBlTools:
    async def initialize(self):
        return self

    def get_tools(self):
        return []


@pytest.mark.asyncio
async def test_pydantic_tools_disable_persistent_timeout_by_default(monkeypatch):
    calls = []

    def fake_bl_tools_core(tools_names, **kwargs):
        calls.append((tools_names, kwargs))
        return _DummyBlTools()

    monkeypatch.setattr(pydantic_tools, "bl_tools_core", fake_bl_tools_core)

    assert await pydantic_tools.bl_tools(["sandbox/example"]) == []
    assert calls == [(["sandbox/example"], {"timeout_enabled": False})]


@pytest.mark.asyncio
async def test_pydantic_tools_preserve_explicit_timeout_setting(monkeypatch):
    calls = []

    def fake_bl_tools_core(tools_names, **kwargs):
        calls.append((tools_names, kwargs))
        return _DummyBlTools()

    monkeypatch.setattr(pydantic_tools, "bl_tools_core", fake_bl_tools_core)

    assert await pydantic_tools.bl_tools(["sandbox/example"], timeout_enabled=True) == []
    assert calls == [(["sandbox/example"], {"timeout_enabled": True})]
