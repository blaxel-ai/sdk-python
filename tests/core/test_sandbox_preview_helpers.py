"""Preview helpers: identical async/sync contracts without changing legacy paths."""

import inspect
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest

from blaxel.core import SandboxPreviewCreateConfiguration
from blaxel.core.client import errors
from blaxel.core.client.models import (
    Metadata,
    Preview,
    PreviewMetadata,
    PreviewSpec,
    PreviewToken,
    PreviewTokenMetadata,
    PreviewTokenSpec,
    Sandbox,
    SandboxSpec,
)
from blaxel.core.client.types import UNSET
from blaxel.core.sandbox import SandboxPreviewCreateConfiguration as ExportedConfiguration
from blaxel.core.sandbox.default import preview as async_module
from blaxel.core.sandbox.sync import preview as sync_module
from tests.integration.core.sandbox import test_preview_helpers as live_helpers

NOW = datetime(2026, 10, 5, tzinfo=timezone.utc)


class ClockMeta(type):
    def __instancecheck__(cls, instance):
        return isinstance(instance, datetime)


class Clock(datetime, metaclass=ClockMeta):
    @classmethod
    def now(cls, tz=None):
        return NOW


async def call(fn, *args, **kwargs):
    result = fn(*args, **kwargs)
    return await result if inspect.isawaitable(result) else result


def model(name="app", public=False):
    return Preview(
        metadata=PreviewMetadata(name=name, resource_name="sandbox"),
        spec=PreviewSpec(port=3000, public=public, url="https://preview.example"),
    )


def raw_token(name="token", hours: float = 2, **kwargs):
    return PreviewToken(
        metadata=PreviewTokenMetadata(name=name),
        spec=PreviewTokenSpec(
            token=kwargs.pop("token", name),
            expires_at=kwargs.pop("expires_at", (NOW + timedelta(hours=hours)).isoformat()),
            **kwargs,
        ),
    )


@pytest.fixture(params=[async_module, sync_module], ids=["async", "sync"])
def lane(request, monkeypatch):
    module = request.param
    prefix = "" if module is async_module else "Sync"
    mock = AsyncMock if module is async_module else Mock
    monkeypatch.setattr(module, "datetime", Clock)
    previews = getattr(module, prefix + "SandboxPreviews")(
        Sandbox(metadata=Metadata(name="sandbox"), spec=SandboxSpec())
    )
    tokens = getattr(module, prefix + "SandboxPreviewTokens")(model())
    mocks = {}
    for name in [
        "create_sandbox_preview",
        "get_sandbox_preview",
        "list_sandbox_preview_tokens",
        "create_sandbox_preview_token",
        "delete_sandbox_preview_token",
    ]:
        mocks[name] = mock()
        monkeypatch.setattr(module, name, mocks[name])
    mocks["create_sandbox_preview"].return_value = model()
    mocks["get_sandbox_preview"].return_value = model()
    mocks["list_sandbox_preview_tokens"].return_value = []
    mocks["create_sandbox_preview_token"].return_value = raw_token()
    return SimpleNamespace(
        module=module, prefix=prefix, previews=previews, tokens=tokens, mocks=mocks
    )


@pytest.mark.parametrize(
    "config,expected",
    [
        ({"port": 3000}, {"name": "preview-3000", "public": False}),
        (SandboxPreviewCreateConfiguration(3000), {"name": "preview-3000", "public": False}),
        ({"port": 3000, "name": "custom", "public": True}, {"name": "custom", "public": True}),
        ({"port": 3000, "name": None}, {"name": "preview-3000", "public": False}),
    ],
)
async def test_shorthand_body(lane, config, expected):
    await call(lane.previews.create, config)
    body = lane.mocks["create_sandbox_preview"].call_args.kwargs["body"]
    assert body.to_dict() == {
        "metadata": {"name": expected["name"]},
        "spec": {"port": 3000, "public": expected["public"]},
    }
    other = type(lane.previews)(Sandbox(metadata=Metadata(name="other"), spec=SandboxSpec()))
    await call(other.create, config)
    assert lane.mocks["create_sandbox_preview"].call_args.args == ("other",)
    assert lane.mocks["create_sandbox_preview"].call_args.kwargs["body"].to_dict() == body.to_dict()


