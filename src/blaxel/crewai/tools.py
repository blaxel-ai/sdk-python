from crewai.tools import BaseTool

from blaxel.core.tools import bl_tools as bl_tools_core
from blaxel.core.tools.common import create_model_from_json_schema
from blaxel.core.tools.types import Tool


class CrewAITool(BaseTool):
    _tool: Tool

    def __init__(self, tool: Tool):
        super().__init__(
            name=tool.name,
            description=tool.description,
            args_schema=create_model_from_json_schema(tool.input_schema),
        )
        self._tool = tool

    def _run(self, *args, **kwargs):
        return self._tool.sync_coroutine(**kwargs)

async def bl_tools(tools_names: list[str], **kwargs) -> list[BaseTool]:
    tools = bl_tools_core(tools_names, **kwargs)
    await tools.initialize()
    return [CrewAITool(tool) for tool in tools.get_tools()]
    return [CrewAITool(tool) for tool in tools.get_tools()]
