from crewai.tools import BaseTool

from .common import create_model_from_json_schema
from .types import Tool


def get_crewai_tools(tools: list[Tool]) -> list[BaseTool]:
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

    return [CrewAITool(tool) for tool in tools]