import json

import pytest

from blaxel.core.common import posthog


class ImmediateThread:
    def __init__(self, target, daemon):
        self.target = target
        self.daemon = daemon

    def start(self):
        self.target()


class Response:
    def __init__(self, is_success):
        self.status_code = 200 if is_success else 503


@pytest.fixture
def telemetry(tmp_path, monkeypatch):
    telemetry_path = tmp_path / "telemetry.json"
    telemetry_path.write_text(
        json.dumps(
            {
                "distinct_id": "test-id",
                "cli": "1.2.3",
                "sdks": {"javascript": "4.5.6"},
                "future_field": {"keep": True},
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setenv("DO_NOT_TRACK", "false")
    monkeypatch.setattr(posthog, "_get_posthog_key", lambda: "test-key")
    monkeypatch.setattr(posthog, "_get_telemetry_path", lambda: telemetry_path)
    monkeypatch.setattr(posthog.settings.__class__, "version", property(lambda self: "1.0.0"))
    monkeypatch.setattr(posthog.threading, "Thread", ImmediateThread)
    posthog._telemetry_state = None
    posthog._pending_sdk_versions.clear()

    yield telemetry_path

    posthog._telemetry_state = None
    posthog._pending_sdk_versions.clear()


def test_installed_sdk_payload_schema(telemetry, monkeypatch):
    payloads = []

    def capture(*args, **kwargs):
        payloads.append(kwargs["json"])
        return Response(True)

    monkeypatch.setattr(posthog.httpx, "post", capture)

    posthog.track_sdk_installed()

    assert len(payloads) == 1
    payload = payloads[0]
    assert payload["event"] == "Installed SDK"
    assert payload["properties"]["language"] == "python"
    assert payload["properties"]["sdk"] == "core"
    assert payload["properties"]["version"] == "1.0.0"
    assert "environment" not in payload["properties"]


def test_failed_delivery_is_retried_without_persisting_version(telemetry, monkeypatch):
    responses = iter([Response(False), Response(True)])
    calls = []

    def capture(*args, **kwargs):
        calls.append(kwargs["json"])
        return next(responses)

    monkeypatch.setattr(posthog.httpx, "post", capture)

    posthog.track_sdk_installed()

    failed_state = json.loads(telemetry.read_text(encoding="utf-8"))
    assert "python" not in failed_state["sdks"]

    posthog.track_sdk_installed()

    assert len(calls) == 2
    successful_state = json.loads(telemetry.read_text(encoding="utf-8"))
    assert successful_state["sdks"]["python"] == "1.0.0"


def test_successful_delivery_is_deduplicated_and_preserves_state(telemetry, monkeypatch):
    calls = []
    threads = []

    class DeferredThread:
        def __init__(self, target, daemon):
            self.target = target
            self.daemon = daemon
            threads.append(self)

        def start(self):
            pass

    def capture(*args, **kwargs):
        calls.append(kwargs["json"])
        return Response(True)

    monkeypatch.setattr(posthog.httpx, "post", capture)
    monkeypatch.setattr(posthog.threading, "Thread", DeferredThread)

    posthog.track_sdk_installed()
    posthog.track_sdk_installed()
    assert len(threads) == 1

    threads[0].target()
    posthog.track_sdk_installed()

    assert len(calls) == 1
    assert len(threads) == 1
    state = json.loads(telemetry.read_text(encoding="utf-8"))
    assert state == {
        "distinct_id": "test-id",
        "cli": "1.2.3",
        "sdks": {"javascript": "4.5.6", "python": "1.0.0"},
        "future_field": {"keep": True},
    }


def test_flush_budget_is_imperceptible():
    """A capture against us.i.posthog.com takes ~250-350ms end to end, so a one
    second ceiling covers the happy path without letting a stalled send register
    as a hang. Because a version is only persisted after a successful delivery,
    an unreachable endpoint makes every later run pay this budget again."""
    assert posthog._POSTHOG_FLUSH_BUDGET <= 1.0


def test_save_merges_writes_from_other_processes(telemetry):
    """~/.blaxel/telemetry.json is shared by the CLI and both SDKs, each of which
    caches it in memory for the life of its process. Writing a stale snapshot
    back wholesale rolls back whatever another process recorded in the meantime,
    which makes that process re-send its "Installed" event on every later run."""
    state = posthog._load_telemetry_state()
    state["sdks"]["python"] = "1.0.0"

    # Another process writes fields this one has never seen.
    telemetry.write_text(
        json.dumps(
            {
                "distinct_id": "test-id",
                "cli": "9.9.9",
                "sdks": {"typescript": "2.0.0"},
                "brand_new_field": True,
            }
        ),
        encoding="utf-8",
    )

    posthog._save_telemetry_state(state)

    written = json.loads(telemetry.read_text(encoding="utf-8"))
    assert written["cli"] == "9.9.9", "another process's CLI version must survive"
    assert written["brand_new_field"] is True, "unknown fields must survive"
    assert written["sdks"]["typescript"] == "2.0.0", "another SDK's version must survive"
    assert written["sdks"]["python"] == "1.0.0", "this process's own version must be written"
