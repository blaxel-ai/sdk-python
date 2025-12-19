"""LangGraph Integration Tests."""

import pytest

from blaxel.langgraph import bl_model, bl_tools


PROMPT = "You are a helpful assistant that can answer questions and help with tasks."

TEST_MODELS = [
    "sandbox-openai",
]


@pytest.mark.asyncio(loop_scope="class")
class TestBlModel:
    """Test bl_model functionality."""

    @pytest.mark.parametrize("model_name", TEST_MODELS)
    async def test_can_invoke_model(self, model_name: str):
        """Test invoking a model."""
        model = await bl_model(model_name)
        result = await model.ainvoke("Say hello in one word")

        assert result is not None
        assert result.content is not None
        assert isinstance(result.content, str)


@pytest.mark.asyncio(loop_scope="class")
class TestAgentWithTools:
    """Test agent with tools."""

    async def test_can_run_agent_with_local_and_remote_tools(self):
        """Test running agent with local and remote tools."""
        from langchain_core.tools import tool as langchain_tool
        from langgraph.prebuilt import create_react_agent

        @langchain_tool
        def weather(city: str) -> str:
            """Get the weather in a specific city."""
            return f"The weather in {city} is sunny"

        model = await bl_model("sandbox-openai")
        tools = await bl_tools(["blaxel-search"])

        assert len(tools) > 0

        agent = create_react_agent(
            model=model,
            tools=[*tools, weather],
            prompt=PROMPT,
        )

        result = await agent.ainvoke({
            "messages": [{"role": "user", "content": "What's the weather in Paris?"}],
        })

        assert result is not None
        assert result["messages"] is not None
        assert len(result["messages"]) > 0
