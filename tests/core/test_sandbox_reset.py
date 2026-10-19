"""Unit tests for resetting a sandbox to a fresh copy of its image.

A reset first asks the control plane to replace the sandbox's instance in one
call, then waits until the sandbox answers. On a control plane without that
call it switches ``spec.enabled`` off, waits for the platform to report the old
instance gone, and switches it back on. The control plane and the sandbox are
mocked so each call, read, write and failure can be scripted.
"""

import asyncio
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from blaxel.core.client.client import Client
from blaxel.core.client.models import (
    CoreEvent,
    Env,
    Error,
    Metadata,
    MetadataLabels,
    Sandbox,
    SandboxRuntime,
    SandboxSpec,
    Status,
    VolumeAttachment,
)
from blaxel.core.sandbox import SandboxAPIError, SandboxInstance, SyncSandboxInstance
from blaxel.core.sandbox.default import sandbox as async_module
from blaxel.core.sandbox.sync import sandbox as sync_module

CREATED_AT = "2026-10-19T12:00:00Z"

DEACTIVATE = ("ai.blaxel.controlplane.api.deactivate", "DEACTIVATED")
TEARING_DOWN = ("ai.blaxel.controlplane.deployment.created", "DEACTIVATED")
TORN_DOWN = ("ai.blaxel.controlplane.deployment.succeeded", "DEACTIVATED")
TEARDOWN_FAILED = ("ai.blaxel.controlplane.deployment.failed", "FAILED")


def record(
    status: str,
    enabled: bool = True,
    events: tuple = (),
    created_at: str = CREATED_AT,
) -> Sandbox:
    # The control plane masks secret values when it returns a sandbox.
    spec = SandboxSpec(
        enabled=enabled,
        region="us-was-1",
        runtime=SandboxRuntime(
            image="blaxel/base-image:latest",
            memory=2048,
            envs=[Env(name="TOKEN", value="****", secret=True)],
        ),
        volumes=[VolumeAttachment(name="data", mount_path="/data")],
    )
    sandbox = Sandbox(
        metadata=Metadata(
            name="my-sandbox", created_at=created_at, url="https://run.example/my-sandbox"
        ),
        spec=spec,
    )
    sandbox.status = Status(status)
    sandbox.events = [CoreEvent(type_=type_, status=st) for type_, st in events]
    return sandbox


def off(*events) -> Sandbox:
    return record("DEACTIVATED", False, events)


# What the control plane answers to the reset call when it has it, and when not.
def reset_done(status: str = "DEPLOYED") -> httpx.Response:
    return httpx.Response(200, json=record(status).to_dict())


def unknown_route() -> httpx.Response:
    return httpx.Response(404, json={"code": 404, "error": "Route not found"})


def refused(code: int, error: str) -> httpx.Response:
    return httpx.Response(code, json={"code": code, "error": error})


# What the sandbox's health route answers: the instance serves it, or the
# gateway has no instance to route to yet.
def healthy():
    return SimpleNamespace(status_code=200, content=b'{"status":"ok"}')


def not_routable():
    return SimpleNamespace(
        status_code=404, content=json.dumps({"error": {"code": "WORKLOAD_UNAVAILABLE"}}).encode()
    )


def health(status: int, body: dict):
    return SimpleNamespace(status_code=status, content=json.dumps(body).encode())


def dropped() -> Exception:
    return httpx.ConnectError("read ECONNRESET")


def not_found() -> Error:
    return Error(code=404, error="Sandbox not found")


def body_of(mock, call: int) -> dict:
    return mock.call_args_list[call].kwargs["body"]


def key_of(post, call: int) -> str:
    """The Idempotency-Key a reset call carried."""
    return post.call_args_list[call].args[2]


ASYNC = "blaxel.core.sandbox.default.sandbox"
SYNC = "blaxel.core.sandbox.sync.sandbox"


# --------------------------------------------------------------------------- async


@pytest.fixture
def aio():
    with (
        patch(f"{ASYNC}._post_reset", new_callable=AsyncMock) as post,
        patch(f"{ASYNC}.get_sandbox", new_callable=AsyncMock) as get,
        patch(f"{ASYNC}.update_sandbox", new_callable=AsyncMock) as update,
        patch(f"{ASYNC}.get_health", new_callable=AsyncMock) as probe,
    ):
        probe.return_value = healthy()
        # The record read alongside the reset call.
        get.return_value = record("DEPLOYED")
        yield SimpleNamespace(post=post, get=get, update=update, probe=probe)


@pytest.fixture
def aio_switch(aio):
    """A control plane without the reset call."""
    aio.post.return_value = unknown_route()
    return aio


# With the reset call.


async def test_reset_resets_the_sandbox_in_one_call_and_waits_until_it_answers(aio):
    aio.post.return_value = reset_done()

    instance = await SandboxInstance.reset("my-sandbox", interval=0)

    assert isinstance(instance, SandboxInstance)
    assert instance.status == "DEPLOYED"
    assert aio.post.await_count == 1
    assert aio.post.call_args.args[0] == "my-sandbox"
    assert len(key_of(aio.post, 0)) == 36
    assert aio.probe.await_count == 1
    # The record is read once, alongside the call, and nothing is switched off and on.
    assert aio.get.await_count == 1
    aio.update.assert_not_called()


async def test_reset_waits_for_the_gateway_to_route_to_the_new_instance(aio):
    aio.post.return_value = reset_done()
    aio.probe.side_effect = [not_routable(), not_routable(), healthy()]

    await SandboxInstance.reset("my-sandbox", interval=0)

    assert aio.probe.await_count == 3


