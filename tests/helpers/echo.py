"""Self-hosted httpbin replacement for the proxy integration tests.

The proxy suite needs an external HTTPS endpoint that echoes back the headers
and body it received. It used to call ``httpbin.org``, which rate-limits the
shared Blaxel egress IPs and answers ``503`` in bursts -- taking ~30 tests down
with it on roughly half of the CI runs.

Instead we host the echo ourselves: one sandbox, one node server, one public
preview. Setup costs ~3s per pytest session and the endpoint is a real external
HTTPS host from the sandbox's point of view, so the proxy/firewall paths under
test are exercised exactly the same way.
"""

from __future__ import annotations

from urllib.parse import urlparse

from blaxel.core.sandbox import SandboxInstance

from .utils import default_image, default_labels, default_region, unique_name

# Serves the subset of httpbin routes the proxy suite actually used:
# /headers, /get, /post, /put, /delete, /redirect/N, /bytes/N.
ECHO_SERVER_SCRIPT = r"""
const http = require("http");

http.createServer((req, res) => {
  let body = "";
  req.on("data", (c) => (body += c));
  req.on("end", () => {
    if (req.url.startsWith("/redirect/")) {
      const n = parseInt(req.url.split("/")[2] || "1", 10);
      res.writeHead(302, { Location: n > 1 ? "/redirect/" + (n - 1) : "/get" });
      res.end();
      return;
    }
    if (req.url.startsWith("/bytes/")) {
      const n = parseInt(req.url.split("/")[2] || "0", 10);
      res.writeHead(200, { "Content-Type": "application/octet-stream" });
      res.end(Buffer.alloc(n, "a"));
      return;
    }
    let parsed = null;
    try {
      parsed = body ? JSON.parse(body) : null;
    } catch (e) {}
    const host = req.headers["x-forwarded-host"] || req.headers.host;
    const proto = req.headers["x-forwarded-proto"] || "https";
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(
      JSON.stringify({
        headers: req.headers,
        method: req.method,
        url: proto + "://" + host + req.url,
        data: body,
        json: parsed,
        args: {},
      })
    );
  });
}).listen(3000, "0.0.0.0", () => console.log("echo listening on 3000"));
""".strip()

_ECHO_PORT = 3000

# Cached for the lifetime of the pytest process: every test class reuses the
# same endpoint instead of paying the setup again.
_echo_url: str | None = None


async def echo_url() -> str:
    """Return the base HTTPS URL of the shared echo server, creating it if needed.

    The sandbox carries ``default_labels`` so the session-level cleanup in
    ``tests/integration/core/conftest.py`` deletes it with everything else.
    """
    global _echo_url
    if _echo_url is not None:
        return _echo_url

    sandbox = await SandboxInstance.create_if_not_exists(
        {
            "name": unique_name("echo"),
            "image": default_image,
            "region": default_region,
            "labels": default_labels,
        }
    )
    await sandbox.fs.write("/tmp/echo-server.js", ECHO_SERVER_SCRIPT)
    await sandbox.process.exec(
        {
            "name": "echo-server",
            "command": "node /tmp/echo-server.js",
            "wait_for_ports": [_ECHO_PORT],
        }
    )
    preview = await sandbox.previews.create_if_not_exists(
        {
            "metadata": {"name": "echo"},
            "spec": {"port": _ECHO_PORT, "public": True},
        }
    )

    _echo_url = preview.spec.url
    return _echo_url


async def echo_host() -> str:
    """Hostname of the echo server, for firewall allow/deny lists."""
    return urlparse(await echo_url()).hostname
