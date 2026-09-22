"""Shared process observation policy for synchronous and asynchronous clients."""

import math
import random
import time
from uuid import uuid4

from .client.models import ProcessResponse
from .client.types import Unset
from .transient_retry import is_transient_reset_error

TERMINAL_PROCESS_STATES = frozenset({"completed", "failed", "killed", "stopped"})


class ProcessObservationError(Exception):
    """The command's outcome could not be observed; the command may still run."""

    def __init__(self, identifier: str, last_observation: ProcessResponse | None, message: str):
        self.identifier = identifier
        self.last_observation = last_observation
        super().__init__(f"Process {identifier}: {message}")


class ProcessWaitTimeout(ProcessObservationError, TimeoutError):
    """The observation deadline expired, without cancelling the command."""


class ProcessExecutionError(Exception):
    """An execution request failed; recover by identifier, never replay the POST."""

    def __init__(self, identifier: str):
        self.identifier = identifier
        super().__init__(
            f"Process {identifier}: execution response unavailable; use get/wait/logs "
            "with this identifier to check the outcome before starting another command"
        )


def process_name(name: str | Unset | None) -> str:
    return name or f"process-{uuid4().hex}"


def retryable_observation(error: Exception) -> bool:
    if isinstance(error, TimeoutError):
        return True
    response = getattr(error, "response", None)
    return getattr(response, "status_code", None) in {
        408,
        429,
        500,
        502,
        503,
        504,
    } or is_transient_reset_error(error)


class ProcessWaitState:
    """One deadline and retry budget, with no nested read retries."""

    def __init__(self, identifier: str, max_wait: float, interval: float):
        if not math.isfinite(max_wait) or max_wait < 0:
            raise ValueError("max_wait must be finite and non-negative")
        if not math.isfinite(interval) or interval <= 0:
            raise ValueError("interval must be finite and positive")
        self.identifier = identifier
        self.deadline = time.monotonic() + max_wait / 1000
        self.interval = interval / 1000
        self.last_observation: ProcessResponse | None = None
        self.last_error: Exception | None = None
        self.failures = 0

    def remaining(self) -> float:
        remaining = self.deadline - time.monotonic()
        if remaining <= 0:
            raise ProcessWaitTimeout(
                self.identifier,
                self.last_observation,
                "Process did not finish in time; command was not cancelled",
            ) from self.last_error
        return remaining

    def observe(self, result: ProcessResponse) -> bool:
        self.last_observation = result
        self.last_error = None
        self.failures = 0
        if result.status in TERMINAL_PROCESS_STATES:
            return True
        if result.status != "running":
            raise ProcessObservationError(
                self.identifier, result, f"unrecognized process state: {result.status}"
            )
        return False

    def failed(self, error: Exception) -> None:
        if not retryable_observation(error):
            raise ProcessObservationError(
                self.identifier, self.last_observation, "could not retrieve status"
            ) from error
        self.last_error = error
        self.failures += 1

    def delay(self) -> float:
        backoff = min(0.2 * 2 ** min(self.failures - 1, 4), 2.0) if self.failures else self.interval
        if self.failures:
            backoff *= random.uniform(0.8, 1.2)
        return min(backoff, self.remaining())