async def test_reset_refreshes_the_instance_it_is_called_on_and_returns_it(aio):
    fresh = record("DEPLOYED")
    fresh.last_used_at = "after"
    aio.post.return_value = httpx.Response(200, json=fresh.to_dict())
    instance = SandboxInstance(record("DEPLOYED"))

    result = await instance.reset(interval=0)

    assert result is instance
    assert instance.sandbox.last_used_at == "after"


async def test_reset_propagates_what_the_control_plane_refuses_without_switching_anything(aio):
    aio.post.return_value = refused(
        409, "This sandbox is archived, unarchive it before resetting it"
    )

    with pytest.raises(SandboxAPIError, match="unarchive it before resetting it") as err:
        await SandboxInstance.reset("my-sandbox", interval=0)

    assert err.value.status_code == 409
    assert aio.post.await_count == 1
    aio.update.assert_not_called()


async def test_reset_propagates_the_error_of_a_sandbox_that_does_not_exist(aio):
    aio.post.return_value = refused(404, "Sandbox not found")

    with pytest.raises(SandboxAPIError) as err:
        await SandboxInstance.reset("my-sandbox")

    assert err.value.status_code == 404
    aio.update.assert_not_called()


async def test_reset_asks_again_after_an_edge_error_or_a_dropped_connection(aio):
    aio.post.side_effect = [refused(502, "Bad Gateway"), dropped(), reset_done()]

    with patch(f"{ASYNC}._retry_delay", return_value=0):
        instance = await SandboxInstance.reset("my-sandbox", interval=0)

    assert instance.status == "DEPLOYED"
    assert aio.post.await_count == 3
    # Each call sent again follows a read showing the same sandbox, and carries
    # the key of the first: a control plane that already ran the reset does not
    # run it again.
    assert aio.get.await_count == 3
    assert key_of(aio.post, 1) == key_of(aio.post, 0)
    assert key_of(aio.post, 2) == key_of(aio.post, 0)


async def test_reset_gives_every_reset_its_own_key(aio):
    aio.post.return_value = reset_done()

    await SandboxInstance.reset("my-sandbox", interval=0)
    await SandboxInstance.reset("my-sandbox", interval=0)

    assert key_of(aio.post, 1) != key_of(aio.post, 0)


async def test_reset_does_not_ask_again_once_the_sandbox_is_created_again(aio):
    aio.post.return_value = refused(502, "Bad Gateway")
    aio.get.side_effect = [
        record("DEPLOYED"),
        record("DEPLOYED", created_at="2026-10-19T12:05:00Z"),
    ]

    with (
        patch(f"{ASYNC}._retry_delay", return_value=0),
        pytest.raises(
            SandboxAPIError,
            match="deleted and created again during its reset; the reset call whose answer "
            "was lost may have reached the new sandbox, which is not reset again",
        ),
    ):
        await SandboxInstance.reset("my-sandbox", interval=0)

    assert aio.post.await_count == 1


async def test_reset_does_not_ask_again_once_the_sandbox_is_deleted(aio):
    aio.post.return_value = refused(504, "Gateway Timeout")
    aio.get.side_effect = [record("DEPLOYED"), not_found()]

    with (
        patch(f"{ASYNC}._retry_delay", return_value=0),
        pytest.raises(SandboxAPIError, match="was deleted"),
    ):
        await SandboxInstance.reset("my-sandbox", interval=0)

    assert aio.post.await_count == 1


async def test_reset_says_so_when_it_reset_another_sandbox_than_the_one_it_started_on(aio):
    aio.post.return_value = httpx.Response(
        200, json=record("DEPLOYED", created_at="2026-10-19T12:05:00Z").to_dict()
    )

    with pytest.raises(
        SandboxAPIError, match="deleted and created again as its reset started; the new sandbox"
    ):
        await SandboxInstance.reset("my-sandbox", interval=0)

    aio.probe.assert_not_called()


async def test_reset_gives_up_waiting_on_the_control_plane_at_max_wait(aio):
    aio.post.side_effect = httpx.ReadTimeout("timed out")

    with pytest.raises(
        SandboxAPIError,
        match="was not reset within 0s; a reset the control plane started still finishes",
    ):
        await SandboxInstance.reset("my-sandbox", interval=0, max_wait=50)


async def test_reset_raises_when_the_sandbox_does_not_answer_in_time(aio):
    aio.post.return_value = reset_done()
    aio.probe.return_value = not_routable()

    with pytest.raises(
        SandboxAPIError,
        match="has a fresh instance but it did not answer within 0s after the reset: 404",
    ):
        await SandboxInstance.reset("my-sandbox", interval=5, max_wait=30)


async def test_reset_does_not_keep_probing_an_answer_that_retrying_cannot_fix(aio):
    aio.post.return_value = reset_done()
    aio.probe.return_value = health(403, {"error": "forbidden"})

    with pytest.raises(SandboxAPIError, match="answered 403 after the reset"):
        await SandboxInstance.reset("my-sandbox", interval=0)

    assert aio.probe.await_count == 1


async def test_reset_treats_a_dropped_probe_as_not_yet(aio):
    aio.post.return_value = reset_done()
    aio.probe.side_effect = [dropped(), httpx.ReadTimeout("timed out"), healthy()]

    await SandboxInstance.reset("my-sandbox", interval=0)

    assert aio.probe.await_count == 3


async def test_reset_posts_through_the_control_plane_client_cut_at_max_wait():
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(
            (
                request.method,
                request.url.path,
                request.extensions.get("timeout"),
                request.headers.get("Idempotency-Key"),
            )
        )
        return httpx.Response(200, json=record("DEPLOYED").to_dict())

    control_plane = Client(
        base_url="https://api.example", httpx_args={"transport": httpx.MockTransport(handler)}
    )
    with patch(f"{ASYNC}.client", control_plane):
        response = await async_module._post_reset(
            "my-sandbox", async_module._reset_deadline(60_000), "key-1"
        )

    assert response.status_code == 200
    method, path, timeout, key = seen[0]
    assert (method, path, key) == ("POST", "/sandboxes/my-sandbox/reset", "key-1")
    assert 0 < timeout["read"] <= 60


