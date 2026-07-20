"""Tests for the lightweight Sentry error boundary and import filtering.

The SDK reports exceptions only when they reach a last-chance runtime boundary and
originate in the installed ``blaxel`` package. Expected optional-integration import
failures remain filtered even when they are unhandled.
"""

import asyncio
import gc
import json
import sys
import threading
import time
from queue import Queue
from types import SimpleNamespace
from typing import Any, cast

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


def _raise_in_file(filename: str, code: str, namespace=None) -> BaseException:
    """Execute ``code`` as if it lived in ``filename`` and return the exception."""
    try:
        exec(compile(code, filename, "exec"), namespace or {})
    except BaseException as error:  # noqa: BLE001 - tests need the raised object
        return error
    raise AssertionError("code did not raise")


def _define_in_file(filename: str, code: str) -> dict:
    namespace: dict = {}
    exec(compile(code, filename, "exec"), namespace)
    return namespace


def _sdk_filename(relative_path: str) -> str:
    return str(sentry._SDK_PACKAGE_ROOT / relative_path)


def _raise_in_sdk(relative_path: str, code: str) -> BaseException:
    return _raise_in_file(_sdk_filename(relative_path), code)


def _exception_group_leaves(error: BaseException) -> list[BaseException]:
    if isinstance(error, sentry._EXCEPTION_GROUP_TYPES):
        leaves = []
        for child in getattr(error, "exceptions"):
            leaves.extend(_exception_group_leaves(child))
        return leaves
    return [error]


def _wait_for_background_capture() -> None:
    deadline = time.monotonic() + 1
    while time.monotonic() < deadline:
        if sentry._background_capture_queue.unfinished_tasks == 0:
            return
        time.sleep(0.01)
    raise AssertionError("background capture did not finish")


@pytest.fixture
def installed_sentry_hooks(monkeypatch):
    """Install all last-chance hooks with in-memory capture and chain recorders."""
    captured = []
    main_hook_calls = []
    thread_hook_calls = []
    unraisable_hook_calls = []
    asyncio_hook_calls = []
    previous_trace = sys.gettrace()
    previous_thread_trace = threading.gettrace()

    def main_hook(exc_type, exc_value, exc_tb):
        main_hook_calls.append((exc_type, exc_value, exc_tb))

    def thread_hook(args):
        thread_hook_calls.append(args)

    def unraisable_hook(args):
        unraisable_hook_calls.append(args)

    def asyncio_hook(loop, context):
        asyncio_hook_calls.append((loop, context))

    def capture(exception, mechanism_type="generic"):
        captured.append((exception, mechanism_type))

    monkeypatch.setattr(blaxel, "__sentry_dsn__", "https://public@example.com/1")
    monkeypatch.setenv("BL_ENV", "prod")
    monkeypatch.setattr(sys, "excepthook", main_hook)
    monkeypatch.setattr(threading, "excepthook", thread_hook)
    monkeypatch.setattr(sys, "unraisablehook", unraisable_hook)
    monkeypatch.setattr(asyncio.BaseEventLoop, "call_exception_handler", asyncio_hook)
    monkeypatch.setattr(sentry.atexit, "register", lambda _callback: None)
    monkeypatch.setattr(sentry, "capture_exception", capture)
    monkeypatch.setattr(sentry, "_handlers_registered", False)
    monkeypatch.setattr(sentry, "_sentry_initialized", False)
    monkeypatch.setattr(sentry, "_sentry_config", None)
    monkeypatch.setattr(sentry, "_original_excepthook", None)
    monkeypatch.setattr(sentry, "_original_threading_excepthook", None)
    monkeypatch.setattr(sentry, "_original_unraisablehook", None)
    monkeypatch.setattr(sentry, "_original_asyncio_call_exception_handler", None)
    monkeypatch.setattr(sentry, "_background_worker_init_lock", threading.Lock())
    monkeypatch.setattr(sentry, "_handler_registration_lock", threading.Lock())
    monkeypatch.setattr(
        sentry,
        "_background_capture_queue",
        Queue(maxsize=sentry._MAX_CAPTURE_EVENTS),
    )
    monkeypatch.setattr(sentry, "_background_capture_thread", None)

    try:
        sentry.init_sentry()
        yield SimpleNamespace(
            captured=captured,
            main_hook=main_hook,
            main_hook_calls=main_hook_calls,
            thread_hook=thread_hook,
            thread_hook_calls=thread_hook_calls,
            unraisable_hook=unraisable_hook,
            unraisable_hook_calls=unraisable_hook_calls,
            asyncio_hook=asyncio_hook,
            asyncio_hook_calls=asyncio_hook_calls,
            previous_trace=previous_trace,
            previous_thread_trace=previous_thread_trace,
        )
    finally:
        sentry._stop_background_capture_worker()
        sys.settrace(previous_trace)
        threading.settrace(previous_thread_trace)


