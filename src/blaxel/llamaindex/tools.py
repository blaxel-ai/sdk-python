from typing import TYPE_CHECKING

from blaxel.core.tools import bl_tools as bl_tools_core
from blaxel.core.tools.common import create_model_from_json_schema
from blaxel.core.tools.types import Tool

if TYPE_CHECKING:
    from llama_index.core.tools import FunctionTool  # type: ignore[import-not-found]


def get_llamaindex_tool(tool: Tool) -> "FunctionTool":
    from llama_index.core.tools import FunctionTool  # type: ignore[import-not-found]
    from llama_index.core.tools.types import (  # type: ignore[import-not-found]
        ToolMetadata,
    )

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


async def bl_tools(tools_names: list[str], **kwargs) -> list["FunctionTool"]:
    tools = bl_tools_core(tools_names, **kwargs)
    await tools.initialize()
    return [get_llamaindex_tool(tool) for tool in tools.get_tools()]
    await tools.initialize()
    return [get_llamaindex_tool(tool) for tool in tools.get_tools()]