async def test_reset_cuts_every_control_plane_call_at_max_wait_and_none_without_one(aio_switch):
    aio_switch.get.side_effect = [record("DEPLOYED"), off(TORN_DOWN), record("DEPLOYED")]
    aio_switch.update.side_effect = [off(DEACTIVATE), record("DEPLOYING")]

    await SandboxInstance.reset("my-sandbox", interval=0, max_wait=60_000)

    for call in [*aio_switch.get.call_args_list, *aio_switch.update.call_args_list]:
        cut = call.kwargs["client"]
        assert isinstance(cut, async_module._DeadlineClient)
        assert 0 < cut.timeout <= 60

    aio_switch.get.reset_mock(side_effect=True)
    aio_switch.update.reset_mock(side_effect=True)
    aio_switch.get.side_effect = [record("DEPLOYED"), off(TORN_DOWN), record("DEPLOYED")]
    aio_switch.update.side_effect = [off(DEACTIVATE), record("DEPLOYING")]

    await SandboxInstance.reset("my-sandbox", interval=0, max_wait=-1)

    for call in [*aio_switch.get.call_args_list, *aio_switch.update.call_args_list]:
        assert call.kwargs["client"] is async_module.client


# Without the reset call.


async def test_reset_switches_off_waits_for_the_platform_to_report_it_gone_and_switches_on(
    aio_switch,
):
    get, update = aio_switch.get, aio_switch.update
    get.side_effect = [
        record("DEPLOYED"),  # entry read
        off(DEACTIVATE),
        off(DEACTIVATE, TEARING_DOWN),
        off(DEACTIVATE, TEARING_DOWN, TORN_DOWN),
        record("DEPLOYING"),
        record("DEPLOYED"),
    ]
    update.side_effect = [off(DEACTIVATE), record("DEPLOYING")]

    instance = await SandboxInstance.reset("my-sandbox", interval=0)

    assert instance.status == "DEPLOYED"
    assert update.await_count == 2
    off_body, on_body = body_of(update, 0), body_of(update, 1)
    assert off_body["spec"]["enabled"] is False
    assert on_body["spec"]["enabled"] is True
    # Everything else is written back as the control plane returned it, masked
    # secret values included, so nothing but ``enabled`` changes.
    expected = record("DEPLOYED").to_dict()["spec"]
    assert {**off_body["spec"], "enabled": True} == expected
    assert on_body["spec"] == expected
    assert off_body["metadata"] == record("DEPLOYED").to_dict()["metadata"]
    # Read-only state is not sent back.
    assert "status" not in off_body
    assert "events" not in off_body
    assert get.await_count == 6
    # The guest is only asked whether it answers once the new instance runs.
    assert aio_switch.probe.await_count == 1
    for call in [*get.call_args_list, *update.call_args_list]:
        assert (call.args or (call.kwargs["sandbox_name"],))[0] == "my-sandbox"


async def test_reset_does_not_switch_it_back_on_before_the_platform_reports_it_gone(aio_switch):
    get, update = aio_switch.get, aio_switch.update
    reads_before_switch_on = []
    get.side_effect = [
        record("DEPLOYED"),
        off(DEACTIVATE, TEARING_DOWN),
        off(DEACTIVATE, TEARING_DOWN),
        off(DEACTIVATE, TEARING_DOWN, TORN_DOWN),
        record("DEPLOYED"),
    ]

    async def switch(*args, **kwargs):
        if kwargs["body"]["spec"]["enabled"]:
            reads_before_switch_on.append(get.await_count)
            return record("DEPLOYING")
        return off(DEACTIVATE)

    update.side_effect = switch

    await SandboxInstance.reset("my-sandbox", interval=0)

    assert reads_before_switch_on == [4]


@pytest.mark.parametrize(
    "status", ["TERMINATED", "DELETING", "ARCHIVED", "ARCHIVING", "UNARCHIVING", "FAILED"]
)
async def test_reset_refuses_a_sandbox_that_cannot_be_reset_before_writing_anything(
    aio_switch, status
):
    # A write to a deleted record would bring the sandbox back to life, and one to
    # a FAILED record has the control plane release and recreate it.
    aio_switch.get.side_effect = [record(status)]

    with pytest.raises(SandboxAPIError, match=f"is {status} and cannot be reset"):
        await SandboxInstance.reset("my-sandbox", interval=0)

    aio_switch.update.assert_not_called()


async def test_reset_propagates_the_error_of_a_sandbox_that_does_not_exist_on_the_switch(
    aio_switch,
):
    aio_switch.get.side_effect = [not_found()]

    with pytest.raises(SandboxAPIError) as err:
        await SandboxInstance.reset("my-sandbox")

    assert err.value.status_code == 404
    aio_switch.update.assert_not_called()


async def test_reset_completes_the_reset_of_a_sandbox_a_failed_reset_left_deactivated(
    aio_switch,
):
    aio_switch.get.side_effect = [
        off(DEACTIVATE, TORN_DOWN),
        off(DEACTIVATE, TORN_DOWN),
        record("DEPLOYED"),
    ]
    aio_switch.update.side_effect = [record("DEPLOYING")]

    instance = await SandboxInstance.reset("my-sandbox", interval=0)

    assert instance.status == "DEPLOYED"
    assert aio_switch.update.await_count == 1
    assert body_of(aio_switch.update, 0)["spec"]["enabled"] is True