@pytest.mark.parametrize(
    "config,message",
    [
        ({}, "Preview port must be an integer between 1 and 65535"),
        *[
            ({"port": p}, "Preview port must be an integer between 1 and 65535")
            for p in [True, False, 0, 65536, 3.1, "3000", None]
        ],
        *[({"port": 3000, "name": n}, "Preview name must be a nonempty string") for n in ["", 1]],
        *[
            ({"port": 3000, "public": p}, "Preview public must be a boolean")
            for p in [None, 1, "false"]
        ],
    ],
)
async def test_shorthand_validation_before_io(lane, config, message):
    for method in [lane.previews.create, lane.previews.create_if_not_exists]:
        with pytest.raises(ValueError, match=message):
            await call(method, config)
    assert all(not mock.called for mock in lane.mocks.values())


async def test_legacy_input_and_get_hit_unchanged(lane):
    full = model(public=True)
    await call(lane.previews.create, full)
    assert lane.mocks["create_sandbox_preview"].call_args.kwargs["body"] is full
    mixed = {"metadata": {"name": "legacy"}, "spec": {"port": 0}, "port": False}
    await call(lane.previews.create, mixed)
    expected = Preview.from_dict(mixed)
    assert expected is not None
    assert (
        lane.mocks["create_sandbox_preview"].call_args.kwargs["body"].to_dict()
        == expected.to_dict()
    )
    lane.mocks["create_sandbox_preview"].reset_mock()
    existing = await call(lane.previews.create_if_not_exists, {"port": 3000})
    assert existing.preview is lane.mocks["get_sandbox_preview"].return_value
    assert existing.spec.public is False
    lane.mocks["create_sandbox_preview"].assert_not_called()


async def test_shorthand_race_only(lane):
    get = lane.mocks["get_sandbox_preview"]
    create = lane.mocks["create_sandbox_preview"]
    get.side_effect = [errors.UnexpectedStatus(404, b"missing"), model(public=True)]
    create.side_effect = errors.UnexpectedStatus(409, b"race")
    result = await call(lane.previews.create_if_not_exists, {"port": 3000})
    assert result.spec.public is True  # returned as-is, never privatized
    assert get.call_count == 2 and create.call_count == 1
    assert all(args.args == ("sandbox", "preview-3000") for args in get.call_args_list)
    get.reset_mock()
    get.side_effect = errors.UnexpectedStatus(404, b"missing")
    with pytest.raises(errors.UnexpectedStatus, match="409"):
        await call(lane.previews.create_if_not_exists, model())
    assert get.call_count == 1  # legacy create conflicts do not gain a retry


@pytest.mark.parametrize("stage", ["get", "create", "reread"])
@pytest.mark.parametrize("status", [403, 429, 500])
async def test_race_failures_propagate(lane, stage, status):
    failure = errors.UnexpectedStatus(status, b"failure")
    get, create = lane.mocks["get_sandbox_preview"], lane.mocks["create_sandbox_preview"]
    if stage == "get":
        get.side_effect = failure
    else:
        get.side_effect = [errors.UnexpectedStatus(404, b"missing"), failure]
        create.side_effect = failure if stage == "create" else errors.UnexpectedStatus(409, b"race")
    with pytest.raises(errors.UnexpectedStatus) as caught:
        await call(lane.previews.create_if_not_exists, {"port": 3000})
    assert caught.value is failure
    assert get.call_count == (2 if stage == "reread" else 1)
    assert create.call_count == (0 if stage == "get" else 1)


async def test_getters_and_delete_by_name(lane):
    preview_cls = getattr(lane.module, lane.prefix + "SandboxPreview")
    token_cls = getattr(lane.module, lane.prefix + "SandboxPreviewToken")
    assert preview_cls(model()).url == "https://preview.example"
    token = token_cls(raw_token())
    assert token.name == "token"
    for missing in [None, UNSET, SimpleNamespace()]:
        assert preview_cls(SimpleNamespace(spec=missing)).url == ""
        assert token_cls(SimpleNamespace(metadata=missing)).name == ""
    for missing in [None, UNSET]:
        assert preview_cls(SimpleNamespace(spec=SimpleNamespace(url=missing))).url == ""
        assert token_cls(SimpleNamespace(metadata=SimpleNamespace(name=missing))).name == ""
    assert all(not mock.called for mock in lane.mocks.values())
    await call(lane.tokens.delete, token.name)
    assert lane.mocks["delete_sandbox_preview_token"].call_args.args == ("sandbox", "app", "token")
    # Preserve the pre-existing differing expires_at return types.
    assert isinstance(token.expires_at, str if lane.module is async_module else datetime)


