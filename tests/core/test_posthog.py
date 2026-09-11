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
