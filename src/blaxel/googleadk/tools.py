import inspect
from typing import Any, Optional, override

from google.adk.tools import BaseTool, ToolContext
from google.genai import types

from blaxel.core.tools import bl_tools as bl_tools_core
from blaxel.core.tools.types import Tool


class GoogleADKTool(BaseTool):
    _tool: Tool

    def __init__(self, tool: Tool):
        super().__init__(
            name=tool.name,
            description=tool.description,
        )
        self._tool = tool

    def _clean_schema(self, schema: dict) -> dict:
        if not isinstance(schema, dict):
            return schema

        # Create a copy of the schema
        cleaned_schema = schema.copy()

        # Remove $schema and additionalProperties at current level
        if "$schema" in cleaned_schema:
            del cleaned_schema["$schema"]
        if "additionalProperties" in cleaned_schema:
            del cleaned_schema["additionalProperties"]

        # Recursively clean properties if they exist
        if "properties" in cleaned_schema:
            cleaned_schema["properties"] = {
                k: self._clean_schema(v) for k, v in cleaned_schema["properties"].items()
            }

        return cleaned_schema

    @override
    def _get_declaration(self) -> Optional[types.FunctionDeclaration]:
        # Clean the schema recursively
        schema = self._clean_schema(self._tool.input_schema)

        function_decl = types.FunctionDeclaration.model_validate(
            types.FunctionDeclaration(
                name=self._tool.name,
                description=self._tool.description,
                parameters=schema,
            )
        )

        return function_decl

    @override
    async def run_async(
        self, *, args: dict[str, Any], tool_context: ToolContext
    ) -> Any:
        args_to_call = args.copy()
        signature = inspect.signature(self._tool.coroutine)
        if 'tool_context' in signature.parameters:
            args_to_call['tool_context'] = tool_context
        return await self._tool.coroutine(**args_to_call) or {}


async def bl_tools(tools_names: list[str], **kwargs: Any) -> list[BaseTool]:
    tools = bl_tools_core(tools_names, **kwargs)
    await tools.initialize()
    return [GoogleADKTool(tool) for tool in tools.get_tools()]
