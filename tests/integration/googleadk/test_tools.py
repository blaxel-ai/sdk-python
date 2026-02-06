"""Google ADK Tools Integration Tests."""

pytest_plugins = []
import pytest  # noqa: E402

pytest.importorskip("google.adk", reason="google-adk not installed (install with: blaxel[googleadk])")

import pytest_asyncio  # noqa: E402
from google.adk.agents import Agent  # noqa: E402
from google.adk.runners import Runner  # noqa: E402
from google.adk.sessions import InMemorySessionService  # noqa: E402
from google.genai import types  # noqa: E402

from blaxel.core.sandbox import SandboxInstance  # noqa: E402
from blaxel.googleadk import bl_model, bl_tools  # noqa: E402
from tests.helpers import default_image, default_labels, unique_name  # noqa: E402


@pytest.mark.asyncio(loop_scope="class")
class TestBlTools:
    """Test bl_tools functionality."""

    sandbox: SandboxInstance | None = None
    sandbox_name: str | None = None

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        """Set up a sandbox for the test class."""
        request.cls.sandbox_name = unique_name("googleadk-tools-test")
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
            model=model,
            tools=tools,
            instruction="You are a helpful assistant. Use the tools available to answer the user's question.",
        )

        session_service = InMemorySessionService()
        session = await session_service.create_session(
            app_name="test", user_id="test-user"
        )

        runner = Runner(agent=agent, app_name="test", session_service=session_service)

        message = types.Content(
            parts=[types.Part(text="List the files and directories in /")],
            role="user",
        )

        events = []
        async for event in runner.run_async(
            user_id="test-user",
            session_id=session.id,
            new_message=message,
        ):
            events.append(event)

        assert len(events) > 0
        # Check that at least one event has content
        has_content = any(
            event.content and event.content.parts
            for event in events
        )
        assert has_content
        # Print the last event with content
        for event in reversed(events):
            if event.content and event.content.parts:
                text = " ".join(p.text for p in event.content.parts if p.text)
                print(f"\n[googleadk agent result] {text}")
                break
