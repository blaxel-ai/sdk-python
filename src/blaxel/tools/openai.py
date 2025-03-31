import json
from typing import Any

from agents import FunctionTool, RunContextWrapper

from .types import Tool


def get_openai_tool(tool: Tool) -> FunctionTool:
    async def openai_coroutine(
      _: RunContextWrapper,
      arguments: dict[str, Any],
    ) -> Any:
        result = await tool.coroutine(**json.loads(arguments))
        return result

    return FunctionTool(
        name=tool.name,
        description=tool.description,
        params_json_schema=tool.input_schema,
        on_invoke_tool=openai_coroutine,
    )

def get_openai_tools(tools: list[Tool]) -> list[FunctionTool]:
    return [get_openai_tool(tool) for tool in tools]
