"""Status waits back off with jitter instead of polling at a fixed interval."""

import pytest

from blaxel.core.common import polling
from blaxel.core.common.polling import POLL_MAX_INTERVAL_SECONDS, poll_delay_seconds
from blaxel.core.image import image as image_module
from blaxel.core.image.image import ImageInstance


def test_delay_starts_at_interval_and_grows_to_the_cap():
    for attempt, target in [(1, 3.0), (2, 4.5), (3, 6.75), (20, POLL_MAX_INTERVAL_SECONDS)]:
        for _ in range(50):
            delay = poll_delay_seconds(attempt, 3.0)
            assert target / 2 <= delay <= target


def test_delays_are_jittered():
    assert len({poll_delay_seconds(5, 2.0) for _ in range(20)}) > 1


def test_interval_above_the_cap_is_kept_and_zero_means_no_wait():
    assert 30 <= poll_delay_seconds(10, 60.0) <= 60
    assert poll_delay_seconds(3, 0) == 0
    assert poll_delay_seconds(10_000, 2.0) <= POLL_MAX_INTERVAL_SECONDS


def test_build_wait_backs_off(monkeypatch: pytest.MonkeyPatch):
    statuses = iter(["DEPLOYED"] + ["BUILDING"] * 8 + ["DEPLOYED"])
    sleeps: list[float] = []
    monkeypatch.setattr(
        ImageInstance, "_get_sandbox_status_sync", lambda self, name: next(statuses)
    )
    monkeypatch.setattr(image_module.time, "sleep", sleeps.append)
    monkeypatch.setattr(polling.random, "uniform", lambda low, high: high)

    image = ImageInstance.from_registry("python:3.12-slim")
    assert image._wait_for_deployment_sync("build", timeout=900) == "DEPLOYED"

    assert sleeps[0] == 3.0
    assert sleeps == sorted(sleeps)
    assert sleeps[-1] == POLL_MAX_INTERVAL_SECONDS


def test_build_wait_keeps_first_interval_until_the_build_starts(monkeypatch: pytest.MonkeyPatch):
    statuses = iter(["DEPLOYED"] * 6 + ["BUILDING", "BUILDING", "DEPLOYED"])
    sleeps: list[float] = []
    monkeypatch.setattr(
        ImageInstance, "_get_sandbox_status_sync", lambda self, name: next(statuses)
    )
    monkeypatch.setattr(image_module.time, "sleep", sleeps.append)
    monkeypatch.setattr(polling.random, "uniform", lambda low, high: high)

    image = ImageInstance.from_registry("python:3.12-slim")
    assert image._wait_for_deployment_sync("build", timeout=900) == "DEPLOYED"

    assert sleeps[:6] == [3.0] * 6
    assert sleeps[6:] == [3.0, 4.5]
