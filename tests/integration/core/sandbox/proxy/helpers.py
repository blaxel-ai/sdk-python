"""Shared helpers for proxy integration tests.

Mirrors the structure of ``tests/integration/sandbox/proxy/helpers.ts`` in the
TypeScript SDK so tests can be ported 1:1.
"""

from __future__ import annotations

import json
import os

from blaxel.core.client.types import Unset

# The proxy/network routing feature is only available in specific regions, so
# these tests override ``tests.helpers.default_region`` (which points at
# ``us-pdx-1``) to keep creating sandboxes in ``us-was-1`` on prod.
_env = os.environ.get("BL_ENV", "prod")
default_region = "eu-dub-1" if _env == "dev" else "us-was-1"

PROXY_HELPER_SCRIPT = r"""
const https = require("https");
const tls = require("tls");
const method = process.argv[2] || "GET";
const targetUrl = process.argv[3] || "https://httpbin.org/headers";
const extraHeaders = process.argv[4] ? JSON.parse(process.argv[4]) : {};
const bodyData = process.argv[5] || null;
const proxyUrl = process.env.HTTPS_PROXY || process.env.https_proxy ||
                 process.env.HTTP_PROXY || process.env.http_proxy;

function fire(socket) {
  const t = new URL(targetUrl);
  const opts = {
    hostname: t.hostname, port: t.port || 443,
    path: t.pathname + t.search, method,
    headers: { ...extraHeaders }, servername: t.hostname,
  };
  if (socket) { opts.socket = socket; opts.agent = false; }
  if (bodyData) {
    opts.headers["Content-Type"] = "application/json";
    opts.headers["Content-Length"] = Buffer.byteLength(bodyData);
  }
  const req = https.request(opts, (r) => {
    let d = ""; r.on("data", c => d += c);
    r.on("end", () => { process.stdout.write(d); process.exit(0); });
  });
  req.on("error", (e) => { process.stderr.write("REQ ERR: " + e.message + "\n"); process.exit(1); });
  if (bodyData) req.write(bodyData);
  req.end();
}

if (!proxyUrl) { fire(null); }
else {
  const p = new URL(proxyUrl);
  const t = new URL(targetUrl);
  const port = parseInt(p.port) || (p.protocol === "https:" ? 443 : 3128);
  const auth = (p.username || p.password)
    ? "Proxy-Authorization: Basic " +
      Buffer.from(decodeURIComponent(p.username||"") + ":" + decodeURIComponent(p.password||"")).toString("base64") + "\r\n"
    : "";
  const connectMsg = "CONNECT " + t.hostname + ":443 HTTP/1.1\r\n" +
    "Host: " + t.hostname + ":443\r\n" + auth + "\r\n";

  function onSocket(sock) {
    let buf = "";
    sock.on("data", function h(chunk) {
      buf += chunk.toString();
      if (buf.indexOf("\r\n\r\n") < 0) return;
      sock.removeListener("data", h);
      const code = parseInt(buf.split(" ")[1]);
      if (code !== 200) {
        process.stderr.write("CONNECT " + code + "\n");
        process.exit(1);
      }
      fire(sock);
    });
    sock.write(connectMsg);
  }

  const timeout = setTimeout(() => { process.stderr.write("PROXY TIMEOUT\n"); process.exit(1); }, 15000);
  if (p.protocol === "https:") {
    const s = tls.connect({ host: p.hostname, port }, () => { clearTimeout(timeout); onSocket(s); });
    s.on("error", (e) => { clearTimeout(timeout); process.stderr.write("PROXY TLS: " + e.message + "\n"); process.exit(1); });
  } else {
    const s = require("net").connect({ host: p.hostname, port }, () => { clearTimeout(timeout); onSocket(s); });
    s.on("error", (e) => { clearTimeout(timeout); process.stderr.write("PROXY TCP: " + e.message + "\n"); process.exit(1); });
  }
}
""".strip()


PYTHON_HELPER_SCRIPT = """
import sys, json, requests
method = sys.argv[1] if len(sys.argv) > 1 else "GET"
url = sys.argv[2] if len(sys.argv) > 2 else "https://httpbin.org/headers"
headers = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
body = sys.argv[4] if len(sys.argv) > 4 else None
resp = requests.request(method, url, headers=headers, data=body, timeout=30)
print(resp.text)
""".strip()


def not_unset(val) -> bool:
    """Return True if val is a real value (not Unset/None)."""
    return val is not None and not isinstance(val, Unset)


def parse_json_output(logs: str | None) -> dict:
    """Extract the first balanced JSON object from command output."""
    if not logs:
        raise ValueError("No output from command")
    trimmed = logs.strip()
    start = trimmed.find("{")
    if start == -1:
        raise ValueError(f"No JSON found in output: {trimmed[:200]}")
    depth = 0
    end = -1
    for i in range(start, len(trimmed)):
        if trimmed[i] == "{":
            depth += 1
        elif trimmed[i] == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    if end == -1:
        raise ValueError(f"Unterminated JSON in output: {trimmed[:300]}")
    return json.loads(trimmed[start:end])


def lowercase_keys(obj: dict[str, str]) -> dict[str, str]:
    return {k.lower(): v for k, v in obj.items()}