class TestUnhandledExceptionHooks:
    def test_init_replaces_last_chance_hooks_without_enabling_tracing(self, installed_sentry_hooks):
        hooks = installed_sentry_hooks

        assert sys.excepthook is sentry._blaxel_excepthook
        assert threading.excepthook is sentry._blaxel_threading_excepthook
        assert sys.unraisablehook is sentry._blaxel_unraisablehook
        assert (
            asyncio.BaseEventLoop.call_exception_handler
            is sentry._blaxel_asyncio_call_exception_handler
        )
        assert sentry._original_excepthook is hooks.main_hook
        assert sentry._original_threading_excepthook is hooks.thread_hook
        assert sentry._original_unraisablehook is hooks.unraisable_hook
        assert sentry._original_asyncio_call_exception_handler is hooks.asyncio_hook
        assert sys.gettrace() is hooks.previous_trace
        assert threading.gettrace() is hooks.previous_thread_trace

    def test_repeated_init_does_not_wrap_or_replace_original_hooks(self, installed_sentry_hooks):
        hooks = installed_sentry_hooks

        sentry.init_sentry()

        assert sentry._original_excepthook is hooks.main_hook
        assert sentry._original_threading_excepthook is hooks.thread_hook
        assert sentry._original_unraisablehook is hooks.unraisable_hook
        assert sentry._original_asyncio_call_exception_handler is hooks.asyncio_hook
        assert sys.excepthook is sentry._blaxel_excepthook
        assert threading.excepthook is sentry._blaxel_threading_excepthook
        assert sys.unraisablehook is sentry._blaxel_unraisablehook

    def test_concurrent_init_preserves_original_hooks(self, installed_sentry_hooks, monkeypatch):
        hooks = installed_sentry_hooks
        starts = []
        counter_lock = threading.Lock()

        def slow_worker_start():
            with counter_lock:
                starts.append(True)
            time.sleep(0.05)

        sys.excepthook = hooks.main_hook
        threading.excepthook = hooks.thread_hook
        sys.unraisablehook = hooks.unraisable_hook
        asyncio.BaseEventLoop.call_exception_handler = hooks.asyncio_hook
        sentry._handlers_registered = False
        sentry._original_excepthook = None
        sentry._original_threading_excepthook = None
        sentry._original_unraisablehook = None
        sentry._original_asyncio_call_exception_handler = None
        monkeypatch.setattr(sentry, "_start_background_capture_worker", slow_worker_start)

        callers = [threading.Thread(target=sentry.init_sentry) for _ in range(4)]
        for caller in callers:
            caller.start()
        for caller in callers:
            caller.join()

        assert len(starts) == 1
        assert sentry._original_excepthook is hooks.main_hook
        assert sentry._original_threading_excepthook is hooks.thread_hook
        assert sentry._original_unraisablehook is hooks.unraisable_hook
        assert sentry._original_asyncio_call_exception_handler is hooks.asyncio_hook

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
                "/tmp/customer/job_reproduction.py",
                "exec",
            ),
            namespace,
        )

        assert namespace["handled_status"] == 404
        assert installed_sentry_hooks.captured == []
        assert installed_sentry_hooks.main_hook_calls == []

    def test_unhandled_sdk_exception_is_captured_and_chained(self, installed_sentry_hooks):
        exc = _raise_in_sdk("core/broken.py", "raise RuntimeError('sdk failure')")

        sys.excepthook(type(exc), exc, exc.__traceback__)
        _wait_for_background_capture()

        assert installed_sentry_hooks.captured == [(exc, "excepthook")]
        assert installed_sentry_hooks.main_hook_calls == [(type(exc), exc, exc.__traceback__)]

    def test_actual_worker_thread_failure_is_captured_and_chained(self, installed_sentry_hooks):
        namespace = _define_in_file(
            _sdk_filename("core/worker.py"),
            "def fail():\n    raise RuntimeError('thread failure')",
        )

        thread = threading.Thread(target=namespace["fail"])
        thread.start()
        thread.join()
        _wait_for_background_capture()

        captured_exception, mechanism = installed_sentry_hooks.captured[0]
        assert str(captured_exception) == "thread failure"
        assert mechanism == "threading"
        assert installed_sentry_hooks.thread_hook_calls[0].exc_value is captured_exception

    @pytest.mark.asyncio
    async def test_abandoned_asyncio_task_failure_is_captured_and_chained(
        self, installed_sentry_hooks
    ):
        namespace = _define_in_file(
            _sdk_filename("core/background.py"),
            """
raised = []
async def fail():
    error = RuntimeError('async task failure')
    raised.append(error)
    raise error
""",
        )

        task = asyncio.create_task(namespace["fail"]())
        await asyncio.sleep(0)
        assert task.done()
        expected_exception = namespace["raised"][0]
        del task
        gc.collect()
        await asyncio.sleep(0)
        _wait_for_background_capture()

        assert installed_sentry_hooks.captured == [(expected_exception, "asyncio")]
        assert installed_sentry_hooks.asyncio_hook_calls
        assert installed_sentry_hooks.asyncio_hook_calls[0][1]["exception"] is expected_exception

    def test_asyncio_hook_chains_without_waiting_for_delivery(
        self, installed_sentry_hooks, monkeypatch
    ):
        exc = _raise_in_sdk("core/background.py", "raise RuntimeError('async failure')")
        started = threading.Event()
        release = threading.Event()
        loop = cast(asyncio.BaseEventLoop, asyncio.new_event_loop())
        context = {"exception": exc}

        def block_capture(_exc_value, _mechanism_type):
            started.set()
            release.wait(timeout=1)

        monkeypatch.setattr(sentry, "_capture_unhandled_exception_safely", block_capture)
        try:
            asyncio.BaseEventLoop.call_exception_handler(loop, context)
            assert started.wait(timeout=1)
            assert installed_sentry_hooks.asyncio_hook_calls == [(loop, context)]
        finally:
            release.set()
            _wait_for_background_capture()
            loop.close()

    def test_background_capture_queues_a_burst_without_blocking_hooks(
        self, installed_sentry_hooks, monkeypatch
    ):
        exceptions = [
            _raise_in_sdk("core/background.py", f"raise RuntimeError('failure {index}')")
            for index in range(3)
        ]
        first_started = threading.Event()
        release_first = threading.Event()
        captured = []

        def capture(exc_value, mechanism_type):
            captured.append((exc_value, mechanism_type))
            if len(captured) == 1:
                first_started.set()
                release_first.wait(timeout=1)

        monkeypatch.setattr(sentry, "_capture_unhandled_exception_safely", capture)

        sentry._capture_unhandled_exception_in_background(exceptions[0], "asyncio")
        assert first_started.wait(timeout=1)
        sentry._capture_unhandled_exception_in_background(exceptions[1], "asyncio")
        sentry._capture_unhandled_exception_in_background(exceptions[2], "asyncio")
        release_first.set()
        _wait_for_background_capture()

        assert captured == [(exception, "asyncio") for exception in exceptions]

    def test_flush_timeout_does_not_wait_for_in_flight_delivery(
        self, installed_sentry_hooks, monkeypatch
    ):
        exc = _raise_in_sdk("core/slow_delivery.py", "raise RuntimeError('slow')")
        started = threading.Event()
        release = threading.Event()

        def slow_capture(_exc, _mechanism):
            started.set()
            release.wait(timeout=1)

        monkeypatch.setattr(sentry, "capture_exception", slow_capture)
        sentry._capture_unhandled_exception_in_background(exc, "asyncio")
        assert started.wait(timeout=1)

        before = time.monotonic()
        sentry.flush_sentry(timeout=0.01)
        elapsed = time.monotonic() - before

        assert elapsed < 0.2
        release.set()
        _wait_for_background_capture()

    def test_background_thread_start_failure_is_contained(
        self, installed_sentry_hooks, monkeypatch
    ):
        exc = _raise_in_sdk("core/background.py", "raise RuntimeError('sdk failure')")

        class FailingThread:
            def __init__(self, **_kwargs):
                pass

            def is_alive(self):
                return False

            def start(self):
                raise RuntimeError("thread unavailable")

        sentry._stop_background_capture_worker()
        monkeypatch.setattr(
            sentry,
            "_background_capture_queue",
            Queue(maxsize=sentry._MAX_CAPTURE_EVENTS),
        )
        monkeypatch.setattr(sentry, "_background_capture_thread", None)
        monkeypatch.setattr(sentry.threading, "Thread", FailingThread)

        sentry._start_background_capture_worker()
        sentry._capture_unhandled_exception_in_background(exc, "asyncio")

        assert sentry._background_capture_queue.empty()
        assert sentry._background_capture_thread is None

    def test_actual_unraisable_failure_is_captured_and_chained(self, installed_sentry_hooks):
        namespace = _define_in_file(
            _sdk_filename("core/finalizer.py"),
            """
class BrokenFinalizer:
    def __del__(self):
        raise RuntimeError('unraisable sdk failure')
""",
        )

        instance = namespace["BrokenFinalizer"]()
        del instance
        gc.collect()
        _wait_for_background_capture()

        captured_exception, mechanism = installed_sentry_hooks.captured[0]
        assert str(captured_exception) == "unraisable sdk failure"
        assert mechanism == "unraisablehook"
        assert installed_sentry_hooks.unraisable_hook_calls[0].exc_value is captured_exception

    def test_unraisable_during_finalization_only_chains(self, installed_sentry_hooks, monkeypatch):
        exc = _raise_in_sdk("core/finalizer.py", "raise RuntimeError('late finalizer')")
        args = SimpleNamespace(exc_value=exc)
        monkeypatch.setattr(sys, "is_finalizing", lambda: True)

        sys.unraisablehook(cast(Any, args))

        assert installed_sentry_hooks.captured == []
        assert installed_sentry_hooks.unraisable_hook_calls == [args]

    def test_unhandled_optional_import_is_filtered_and_chained(self, installed_sentry_hooks):
        exc = _raise_in_sdk(
            "openai/model.py",
            "raise ModuleNotFoundError(\"No module named 'agents'\", name='agents')",
        )

        sys.excepthook(type(exc), exc, exc.__traceback__)
        _wait_for_background_capture()

        assert installed_sentry_hooks.captured == []
        assert installed_sentry_hooks.main_hook_calls == [(type(exc), exc, exc.__traceback__)]

    def test_similar_application_path_is_not_treated_as_sdk(self, installed_sentry_hooks):
        exc = _raise_in_file(
            "/tmp/customer/blaxel/core/broken.py",
            "raise RuntimeError('application failure')",
        )

        sys.excepthook(type(exc), exc, exc.__traceback__)
        _wait_for_background_capture()

        assert installed_sentry_hooks.captured == []
        assert installed_sentry_hooks.main_hook_calls == [(type(exc), exc, exc.__traceback__)]

    def test_reporting_failures_are_swallowed_and_all_hooks_still_chain(
        self, installed_sentry_hooks, monkeypatch
    ):
        exc = _raise_in_sdk("core/broken.py", "raise RuntimeError('sdk failure')")
        thread_args = threading.ExceptHookArgs((type(exc), exc, exc.__traceback__, None))
        unraisable_args = SimpleNamespace(exc_value=exc)
        asyncio_context = {"message": "Task exception was never retrieved", "exception": exc}
        loop = cast(asyncio.BaseEventLoop, asyncio.new_event_loop())

        def fail_classification(_exc_value):
            raise RuntimeError("classification failed")

        monkeypatch.setattr(sentry, "_filter_reportable_exception", fail_classification)

        try:
            sys.excepthook(type(exc), exc, exc.__traceback__)
            _wait_for_background_capture()
            threading.excepthook(thread_args)
            sys.unraisablehook(cast(Any, unraisable_args))
            _wait_for_background_capture()
            asyncio.BaseEventLoop.call_exception_handler(loop, asyncio_context)
            _wait_for_background_capture()
        finally:
            loop.close()

        assert installed_sentry_hooks.captured == []
        assert installed_sentry_hooks.main_hook_calls == [(type(exc), exc, exc.__traceback__)]
        assert installed_sentry_hooks.thread_hook_calls == [thread_args]
        assert installed_sentry_hooks.unraisable_hook_calls == [unraisable_args]
        assert installed_sentry_hooks.asyncio_hook_calls == [(loop, asyncio_context)]

    @pytest.mark.skipif(
        not sentry._EXCEPTION_GROUP_TYPES,
        reason="Exception groups require Python 3.11 or the exceptiongroup backport",
    )
    def test_exception_group_preserves_every_reportable_sdk_leaf(self, installed_sentry_hooks):
        first_sdk_exc = _raise_in_sdk("core/broken.py", "raise RuntimeError('first sdk failure')")
        second_sdk_exc = _raise_in_sdk(
            "core/also_broken.py", "raise RuntimeError('second sdk failure')"
        )
        optional_exc = _raise_in_sdk(
            "openai/model.py",
            "raise ModuleNotFoundError(\"No module named 'agents'\", name='agents')",
        )
        group_type = sentry._EXCEPTION_GROUP_TYPES[0]
        nested_group = group_type("nested", [second_sdk_exc])
        group = group_type("task failures", [optional_exc, first_sdk_exc, nested_group])

        sys.excepthook(type(group), group, group.__traceback__)
        _wait_for_background_capture()

        assert len(installed_sentry_hooks.captured) == 1
        captured_group, mechanism = installed_sentry_hooks.captured[0]
        assert mechanism == "excepthook"
        assert isinstance(captured_group, sentry._EXCEPTION_GROUP_TYPES)
        assert getattr(captured_group, "message") == "task failures"
        assert _exception_group_leaves(captured_group) == [first_sdk_exc, second_sdk_exc]
        assert installed_sentry_hooks.main_hook_calls == [(type(group), group, group.__traceback__)]

        values = sentry._exception_values(captured_group, mechanism)
        assert [value["mechanism"]["exception_id"] for value in values] == [3, 2, 1, 0]
        assert values[-1]["value"] == "Unhandled SDK exception group (2 sub-exceptions)"
        assert values[-1]["mechanism"] == {
            "type": "excepthook",
            "handled": False,
            "exception_id": 0,
            "is_exception_group": True,
        }
        assert all(value["mechanism"]["handled"] is False for value in values)

    @pytest.mark.skipif(
        not sentry._EXCEPTION_GROUP_TYPES,
        reason="Exception groups require Python 3.11 or the exceptiongroup backport",
    )
    def test_optional_only_exception_group_is_filtered_in_thread(self, installed_sentry_hooks):
        optional_exc = _raise_in_sdk(
            "openai/model.py",
            "raise ModuleNotFoundError(\"No module named 'agents'\", name='agents')",
        )
        group_type = sentry._EXCEPTION_GROUP_TYPES[0]
        group = group_type("task failures", [optional_exc])
        args = threading.ExceptHookArgs((type(group), group, group.__traceback__, None))

        threading.excepthook(args)

        assert installed_sentry_hooks.captured == []
        assert installed_sentry_hooks.thread_hook_calls == [args]


