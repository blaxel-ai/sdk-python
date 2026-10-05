"""Shared exceptions and the error shapes returned by Blaxel backends."""

import json
from collections.abc import Mapping, Sequence
from typing import Any, Literal, TypedDict, TypeGuard, TypeVar, Union, overload

import httpx

# Keep this list in sync with the TypeScript SDK. New backends may return other
# strings; BlaxelError.code deliberately accepts those as well as numeric codes.
BlaxelErrorCode = Literal[
    # Edge gateway
    "ROUTE_NOT_FOUND",
    "WORKLOAD_NOT_FOUND",
    "WORKSPACE_NOT_FOUND",
    "WORKLOAD_UNAVAILABLE",
    "WORKLOAD_FAILED",
    "ROUTING_UNAVAILABLE",
    "AUTHENTICATION_REQUIRED",
    "AUTHENTICATION_FAILED",
    "TOKEN_REVOKED",
    "FORBIDDEN",
    "BAD_REQUEST",
    "USAGE_LIMIT_EXCEEDED",
    "POLICY_VIOLATION",
    "UPSTREAM_CONNECT_FAILED",
    "UPSTREAM_CONNECT_TIMEOUT",
    "UPSTREAM_ERROR",
    "UPSTREAM_TIMEOUT",
    "GATEWAY_INTERNAL_ERROR",
    # Control-plane authentication
    "UNAUTHORIZED",
    "UNAUTHORIZED_WORKSPACE",
    "AUTHENTICATION_UNAVAILABLE",
    "WORKSPACE_REQUIRED",
    # Sandbox creation and fork
    "READ_FAILED",
    "PARSE_FAILED",
    "VALIDATION_FAILED",
    "VALIDATION_ERROR",
    "INVALID_INPUT",
    "INVALID_IMAGE",
    "IMAGE_NOT_FOUND",
    "UPLOAD_NOT_SUPPORTED",
    "UNSUPPORTED_GENERATION",
    "KERNEL_GENERATION_MISMATCH",
    "INVALID_PORTS",
    "INVALID_REGION",
    "REGION_MISMATCH",
    "INVALID_VOLUME",
    "INVALID_VOLUME_COUNT",
    "INVALID_VOLUME_REGION",
    "VOLUME_ALREADY_ATTACHED",
    "VOLUME_PROVIDER_MISMATCH",
    "VOLUME_NOT_FOUND",
    "ACCOUNT_NOT_FOUND",
    "SANDBOX_ALREADY_EXISTS",
    "SANDBOX_DELETION_IN_PROGRESS",
    "SANDBOX_DELETED",
    "VOLUME_DELETED",
    "CREATION_TIMEOUT",
    "QUOTA_EXCEEDED",
    "RATE_LIMIT_EXCEEDED",
    "WORKSPACE_RATE_LIMIT_EXCEEDED",
    "SERVICE_UNAVAILABLE",
    "DATABASE_ERROR",
    "LOCK_ACQUISITION_FAILED",
    "VOLUME_LOOKUP_FAILED",
    "BUILD_TRIGGER_ERROR",
    "PRESIGNED_URL_ERROR",
    "UPLOAD_UNAVAILABLE",
    "DEPLOYMENT_FAILED",
    "CLUSTER_GATEWAY_ERROR",
    "LOCKDOWN_ERROR",
    "PROXY_CONFIG_ERROR",
    "VALIDATED_DATA_ERROR",
    "WORKSPACE_DATA_MISSING",
    "CALLBACK_SEND_FAILED",
    "FORK_FAILED",
    "HANDLER_ERROR",
    "INTERNAL_ERROR",
    "UNKNOWN_ERROR",
]
BlaxelErrorCodeValue = Union[BlaxelErrorCode, str, int]


class BlaxelApiErrorBody(TypedDict):
    """Generic control-plane error; ``code`` is the numeric HTTP status."""

    error: str
    code: int


class _ActionErrorRequired(TypedDict):
    code: Union[BlaxelErrorCode, str]
    message: str
    status_code: int


class BlaxelActionErrorBody(_ActionErrorRequired, total=False):
    """Control-plane sandbox creation/fork error."""

    reason: str
    step: str
    workspace: str
    sandbox_name: str
    timestamp: str
    cause: str
    details: dict[str, Any]


class _PlatformErrorRequired(TypedDict):
    code: str
    message: str
    status: int


class _PlatformError(_PlatformErrorRequired, total=False):
    origin: Literal["platform"]
    retryable: bool
    dispatch_state: Literal["not_dispatched", "dispatched_unknown"]
    safe_to_retry_request: bool
    action: str
    do_not: str
    docs_url: str
    timestamp: str


class BlaxelPlatformErrorBody(TypedDict):
    """Error envelope returned by the edge gateway (and for revoked tokens)."""

    error: _PlatformError


class BlaxelSandboxApiErrorBody(TypedDict):
    """Sandbox API error (filesystem, process, etc.)."""

    error: str


_REQUEST_ID_HEADERS = ("x-cf-request-id", "x-amz-cf-id", "cf-ray")


