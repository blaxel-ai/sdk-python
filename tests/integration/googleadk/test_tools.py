"""Google ADK Tools Integration Tests."""

pytest_plugins = []
import pytest  # noqa: E402

pytest.importorskip("google.adk", reason="google-adk not installed (install with: blaxel[googleadk])")

import pytest_asyncio  # noqa: E402

from blaxel.core.sandbox import SandboxInstance  # noqa: E402
from blaxel.googleadk import bl_tools  # noqa: E402
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

    async def test_can_load_tools_from_sandbox(self):
        """Test loading tools from sandbox."""
        tools = await bl_tools([f"sandbox/{self.sandbox_name}"])

        assert len(tools) > 0