class TestSentryDelivery:
    def test_successful_delivery_is_not_duplicated_by_flush(self, monkeypatch):
        exc = _raise_in_sdk("core/delivery.py", "raise RuntimeError('delivery failure')")
        sent_events = []
        monkeypatch.setattr(sentry, "_sentry_initialized", True)
        monkeypatch.setattr(sentry, "_sentry_config", {"public_key": "key"})

        def send(event):
            sent_events.append(event)
            return True

        monkeypatch.setattr(sentry, "_send_to_sentry", send)

        sentry.capture_exception(exc, "excepthook")
        sentry.flush_sentry()

        assert len(sent_events) == 1

    def test_failed_delivery_is_best_effort_and_not_retried_during_flush(self, monkeypatch):
        exc = _raise_in_sdk("core/delivery.py", "raise RuntimeError('sentry unavailable')")
        sent_events = []

        def send(event):
            sent_events.append(event)
            return False

        monkeypatch.setattr(sentry, "_sentry_initialized", True)
        monkeypatch.setattr(sentry, "_sentry_config", {"public_key": "key"})
        monkeypatch.setattr(sentry, "_send_to_sentry", send)

        sentry.capture_exception(exc, "excepthook")
        sentry.flush_sentry()

        assert len(sent_events) == 1

    def test_distinct_occurrences_with_the_same_message_are_both_delivered(self, monkeypatch):
        first = _raise_in_sdk("core/repeated.py", "raise RuntimeError('same failure')")
        second = _raise_in_sdk("core/repeated.py", "raise RuntimeError('same failure')")
        sent_events = []

        def send(event):
            sent_events.append(event)
            return True

        monkeypatch.setattr(sentry, "_sentry_initialized", True)
        monkeypatch.setattr(sentry, "_sentry_config", {"public_key": "key"})
        monkeypatch.setattr(sentry, "_send_to_sentry", send)

        sentry.capture_exception(first, "excepthook")
        sentry.capture_exception(second, "excepthook")

        assert len(sent_events) == 2


