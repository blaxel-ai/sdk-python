"""Archive and unarchive waits read at the first interval until the operation is seen pending."""

import asyncio
from types import SimpleNamespace

import pytest

from blaxel.core.sandbox.default import sandbox as async_module
from blaxel.core.sandbox.sync import sandbox as sync_module

INTERVAL_MS = 2_000


def _statuses(entry: str, pending: str, target: str) -> list[str]:
    # Long enough at the entry status that an unbounded backoff would grow
    # well past the first interval before the pending status shows up.
    return [entry] * 8 + [pending] * 6 + [target]


def _fake_reads(statuses: list[str]):
    reads = iter(statuses)

    def read(*_args, **_kwargs):
        return SimpleNamespace(status=next(reads))

    return read


def _check_delays(delays: list[float], entry_reads: int) -> None:
    before_start = delays[: entry_reads + 1]
    assert all(delay <= INTERVAL_MS / 1000 for delay in before_start), before_start
    # Once pending, the wait backs off: a later read waits longer than the first interval.
    assert max(delays[entry_reads + 1 :]) > INTERVAL_MS / 1000


@pytest.mark.parametrize(
    "module_name",
    ["archive", "unarchive"],
)
def test_sync_wait_holds_first_interval_until_pending(monkeypatch, module_name):
    descriptor = vars(sync_module.SyncSandboxInstance)[module_name]
    statuses = _statuses(descriptor._entry, sorted(descriptor._pending)[0], descriptor._target)
    delays: list[float] = []
    monkeypatch.setattr(sync_module, "get_sandbox", _fake_reads(statuses))
    monkeypatch.setattr(sync_module, "_unwrap_response", lambda response, _what: response)
    monkeypatch.setattr(sync_module, "_status_of", lambda sandbox: sandbox.status)
    monkeypatch.setattr(sync_module.time, "sleep", delays.append)

    result = descriptor._wait("sbx", 600_000, INTERVAL_MS)

    assert result.status == descriptor._target
    _check_delays(delays, 8)


@pytest.mark.parametrize(
    "module_name",
    ["archive", "unarchive"],
)
def test_async_wait_holds_first_interval_until_pending(monkeypatch, module_name):
    descriptor = vars(async_module.SandboxInstance)[module_name]
    statuses = _statuses(descriptor._entry, sorted(descriptor._pending)[0], descriptor._target)
    delays: list[float] = []
    read = _fake_reads(statuses)

    async def fake_get(*args, **kwargs):
        return read(*args, **kwargs)

    async def fake_sleep(delay):
        delays.append(delay)

    monkeypatch.setattr(async_module, "get_sandbox", fake_get)
    monkeypatch.setattr(async_module, "_unwrap_response", lambda response, _what: response)
    monkeypatch.setattr(async_module, "_status_of", lambda sandbox: sandbox.status)
    monkeypatch.setattr(async_module.asyncio, "sleep", fake_sleep)

    result = asyncio.run(descriptor._wait("sbx", 600_000, INTERVAL_MS))

    assert result.status == descriptor._target
    _check_delays(delays, 8)