async def test_reset_leaves_the_sandbox_as_it_was_when_it_cannot_be_taken_down(aio_switch):
    aio_switch.get.side_effect = [record("DEPLOYED")]
    aio_switch.update.side_effect = [Error(code=500, error="boom")]

    with pytest.raises(SandboxAPIError, match="could not be reset, it was left as it was: boom"):
        await SandboxInstance.reset("my-sandbox", interval=0)

    assert aio_switch.update.await_count == 1


async def test_reset_does_not_switch_it_back_on_when_the_control_plane_did_not_take_it_down(
    aio_switch,
):
    aio_switch.get.side_effect = [record("DEPLOYED")]
    aio_switch.update.side_effect = [record("DEPLOYED")]

    with pytest.raises(SandboxAPIError, match="did not take it down"):
        await SandboxInstance.reset("my-sandbox", interval=0)

    assert aio_switch.update.await_count == 1


async def test_reset_does_not_switch_it_back_on_when_the_sandbox_is_deleted_during_the_teardown(
    aio_switch,
):
    aio_switch.get.side_effect = [record("DEPLOYED"), not_found()]
    aio_switch.update.side_effect = [off(DEACTIVATE)]

    with pytest.raises(SandboxAPIError, match="was deleted during its reset"):
        await SandboxInstance.reset("my-sandbox", interval=0)

    assert aio_switch.update.await_count == 1


@pytest.mark.parametrize("status", ["DELETING", "TERMINATED", "DEPLOYING"])
async def test_reset_does_not_switch_it_back_on_when_it_changes_during_the_teardown(
    aio_switch, status
):
    aio_switch.get.side_effect = [
        record("DEPLOYED"),
        record(status, status == "DEPLOYING", (TORN_DOWN,)),
    ]
    aio_switch.update.side_effect = [off(DEACTIVATE)]

    with pytest.raises(
        SandboxAPIError, match=f"is {status} while it should be switched off for the reset"
    ):
        await SandboxInstance.reset("my-sandbox", interval=0)

    assert aio_switch.update.await_count == 1


async def test_reset_leaves_a_sandbox_created_again_under_the_same_name_alone(aio_switch):
    aio_switch.get.side_effect = [
        record("DEPLOYED"),
        record("DEACTIVATED", False, (TORN_DOWN,), "2026-10-19T12:05:00Z"),
    ]
    aio_switch.update.side_effect = [off(DEACTIVATE)]

    with pytest.raises(SandboxAPIError, match="was deleted and created again during its reset"):
        await SandboxInstance.reset("my-sandbox", interval=0)

    assert aio_switch.update.await_count == 1


async def test_reset_says_a_failed_teardown_cannot_be_finished_by_resetting_again(aio_switch):
    aio_switch.get.side_effect = [record("DEPLOYED"), off(DEACTIVATE, TEARDOWN_FAILED)]
    aio_switch.update.side_effect = [off(DEACTIVATE)]

    with pytest.raises(SandboxAPIError) as err:
        await SandboxInstance.reset("my-sandbox", interval=0)

    # Resetting again would find the sandbox off with the failed teardown still
    # newest, so the error points elsewhere.
    assert str(err.value) == (
        "Sandbox my-sandbox could not be taken down for the reset: the platform reported the "
        "teardown failed. It is left switched off; delete it and create it again to get a "
        "fresh instance"
    )
    assert "reset(" not in str(err.value)
    assert aio_switch.update.await_count == 1


async def test_reset_leaves_the_sandbox_deactivated_when_the_teardown_outlives_max_wait(
    aio_switch,
):
    aio_switch.get.side_effect = [record("DEPLOYED")] + [off(DEACTIVATE, TEARING_DOWN)] * 100
    aio_switch.update.side_effect = [off(DEACTIVATE)]

    with pytest.raises(
        SandboxAPIError,
        match=r"was not reported gone within 0s, it is left DEACTIVATED; "
        r'call SandboxInstance\.reset\("my-sandbox"\) again',
    ):
        await SandboxInstance.reset("my-sandbox", interval=5, max_wait=30)

    assert aio_switch.update.await_count == 1


async def test_reset_keeps_reading_the_record_through_edge_errors_and_dropped_connections(
    aio_switch,
):
    aio_switch.get.side_effect = [
        record("DEPLOYED"),
        SandboxAPIError("Bad Gateway", status_code=502),
        dropped(),
        off(TORN_DOWN),
        record("DEPLOYED"),
    ]
    aio_switch.update.side_effect = [off(DEACTIVATE), record("DEPLOYING")]

    with patch(f"{ASYNC}._retry_delay", return_value=0):
        instance = await SandboxInstance.reset("my-sandbox", interval=0)

    assert instance.status == "DEPLOYED"


async def test_reset_cuts_a_read_that_times_out_at_max_wait(aio_switch):
    aio_switch.get.side_effect = [record("DEPLOYED"), httpx.ReadTimeout("timed out")]
    aio_switch.update.side_effect = [off(DEACTIVATE)]

    with pytest.raises(SandboxAPIError, match="could not be read again, it is left DEACTIVATED"):
        await SandboxInstance.reset("my-sandbox", interval=0, max_wait=80)


async def test_reset_says_the_sandbox_is_left_deactivated_when_it_cannot_be_switched_on(
    aio_switch,
):
    aio_switch.get.side_effect = [record("DEPLOYED"), off(TORN_DOWN)]
    aio_switch.update.side_effect = [off(DEACTIVATE), Error(code=500, error="boom")]

    with pytest.raises(
        SandboxAPIError,
        match=r'left DEACTIVATED; call SandboxInstance\.reset\("my-sandbox"\) again',
    ) as err:
        await SandboxInstance.reset("my-sandbox", interval=0)

    assert err.value.status_code == 500


