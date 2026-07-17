"""Tests for the lightweight Sentry error boundary and import filtering.

The SDK reports unhandled exceptions that originate in ``blaxel`` code. Expected
optional-integration import failures are filtered even when they are unhandled.
"""

import builtins
import sys
import threading
from types import SimpleNamespace

import httpx
import pytest

import blaxel
import blaxel.core.common.sentry as sentry
from blaxel.core.client import Client, errors
from blaxel.core.client.api.jobs.create_job_execution import _parse_response
from blaxel.core.common.sentry import (
    _OPTIONAL_INTEGRATION_ENTRYPOINT_MODULES,
    _is_optional_dependency_error,
)


def _raise_in_file(filename: str, code: str) -> Exception:
    """Execute ``code`` as if it lived in ``filename`` and return the exception."""
    try:
        exec(compile(code, filename, "exec"), {})
    except Exception as e:  # noqa: BLE001 - we want the raised exception object
        return e
    raise AssertionError("code did not raise")


@pytest.fixture
def installed_sentry_hooks(monkeypatch):
    """Install hooks with network capture replaced by an in-memory recorder."""
    captured = []
    main_hook_calls = []
    thread_hook_calls = []
    previous_trace = sys.gettrace()
    previous_thread_trace = threading.gettrace()

    def main_hook(exc_type, exc_value, exc_tb):
        main_hook_calls.append((exc_type, exc_value, exc_tb))

    def thread_hook(args):
        thread_hook_calls.append(args)

    monkeypatch.setattr(blaxel, "__sentry_dsn__", "https://public@example.com/1")
    monkeypatch.setenv("BL_ENV", "prod")
    monkeypatch.setattr(sys, "excepthook", main_hook)
    monkeypatch.setattr(threading, "excepthook", thread_hook)
    monkeypatch.setattr(sentry.atexit, "register", lambda _callback: None)
    monkeypatch.setattr(sentry, "capture_exception", captured.append)
    monkeypatch.setattr(sentry, "_handlers_registered", False)
    monkeypatch.setattr(sentry, "_sentry_initialized", False)
    monkeypatch.setattr(sentry, "_sentry_config", None)
    monkeypatch.setattr(sentry, "_original_excepthook", None)
    monkeypatch.setattr(sentry, "_original_threading_excepthook", None)

    try:
        sentry.init_sentry()
        yield SimpleNamespace(
            captured=captured,
            main_hook=main_hook,
            main_hook_calls=main_hook_calls,
            thread_hook=thread_hook,
            thread_hook_calls=thread_hook_calls,
            previous_trace=previous_trace,
            previous_thread_trace=previous_thread_trace,
        )
    finally:
        sys.settrace(previous_trace)
        threading.settrace(previous_thread_trace)