class TestSentryPayloadPrivacy:
    def test_public_capture_rejects_application_exception(self, monkeypatch):
        exc = _raise_in_file(
            "/tmp/customer/blaxel/core/application.py",
            "raise RuntimeError('private application failure')",
        )
        sent_events = []
        monkeypatch.setattr(sentry, "_sentry_initialized", True)
        monkeypatch.setattr(sentry, "_sentry_config", {"public_key": "key"})
        monkeypatch.setattr(sentry, "_send_to_sentry", sent_events.append)

        sentry.capture_exception(exc)

        assert sent_events == []

    def test_event_contains_only_package_relative_sdk_frames(self):
        namespace = _define_in_file(
            _sdk_filename("core/private_failure.py"),
            "def fail():\n    raise RuntimeError('sdk failure')",
        )
        exc = _raise_in_file(
            "/tmp/customer/private/application.py",
            "fail()",
            {"fail": namespace["fail"]},
        )

        event = sentry._error_to_sentry_event(exc, "excepthook")
        frames = event["exception"]["values"][0]["stacktrace"]["frames"]

        assert frames
        assert all(frame["filename"].startswith("blaxel/") for frame in frames)
        assert all(not frame["filename"].startswith("/") for frame in frames)
        assert all("customer" not in frame["filename"] for frame in frames)
        exception_value = event["exception"]["values"][0]
        assert exception_value["value"] == "Unhandled SDK exception"
        assert "sdk failure" not in json.dumps(event)
        assert exception_value["mechanism"] == {
            "type": "excepthook",
            "handled": False,
        }

    def test_response_content_is_not_serialized(self):
        exc = _raise_in_file(
            "/tmp/customer/request.py",
            """
_parse_response(
    client=Client(base_url="https://api.blaxel.ai"),
    response=httpx.Response(
        404,
        content=b'{"error":"token=top-secret-customer-value"}',
    ),
)
""",
            {"Client": Client, "httpx": httpx, "_parse_response": _parse_response},
        )

        setattr(exc, "code", "CUSTOMER_SECRET")
        event = sentry._error_to_sentry_event(exc, "excepthook")
        serialized_event = json.dumps(event)

        assert "top-secret-customer-value" not in serialized_event
        assert "CUSTOMER_SECRET" not in serialized_event
        assert event["exception"]["values"][0]["value"] == ("Unhandled SDK exception (HTTP 404)")