async def test_reset_writes_the_switch_on_again_after_a_dropped_connection(aio_switch):
    # Read again before the second switch-on: still the same sandbox, still off,
    # and changed since (another label), which the second write is built from.
    reread = off(TORN_DOWN)
    reread.metadata.labels = MetadataLabels.from_dict({"team": "b"})
    aio_switch.get.side_effect = [record("DEPLOYED"), off(TORN_DOWN), reread, record("DEPLOYED")]
    aio_switch.update.side_effect = [off(DEACTIVATE), dropped(), record("DEPLOYING")]

    with patch(f"{ASYNC}._retry_delay", return_value=0):
        instance = await SandboxInstance.reset("my-sandbox", interval=0)

    assert instance.status == "DEPLOYED"
    assert aio_switch.update.await_count == 3
    assert body_of(aio_switch.update, 2)["spec"]["enabled"] is True
    assert body_of(aio_switch.update, 2)["metadata"]["labels"] == {"team": "b"}


async def test_reset_stops_when_the_switch_off_answers_for_a_sandbox_created_again(aio_switch):
    aio_switch.get.side_effect = [record("DEPLOYED")]
    aio_switch.update.side_effect = [
        record("DEACTIVATED", False, (DEACTIVATE,), "2026-10-19T12:05:00Z")
    ]

    with pytest.raises(SandboxAPIError) as err:
        await SandboxInstance.reset("my-sandbox", interval=0)

    assert str(err.value) == (
        "Sandbox my-sandbox was deleted and created again while it was being switched off for "
        "its reset; the new sandbox was written to and is left switched off"
    )
    assert err.value.status_code is None
    assert aio_switch.update.await_count == 1
    assert aio_switch.get.await_count == 1


async def test_reset_does_not_send_the_switch_off_again_to_a_sandbox_created_again(aio_switch):
    aio_switch.get.side_effect = [
        record("DEPLOYED"),
        record("DEPLOYED", True, (), "2026-10-19T12:05:00Z"),
    ]
    aio_switch.update.side_effect = [dropped()]

    with (
        patch(f"{ASYNC}._retry_delay", return_value=0),
        pytest.raises(SandboxAPIError, match="answer was lost may have reached the new sandbox"),
    ):
        await SandboxInstance.reset("my-sandbox", interval=0)

    assert aio_switch.update.await_count == 1


async def test_reset_does_not_send_the_switch_on_again_to_a_sandbox_deleted_meanwhile(aio_switch):
    aio_switch.get.side_effect = [record("DEPLOYED"), off(TORN_DOWN), not_found()]
    aio_switch.update.side_effect = [off(DEACTIVATE), dropped()]

    with (
        patch(f"{ASYNC}._retry_delay", return_value=0),
        pytest.raises(SandboxAPIError, match="was deleted during its reset") as err,
    ):
        await SandboxInstance.reset("my-sandbox", interval=0)

    assert err.value.status_code == 404
    assert aio_switch.update.await_count == 2


async def test_reset_does_not_send_the_switch_on_again_to_a_sandbox_created_again(aio_switch):
    aio_switch.get.side_effect = [
        record("DEPLOYED"),
        off(TORN_DOWN),
        record("DEACTIVATED", False, (TORN_DOWN,), "2026-10-19T12:05:00Z"),
    ]
    aio_switch.update.side_effect = [off(DEACTIVATE), dropped()]

    with (
        patch(f"{ASYNC}._retry_delay", return_value=0),
        pytest.raises(SandboxAPIError, match="answer was lost may have reached the new sandbox"),
    ):
        await SandboxInstance.reset("my-sandbox", interval=0)

    assert aio_switch.update.await_count == 2


async def test_reset_does_not_send_a_switch_on_that_landed_again(aio_switch):
    # The write was cut short but the record already reads switched on.
    aio_switch.get.side_effect = [
        record("DEPLOYED"),
        off(TORN_DOWN),
        record("DEPLOYING"),
        record("DEPLOYED"),
    ]
    aio_switch.update.side_effect = [off(DEACTIVATE), dropped()]

    with patch(f"{ASYNC}._retry_delay", return_value=0):
        instance = await SandboxInstance.reset("my-sandbox", interval=0)

    assert instance.status == "DEPLOYED"
    assert aio_switch.update.await_count == 2


async def test_reset_does_not_send_a_switch_off_that_landed_again(aio_switch):
    aio_switch.get.side_effect = [
        record("DEPLOYED"),
        off(DEACTIVATE),  # the re-read after the cut write: it landed
        off(DEACTIVATE, TORN_DOWN),
        record("DEPLOYED"),
    ]
    aio_switch.update.side_effect = [dropped(), record("DEPLOYING")]

    with patch(f"{ASYNC}._retry_delay", return_value=0):
        instance = await SandboxInstance.reset("my-sandbox", interval=0)

    assert instance.status == "DEPLOYED"
    assert aio_switch.update.await_count == 2
    assert body_of(aio_switch.update, 1)["spec"]["enabled"] is True


async def test_reset_does_not_send_the_switch_off_again_to_a_sandbox_no_longer_running(
    aio_switch,
):
    aio_switch.get.side_effect = [record("DEPLOYED"), record("DELETING")]
    aio_switch.update.side_effect = [dropped()]

    with (
        patch(f"{ASYNC}._retry_delay", return_value=0),
        pytest.raises(
            SandboxAPIError, match="is DELETING while it should be running for the reset"
        ),
    ):
        await SandboxInstance.reset("my-sandbox", interval=0)

    assert aio_switch.update.await_count == 1


