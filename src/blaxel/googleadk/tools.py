import inspect
from typing import Any

from google.adk.tools import BaseTool, ToolContext  # type: ignore[import-not-found]
from google.genai import types  # type: ignore[import-not-found]

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

        # Google genai Schema expects type as a single enum string (e.g. "STRING"),
        # not a JSON Schema union list like ["null", "string"].
        if "type" in cleaned_schema and isinstance(cleaned_schema["type"], list):
            type_list = [t for t in cleaned_schema["type"] if t != "null"]
            cleaned_schema["type"] = type_list[0].upper() if type_list else "STRING"
            # Mark as nullable if "null" was in the original list
            if "null" in schema["type"]:
                cleaned_schema["nullable"] = True
        elif "type" in cleaned_schema and isinstance(cleaned_schema["type"], str):
            cleaned_schema["type"] = cleaned_schema["type"].upper()

        # Ensure object types have properties
        if cleaned_schema.get("type") == "OBJECT" and "properties" not in cleaned_schema:
            cleaned_schema["properties"] = {}

        # Recursively clean properties if they exist
        if "properties" in cleaned_schema:
            cleaned_schema["properties"] = {
                k: self._clean_schema(v) for k, v in cleaned_schema["properties"].items()
            }

        # Recursively clean items for array types
        if "items" in cleaned_schema and isinstance(cleaned_schema["items"], dict):
            cleaned_schema["items"] = self._clean_schema(cleaned_schema["items"])

        return cleaned_schema

    def _get_declaration(self) -> types.FunctionDeclaration | None:
        # Clean the schema recursively
        schema = self._clean_schema(self._tool.input_schema)

        function_decl = types.FunctionDeclaration.model_validate(
            types.FunctionDeclaration(
                name=self._tool.name,
                description=self._tool.description,
                parameters=types.Schema(**schema),
            )
        )

        return function_decl

    async def run_async(self, *, args: dict[str, Any], tool_context: ToolContext) -> Any:
        if not self._tool.coroutine:
            raise ValueError(f"Tool {self._tool.name} does not have a coroutine defined")
        args_to_call = args.copy()
        signature = inspect.signature(self._tool.coroutine)
        if "tool_context" in signature.parameters:
            args_to_call["tool_context"] = tool_context
        return await self._tool.coroutine(**args_to_call) or {}


async def bl_tools(tools_names: list[str], **kwargs: Any) -> list[BaseTool]:
    tools = bl_tools_core(tools_names, **kwargs)
    await tools.initialize()
    return [GoogleADKTool(tool) for tool in tools.get_tools()]
