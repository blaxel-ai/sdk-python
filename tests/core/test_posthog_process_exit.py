"""The SDK sends "Installed SDK" from a background thread, but plenty of real
usage is a script that imports blaxel, does one thing and exits. If the send is
not flushed before the interpreter tears down, those users are simply never
counted. These tests run a genuine short-lived subprocess against a real socket
rather than mocking the transport, because the bug only exists at process exit.
"""

import json
import subprocess
import sys
import textwrap
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

SRC = str(Path(__file__).resolve().parents[2] / "src")


class _CaptureServer:
    """Minimal stand-in for the PostHog /capture/ endpoint."""

    def __init__(self, status=200):
        self.events = []
        self._status = status
        captured = self.events
        status_code = self._status

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):  # noqa: N802
                length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(length)
                try:
                    captured.append(json.loads(body))
                except ValueError:
                    captured.append({"__unparsed__": body.decode("utf-8", "replace")})
                self.send_response(status_code)
                self.end_headers()
                self.wfile.write(b"{}")

            def log_message(self, *args):
                pass

        self._server = HTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self._server.server_port}"

    def __enter__(self):
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        return self

    def __exit__(self, *exc):
        self._server.shutdown()
        self._server.server_close()


def _run_sdk_process(tmp_path, posthog_host):
    """Import the SDK, fire the install event, and exit immediately."""
    script = textwrap.dedent(
        f"""
        import sys
        sys.path.insert(0, {SRC!r})
        import blaxel
        blaxel.__version__ = "1.0.0"
        blaxel.__posthog_key__ = "test-key"
        from blaxel.core.common import posthog
        posthog._POSTHOG_HOST = {posthog_host!r}
        posthog.track_sdk_installed()
        # No sleep, no join: exit the way a one-shot script would.
        """
    )
    return subprocess.run(
        [sys.executable, "-c", script],
        env={
            "HOME": str(tmp_path),
            "USERPROFILE": str(tmp_path),
            "DO_NOT_TRACK": "0",
            "PATH": "/usr/bin:/bin",
        },
        capture_output=True,
        text=True,
        timeout=60,
    )


def test_short_lived_process_still_delivers_installed_sdk(tmp_path):
    with _CaptureServer() as server:
        result = _run_sdk_process(tmp_path, server.url)

    assert result.returncode == 0, result.stderr
    assert len(server.events) == 1, (
        "a script that exits right after import must still report its install; "
        f"stderr={result.stderr}"
    )
    properties = server.events[0]["properties"]
    assert server.events[0]["event"] == "Installed SDK"
    assert properties["language"] == "python"
    assert properties["sdk"] == "core"
    assert properties["version"] == "1.0.0"

    state = json.loads((tmp_path / ".blaxel" / "telemetry.json").read_text())
    assert state["sdks"]["python"] == "1.0.0", "delivery must be recorded so it is not re-sent"


def test_short_lived_process_does_not_record_a_failed_delivery(tmp_path):
    """Flushing at exit must not paper over a rejected send: if PostHog did not
    accept the event, the version stays unrecorded so a later run retries."""
    with _CaptureServer(status=500) as server:
        result = _run_sdk_process(tmp_path, server.url)

    assert result.returncode == 0, result.stderr
    assert len(server.events) == 1
    state = json.loads((tmp_path / ".blaxel" / "telemetry.json").read_text())
    assert "python" not in state.get("sdks", {})


def test_exit_is_not_delayed_when_endpoint_hangs(tmp_path):
    """A server that accepts the connection and never answers must not hold the
    interpreter open; the flush is bounded and the event is simply dropped."""
    import socket
    import time

    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(("127.0.0.1", 0))
    listener.listen(5)
    host = f"http://127.0.0.1:{listener.getsockname()[1]}"

    accepted = []

    def accept_and_hang():
        try:
            conn, _ = listener.accept()
            accepted.append(conn)  # hold it open, never respond
        except OSError:
            pass

    threading.Thread(target=accept_and_hang, daemon=True).start()

    start = time.monotonic()
    result = _run_sdk_process(tmp_path, host)
    elapsed = time.monotonic() - start

    for conn in accepted:
        conn.close()
    listener.close()

    assert result.returncode == 0, result.stderr
    # Generous ceiling: interpreter startup plus SDK import dominates here, the
    # point is that the 5s transport timeout is not what bounds exit.
    assert elapsed < 4.0, f"process exit was delayed {elapsed:.1f}s by unreachable telemetry"
