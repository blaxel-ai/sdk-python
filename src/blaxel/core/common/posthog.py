import json
import logging
import platform
import threading
import uuid
from pathlib import Path
from typing import Callable

import httpx

from .settings import settings

logger = logging.getLogger(__name__)

# PostHog API key injected at build time via sed in CI
_POSTHOG_KEY = ""

# PostHog API endpoint
_POSTHOG_HOST = "https://us.i.posthog.com"

# Telemetry state file path: ~/.blaxel/telemetry.json
_telemetry_state: dict | None = None
_telemetry_lock = threading.Lock()
_pending_sdk_versions: set[tuple[str, str]] = set()


def _get_posthog_key() -> str:
    """Return the PostHog API key injected at build time."""
    import blaxel

    return getattr(blaxel, "__posthog_key__", "") or _POSTHOG_KEY


def _get_telemetry_path() -> Path | None:
    """Return the path to the telemetry state file."""
    try:
        return Path.home() / ".blaxel" / "telemetry.json"
    except Exception:
        return None


def _load_telemetry_state() -> dict:
    """Load the telemetry state from disk."""
    global _telemetry_state
    with _telemetry_lock:
        if _telemetry_state is not None:
            return _telemetry_state

        _telemetry_state = {"distinct_id": "", "sdks": {}}

        telemetry_path = _get_telemetry_path()
        if not telemetry_path:
            return _telemetry_state

        try:
            data = telemetry_path.read_text(encoding="utf-8")
            parsed = json.loads(data)
            _telemetry_state = {
                **parsed,
                "distinct_id": parsed.get("distinct_id", ""),
                "sdks": parsed.get("sdks") or {},
            }
        except Exception:
            # File doesn't exist or is invalid - use defaults
            pass

        return _telemetry_state


def _save_telemetry_state(state: dict) -> None:
    """Save the telemetry state to disk."""
    telemetry_path = _get_telemetry_path()
    if not telemetry_path:
        return

    try:
        telemetry_path.parent.mkdir(parents=True, exist_ok=True)
        telemetry_path.write_text(
            json.dumps(state, indent=2),
            encoding="utf-8",
        )
        telemetry_path.chmod(0o600)
    except Exception:
        # Silently fail
        pass


def _get_distinct_id() -> str:
    """Return a persistent anonymous UUID for PostHog events.

    The UUID is generated on first use and stored in ~/.blaxel/telemetry.json.
    """
    state = _load_telemetry_state()
    if state["distinct_id"]:
        return state["distinct_id"]

    state["distinct_id"] = str(uuid.uuid4())
    _save_telemetry_state(state)
    return state["distinct_id"]


def _get_os_arch() -> str:
    """Get OS and architecture string."""
    try:
        system = platform.system().lower()
        machine = platform.machine().lower()
        if machine in ("x86_64", "amd64"):
            arch = "amd64"
        elif machine in ("aarch64", "arm64"):
            arch = "arm64"
        else:
            arch = machine
        return f"{system}/{arch}"
    except Exception:
        return "unknown/unknown"


def _capture_posthog_event(
    event: str,
    properties: dict | None = None,
    on_complete: Callable[[bool], None] | None = None,
) -> bool:
    """Fire-and-forget HTTP POST to PostHog capture endpoint."""
    api_key = _get_posthog_key()
    if not api_key:
        return False

    distinct_id = _get_distinct_id()
    payload = {
        "api_key": api_key,
        "event": event,
        "distinct_id": distinct_id,
        "properties": {
            "$lib": "blaxel-sdk-python",
            "$lib_version": settings.version,
            "os_arch": _get_os_arch(),
            **(properties or {}),
        },
    }

    def send() -> None:
        successful = False
        try:
            response = httpx.post(
                f"{_POSTHOG_HOST}/capture/",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=5.0,
            )
            successful = 200 <= response.status_code < 300
        except Exception:
            # Silently fail - telemetry should never break the SDK
            pass
        finally:
            if on_complete:
                try:
                    on_complete(successful)
                except Exception:
                    # Telemetry callbacks must never break the SDK
                    pass

    try:
        thread = threading.Thread(target=send, daemon=True)
        thread.start()
        return True
    except Exception:
        return False


def track_sdk_installed() -> None:
    """Track 'Installed SDK' event, deduplicated by version.

    Only fires once per SDK version. Respects DO_NOT_TRACK env var
    and ~/.blaxel/config.yaml tracking setting.
    """
    try:
        # Check tracking consent
        if not settings.tracking:
            return

        api_key = _get_posthog_key()
        if not api_key:
            return

        version = settings.version
        if not version or version == "unknown":
            return

        state = _load_telemetry_state()
        sdk_key = "python"
        pending_key = (sdk_key, version)

        # Reserve this version in memory so concurrent calls do not send duplicates.
        # It is only written to persistent state after PostHog accepts the event.
        with _telemetry_lock:
            if state.get("sdks", {}).get(sdk_key) == version:
                return
            if pending_key in _pending_sdk_versions:
                return
            _pending_sdk_versions.add(pending_key)

        def delivery_complete(successful: bool) -> None:
            with _telemetry_lock:
                _pending_sdk_versions.discard(pending_key)
                if not successful:
                    return
                if "sdks" not in state:
                    state["sdks"] = {}
                state["sdks"][sdk_key] = version
                _save_telemetry_state(state)

        try:
            started = _capture_posthog_event(
                "Installed SDK",
                {
                    "language": "python",
                    "sdk": "core",
                    "version": version,
                },
                on_complete=delivery_complete,
            )
        except Exception:
            started = False
        if not started:
            with _telemetry_lock:
                _pending_sdk_versions.discard(pending_key)
    except Exception:
        # Silently fail - telemetry should never break the SDK
        pass
