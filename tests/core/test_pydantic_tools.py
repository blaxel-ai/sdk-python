"""Tests for the Pydantic AI tools wrapper."""

import inspect
from typing import cast

import pytest
from pydantic_ai import RunContext

from blaxel.core.tools.types import Tool
from blaxel.pydantic import tools as pydantic_tools


class _DummyBlTools:
    async def initialize(self):
        return self

    def get_tools(self):
        return []


@pytest.mark.asyncio
async def test_pydantic_tools_mark_external_schemas_as_non_strict():
    async def invoke(**_kwargs):
        return None

    tool = Tool(
        name="codegenParallelApply",
        description="Apply code edits in parallel",
        input_schema={
            "type": "object",
            "properties": {
                "editRegions": {
                    "type": ["null", "array"],
                    "items": {
                        "type": "object",
                        "properties": {"path": {"type": "string"}},
                        "additionalProperties": False,
                    },
                }
            },
        },
        coroutine=invoke,
    )

    converted = pydantic_tools.get_pydantic_tool(tool)
    assert converted.prepare is not None
    context = cast(RunContext[object], object())
    prepared = converted.prepare(context, converted.tool_def)
    if inspect.isawaitable(prepared):
        prepared = await prepared

    assert prepared is not None
    assert prepared.strict is False


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
