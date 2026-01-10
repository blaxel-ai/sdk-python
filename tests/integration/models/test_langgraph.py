"""LangGraph Integration Tests."""

import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from blaxel.langgraph import bl_model, bl_tools
from tests.helpers import default_image, default_labels, unique_name

PROMPT = "You are a helpful assistant that can execute commands in a sandbox environment."

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

    sandbox: SandboxInstance = None
    sandbox_name: str = None

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        """Set up a sandbox for the test class."""
        request.cls.sandbox_name = unique_name("langgraph-model-test")
        request.cls.sandbox = await SandboxInstance.create(
            {
                "name": request.cls.sandbox_name,
                "image": default_image,
                "memory": 2048,
                "labels": default_labels,
            }
        )

        yield

        # Cleanup
        try:
            await SandboxInstance.delete(request.cls.sandbox_name)
        except Exception:
            pass

    async def test_can_run_agent_with_local_and_sandbox_tools(self):
        """Test running agent with local and sandbox tools."""
        from langchain_core.tools import tool as langchain_tool
        from langgraph.prebuilt import create_react_agent

        @langchain_tool
        def weather(city: str) -> str:
            """Get the weather in a specific city."""
            return f"The weather in {city} is sunny"

        model = await bl_model("sandbox-openai")
        tools = await bl_tools([f"sandbox/{self.sandbox_name}"], timeout_enabled=False)

        assert len(tools) > 0

        agent = create_react_agent(
            model=model,
            tools=[*tools, weather],
            prompt=PROMPT,
        )

        result = await agent.ainvoke(
            {
                "messages": [
                    {"role": "user", "content": "Execute the command: echo 'Hello from sandbox'"}
                ],
            }
        )

        assert result is not None
        assert result["messages"] is not None
        assert len(result["messages"]) > 0