async def test_empty_list_create_normalized_expiry_and_metadata(lane):
    result = await call(lane.tokens.create_if_expired)
    assert result.name == "token"
    body = lane.mocks["create_sandbox_preview_token"].call_args.kwargs["body"]
    assert body.metadata.name == ""
    assert body.spec.expires_at == "2026-10-06T00:00:00Z"
    assert lane.mocks["list_sandbox_preview_tokens"].call_count == 1
    lane.mocks["delete_sandbox_preview_token"].assert_not_called()


async def test_only_short_lived_token_creates_exactly_once(lane):
    short = raw_token("short", hours=0.5)
    lane.mocks["list_sandbox_preview_tokens"].return_value = [short]
    result = await call(lane.tokens.create_if_expired)
    assert result.preview_token is lane.mocks["create_sandbox_preview_token"].return_value
    assert result.preview_token is not short
    lane.mocks["list_sandbox_preview_tokens"].assert_called_once()
    lane.mocks["create_sandbox_preview_token"].assert_called_once()
    lane.mocks["delete_sandbox_preview_token"].assert_not_called()


async def test_latest_ceiling_threshold_ties_and_invalid_raw_entries(lane):
    first = raw_token("first", 3)
    entries = [
        None,
        SimpleNamespace(),
        PreviewToken(metadata=PreviewTokenMetadata(name="empty"), spec=PreviewTokenSpec()),
        raw_token(token=""),
        raw_token(expired=True),
        raw_token(expires_at="invalid"),
        raw_token(hours=-1),
        raw_token(hours=0),
        raw_token(hours=0.5),
        raw_token("threshold", 1),
        first,
        raw_token("tie", 3),
        raw_token("above-ceiling", 5),
    ]
    lane.mocks["list_sandbox_preview_tokens"].return_value = entries
    result = await call(lane.tokens.create_if_expired, NOW + timedelta(hours=4))
    assert result.preview_token is first
    lane.mocks["create_sandbox_preview_token"].assert_not_called()
    lane.mocks["delete_sandbox_preview_token"].assert_not_called()
    lane.mocks["list_sandbox_preview_tokens"].return_value = [raw_token("threshold", 1)]
    assert (await call(lane.tokens.create_if_expired, NOW + timedelta(hours=1))).name == "threshold"
    lane.mocks["list_sandbox_preview_tokens"].return_value = [raw_token(hours=0)]
    await call(lane.tokens.create_if_expired, min_validity=timedelta(0))
    assert lane.mocks["create_sandbox_preview_token"].call_count == 1


@pytest.mark.parametrize(
    "expiry",
    [datetime(2026, 10, 5, 2), datetime(2026, 10, 5, 7, tzinfo=timezone(timedelta(hours=5)))],
)
async def test_aware_and_naive_utc_expiry(lane, expiry):
    await call(lane.tokens.create_if_expired, expiry)
    body = lane.mocks["create_sandbox_preview_token"].call_args.kwargs["body"]
    assert body.spec.expires_at == "2026-10-05T02:00:00Z"
    lane.mocks["list_sandbox_preview_tokens"].return_value = [
        raw_token(expires_at="2026-10-05T07:00:00+05:00")
    ]
    assert (await call(lane.tokens.create_if_expired, expiry)).name == "token"
    assert lane.mocks["create_sandbox_preview_token"].call_count == 1


@pytest.mark.parametrize(
    "kwargs,message",
    [
        ({"min_validity": -1}, "min_validity must be a non-negative timedelta"),
        ({"min_validity": timedelta(seconds=-1)}, "min_validity must be a non-negative timedelta"),
        *[
            (
                {"expires_at": e},
                "expires_at must be a valid future datetime at least min_validity from now",
            )
            for e in ["invalid", 1, NOW, NOW - timedelta(seconds=1), NOW + timedelta(minutes=59)]
        ],
    ],
)
async def test_token_validation_before_io(lane, kwargs, message):
    with pytest.raises(ValueError, match=message):
        await call(lane.tokens.create_if_expired, **kwargs)
    assert all(not mock.called for mock in lane.mocks.values())


