import json
from typing import Any

from agents import FunctionTool, RunContextWrapper

from blaxel.core.tools import bl_tools as bl_tools_core
from blaxel.core.tools.types import Tool


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

async def bl_tools(tools_names: list[str], **kwargs) -> list[FunctionTool]:
    tools = bl_tools_core(tools_names, **kwargs)
    await tools.initialize()
    return [get_openai_tool(tool) for tool in tools.get_tools()]
    return [get_openai_tool(tool) for tool in tools.get_tools()]
