from typing import Any

from crewai.tools import BaseTool
from pydantic import BaseModel

from blaxel.core.tools import bl_tools as bl_tools_core
from blaxel.core.tools.types import Tool


def _clean_schema_for_openai(schema: dict) -> dict:
    """Clean JSON schema to be compatible with OpenAI strict mode.

    Recursively resolves anyOf patterns, ensures all schemas have type keys,
    removes additionalProperties and $schema, and ensures object types have
    properties and required fields.
    """
    if not isinstance(schema, dict):
        return schema

    cleaned = schema.copy()

    # Remove unsupported keys
    cleaned.pop("$schema", None)
    cleaned.pop("additionalProperties", None)

    # Resolve anyOf: pick the non-null type
    if "anyOf" in cleaned:
        any_of = cleaned.pop("anyOf")
        non_null = [s for s in any_of if s.get("type") != "null"]
        if non_null:
            # Merge the first non-null variant into current schema
            resolved = _clean_schema_for_openai(non_null[0])
            cleaned.update(resolved)
        else:
            cleaned["type"] = "string"

    # Ensure type exists
    if "type" not in cleaned and "properties" in cleaned:
        cleaned["type"] = "object"

    # Handle object types
    if cleaned.get("type") == "object":
        if "properties" not in cleaned:
            cleaned["properties"] = {}
        if "required" not in cleaned:
            cleaned["required"] = list(cleaned["properties"].keys())

    # Recursively clean properties
    if "properties" in cleaned:
        cleaned["properties"] = {
            k: _clean_schema_for_openai(v) for k, v in cleaned["properties"].items()
        }

    # Recursively clean array items
    if "items" in cleaned:
        cleaned["items"] = _clean_schema_for_openai(cleaned["items"])
        # Ensure items has a type
        if "type" not in cleaned["items"]:
            cleaned["items"]["type"] = "string"

    return cleaned


def _make_clean_args_schema(tool: Tool) -> type[BaseModel]:
    """Create a Pydantic model whose JSON schema returns the pre-cleaned schema.

    CrewAI calls model_json_schema() on args_schema to build the OpenAI tool
    parameters. By overriding model_json_schema we ensure the cleaned schema
    is used directly, avoiding issues with Pydantic re-introducing anyOf or
    dropping type keys on array items.
    """
    clean = _clean_schema_for_openai(tool.input_schema)

    class CleanArgsSchema(BaseModel):
        @classmethod
        def model_json_schema(cls, *args: Any, **kwargs: Any) -> dict[str, Any]:
            return clean

    CleanArgsSchema.__name__ = f"{tool.name}Schema"
    CleanArgsSchema.__qualname__ = f"{tool.name}Schema"
    return CleanArgsSchema


class CrewAITool(BaseTool):
    _tool: Tool

    def __init__(self, tool: Tool):
        super().__init__(
            name=tool.name,
            description=tool.description,
            args_schema=_make_clean_args_schema(tool),
        )
        self._tool = tool

    def _run(self, *args, **kwargs):
        if not self._tool.sync_coroutine:
            raise ValueError(f"Tool {self._tool.name} does not have a sync_coroutine defined")
        return self._tool.sync_coroutine(**kwargs)

    async def _arun(self, *args, **kwargs):
        if not self._tool.coroutine:
            raise ValueError(f"Tool {self._tool.name} does not have a coroutine defined")
        return await self._tool.coroutine(**kwargs)


async def bl_tools(tools_names: list[str], **kwargs) -> list[BaseTool]:
    tools = bl_tools_core(tools_names, **kwargs)
    await tools.initialize()
    return [CrewAITool(tool) for tool in tools.get_tools()]