async def test_reset_stops_when_the_switch_on_answers_for_a_sandbox_created_again(aio_switch):
    aio_switch.get.side_effect = [record("DEPLOYED"), off(TORN_DOWN)]
    aio_switch.update.side_effect = [
        off(DEACTIVATE),
        record("DEPLOYING", True, (), "2026-10-19T12:05:00Z"),
    ]

    with pytest.raises(SandboxAPIError) as err:
        await SandboxInstance.reset("my-sandbox", interval=0)

    assert str(err.value) == (
        "Sandbox my-sandbox was deleted and created again while it was being switched back on "
        "for its reset; the new sandbox was written to and is left switched on"
    )
    assert err.value.status_code is None
    aio_switch.probe.assert_not_called()


async def test_reset_stops_waiting_for_the_redeploy_of_a_sandbox_created_again(aio_switch):
    aio_switch.get.side_effect = [
        record("DEPLOYED"),
        off(TORN_DOWN),
        record("DEPLOYING", True, (), "2026-10-19T12:05:00Z"),
    ]
    aio_switch.update.side_effect = [off(DEACTIVATE), record("DEPLOYING")]

    with pytest.raises(SandboxAPIError, match="was deleted and created again during its reset"):
        await SandboxInstance.reset("my-sandbox", interval=0)

    aio_switch.probe.assert_not_called()


async def test_reset_raises_when_the_sandbox_fails_to_deploy_again(aio_switch):
    aio_switch.get.side_effect = [record("DEPLOYED"), off(TORN_DOWN), record("FAILED")]
    aio_switch.update.side_effect = [off(DEACTIVATE), record("DEPLOYING")]

    with pytest.raises(SandboxAPIError, match="failed to deploy again"):
        await SandboxInstance.reset("my-sandbox", interval=0)


async def test_reset_tolerates_the_record_still_reading_off_right_after_the_switch_on_write(
    aio_switch,
):
    aio_switch.get.side_effect = [
        record("DEPLOYED"),
        off(TORN_DOWN),
        off(TORN_DOWN),
        record("DEPLOYING"),
        record("DEPLOYED"),
    ]
    aio_switch.update.side_effect = [off(DEACTIVATE), record("DEPLOYING")]

    instance = await SandboxInstance.reset("my-sandbox", interval=0)

    assert instance.status == "DEPLOYED"


async def test_reset_raises_when_the_sandbox_is_taken_down_again_once_it_is_redeploying(
    aio_switch,
):
    aio_switch.get.side_effect = [
        record("DEPLOYED"),
        off(TORN_DOWN),
        record("DEPLOYING"),
        off(TORN_DOWN),
    ]
    aio_switch.update.side_effect = [off(DEACTIVATE), record("DEPLOYING")]

    with pytest.raises(SandboxAPIError, match="is DEACTIVATED while it should be deployed again"):
        await SandboxInstance.reset("my-sandbox", interval=0)


async def test_reset_gives_up_after_max_wait_while_it_redeploys(aio_switch):
    aio_switch.get.side_effect = [record("DEPLOYED"), off(TORN_DOWN)] + [record("DEPLOYING")] * 100
    aio_switch.update.side_effect = [off(DEACTIVATE), record("DEPLOYING")]

    with pytest.raises(SandboxAPIError, match="is still DEPLOYING after waiting 0s"):
        await SandboxInstance.reset("my-sandbox", interval=5, max_wait=40)


async def test_reset_waits_until_the_sandbox_answers_not_only_until_it_is_deployed(aio_switch):
    aio_switch.get.side_effect = [record("DEPLOYED"), off(TORN_DOWN), record("DEPLOYED")]
    aio_switch.update.side_effect = [off(DEACTIVATE), record("DEPLOYING")]
    aio_switch.probe.side_effect = [
        not_routable(),
        health(503, {"error": "unavailable"}),
        healthy(),
    ]

    instance = await SandboxInstance.reset("my-sandbox", interval=0)

    assert instance.status == "DEPLOYED"
    assert aio_switch.probe.await_count == 3


# ---------------------------------------------------------------------------- sync


@pytest.fixture
def blocking():
    with (
        patch(f"{SYNC}._post_reset", new_callable=MagicMock) as post,
        patch(f"{SYNC}.get_sandbox", new_callable=MagicMock) as get,
        patch(f"{SYNC}.update_sandbox", new_callable=MagicMock) as update,
        patch(f"{SYNC}.get_health", new_callable=MagicMock) as probe,
    ):
        probe.return_value = healthy()
        # The record read alongside the reset call.
        get.return_value = record("DEPLOYED")
        yield SimpleNamespace(post=post, get=get, update=update, probe=probe)


@pytest.fixture
def blocking_switch(blocking):
    blocking.post.return_value = unknown_route()
    return blocking


def test_sync_reset_resets_the_sandbox_in_one_call_and_waits_until_it_answers(blocking):
    blocking.post.return_value = reset_done()
    blocking.probe.side_effect = [not_routable(), healthy()]

    instance = SyncSandboxInstance.reset("my-sandbox", interval=0)

    assert isinstance(instance, SyncSandboxInstance)
    assert instance.status == "DEPLOYED"
    assert blocking.post.call_count == 1
    assert len(key_of(blocking.post, 0)) == 36
    assert blocking.probe.call_count == 2
    # The record is read once, alongside the call, and nothing is switched off and on.
    assert blocking.get.call_count == 1
    blocking.update.assert_not_called()


def test_sync_reset_refreshes_the_instance_it_is_called_on_and_returns_it(blocking):
    fresh = record("DEPLOYED")
    fresh.last_used_at = "after"
    blocking.post.return_value = httpx.Response(200, json=fresh.to_dict())
    instance = SyncSandboxInstance(record("DEPLOYED"))

    result = instance.reset(interval=0)

    assert result is instance
    assert instance.sandbox.last_used_at == "after"


def test_sync_reset_propagates_what_the_control_plane_refuses(blocking):
    blocking.post.return_value = refused(409, "This sandbox is stopped")

    with pytest.raises(SandboxAPIError, match="This sandbox is stopped") as err:
        SyncSandboxInstance.reset("my-sandbox", interval=0)

    assert err.value.status_code == 409
    blocking.update.assert_not_called()


