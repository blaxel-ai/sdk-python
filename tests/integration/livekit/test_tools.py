"""LiveKit Tools Integration Tests."""

pytest_plugins = []
import pytest  # noqa: E402

pytest.importorskip("livekit.agents", reason="livekit-agents not installed (install with: blaxel[livekit])")

import pytest_asyncio  # noqa: E402

from blaxel.core.sandbox import SandboxInstance  # noqa: E402
from blaxel.livekit import bl_tools  # noqa: E402
from tests.helpers import default_image, default_labels, unique_name  # noqa: E402


@pytest.mark.asyncio(loop_scope="class")
class TestBlTools:
    """Test bl_tools functionality."""

    sandbox: SandboxInstance | None = None
    sandbox_name: str | None = None

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        """Set up a sandbox for the test class."""
        request.cls.sandbox_name = unique_name("livekit-tools-test")
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

        def _get_tool_name(t):
            info = getattr(t, "__livekit_raw_tool_info", None)
            return info.name if info else ""

        exec_tool = next(
            (t for t in tools if "exec" in _get_tool_name(t).lower()),
            None,
        )
        assert exec_tool is not None
        result = await exec_tool({"command": "echo 'hello'"})
        assert result is not None
