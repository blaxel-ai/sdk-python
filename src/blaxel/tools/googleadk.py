import inspect
import json
from typing import Any, Optional, override

from google.adk.tools import BaseTool, ToolContext
from google.genai import types

from .types import Tool


def get_googleadk_tools(tools: list[Tool]) -> list[BaseTool]:
    class GoogleADKTool(BaseTool):
        _tool: Tool

        def __init__(self, tool: Tool):
            super().__init__(
                name=tool.name,
                description=tool.description,
            )
            self._tool = tool

        @override
        def _get_declaration(self) -> Optional[types.FunctionDeclaration]:
            # Create a copy of the schema and remove $schema and additionalProperties
            schema = self._tool.input_schema.copy()
            if "$schema" in schema:
                del schema["$schema"]
            if "additionalProperties" in schema:
                del schema["additionalProperties"]

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
    return [GoogleADKTool(tool) for tool in tools]