

from llama_index.core.tools import FunctionTool
from llama_index.core.tools.types import ToolMetadata

from .common import create_model_from_json_schema
from .types import Tool


def get_llamaindex_tool(tool: Tool) -> FunctionTool:
    model_schema = create_model_from_json_schema(
        tool.input_schema, model_name=f"{tool.name}_Schema"
    )
    return FunctionTool(
        fn=tool.sync_coroutine,
        async_fn=tool.coroutine,
        metadata=ToolMetadata(
            description=tool.description,
            name=tool.name,
            fn_schema=model_schema,
        ),
    )

def get_llamaindex_tools(tools: list[Tool]) -> list[FunctionTool]:
    return [get_llamaindex_tool(tool) for tool in tools]