async def test_public_rejected_and_absent_public_not_guessed(lane):
    lane.tokens.preview.spec.public = True
    with pytest.raises(ValueError, match="Cannot create or reuse a token for a public preview"):
        await call(lane.tokens.create_if_expired)
    assert all(not mock.called for mock in lane.mocks.values())
    lane.tokens.preview.spec.public = UNSET
    await call(lane.tokens.create_if_expired)
    assert lane.mocks["list_sandbox_preview_tokens"].call_count == 1


@pytest.mark.parametrize("stage", ["list", "create"])
async def test_token_http_failures_no_retry(lane, stage):
    failure = errors.UnexpectedStatus(403, b"denied")
    endpoint = "list_sandbox_preview_tokens" if stage == "list" else "create_sandbox_preview_token"
    lane.mocks[endpoint].side_effect = failure
    with pytest.raises(errors.UnexpectedStatus) as caught:
        await call(lane.tokens.create_if_expired)
    assert caught.value is failure
    assert lane.mocks[endpoint].call_count == 1
    lane.mocks["delete_sandbox_preview_token"].assert_not_called()


@pytest.mark.parametrize("response", [None, {}, raw_token()])
async def test_nonlist_success_is_not_empty_list(lane, response):
    lane.mocks["list_sandbox_preview_tokens"].return_value = response
    with pytest.raises(RuntimeError, match="Failed to list preview tokens"):
        await call(lane.tokens.create_if_expired)
    lane.mocks["create_sandbox_preview_token"].assert_not_called()


async def test_sync_create_metadata_prerequisite_and_list_bug_untouched(lane):
    await call(lane.tokens.create, NOW + timedelta(hours=2))
    assert lane.mocks["create_sandbox_preview_token"].call_args.kwargs["body"].metadata.name == ""
    if lane.module is sync_module:
        with pytest.raises(errors.UnexpectedStatus) as caught:
            lane.tokens.list()
        assert caught.value.status_code == 400
        assert caught.value.content == b"Failed to list preview tokens"


@pytest.mark.parametrize("status", [401, 200])
async def test_live_poll_retries_both_expected_statuses(monkeypatch, status):
    client = AsyncMock()
    client.get.side_effect = [SimpleNamespace(status_code=503), SimpleNamespace(status_code=status)]
    monkeypatch.setattr(live_helpers.asyncio, "sleep", AsyncMock())
    response = await live_helpers._wait_for_http(client, "https://preview.example", status)
    assert response.status_code == status
    assert client.get.call_count == 2


@pytest.mark.parametrize("failure_stage", ["setup", "test", "cleanup"])
async def test_live_cleanup_does_not_mask_original_error(monkeypatch, failure_stage):
    original = RuntimeError("original setup failure")
    cleanup_failure = ValueError("cleanup failure")
    owner = live_helpers.TestPreviewHelpers()
    sandbox = SimpleNamespace(process=SimpleNamespace(exec=AsyncMock()))
    manager = SimpleNamespace(
        create=AsyncMock(return_value=sandbox),
        delete=AsyncMock(side_effect=cleanup_failure),
    )
    request = SimpleNamespace(
        param=manager, cls=type(owner), session=SimpleNamespace(testsfailed=0)
    )
    monkeypatch.setattr(type(owner), "sandbox", None, raising=False)
    generator = getattr(live_helpers.TestPreviewHelpers.cleanup, "__wrapped__")(owner, request)
    if failure_stage == "setup":
        sandbox.process.exec.side_effect = original
        with pytest.raises(RuntimeError) as caught:
            await anext(generator)
        assert caught.value is original
    else:
        await anext(generator)
        if failure_stage == "test":
            # Pytest records the call failure before resuming the yield fixture.
            request.session.testsfailed += 1
            with pytest.raises(StopAsyncIteration):
                await anext(generator)
        else:
            with pytest.raises(ValueError) as caught:
                await anext(generator)
            assert caught.value is cleanup_failure
    manager.delete.assert_called_once()


def test_export_smoke():
    assert ExportedConfiguration is SandboxPreviewCreateConfiguration
    assert SandboxPreviewCreateConfiguration.from_dict({"port": 1}).port == 1
    assert async_module.SandboxPreviews and sync_module.SyncSandboxPreviews
