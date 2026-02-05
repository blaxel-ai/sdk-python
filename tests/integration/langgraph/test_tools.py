"""LangGraph Tools Integration Tests."""

pytest_plugins = []
import pytest  # noqa: E402

pytest.importorskip("langgraph", reason="langgraph not installed (install with: blaxel[langgraph])")

import pytest_asyncio  # noqa: E402
from langgraph.prebuilt import create_react_agent  # noqa: E402

from blaxel.core.sandbox import SandboxInstance  # noqa: E402
from blaxel.langgraph import bl_model, bl_tools  # noqa: E402
from tests.helpers import default_image, default_labels, unique_name  # noqa: E402


@pytest.mark.asyncio(loop_scope="class")
class TestBlTools:
    """Test bl_tools functionality."""

    sandbox: SandboxInstance | None = None
    sandbox_name: str | None = None

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        """Set up a sandbox for the test class."""
        request.cls.sandbox_name = unique_name("langgraph-tools-test")
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

    async def test_can_load_tools_from_sandbox(self):
        """Test loading tools from sandbox."""
        tools = await bl_tools([f"sandbox/{self.sandbox_name}"])

        assert len(tools) > 0

    async def test_can_invoke_a_tool(self):
        """Test invoking a tool."""
        tools = await bl_tools([f"sandbox/{self.sandbox_name}"])

        assert len(tools) > 0

        exec_tool = next((t for t in tools if "exec" in t.name.lower()), None)
        assert exec_tool is not None
        result = await exec_tool.ainvoke({"command": "echo 'hello'"})
        assert result is not None

    async def test_agent_can_use_tools(self):
        """Test that an agent can use sandbox tools to list files."""
        model = await bl_model("sandbox-openai")
        tools = await bl_tools([f"sandbox/{self.sandbox_name}"])

        agent = create_react_agent(model, tools)
        result = await agent.ainvoke({"messages": [("user", "List the files and directories in /")]})

        assert result is not None
        assert "messages" in result
        assert len(result["messages"]) > 1
        print(f"\n[langgraph agent result] {result['messages'][-1].content}")