class TestUnhandledExceptionHooks:
    def test_init_replaces_exception_hooks_without_enabling_tracing(self, installed_sentry_hooks):
        hooks = installed_sentry_hooks

        assert sys.excepthook is sentry._blaxel_excepthook
        assert threading.excepthook is sentry._blaxel_threading_excepthook
        assert sentry._original_excepthook is hooks.main_hook
        assert sentry._original_threading_excepthook is hooks.thread_hook
        assert sys.gettrace() is hooks.previous_trace
        assert threading.gettrace() is hooks.previous_thread_trace

    def test_handled_job_404_is_not_captured(self, installed_sentry_hooks):
        """Regression for SDK-PYTHON-DB: callers may handle a missing job."""
        namespace = {
            "Client": Client,
            "errors": errors,
            "httpx": httpx,
            "_parse_response": _parse_response,
        }
        exec(
            compile(
                """
try:
    _parse_response(
        client=Client(base_url="https://api.blaxel.ai"),
        response=httpx.Response(
            404,
            content=b'{"code":404,"error":"Job not found"}',
        ),
    )
except errors.UnexpectedStatus as exc:
    handled_status = exc.status_code
""",
                "/tmp/site-packages/blaxel/core/jobs/reproduction.py",
                "exec",
            ),
            namespace,
        )

        assert namespace["handled_status"] == 404
        assert installed_sentry_hooks.captured == []
        assert installed_sentry_hooks.main_hook_calls == []

    def test_unhandled_sdk_exception_is_captured_and_chained(self, installed_sentry_hooks):
        exc = _raise_in_file(
            "/tmp/site-packages/blaxel/core/broken.py",
            "raise RuntimeError('sdk failure')",
        )

        sys.excepthook(type(exc), exc, exc.__traceback__)

        assert installed_sentry_hooks.captured == [exc]
        assert installed_sentry_hooks.main_hook_calls == [(type(exc), exc, exc.__traceback__)]

    def test_unhandled_thread_exception_is_captured_and_chained(self, installed_sentry_hooks):
        exc = _raise_in_file(
            "/tmp/site-packages/blaxel/core/worker.py",
            "raise RuntimeError('thread failure')",
        )
        args = threading.ExceptHookArgs(
            (type(exc), exc, exc.__traceback__, None),
        )

        threading.excepthook(args)

        assert installed_sentry_hooks.captured == [exc]
        assert installed_sentry_hooks.thread_hook_calls == [args]

    def test_unhandled_optional_import_is_filtered_and_chained(self, installed_sentry_hooks):
        exc = _raise_in_file(
            "/tmp/site-packages/blaxel/openai/model.py",
            "raise ModuleNotFoundError(\"No module named 'agents'\", name='agents')",
        )

        sys.excepthook(type(exc), exc, exc.__traceback__)

        assert installed_sentry_hooks.captured == []
        assert installed_sentry_hooks.main_hook_calls == [(type(exc), exc, exc.__traceback__)]

    def test_original_hooks_are_chained_when_classification_fails(
        self, installed_sentry_hooks, monkeypatch
    ):
        exc = _raise_in_file(
            "/tmp/site-packages/blaxel/core/broken.py",
            "raise RuntimeError('sdk failure')",
        )
        args = threading.ExceptHookArgs(
            (type(exc), exc, exc.__traceback__, None),
        )

        def fail_classification(_exc_type, _exc_value):
            raise RuntimeError("classification failed")

        monkeypatch.setattr(sentry, "_should_capture_unhandled_exception", fail_classification)

        with pytest.raises(RuntimeError, match="classification failed"):
            sys.excepthook(type(exc), exc, exc.__traceback__)
        with pytest.raises(RuntimeError, match="classification failed"):
            threading.excepthook(args)

        assert installed_sentry_hooks.main_hook_calls == [(type(exc), exc, exc.__traceback__)]
        assert installed_sentry_hooks.thread_hook_calls == [args]

    @pytest.mark.skipif(sys.version_info < (3, 11), reason="ExceptionGroup requires Python 3.11")
    def test_exception_group_captures_first_sdk_failure(self, installed_sentry_hooks):
        first_sdk_exc = _raise_in_file(
            "/tmp/site-packages/blaxel/core/broken.py",
            "raise RuntimeError('first sdk failure')",
        )
        second_sdk_exc = _raise_in_file(
            "/tmp/site-packages/blaxel/core/also_broken.py",
            "raise RuntimeError('second sdk failure')",
        )
        optional_exc = _raise_in_file(
            "/tmp/site-packages/blaxel/openai/model.py",
            "raise ModuleNotFoundError(\"No module named 'agents'\", name='agents')",
        )
        exception_group_type = getattr(builtins, "ExceptionGroup")
        group = exception_group_type(
            "task failures",
            [optional_exc, first_sdk_exc, second_sdk_exc],
        )

        sys.excepthook(type(group), group, group.__traceback__)

        assert installed_sentry_hooks.captured == [first_sdk_exc]
        assert installed_sentry_hooks.main_hook_calls == [(type(group), group, group.__traceback__)]

    @pytest.mark.skipif(sys.version_info < (3, 11), reason="ExceptionGroup requires Python 3.11")
    def test_optional_only_exception_group_is_filtered_in_thread(self, installed_sentry_hooks):
        optional_exc = _raise_in_file(
            "/tmp/site-packages/blaxel/openai/model.py",
            "raise ModuleNotFoundError(\"No module named 'agents'\", name='agents')",
        )
        exception_group_type = getattr(builtins, "ExceptionGroup")
        group = exception_group_type("task failures", [optional_exc])
        args = threading.ExceptHookArgs(
            (type(group), group, group.__traceback__, None),
        )

        threading.excepthook(args)

        assert installed_sentry_hooks.captured == []
        assert installed_sentry_hooks.thread_hook_calls == [args]


