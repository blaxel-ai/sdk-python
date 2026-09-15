import inspect

import pytest

pytest.importorskip("google.adk", reason="google-adk is not installed")

from google.adk.agents import Agent  # noqa: E402
from google.adk.runners import Runner  # noqa: E402
from google.adk.sessions import InMemorySessionService  # noqa: E402

from blaxel.core.tools.types import Tool  # noqa: E402
from blaxel.googleadk.model import get_google_adk_model  # noqa: E402
from blaxel.googleadk.tools import GoogleADKTool  # noqa: E402


@pytest.mark.asyncio
async def test_googleadk_adapter_constructs_runner_and_invokes_tool():
    expected_tool_context = object()

    async def add(a: int, b: int, tool_context=None) -> dict[str, int]:
        assert tool_context is expected_tool_context
        return {"sum": a + b}

    tool = Tool(
        name="add",
        description="Add two numbers",
        input_schema={
            "type": "object",
            "properties": {
                "a": {"type": "integer"},
                "b": {"type": "integer"},
            },
            "required": ["a", "b"],
            "additionalProperties": False,
        },
        coroutine=add,
    )

    wrapped_tool = GoogleADKTool(tool)
    declaration = wrapped_tool._get_declaration()
    assert declaration is not None
    assert declaration.name == "add"
    assert await wrapped_tool.run_async(
        args={"a": 2, "b": 3}, tool_context=expected_tool_context
    ) == {"sum": 5}

    model = await get_google_adk_model(
        "https://example.invalid", "openai", "compatibility-test"
    )
    agent = Agent(
        name="compatibility_test",
        instruction="Do not run.",
        model=model,
        tools=[wrapped_tool],
    )
    session_service = InMemorySessionService()
    session_result = session_service.create_session(
        app_name="compatibility-test",
        user_id="compatibility-user",
    )
    session = await session_result if inspect.isawaitable(session_result) else session_result
    runner = Runner(
        agent=agent,
        app_name="compatibility-test",
        session_service=session_service,
    )

    assert session is not None
    assert runner is not None
