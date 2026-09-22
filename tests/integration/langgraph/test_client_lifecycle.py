"""Exercise pooled model connections across the suite's separate class loops."""

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest
from langchain_openai import ChatOpenAI


@pytest.fixture(scope="session")
def local_model_url():
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def do_POST(self):
            self.rfile.read(int(self.headers["Content-Length"]))
            body = json.dumps(
                {
                    "id": "local",
                    "object": "chat.completion",
                    "created": 0,
                    "model": "local",
                    "choices": [
                        {
                            "index": 0,
                            "message": {"role": "assistant", "content": "hello"},
                            "finish_reason": "stop",
                        }
                    ],
                }
            ).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/v1"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


async def invoke_local_model(url, client):
    model = ChatOpenAI(
        api_key="local",
        base_url=url,
        model="local",
        max_retries=0,
        http_async_client=client,
    )
    assert (await model.ainvoke("hello")).content == "hello"


@pytest.mark.asyncio(loop_scope="class")
class TestFirstModelLoop:
    async def test_request(self, local_model_url, model_http_client):
        await invoke_local_model(local_model_url, model_http_client)


@pytest.mark.asyncio(loop_scope="class")
class TestNextModelLoop:
    async def test_request(self, local_model_url, model_http_client):
        await invoke_local_model(local_model_url, model_http_client)