class TestIsOptionalDependencyError:
    """Cover the import-error classification used to suppress Sentry noise."""

    def test_missing_integration_submodule_is_optional(self):
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
        for package in _OPTIONAL_INTEGRATION_ENTRYPOINT_MODULES:
            exc = ModuleNotFoundError(f"No module named '{package}'", name=package)
            assert _is_optional_dependency_error(type(exc), exc) is True, package

    def test_each_optional_integration_entrypoint_module_is_covered(self):
        for package, entrypoints in _OPTIONAL_INTEGRATION_ENTRYPOINT_MODULES.items():
            for entrypoint in entrypoints:
                missing = f"{package}.{entrypoint}"
                exc = ModuleNotFoundError(f"No module named '{missing}'", name=missing)
                assert _is_optional_dependency_error(type(exc), exc) is True, missing

    def test_opentelemetry_dependency_is_optional(self):
        exc = ModuleNotFoundError("No module named 'opentelemetry'", name="opentelemetry")
        assert _is_optional_dependency_error(type(exc), exc) is True

    def test_missing_third_party_dep_while_loading_integration_is_optional(self):
        exc = _raise_in_sdk(
            "openai/model.py",
            "raise ModuleNotFoundError(\"No module named 'agents'\", name='agents')",
        )
        assert _is_optional_dependency_error(type(exc), exc) is True

    def test_similar_application_path_does_not_count_as_optional_integration(self):
        exc = _raise_in_file(
            "/tmp/customer/blaxel/openai/model.py",
            "raise ModuleNotFoundError(\"No module named 'agents'\", name='agents')",
        )
        assert _is_optional_dependency_error(type(exc), exc) is False

    def test_missing_nested_blaxel_module_inside_integration_is_not_optional(self):
        exc = ModuleNotFoundError(
            "No module named 'blaxel.pydantic.custom.gemni'",
            name="blaxel.pydantic.custom.gemni",
        )
        assert _is_optional_dependency_error(ModuleNotFoundError, exc) is False

    def test_wrapped_integration_import_guard_error_is_optional(self):
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
        exc = _raise_in_sdk(
            "core/common/settings.py",
            "raise ModuleNotFoundError(\"No module named 'httpx'\", name='httpx')",
        )
        assert _is_optional_dependency_error(type(exc), exc) is False

    def test_core_module_import_error_is_not_optional(self):
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