def test_sync_reset_gives_up_waiting_on_the_control_plane_at_max_wait(blocking):
    blocking.post.side_effect = httpx.ReadTimeout("timed out")

    with pytest.raises(SandboxAPIError, match="was not reset within 0s"):
        SyncSandboxInstance.reset("my-sandbox", interval=0, max_wait=50)


def test_sync_reset_posts_through_the_control_plane_client_cut_at_max_wait():
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(
            (
                request.method,
                request.url.path,
                request.extensions.get("timeout"),
                request.headers.get("Idempotency-Key"),
            )
        )
        return httpx.Response(200, json=record("DEPLOYED").to_dict())

    control_plane = Client(
        base_url="https://api.example", httpx_args={"transport": httpx.MockTransport(handler)}
    )
    with patch(f"{SYNC}.client", control_plane):
        response = sync_module._post_reset(
            "my-sandbox", sync_module._reset_deadline(60_000), "key-1"
        )

    assert response.status_code == 200
    method, path, timeout, key = seen[0]
    assert (method, path, key) == ("POST", "/sandboxes/my-sandbox/reset", "key-1")
    assert 0 < timeout["read"] <= 60


def test_sync_reset_asks_again_with_the_same_key_while_it_is_the_same_sandbox(blocking):
    blocking.post.side_effect = [refused(502, "Bad Gateway"), reset_done()]

    with patch(f"{SYNC}._retry_delay", return_value=0):
        SyncSandboxInstance.reset("my-sandbox", interval=0)

    assert blocking.post.call_count == 2
    assert blocking.get.call_count == 2
    assert key_of(blocking.post, 1) == key_of(blocking.post, 0)


def test_sync_reset_does_not_ask_again_once_the_sandbox_is_created_again(blocking):
    blocking.post.return_value = refused(502, "Bad Gateway")
    blocking.get.side_effect = [
        record("DEPLOYED"),
        record("DEPLOYED", created_at="2026-10-19T12:05:00Z"),
    ]

    with (
        patch(f"{SYNC}._retry_delay", return_value=0),
        pytest.raises(SandboxAPIError, match="which is not reset again"),
    ):
        SyncSandboxInstance.reset("my-sandbox", interval=0)

    assert blocking.post.call_count == 1


def test_sync_reset_says_so_when_it_reset_another_sandbox_than_the_one_it_started_on(blocking):
    blocking.post.return_value = httpx.Response(
        200, json=record("DEPLOYED", created_at="2026-10-19T12:05:00Z").to_dict()
    )

    with pytest.raises(SandboxAPIError, match="as its reset started; the new sandbox was reset"):
        SyncSandboxInstance.reset("my-sandbox", interval=0)

    blocking.probe.assert_not_called()


def test_sync_reset_switches_off_waits_for_the_platform_and_switches_on(blocking_switch):
    get, update = blocking_switch.get, blocking_switch.update
    get.side_effect = [
        record("DEPLOYED"),
        off(DEACTIVATE, TEARING_DOWN),
        off(DEACTIVATE, TEARING_DOWN, TORN_DOWN),
        record("DEPLOYED"),
    ]
    update.side_effect = [off(DEACTIVATE), record("DEPLOYING")]

    instance = SyncSandboxInstance.reset("my-sandbox", interval=0)

    assert instance.status == "DEPLOYED"
    assert [body_of(update, i)["spec"]["enabled"] for i in range(2)] == [False, True]
    assert get.call_count == 4
    for call in [*get.call_args_list, *update.call_args_list]:
        assert isinstance(call.kwargs["client"], async_module._DeadlineClient)


@pytest.mark.parametrize("status", ["TERMINATED", "DELETING", "ARCHIVED", "FAILED"])
def test_sync_reset_refuses_a_sandbox_that_cannot_be_reset_before_writing_anything(
    blocking_switch, status
):
    blocking_switch.get.side_effect = [record(status)]

    with pytest.raises(SandboxAPIError, match=f"is {status} and cannot be reset"):
        SyncSandboxInstance.reset("my-sandbox", interval=0)

    blocking_switch.update.assert_not_called()


def test_sync_reset_does_not_switch_it_back_on_when_the_sandbox_is_deleted_meanwhile(
    blocking_switch,
):
    blocking_switch.get.side_effect = [record("DEPLOYED"), not_found()]
    blocking_switch.update.side_effect = [off(DEACTIVATE)]

    with pytest.raises(SandboxAPIError, match="was deleted during its reset"):
        SyncSandboxInstance.reset("my-sandbox", interval=0)

    assert blocking_switch.update.call_count == 1


def test_sync_reset_leaves_the_sandbox_deactivated_when_the_teardown_outlives_max_wait(
    blocking_switch,
):
    blocking_switch.get.side_effect = [record("DEPLOYED")] + [off(DEACTIVATE, TEARING_DOWN)] * 100
    blocking_switch.update.side_effect = [off(DEACTIVATE)]

    with pytest.raises(
        SandboxAPIError,
        match=r"not reported gone within 0s, it is left DEACTIVATED; "
        r'call SyncSandboxInstance\.reset\("my-sandbox"\) again',
    ):
        SyncSandboxInstance.reset("my-sandbox", interval=5, max_wait=30)

    assert blocking_switch.update.call_count == 1


def test_sync_reset_says_the_sandbox_is_left_deactivated_when_it_cannot_be_switched_on(
    blocking_switch,
):
    blocking_switch.get.side_effect = [record("DEPLOYED"), off(TORN_DOWN)]
    blocking_switch.update.side_effect = [off(DEACTIVATE), Error(code=500, error="boom")]

    with pytest.raises(
        SandboxAPIError,
        match=r'left DEACTIVATED; call SyncSandboxInstance\.reset\("my-sandbox"\) again',
    ):
        SyncSandboxInstance.reset("my-sandbox", interval=0)


