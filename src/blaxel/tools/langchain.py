from langchain_core.tools import StructuredTool

from .types import Tool


def get_langchain_tool(tool: Tool) -> StructuredTool:
    return StructuredTool(
        name=tool.name,
        description=tool.description,
        args_schema=tool.input_schema,
        coroutine=tool.coroutine
    )

def get_langchain_tools(tools: list[Tool]) -> list[StructuredTool]:
    return [get_langchain_tool(tool) for tool in tools]