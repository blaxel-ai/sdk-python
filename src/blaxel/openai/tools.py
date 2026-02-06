import json
from typing import Any

from agents import FunctionTool  # type: ignore[import-not-found]
from agents.tool_context import ToolContext  # type: ignore[import-not-found]

from blaxel.core.tools import bl_tools as bl_tools_core
from blaxel.core.tools.types import Tool


def _clean_schema_for_openai(schema: dict) -> dict:
    """Clean JSON schema to be compatible with OpenAI agents SDK.

    OpenAI agents SDK doesn't allow additionalProperties on object types.
    This function recursively removes additionalProperties and $schema fields.
    """
    if not isinstance(schema, dict):
        return schema

    cleaned_schema = schema.copy()

    # Remove $schema and additionalProperties at current level
    if "$schema" in cleaned_schema:
        del cleaned_schema["$schema"]
    if "additionalProperties" in cleaned_schema:
        del cleaned_schema["additionalProperties"]

    # Ensure object type schemas have properties
    if cleaned_schema.get("type") == "object":
        if "properties" not in cleaned_schema:
            cleaned_schema["properties"] = {}
        if "required" not in cleaned_schema:
            cleaned_schema["required"] = []

    # Recursively clean properties if they exist
    if "properties" in cleaned_schema:
        cleaned_schema["properties"] = {
            k: _clean_schema_for_openai(v) for k, v in cleaned_schema["properties"].items()
        }

    # Recursively clean items for array types
    if "items" in cleaned_schema:
        cleaned_schema["items"] = _clean_schema_for_openai(cleaned_schema["items"])

    return cleaned_schema


def get_openai_tool(tool: Tool) -> FunctionTool:
    async def openai_coroutine(
        _: ToolContext[Any],
        arguments: str,
    ) -> Any:
        if not tool.coroutine:
            raise ValueError(f"Tool {tool.name} does not have a coroutine defined")
        result = await tool.coroutine(**json.loads(arguments))
        return result

    cleaned_schema = _clean_schema_for_openai(tool.input_schema)

    return FunctionTool(
        name=tool.name,
        description=tool.description,
        params_json_schema=cleaned_schema,
        on_invoke_tool=openai_coroutine,
    )


async def bl_tools(tools_names: list[str], **kwargs) -> list[FunctionTool]:
    tools = bl_tools_core(tools_names, **kwargs)
    await tools.initialize()
    return [get_openai_tool(tool) for tool in tools.get_tools()]