class TestIsOptionalDependencyError:
    """Cover the import-error classification used to suppress Sentry noise."""

    def test_missing_integration_submodule_is_optional(self):
        """The exact production symptom: a stripped install missing model.py.

        ``from .model import *`` in ``blaxel/openai/__init__.py`` raises
        ``ModuleNotFoundError: No module named 'blaxel.openai.model'``.
        """
        exc = ModuleNotFoundError(
            "No module named 'blaxel.openai.model'", name="blaxel.openai.model"
        )
        assert _is_optional_dependency_error(type(exc), exc) is True

    def test_missing_livekit_submodule_is_optional(self):
        exc = ModuleNotFoundError(
            "No module named 'blaxel.livekit.model'", name="blaxel.livekit.model"
        )
        assert _is_optional_dependency_error(type(exc), exc) is True

    def test_each_optional_integration_package_is_covered(self):
        for pkg in _OPTIONAL_INTEGRATION_ENTRYPOINT_MODULES:
            exc = ModuleNotFoundError(f"No module named '{pkg}'", name=pkg)
            assert _is_optional_dependency_error(type(exc), exc) is True, pkg

    def test_each_optional_integration_entrypoint_module_is_covered(self):
        for pkg, entrypoints in _OPTIONAL_INTEGRATION_ENTRYPOINT_MODULES.items():
            for entrypoint in entrypoints:
                missing = f"{pkg}.{entrypoint}"
                exc = ModuleNotFoundError(f"No module named '{missing}'", name=missing)
                assert _is_optional_dependency_error(type(exc), exc) is True, missing

    def test_opentelemetry_dependency_is_optional(self):
        """Existing behavior: opentelemetry import errors are still suppressed."""
        exc = ModuleNotFoundError("No module named 'opentelemetry'", name="opentelemetry")
        assert _is_optional_dependency_error(type(exc), exc) is True

    def test_missing_third_party_dep_while_loading_integration_is_optional(self):
        """A missing extra dep (e.g. ``agents`` for blaxel[openai]) is expected."""
        exc = _raise_in_file(
            "/usr/lib/python3.12/site-packages/blaxel/openai/model.py",
            "raise ModuleNotFoundError(\"No module named 'agents'\", name='agents')",
        )
        assert _is_optional_dependency_error(type(exc), exc) is True

    def test_missing_nested_blaxel_module_inside_integration_is_not_optional(self):
        """Internal integration packaging/import bugs must still reach Sentry."""
        exc = ModuleNotFoundError(
            "No module named 'blaxel.pydantic.custom.gemni'",
            name="blaxel.pydantic.custom.gemni",
        )
        assert _is_optional_dependency_error(ModuleNotFoundError, exc) is False

    def test_wrapped_integration_import_guard_error_is_optional(self):
        """The friendly optional-extra guard from blaxel.openai stays quiet."""
        cause = ModuleNotFoundError(
            "No module named 'blaxel.openai.model'",
            name="blaxel.openai.model",
        )
        exc = ImportError(
            "The openai extra dependencies are required to use the OpenAI Agents integration. "
            "Install them with: pip install blaxel[openai]"
        )
        exc.__cause__ = cause

        assert _is_optional_dependency_error(type(exc), exc) is True

    def test_missing_third_party_dep_outside_integration_is_not_optional(self):
        """A third-party import failure outside any optional integration (e.g. a
        genuine missing core dependency) must still be reported."""
        exc = _raise_in_file(
            "/usr/lib/python3.12/site-packages/blaxel/core/common/settings.py",
            "raise ModuleNotFoundError(\"No module named 'httpx'\", name='httpx')",
        )
        assert _is_optional_dependency_error(type(exc), exc) is False

    def test_core_module_import_error_is_not_optional(self):
        """A genuine SDK bug failing on a ``blaxel.*`` core module is captured."""
        exc = ModuleNotFoundError(
            "No module named 'blaxel.core.missing'", name="blaxel.core.missing"
        )
        assert _is_optional_dependency_error(type(exc), exc) is False

    def test_non_import_error_is_not_optional(self):
        exc = ValueError("not an import error")
        assert _is_optional_dependency_error(type(exc), exc) is False

    def test_circular_import_error_cause_is_not_optional(self):
        exc = ImportError("wrapped import failed")
        exc.__cause__ = exc

        assert _is_optional_dependency_error(type(exc), exc) is False
