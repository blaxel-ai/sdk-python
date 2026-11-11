"""Delays between the status reads of a long wait (sandbox archive, image build).

A wait that reads the control plane at a fixed interval sends the same load for
its whole length, and many clients that started together read in step. Each
wait here starts at its interval, grows it by half after every read up to
``POLL_MAX_INTERVAL_SECONDS``, and draws each delay at random between half and
all of that value, so a few hundred waits at once stay well under the API's
per-client request limits.
"""

import random

POLL_MAX_INTERVAL_SECONDS = 30.0
POLL_GROWTH = 1.5
# 1.5 ** 64 is far past any cap; bounding the exponent avoids a float overflow
# on a wait that runs for a very long time.
_MAX_EXPONENT = 64


def poll_delay_seconds(
    attempt: int,
    initial_seconds: float,
    max_seconds: float = POLL_MAX_INTERVAL_SECONDS,
) -> float:
    """Return the delay before status read number ``attempt`` (1-based) of a wait.

    The delay grows from ``initial_seconds`` by half per read up to
    ``max_seconds`` (or ``initial_seconds`` when that is larger), and is drawn
    between half and all of that value.
    """
    if initial_seconds <= 0:
        return 0.0
    ceiling = max(max_seconds, initial_seconds)
    exponent = min(max(attempt - 1, 0), _MAX_EXPONENT)
    target = min(initial_seconds * POLL_GROWTH**exponent, ceiling)
    return random.uniform(target / 2, target)