def test_sync_reset_writes_the_switch_on_again_after_a_dropped_connection(blocking_switch):
    blocking_switch.get.side_effect = [
        record("DEPLOYED"),
        off(TORN_DOWN),
        off(TORN_DOWN),
        record("DEPLOYED"),
    ]
    blocking_switch.update.side_effect = [off(DEACTIVATE), dropped(), record("DEPLOYING")]

    with patch(f"{SYNC}._retry_delay", return_value=0):
        instance = SyncSandboxInstance.reset("my-sandbox", interval=0)

    assert instance.status == "DEPLOYED"
    assert blocking_switch.update.call_count == 3


def test_sync_reset_stops_when_the_switch_off_answers_for_a_sandbox_created_again(
    blocking_switch,
):
    blocking_switch.get.side_effect = [record("DEPLOYED")]
    blocking_switch.update.side_effect = [
        record("DEACTIVATED", False, (DEACTIVATE,), "2026-10-19T12:05:00Z")
    ]

    with pytest.raises(
        SandboxAPIError, match="was deleted and created again while it was being switched off"
    ):
        SyncSandboxInstance.reset("my-sandbox", interval=0)

    assert blocking_switch.update.call_count == 1


def test_sync_reset_does_not_send_a_write_again_to_a_sandbox_deleted_meanwhile(blocking_switch):
    blocking_switch.get.side_effect = [record("DEPLOYED"), off(TORN_DOWN), not_found()]
    blocking_switch.update.side_effect = [off(DEACTIVATE), dropped()]

    with (
        patch(f"{SYNC}._retry_delay", return_value=0),
        pytest.raises(SandboxAPIError, match="was deleted during its reset"),
    ):
        SyncSandboxInstance.reset("my-sandbox", interval=0)

    assert blocking_switch.update.call_count == 2


def test_sync_reset_does_not_send_the_switch_off_again_to_a_sandbox_created_again(
    blocking_switch,
):
    blocking_switch.get.side_effect = [
        record("DEPLOYED"),
        record("DEPLOYED", True, (), "2026-10-19T12:05:00Z"),
    ]
    blocking_switch.update.side_effect = [dropped()]

    with (
        patch(f"{SYNC}._retry_delay", return_value=0),
        pytest.raises(SandboxAPIError, match="answer was lost may have reached the new sandbox"),
    ):
        SyncSandboxInstance.reset("my-sandbox", interval=0)

    assert blocking_switch.update.call_count == 1


def test_sync_reset_does_not_send_a_switch_on_that_landed_again(blocking_switch):
    blocking_switch.get.side_effect = [
        record("DEPLOYED"),
        off(TORN_DOWN),
        record("DEPLOYING"),
        record("DEPLOYED"),
    ]
    blocking_switch.update.side_effect = [off(DEACTIVATE), dropped()]

    with patch(f"{SYNC}._retry_delay", return_value=0):
        instance = SyncSandboxInstance.reset("my-sandbox", interval=0)

    assert instance.status == "DEPLOYED"
    assert blocking_switch.update.call_count == 2


def test_sync_reset_stops_when_the_switch_on_answers_for_a_sandbox_created_again(
    blocking_switch,
):
    blocking_switch.get.side_effect = [record("DEPLOYED"), off(TORN_DOWN)]
    blocking_switch.update.side_effect = [
        off(DEACTIVATE),
        record("DEPLOYING", True, (), "2026-10-19T12:05:00Z"),
    ]

    with pytest.raises(SandboxAPIError, match="while it was being switched back on for its reset"):
        SyncSandboxInstance.reset("my-sandbox", interval=0)


def test_sync_reset_stops_waiting_for_the_redeploy_of_a_sandbox_created_again(blocking_switch):
    blocking_switch.get.side_effect = [
        record("DEPLOYED"),
        off(TORN_DOWN),
        record("DEPLOYING", True, (), "2026-10-19T12:05:00Z"),
    ]
    blocking_switch.update.side_effect = [off(DEACTIVATE), record("DEPLOYING")]

    with pytest.raises(SandboxAPIError, match="was deleted and created again during its reset"):
        SyncSandboxInstance.reset("my-sandbox", interval=0)


def test_sync_reset_says_a_failed_teardown_cannot_be_finished_by_resetting_again(
    blocking_switch,
):
    blocking_switch.get.side_effect = [record("DEPLOYED"), off(DEACTIVATE, TEARDOWN_FAILED)]
    blocking_switch.update.side_effect = [off(DEACTIVATE)]

    with pytest.raises(
        SandboxAPIError, match="the platform reported the teardown failed. It is left switched off"
    ):
        SyncSandboxInstance.reset("my-sandbox", interval=0)


def test_sync_reset_raises_when_a_deployed_sandbox_does_not_answer_in_time(blocking_switch):
    blocking_switch.get.side_effect = [record("DEPLOYED"), off(TORN_DOWN)] + [
        record("DEPLOYED")
    ] * 10
    blocking_switch.update.side_effect = [off(DEACTIVATE), record("DEPLOYING")]
    blocking_switch.probe.return_value = not_routable()

    with pytest.raises(SandboxAPIError, match="did not answer within 0s after the reset: 404"):
        SyncSandboxInstance.reset("my-sandbox", interval=5, max_wait=40)


def test_the_async_and_sync_resets_share_their_wait_defaults():
    assert asyncio.iscoroutinefunction(SandboxInstance.reset)
    assert async_module.RESET_POLL_MS == 200
    assert sync_module.RESET_POLL_MS == async_module.RESET_POLL_MS
