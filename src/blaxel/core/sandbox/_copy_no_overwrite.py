"""Shared by the async and sync ``cp(..., no_overwrite=True)``: one sandbox API copy request.

The sandbox API creates every entry exclusively and answers 409 ``FILE_ALREADY_EXISTS``
when the final target exists. Requests are not retried: a copy may have created
entries before a connection reset.
"""

from typing import Any, Callable

import httpx

from .types import CopyResponse

COPY_PATH = "/filesystem-copy"


def _copy_body(source: str, destination: str) -> dict[str, Any]:
    if not source or not destination:
        raise ValueError("source and destination must be nonempty paths")
    return {"source": source, "destination": destination, "noOverwrite": True}


def _copy_result(
    response: httpx.Response,
    source: str,
    destination: str,
    handle_response_error: Callable[[httpx.Response], None],
) -> CopyResponse:
    try:
        error = response.json() if response.content else None
    except ValueError:
        error = None
    code = error.get("code") if isinstance(error, dict) else None
    if response.status_code == 409 and code == "FILE_ALREADY_EXISTS":
        raise FileExistsError(
            f"Could not copy {source} to {destination}: destination already exists"
        )
    if response.status_code == 404 and not isinstance(error, dict):
        # An older sandbox API has no copy endpoint. Never fall back to an overwriting copy.
        raise RuntimeError(
            "cp with no_overwrite needs a newer sandbox API: this sandbox has no "
            "/filesystem-copy endpoint; update its image"
        )
    handle_response_error(response)
    return CopyResponse(message="Files copied", source=source, destination=destination)
