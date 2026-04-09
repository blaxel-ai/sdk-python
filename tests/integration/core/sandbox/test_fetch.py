import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from tests.helpers import default_labels, default_region, unique_name


NODE_SERVER_COMMAND = """sleep 2 && node -e "
const http = require('http');
const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('OK');
});
server.listen(3000);
"
"""


@pytest.mark.asyncio(loop_scope="class")
class TestFetch:
    """Test sandbox.fetch() for proxied port access."""

    sandbox: SandboxInstance
    sandbox_name: str

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        """Set up a sandbox with port 3000 exposed."""
        request.cls.sandbox_name = unique_name("fetch-test")
        request.cls.sandbox = await SandboxInstance.create(
            {
                "name": request.cls.sandbox_name,
                "image": "blaxel/node:latest",
                "memory": 2048,
                "ports": [{"target": 3000}],
                "region": default_region,
                "labels": default_labels,
            }
        )

        yield

        try:
            await request.cls.sandbox.delete()
        except Exception:
            pass

    async def test_fetch_returns_response_from_port(self):
        """Test that sandbox.fetch() can reach a server running inside the sandbox."""
        await self.sandbox.process.exec(
            {
                "name": "http-server",
                "command": NODE_SERVER_COMMAND,
                "wait_for_ports": [3000],
            }
        )

        response = await self.sandbox.fetch(3000)
        assert response.status_code == 200
        assert response.text == "OK"

    async def test_fetch_with_path(self):
        """Test that sandbox.fetch() forwards the path correctly."""
        response = await self.sandbox.fetch(3000, "/some/path")
        assert response.status_code == 200
