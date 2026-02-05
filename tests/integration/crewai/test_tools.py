"""CrewAI Tools Integration Tests."""

pytest_plugins = []
import pytest  # noqa: E402

pytest.importorskip("crewai", reason="crewai not installed (install with: blaxel[crewai])")

import pytest_asyncio  # noqa: E402
from crewai import Agent, Crew, Task  # type: ignore[import-not-found]

from blaxel.core.sandbox import SandboxInstance  # noqa: E402
from blaxel.crewai import bl_model, bl_tools  # noqa: E402
from tests.helpers import default_image, default_labels, unique_name  # noqa: E402


@pytest.mark.asyncio(loop_scope="class")
class TestBlTools:
    """Test bl_tools functionality."""

    sandbox: SandboxInstance | None = None
    sandbox_name: str | None = None

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        """Set up a sandbox for the test class."""
        request.cls.sandbox_name = unique_name("crewai-tools-test")
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
            role="File Explorer",
            goal="List files and directories using available tools",
            backstory="You are a helpful assistant that can explore file systems.",
            tools=tools,
            llm=model,
            verbose=False,
        )
        task = Task(
            description="List the files and directories in /",
            expected_output="A list of files and directories",
            agent=agent,
        )
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=False,
        )

        result = await crew.kickoff_async()

        assert result is not None
        assert result.raw is not None
        print(f"\n[crewai agent result] {result.raw}")
