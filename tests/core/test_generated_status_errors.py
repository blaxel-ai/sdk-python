import httpx
import pytest

from blaxel.core.client import errors
from blaxel.core.client.api.drives import create_drive
from blaxel.core.client.api.volumes import create_volume
from blaxel.core.client.client import Client
from blaxel.core.client.models.drive import Drive
from blaxel.core.client.models.volume import Volume
from blaxel.core.sandbox.client import errors as sandbox_errors
from blaxel.core.sandbox.client.api.drive import get_drives_mount
from blaxel.core.sandbox.client.client import Client as SandboxClient


def _drive() -> Drive:
    return Drive(metadata={"name": "test-drive"}, spec={})  # type: ignore[arg-type]


def _volume() -> Volume:
    return Volume(metadata={"name": "test-volume"}, spec={"size": 1024})  # type: ignore[arg-type]


def _response(
    status_code: int,
    *,
    content: bytes,
    headers: dict[str, str] | None = None,
    path: str = "/drives",
) -> httpx.Response:
    return httpx.Response(
        status_code,
        content=content,
        headers=headers,
        request=httpx.Request("POST", f"https://api.blaxel.test{path}"),
    )


def test_drive_create_sync_raises_typed_conflict_without_raw_body() -> None:
    sensitive_body = (
        b'{"error":"Resource already exists: customer-drive-123",'
        b'"code":409,"message":"token=private-token /Users/alice/project"}'
    )

    def handler(_: httpx.Request) -> httpx.Response:
        return _response(409, content=sensitive_body)

    http_client = httpx.Client(
        base_url="https://api.blaxel.test",
        transport=httpx.MockTransport(handler),
    )
    client = Client(base_url="https://api.blaxel.test").set_httpx_client(http_client)

    with pytest.raises(errors.ConflictError) as exc_info:
        create_drive.sync(client=client, body=_drive())

    exc = exc_info.value
    assert isinstance(exc, errors.UnexpectedStatus)
    assert exc.status_code == 409
    assert exc.error_code is None
    assert exc.content == sensitive_body
    assert exc.body_preview.startswith("<response body:")
    assert str(exc) == "HTTP 409 Conflict"
    assert "customer-drive-123" not in str(exc)
    assert "private-token" not in str(exc)
    assert "/Users/alice" not in str(exc)


@pytest.mark.asyncio
async def test_volume_create_async_raises_typed_rate_limit_with_retry_after() -> None:
    async def handler(_: httpx.Request) -> httpx.Response:
        return _response(
            429,
            content=b"quota backend unavailable for customer@example.com",
            headers={"Content-Type": "text/plain", "Retry-After": "7"},
            path="/volumes",
        )

    transport = httpx.MockTransport(handler)
    client = Client(
        base_url="https://api.blaxel.test",
        httpx_args={"transport": transport},
    )

    with pytest.raises(errors.RateLimitError) as exc_info:
        await create_volume.asyncio(client=client, body=_volume())

    exc = exc_info.value
    assert isinstance(exc, errors.UnexpectedStatus)
    assert exc.status_code == 429
    assert exc.retry_after == "7"
    assert exc.retry_after_seconds == 7
    assert exc.retryable is True
    assert exc.error_code is None
    assert exc.body_preview.startswith("<response body:")
    assert str(exc) == "HTTP 429 Too Many Requests"
    assert "customer@example.com" not in str(exc)
    await client.get_async_httpx_client().aclose()


def test_typed_rate_limit_preserves_stable_error_metadata() -> None:
    error = errors.from_response(
        429,
        (
            b'{"error":{"code":"USAGE_LIMIT_EXCEEDED",'
            b'"message":"workspace private-workspace exhausted quota",'
            b'"retryable":false,"authorization":"Bearer private",'
            b'"retry_after_seconds":19}}'
        ),
    )

    assert isinstance(error, errors.RateLimitError)
    assert error.error_code == "USAGE_LIMIT_EXCEEDED"
    assert error.retryable is False
    assert error.retry_after == "19"
    assert error.retry_after_seconds == 19
    assert str(error) == "HTTP 429 Too Many Requests"
    assert error.error_code not in str(error)
    assert "private-workspace" not in str(error)
    assert "Bearer private" not in str(error)