def _read_header(headers: Mapping[str, str] | None, name: str) -> str | None:
    if headers is not None:
        for key, value in headers.items():
            if key.lower() == name and value:
                return value
    return None


def _decode_error_body(content: bytes) -> Any:
    try:
        return json.loads(content)
    except (UnicodeDecodeError, ValueError, RecursionError):
        return content.decode("utf-8", errors="replace")


def _response_snapshot(response: httpx.Response) -> httpx.Response:
    """Retain response diagnostics without retaining the authenticated request.

    Do not copy history, next_request, streams, or opaque transport extensions:
    they can point back to requests and their authorization headers. Content is
    already decoded, so restore the original headers only after construction to
    avoid decoding compressed content twice.
    """
    snapshot = httpx.Response(
        response.status_code,
        content=response.content,
        extensions={
            "reason_phrase": response.reason_phrase.encode("ascii", errors="replace"),
            "http_version": response.http_version.encode("ascii", errors="replace"),
        },
    )
    snapshot.headers = response.headers.copy()
    encoding = response.encoding
    if encoding is not None:
        snapshot.encoding = encoding
    return snapshot


def _body_metadata(body: Any) -> tuple[BlaxelErrorCodeValue | None, bool | None]:
    code = None
    retryable = None
    if isinstance(body, dict):
        nested = body.get("error")
        # Top-level code wins, just as it does in the TypeScript SDK.
        for source in (body, nested):
            if not isinstance(source, dict):
                continue
            candidate = source.get("code")
            if code is None and (
                (isinstance(candidate, str) and candidate)
                or (isinstance(candidate, int) and not isinstance(candidate, bool))
            ):
                code = candidate
        for source in (nested, body):
            if isinstance(source, dict) and isinstance(source.get("retryable"), bool):
                retryable = source["retryable"]
                break
    return code, retryable


class BlaxelError(Exception):
    """Common base for Blaxel API errors, without wrapping network/validation failures.

    Existing subclasses keep their exception messages and legacy attributes.
    ``code`` may be a known code, a newer string, or a numeric HTTP status. A
    missing status/code/request ID/retry hint is represented by ``None``.
    """

    status: int | None
    code: BlaxelErrorCodeValue | None
    message: str
    request_id: str | None
    retryable: bool | None
    body: Any
    response: httpx.Response | None

    def __init__(
        self,
        message: str,
        *,
        status: int | None = None,
        code: BlaxelErrorCodeValue | None = None,
        body: Any = None,
        response: httpx.Response | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        super().__init__(message)
        if response is not None:
            if status is None:
                status = response.status_code
            if body is None:
                body = _decode_error_body(response.content)
            headers = response.headers
        parsed_code, retryable = _body_metadata(body)
        self.status = status
        self.code = code if code is not None else parsed_code
        if self.code is None:
            self.code = _read_header(headers, "x-blaxel-error-code")
        self.message = str(message)
        self.request_id = next(
            (value for name in _REQUEST_ID_HEADERS if (value := _read_header(headers, name))),
            None,
        )
        self.retryable = retryable
        self.body = body
        self.response = _response_snapshot(response) if response is not None else None


ErrorT = TypeVar("ErrorT", bound=BlaxelError)


@overload
def is_blaxel_error(
    err: ErrorT,
    code: BlaxelErrorCodeValue | Sequence[BlaxelErrorCodeValue] | None = None,
) -> TypeGuard[ErrorT]: ...


@overload
def is_blaxel_error(
    err: object,
    code: BlaxelErrorCodeValue | Sequence[BlaxelErrorCodeValue] | None = None,
) -> TypeGuard[BlaxelError]: ...


def is_blaxel_error(
    err: object,
    code: BlaxelErrorCodeValue | Sequence[BlaxelErrorCodeValue] | None = None,
) -> TypeGuard[BlaxelError]:
    """Check for a BlaxelError, optionally matching one code or a sequence of codes."""
    if not isinstance(err, BlaxelError):
        return False
    if code is None:
        return True
    return err.code == code if isinstance(code, str | int) else err.code in code


class _APIError(BlaxelError):
    """Shared implementation for resource wrappers, retaining their old constructors."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        code: BlaxelErrorCodeValue | None = None,
        *,
        error: Any = None,
        body: Any = None,
        response: httpx.Response | None = None,
    ) -> None:
        if error is not None:
            response = response if response is not None else getattr(error, "_response", None)
            if body is None and response is None:
                body = error.to_dict()
        super().__init__(message, status=status_code, code=code, body=body, response=response)
        self.status_code = status_code
        # This field already existed on resource wrappers, including None.
        # Wire metadata must not replace the caller's legacy value.
        self.code = code


__all__ = [
    "BlaxelError",
    "BlaxelErrorCode",
    "BlaxelErrorCodeValue",
    "BlaxelApiErrorBody",
    "BlaxelActionErrorBody",
    "BlaxelPlatformErrorBody",
    "BlaxelSandboxApiErrorBody",
    "is_blaxel_error",
]
