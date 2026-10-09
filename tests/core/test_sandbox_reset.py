"""Unit tests for resetting a sandbox to a fresh copy of its image.

A reset switches ``spec.enabled`` off and on again through the existing update
call, then waits until the sandbox is DEPLOYED and answers. The control plane
and the sandbox are mocked so each write, read and failure can be scripted.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from blaxel.core.client.models import (
    Env,
    Error,
    Metadata,
    Sandbox,
    SandboxRuntime,
    SandboxSpec,
    Status,
    VolumeAttachment,
)
from blaxel.core.sandbox import SandboxAPIError, SandboxInstance, SyncSandboxInstance
from blaxel.core.sandbox.default.filesystem import SandboxFileSystem
from blaxel.core.sandbox.sync.filesystem import SyncSandboxFileSystem
from blaxel.core.sandbox.types import ResponseError


def record(status: str, enabled: bool = True) -> Sandbox:
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
    sandbox = Sandbox(metadata=Metadata(name="my-sandbox"), spec=spec)
    sandbox.status = Status(status)
    return sandbox


def not_routable() -> ResponseError:
    """What the sandbox answers while its route is not up yet, right after DEPLOYED."""
    response = httpx.Response(404, json={"code": "WORKLOAD_UNAVAILABLE", "retryable": True})
    return ResponseError(response)


def body_of(mock, call: int) -> dict:
    return mock.call_args_list[call].kwargs["body"]


ASYNC = "blaxel.core.sandbox.default.sandbox"
SYNC = "blaxel.core.sandbox.sync.sandbox"


# --------------------------------------------------------------------------- async


@pytest.fixture
def aio():
    with (
        patch(f"{ASYNC}.get_sandbox", new_callable=AsyncMock) as get,
        patch(f"{ASYNC}.update_sandbox", new_callable=AsyncMock) as update,
        patch.object(SandboxFileSystem, "ls", new_callable=AsyncMock) as ls,
    ):
        ls.return_value = {}
        yield get, update, ls


@pytest.mark.asyncio
async def test_reset_switches_the_sandbox_off_and_on_then_waits_until_it_is_deployed(aio):
    get, update, _ = aio
    get.side_effect = [record("DEPLOYED"), record("DEPLOYING"), record("DEPLOYED")]
    update.side_effect = [record("DEACTIVATED", False), record("DEPLOYING")]

    instance = await SandboxInstance.reset("my-sandbox", interval=0)

    assert isinstance(instance, SandboxInstance)
    assert instance.status == "DEPLOYED"
    assert instance.metadata.name == "my-sandbox"
    assert update.await_count == 2
    off, on = body_of(update, 0), body_of(update, 1)
    assert off["spec"]["enabled"] is False
    assert on["spec"]["enabled"] is True
    # Everything else is written back as the control plane returned it, masked
    # secret values included, so nothing but ``enabled`` changes.
    expected = record("DEPLOYED").to_dict()["spec"]
    assert {**off["spec"], "enabled": True} == expected
    assert on["spec"] == expected
    assert off["metadata"] == record("DEPLOYED").to_dict()["metadata"]
    # Read-only state is not sent back.
    assert "status" not in off
    assert get.await_count == 3
    for call in [*get.call_args_list, *update.call_args_list]:
        assert (call.args or (call.kwargs["sandbox_name"],))[0] == "my-sandbox"


@pytest.mark.asyncio
async def test_reset_refreshes_the_instance_it_is_called_on_and_returns_it(aio):
    get, update, _ = aio
    fresh = record("DEPLOYED")
    fresh.last_used_at = "after"
    get.side_effect = [record("DEPLOYED"), fresh]
    update.side_effect = [record("DEACTIVATED", False), record("DEPLOYING")]
    instance = SandboxInstance(record("DEPLOYED"))

    result = await instance.reset(interval=0)

    assert result is instance
    assert instance.last_used_at == "after"
    assert instance.config.sandbox is instance.sandbox


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status", ["TERMINATED", "DELETING", "ARCHIVED", "ARCHIVING", "UNARCHIVING"]
)
async def test_reset_refuses_a_sandbox_that_cannot_be_reset_before_writing_anything(aio, status):
    # A write to a deleted record would bring the sandbox back to life.
    get, update, _ = aio
    get.return_value = record(status)

    with pytest.raises(SandboxAPIError, match=f"is {status} and cannot be reset"):
        await SandboxInstance.reset("my-sandbox", interval=0)

    update.assert_not_awaited()


@pytest.mark.asyncio
async def test_reset_propagates_the_error_of_a_sandbox_that_does_not_exist(aio):
    get, update, _ = aio
    get.return_value = Error(error="Sandbox not found", code=404)

    with pytest.raises(SandboxAPIError) as raised:
        await SandboxInstance.reset("my-sandbox")

    assert raised.value.status_code == 404
    update.assert_not_awaited()


@pytest.mark.asyncio
async def test_reset_only_switches_a_disabled_sandbox_back_on(aio):
    get, update, _ = aio
    get.side_effect = [record("DEACTIVATED", False), record("DEPLOYED")]
    update.side_effect = [record("DEPLOYING")]

    instance = await SandboxInstance.reset("my-sandbox", interval=0)

    assert instance.status == "DEPLOYED"
    assert update.await_count == 1
    assert body_of(update, 0)["spec"]["enabled"] is True


@pytest.mark.asyncio
async def test_reset_completes_a_reset_that_left_the_sandbox_going_off(aio):
    get, update, _ = aio
    get.side_effect = [record("DEACTIVATING", True), record("DEPLOYED")]
    update.side_effect = [record("DEPLOYING")]

    await SandboxInstance.reset("my-sandbox", interval=0)

    assert update.await_count == 1
    assert body_of(update, 0)["spec"]["enabled"] is True


@pytest.mark.asyncio
async def test_reset_leaves_the_sandbox_as_it_was_when_it_cannot_be_taken_down(aio):
    get, update, _ = aio
    get.return_value = record("DEPLOYED")
    update.return_value = Error(error="not allowed", code=403)

    with pytest.raises(
        SandboxAPIError, match="could not be reset, it was left as it was"
    ) as raised:
        await SandboxInstance.reset("my-sandbox", interval=0)

    assert raised.value.status_code == 403
    assert isinstance(raised.value.__cause__, SandboxAPIError)
    assert update.await_count == 1


@pytest.mark.asyncio
async def test_reset_does_not_switch_it_back_on_when_the_control_plane_did_not_take_it_down(aio):
    get, update, _ = aio
    get.return_value = record("DEPLOYED")
    update.return_value = record("DEPLOYED")

    with pytest.raises(SandboxAPIError, match=r"did not take it down \(it is DEPLOYED\)"):
        await SandboxInstance.reset("my-sandbox", interval=0)

    assert update.await_count == 1


@pytest.mark.asyncio
async def test_reset_says_the_sandbox_is_left_deactivated_when_it_cannot_be_switched_on(aio):
    get, update, _ = aio
    get.return_value = record("DEPLOYED")
    update.side_effect = [record("DEACTIVATED", False), Error(error="internal", code=500)]

    with pytest.raises(
        SandboxAPIError,
        match=r'left DEACTIVATED; call SandboxInstance\.reset\("my-sandbox"\) again',
    ) as raised:
        await SandboxInstance.reset("my-sandbox", interval=0)

    assert raised.value.status_code == 500


@pytest.mark.asyncio
async def test_reset_retries_the_write_that_switches_it_back_on_after_a_dropped_connection(aio):
    get, update, _ = aio
    get.side_effect = [record("DEPLOYED"), record("DEPLOYED")]
    update.side_effect = [
        record("DEACTIVATED", False),
        httpx.RemoteProtocolError("Server disconnected without sending a response"),
        record("DEPLOYING"),
    ]

    instance = await SandboxInstance.reset("my-sandbox", interval=0)

    assert instance.status == "DEPLOYED"
    assert update.await_count == 3
    assert body_of(update, 2)["spec"]["enabled"] is True


@pytest.mark.asyncio
async def test_reset_raises_when_the_sandbox_fails_to_deploy_again(aio):
    get, update, _ = aio
    get.side_effect = [record("DEPLOYED"), record("FAILED")]
    update.side_effect = [record("DEACTIVATED", False), record("DEPLOYING")]

    with pytest.raises(SandboxAPIError, match="failed to deploy again"):
        await SandboxInstance.reset("my-sandbox", interval=0)


@pytest.mark.asyncio
async def test_reset_tolerates_the_record_still_reading_off_right_after_the_switch_on_write(aio):
    get, update, _ = aio
    get.side_effect = [
        record("DEPLOYED"),
        record("DEACTIVATED", False),
        record("DEACTIVATING", False),
        record("DEPLOYING"),
        record("DEPLOYED"),
    ]
    update.side_effect = [record("DEACTIVATED", False), record("DEACTIVATED", True)]

    instance = await SandboxInstance.reset("my-sandbox", interval=0)

    assert instance.status == "DEPLOYED"
    assert get.await_count == 5


@pytest.mark.asyncio
async def test_reset_does_not_tolerate_a_sandbox_that_stays_off_within_the_wait_asked_for(aio):
    get, update, _ = aio
    get.side_effect = [record("DEPLOYED"), record("DEACTIVATED", False)]
    update.side_effect = [record("DEACTIVATED", False), record("DEACTIVATED", True)]

    with pytest.raises(SandboxAPIError, match="is DEACTIVATED while it should be deployed again"):
        await SandboxInstance.reset("my-sandbox", interval=0, max_wait=0)


@pytest.mark.asyncio
async def test_reset_raises_when_the_sandbox_is_taken_down_again_once_it_is_redeploying(aio):
    get, update, _ = aio
    get.side_effect = [record("DEPLOYED"), record("DEPLOYING"), record("DEACTIVATED", False)]
    update.side_effect = [record("DEACTIVATED", False), record("DEPLOYING")]

    with pytest.raises(SandboxAPIError, match="is DEACTIVATED while it should be deployed again"):
        await SandboxInstance.reset("my-sandbox", interval=0)


@pytest.mark.asyncio
async def test_reset_lets_the_teardown_finish_before_it_switches_the_sandbox_back_on(aio):
    get, update, _ = aio
    get.side_effect = [
        record("DEPLOYED"),
        record("DEACTIVATING", False),
        record("DEACTIVATED", False),
        record("DEPLOYED"),
    ]
    update.side_effect = [record("DEACTIVATING", False), record("DEPLOYING")]

    instance = await SandboxInstance.reset("my-sandbox", interval=0)

    assert instance.status == "DEPLOYED"
    assert update.await_count == 2
    assert body_of(update, 1)["spec"]["enabled"] is True
    # Switching it on came after the sandbox read DEACTIVATED: two reads, then the write.
    assert get.await_count == 4


@pytest.mark.asyncio
async def test_reset_does_not_switch_it_back_on_when_the_teardown_ends_up_somewhere_else(aio):
    get, update, _ = aio
    get.side_effect = [record("DEPLOYED"), record("DEPLOYED")]
    update.side_effect = [record("DEACTIVATING", False)]

    with pytest.raises(SandboxAPIError, match=r"did not finish taking it down \(it is DEPLOYED\)"):
        await SandboxInstance.reset("my-sandbox", interval=0)
    assert update.await_count == 1


@pytest.mark.asyncio
async def test_reset_gives_up_after_max_wait(aio):
    get, update, _ = aio
    get.side_effect = [record("DEPLOYED"), record("DEPLOYING")]
    update.side_effect = [record("DEACTIVATED", False), record("DEPLOYING")]

    with pytest.raises(SandboxAPIError, match="still DEPLOYING after waiting 0s"):
        await SandboxInstance.reset("my-sandbox", interval=0, max_wait=0)


@pytest.mark.asyncio
async def test_reset_waits_indefinitely_when_max_wait_is_minus_one(aio):
    get, update, _ = aio
    get.side_effect = [record("DEPLOYED"), *[record("DEPLOYING")] * 5, record("DEPLOYED")]
    update.side_effect = [record("DEACTIVATED", False), record("DEPLOYING")]

    instance = await SandboxInstance.reset("my-sandbox", interval=0, max_wait=-1)

    assert instance.status == "DEPLOYED"
    assert get.await_count == 7


@pytest.mark.asyncio
async def test_reset_waits_until_the_sandbox_answers_not_only_until_it_is_deployed(aio):
    # The record is DEPLOYED a couple of seconds before the route is up.
    get, update, ls = aio
    get.side_effect = [record("DEPLOYED"), record("DEPLOYED")]
    update.side_effect = [record("DEACTIVATED", False), record("DEPLOYING")]
    ls.side_effect = [not_routable(), not_routable(), {}]

    instance = await SandboxInstance.reset("my-sandbox", interval=0)

    assert instance.status == "DEPLOYED"
    assert ls.await_count == 3
    # The record is read once: the readiness check does not poll it again.
    assert get.await_count == 2


@pytest.mark.asyncio
async def test_reset_raises_when_a_deployed_sandbox_does_not_answer_in_time(aio):
    get, update, ls = aio
    get.return_value = record("DEPLOYED")
    update.side_effect = [record("DEACTIVATED", False), record("DEPLOYING")]
    ls.side_effect = not_routable()

    with pytest.raises(SandboxAPIError, match="was deployed again but did not answer within 0s"):
        await SandboxInstance.reset("my-sandbox", interval=0, max_wait=0)


@pytest.mark.asyncio
async def test_reset_does_not_keep_waiting_on_an_error_that_retrying_cannot_fix(aio):
    get, update, ls = aio
    get.return_value = record("DEPLOYED")
    update.side_effect = [record("DEACTIVATED", False), record("DEPLOYING")]
    ls.side_effect = ResponseError(httpx.Response(403, json={"error": "forbidden"}))

    with pytest.raises(SandboxAPIError, match="was deployed again but does not answer"):
        await SandboxInstance.reset("my-sandbox", interval=0)

    assert ls.await_count == 1


# ---------------------------------------------------------------------------- sync


@pytest.fixture
def blocking():
    with (
        patch(f"{SYNC}.get_sandbox", new_callable=MagicMock) as get,
        patch(f"{SYNC}.update_sandbox", new_callable=MagicMock) as update,
        patch.object(SyncSandboxFileSystem, "ls", new_callable=MagicMock) as ls,
    ):
        ls.return_value = {}
        yield get, update, ls


def test_sync_reset_switches_the_sandbox_off_and_on_then_waits_until_it_is_deployed(blocking):
    get, update, ls = blocking
    get.side_effect = [record("DEPLOYED"), record("DEPLOYING"), record("DEPLOYED")]
    update.side_effect = [record("DEACTIVATED", False), record("DEPLOYING")]

    instance = SyncSandboxInstance.reset("my-sandbox", interval=0)

    assert isinstance(instance, SyncSandboxInstance)
    assert instance.status == "DEPLOYED"
    assert [body_of(update, i)["spec"]["enabled"] for i in range(2)] == [False, True]
    assert get.call_count == 3
    assert ls.call_count == 1


def test_sync_reset_refreshes_the_instance_it_is_called_on_and_returns_it(blocking):
    get, update, _ = blocking
    fresh = record("DEPLOYED")
    fresh.last_used_at = "after"
    get.side_effect = [record("DEPLOYED"), fresh]
    update.side_effect = [record("DEACTIVATED", False), record("DEPLOYING")]
    instance = SyncSandboxInstance(record("DEPLOYED"))

    result = instance.reset(interval=0)

    assert result is instance
    assert instance.last_used_at == "after"
    assert instance.config.sandbox is instance.sandbox


@pytest.mark.parametrize("status", ["TERMINATED", "DELETING", "ARCHIVED"])
def test_sync_reset_refuses_a_sandbox_that_cannot_be_reset_before_writing_anything(
    blocking, status
):
    get, update, _ = blocking
    get.return_value = record(status)

    with pytest.raises(SandboxAPIError, match=f"is {status} and cannot be reset"):
        SyncSandboxInstance.reset("my-sandbox", interval=0)

    update.assert_not_called()


def test_sync_reset_says_the_sandbox_is_left_deactivated_when_it_cannot_be_switched_on(blocking):
    get, update, _ = blocking
    get.return_value = record("DEPLOYED")
    update.side_effect = [record("DEACTIVATED", False), Error(error="internal", code=500)]

    with pytest.raises(
        SandboxAPIError,
        match=r'left DEACTIVATED; call SyncSandboxInstance\.reset\("my-sandbox"\) again',
    ):
        SyncSandboxInstance.reset("my-sandbox", interval=0)


def test_sync_reset_leaves_the_sandbox_as_it_was_when_it_cannot_be_taken_down(blocking):
    get, update, _ = blocking
    get.return_value = record("DEPLOYED")
    update.return_value = Error(error="not allowed", code=403)

    with pytest.raises(SandboxAPIError, match="could not be reset, it was left as it was"):
        SyncSandboxInstance.reset("my-sandbox", interval=0)

    assert update.call_count == 1


def test_sync_reset_waits_until_the_sandbox_answers_not_only_until_it_is_deployed(blocking):
    get, update, ls = blocking
    get.side_effect = [record("DEPLOYED"), record("DEPLOYED")]
    update.side_effect = [record("DEACTIVATED", False), record("DEPLOYING")]
    ls.side_effect = [not_routable(), not_routable(), {}]

    instance = SyncSandboxInstance.reset("my-sandbox", interval=0)

    assert instance.status == "DEPLOYED"
    assert ls.call_count == 3
    assert get.call_count == 2


def test_sync_reset_tolerates_the_record_still_reading_off_right_after_the_switch_on_write(
    blocking,
):
    get, update, _ = blocking
    get.side_effect = [
        record("DEPLOYED"),
        record("DEACTIVATED", False),
        record("DEPLOYING"),
        record("DEPLOYED"),
    ]
    update.side_effect = [record("DEACTIVATED", False), record("DEACTIVATED", True)]

    instance = SyncSandboxInstance.reset("my-sandbox", interval=0)

    assert instance.status == "DEPLOYED"
    assert get.call_count == 4


def test_sync_reset_lets_the_teardown_finish_before_it_switches_the_sandbox_back_on(blocking):
    get, update, _ = blocking
    get.side_effect = [
        record("DEPLOYED"),
        record("DEACTIVATING", False),
        record("DEACTIVATED", False),
        record("DEPLOYED"),
    ]
    update.side_effect = [record("DEACTIVATING", False), record("DEPLOYING")]

    instance = SyncSandboxInstance.reset("my-sandbox", interval=0)

    assert instance.status == "DEPLOYED"
    assert update.call_count == 2
    assert get.call_count == 4


def test_sync_reset_waits_indefinitely_when_max_wait_is_minus_one(blocking):
    get, update, _ = blocking
    get.side_effect = [record("DEPLOYED"), *[record("DEPLOYING")] * 5, record("DEPLOYED")]
    update.side_effect = [record("DEACTIVATED", False), record("DEPLOYING")]

    instance = SyncSandboxInstance.reset("my-sandbox", interval=0, max_wait=-1)

    assert instance.status == "DEPLOYED"
    assert get.call_count == 7


def test_sync_reset_raises_when_a_deployed_sandbox_does_not_answer_in_time(blocking):
    get, update, ls = blocking
    get.return_value = record("DEPLOYED")
    update.side_effect = [record("DEACTIVATED", False), record("DEPLOYING")]
    ls.side_effect = not_routable()

    with pytest.raises(SandboxAPIError, match="was deployed again but did not answer within 0s"):
        SyncSandboxInstance.reset("my-sandbox", interval=0, max_wait=0)


def test_sync_reset_retries_the_write_that_switches_it_back_on_after_a_dropped_connection(
    blocking,
):
    get, update, _ = blocking
    get.side_effect = [record("DEPLOYED"), record("DEPLOYED")]
    update.side_effect = [
        record("DEACTIVATED", False),
        httpx.RemoteProtocolError("Server disconnected without sending a response"),
        record("DEPLOYING"),
    ]

    instance = SyncSandboxInstance.reset("my-sandbox", interval=0)

    assert instance.status == "DEPLOYED"
    assert update.call_count == 3