def test_body_derived_code_is_metadata_only_not_exception_text() -> None:
    error = errors.from_response(
        409,
        b'{"error":{"code":"PRIVATE_WORKSPACE_SECRET","retryable":false}}',
    )

    assert isinstance(error, errors.ConflictError)
    assert error.error_code == "PRIVATE_WORKSPACE_SECRET"
    assert str(error) == "HTTP 409 Conflict"
    assert "PRIVATE_WORKSPACE_SECRET" not in str(error)


@pytest.mark.parametrize("status_code", [409, 429])
def test_typed_status_returns_none_when_raising_is_disabled(status_code: int) -> None:
    client = Client(
        base_url="https://api.blaxel.test",
        raise_on_unexpected_status=False,
    )
    response = _response(status_code, content=b"not json")

    assert create_drive._parse_response(client=client, response=response) is None


def test_unknown_status_retains_unexpected_status_type() -> None:
    client = Client(base_url="https://api.blaxel.test")
    response = _response(418, content=b"private teapot response")

    with pytest.raises(errors.UnexpectedStatus) as exc_info:
        create_drive._parse_response(client=client, response=response)

    assert type(exc_info.value) is errors.UnexpectedStatus
    assert str(exc_info.value) == "Unexpected HTTP status 418"
    assert "private teapot response" not in str(exc_info.value)


def test_invalid_retry_after_is_not_retained() -> None:
    error = errors.from_response(
        429,
        b"rate limited",
        {"Retry-After": "private-header-value"},
    )

    assert isinstance(error, errors.RateLimitError)
    assert error.retry_after is None

    boolean_retry_after = errors.from_response(429, b'{"retry_after":true}')
    assert isinstance(boolean_retry_after, errors.RateLimitError)
    assert boolean_retry_after.retry_after is None


def test_http_date_retry_after_is_preserved_without_becoming_seconds() -> None:
    retry_at = "Wed, 21 Oct 2037 07:28:00 GMT"

    error = errors.from_response(429, b"rate limited", {"rEtRy-AfTeR": retry_at})

    assert isinstance(error, errors.RateLimitError)
    assert error.retry_after == retry_at
    assert error.retry_after_seconds is None


def test_http_date_retry_after_drops_comments_and_normalizes_timezone() -> None:
    error = errors.from_response(
        429,
        b"rate limited",
        {"Retry-After": "Wed, 21 Oct 2037 00:28:00 -0700 (private@example.com)"},
    )

    assert isinstance(error, errors.RateLimitError)
    assert error.retry_after == "Wed, 21 Oct 2037 07:28:00 GMT"
    assert error.retry_after_seconds is None
    assert "private@example.com" not in error.retry_after


def test_body_summary_never_exposes_user_controlled_json_keys() -> None:
    error = errors.from_response(
        418,
        b'{"customer@example.com":{"private-token":"private-value"}}',
    )

    assert type(error) is errors.UnexpectedStatus
    assert error.body_preview.startswith("<response body:")
    assert str(error) == "Unexpected HTTP status 418"
    assert "customer@example.com" not in str(error)
    assert "private-token" not in str(error)
    assert "private-value" not in str(error)


def test_malformed_metadata_cannot_mask_rate_limit_error() -> None:
    oversized_integer = b'{"retry_after":' + (b"9" * 5_000) + b"}"

    error = errors.from_response(429, oversized_integer)

    assert isinstance(error, errors.RateLimitError)
    assert error.retry_after is None
    assert "999999" not in str(error)


def test_sandbox_generated_client_uses_the_same_typed_safe_errors() -> None:
    response = _response(
        409,
        content=b'{"error":"private mount path /mnt/customer"}',
        path="/drives/mount",
    )

    with pytest.raises(sandbox_errors.ConflictError) as exc_info:
        get_drives_mount._parse_response(
            client=SandboxClient(base_url="https://api.blaxel.test"),
            response=response,
        )

    assert isinstance(exc_info.value, sandbox_errors.UnexpectedStatus)
    assert "/mnt/customer" not in str(exc_info.value)
