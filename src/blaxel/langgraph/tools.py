from typing import Any, Dict

from langchain_core.tools import StructuredTool
from mcp.types import (
    CallToolResult,
    EmbeddedResource,
    ImageContent,
    TextContent,
)

from blaxel.core.tools import bl_tools as bl_tools_core
from blaxel.core.tools.types import Tool, ToolException

NonTextContent = ImageContent | EmbeddedResource


def _clean_schema_for_openai(schema: Dict[str, Any]) -> Dict[str, Any]:
    """Clean JSON schema to be compatible with OpenAI function calling.

    OpenAI requires object schemas to have a 'properties' field, even if empty.
    This function ensures the schema is properly formatted.
    """
    if not isinstance(schema, dict):
        return schema

    cleaned = schema.copy()

    # Ensure object type schemas have properties
    if cleaned.get("type") == "object":
        if "properties" not in cleaned:
            cleaned["properties"] = {}
        if "required" not in cleaned:
            cleaned["required"] = []

    # Recursively clean nested schemas
    if "properties" in cleaned:
        cleaned["properties"] = {
            k: _clean_schema_for_openai(v) for k, v in cleaned["properties"].items()
        }
    if "items" in cleaned and isinstance(cleaned["items"], dict):
        cleaned["items"] = _clean_schema_for_openai(cleaned["items"])

    return cleaned


def get_langchain_tool(tool: Tool) -> StructuredTool:
    async def langchain_coroutine(
        **arguments: dict[str, Any],
    ) -> tuple[str | list[str], list[NonTextContent] | None]:
        result: CallToolResult = await tool.coroutine(**arguments)
        text_contents: list[TextContent] = []
        non_text_contents = []
        for content in result.content:
            if isinstance(content, TextContent):
                text_contents.append(content)
            else:
                non_text_contents.append(content)

        tool_content: str | list[str] = [content.text for content in text_contents]
        if len(text_contents) == 1:
            tool_content = tool_content[0]

        if result.isError:
            raise ToolException(tool_content)

        return tool_content, non_text_contents or None

    # Clean the schema to ensure OpenAI compatibility
    cleaned_schema = _clean_schema_for_openai(tool.input_schema)

    return StructuredTool(
        name=tool.name,
        description=tool.description,
        args_schema=cleaned_schema,
        coroutine=langchain_coroutine,
        sync_coroutine=tool.sync_coroutine,
    )


async def bl_tools(tools_names: list[str], **kwargs) -> list[StructuredTool]:
    tools = bl_tools_core(tools_names, **kwargs)
    await tools.initialize()
    return [get_langchain_tool(tool) for tool in tools.get_tools()]
