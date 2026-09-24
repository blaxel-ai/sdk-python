import pytest

pytest.importorskip("agents", reason="openai-agents is not installed")

from agents import Agent, OpenAIChatCompletionsModel  # noqa: E402
from openai import AsyncOpenAI  # noqa: E402

from blaxel.core.tools.types import Tool  # noqa: E402
from blaxel.openai.model import DynamicHeadersHTTPClient  # noqa: E402
from blaxel.openai.tools import get_openai_tool  # noqa: E402


@pytest.mark.asyncio
async def test_openai_adapter_constructs_agent_and_invokes_tool():
    async def add(a: int, b: int) -> dict[str, int]:
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

    wrapped_tool = get_openai_tool(tool)
    assert await wrapped_tool.on_invoke_tool(None, '{"a": 2, "b": 3}') == {"sum": 5}

    http_client = DynamicHeadersHTTPClient(base_url="https://example.invalid")
    try:
        model = OpenAIChatCompletionsModel(
            model="compatibility-test",
            openai_client=AsyncOpenAI(
                base_url="https://example.invalid/v1",
                api_key="not-a-secret",
                http_client=http_client,
            ),
        )
        agent = Agent(
            name="compatibility-test",
            instructions="Do not run.",
            model=model,
            tools=[wrapped_tool],
        )
        assert agent is not None
    finally:
        await http_client.aclose()
