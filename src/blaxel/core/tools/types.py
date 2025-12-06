from typing import Any, Awaitable, Callable, Dict

from pydantic import BaseModel


class ToolException(Exception):  # noqa: N818
    """Optional exception that tool throws when execution error occurs.

    When this exception is thrown, the agent will not stop working,
    but it will handle the exception according to the handle_tool_error
    variable of the tool, and the processing result will be returned
    to the agent as observation, and printed in red on the console.
    """


class Tool(BaseModel):
    name: str
    description: str
    input_schema: Dict[str, Any]
    coroutine: Callable[..., Awaitable[Any]] | None = None
    sync_coroutine: Callable[..., Any] | None = None
