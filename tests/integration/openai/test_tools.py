"""OpenAI Tools Integration Tests."""

pytest_plugins = []
import pytest  # noqa: E402

pytest.importorskip("agents", reason="openai-agents not installed (install with: blaxel[openai])")

import pytest_asyncio  # noqa: E402
from agents import Agent, Runner  # noqa: E402

from blaxel.core.sandbox import SandboxInstance  # noqa: E402
from blaxel.openai import bl_model, bl_tools  # noqa: E402
from tests.helpers import default_image, default_labels, unique_name  # noqa: E402


@pytest.mark.asyncio(loop_scope="class")
class TestBlTools:
    """Test bl_tools functionality."""

    sandbox: SandboxInstance | None = None
    sandbox_name: str | None = None

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        """Set up a sandbox for the test class."""
        request.cls.sandbox_name = unique_name("openai-tools-test")
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
            await request.cls.sandbox.delete()
        except Exception:
            pass

    async def test_agent_can_use_tools(self):
        """Test that an agent can use sandbox tools to list files."""
        model = await bl_model("sandbox-openai")
        tools = await bl_tools([f"sandbox/{self.sandbox_name}"])

        agent = Agent(
            name="test",
            instructions="You are a helpful assistant. Use the tools available to answer the user's question.",
            model=model,
            tools=tools,
        )
        result = await Runner.run(agent, input="List the files and directories in /")

        assert result is not None
        assert result.final_output is not None
        print(f"\n[openai agent result] {result.final_output}")
