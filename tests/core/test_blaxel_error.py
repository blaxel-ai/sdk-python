"""Compatibility and metadata tests for the shared public API error contract."""

from typing import get_args
from unittest.mock import patch

import httpx
import pytest

from blaxel.core import (
    ApplicationAPIError,
    BlaxelError,
    BlaxelErrorCode,
    DriveAPIError,
    ResponseError,
    SandboxAPIError,
    SandboxCreationTimeoutError,
    SandboxInstance,
    SnapshotAPIError,
    SyncSandboxInstance,
    VolumeAPIError,
    is_blaxel_error,
)
from blaxel.core.client import errors
from blaxel.core.client.api.compute import create_sandbox, get_sandbox
from blaxel.core.client.client import Client
from blaxel.core.client.models.error import Error
from blaxel.core.client.models.sandbox_error import SandboxError
from blaxel.core.sandbox.client import errors as sandbox_errors
from blaxel.core.sandbox.client.api.process import get_process_identifier
from blaxel.core.sandbox.client.client import Client as SandboxClient
from blaxel.core.sandbox.client.models.error_response import ErrorResponse

GENERIC = {"code": 404, "error": "Sandbox not found"}
ACTION = {
    "code": "SANDBOX_ALREADY_EXISTS",
    "message": "Sandbox sbx already exists",
    "status_code": 409,
    "reason": "CREATION_IN_PROGRESS",
}
PLATFORM = {
    "error": {
        "code": "WORKLOAD_UNAVAILABLE",
        "message": "The workload is not available.",
        "status": 404,
        "retryable": True,
        "origin": "platform",
    }
}
CONFIG = {"name": "sbx", "region": "us-pdx-1"}


@pytest.mark.parametrize(
    "body,code,retryable",
    [
        (GENERIC, 404, None),
        (ACTION, "SANDBOX_ALREADY_EXISTS", None),
        (PLATFORM, "WORKLOAD_UNAVAILABLE", True),
    ],
)
def test_three_wire_shapes(body, code, retryable):
    response = httpx.Response(404, json=body, headers={"X-Cf-Request-Id": "req-1"})
    error = BlaxelError("unchanged message", response=response)
    assert error.status == 404
    assert error.code == code
    assert error.retryable is retryable
    assert error.request_id == "req-1"
    assert error.message == str(error) == "unchanged message"
    assert error.body == body
    assert error.response is response


@pytest.mark.parametrize(
    "headers,expected",
    [
        ({"X-Cf-Request-Id": "cf", "X-Amz-Cf-Id": "amz", "CF-Ray": "ray"}, "cf"),
        ({"X-Amz-Cf-Id": "amz", "CF-Ray": "ray"}, "amz"),
        ({"CF-Ray": "ray"}, "ray"),
        ({"X-Cf-Request-Id": "", "CF-Ray": "ray"}, "ray"),
        ({}, None),
    ],
)
def test_header_fallback_and_request_id_precedence(headers, expected):
    error = BlaxelError(
        "denied",
        response=httpx.Response(
            401,
            json={"error": "denied"},
            headers={**headers, "X-Blaxel-Error-Code": "TOKEN_REVOKED"},
        ),
    )
    assert error.code == "TOKEN_REVOKED"
    assert error.request_id == expected


def test_explicit_values_and_top_level_body_code_win():
    response = httpx.Response(503, headers={"X-Blaxel-Error-Code": "TOKEN_REVOKED"})
    error = BlaxelError("x", status=400, code="INVALID_IMAGE", body=PLATFORM, response=response)
    assert error.status == 400
    assert error.code == "INVALID_IMAGE"
    assert error.retryable is True
    assert BlaxelError("x", body={"code": 409, **PLATFORM}).code == 409


@pytest.mark.parametrize(
    "body", [None, [], "text", {"code": True}, {"code": ""}, {"error": {"retryable": "true"}}]
)
def test_missing_or_malformed_metadata(body):
    error = BlaxelError("x", body=body)
    assert error.status is None
    assert error.code is None
    assert error.retryable is None
    assert error.request_id is None
    assert error.response is None


def test_unknown_codes_and_predicate():
    error = BlaxelError("x", body={"code": "future-code"})
    assert is_blaxel_error(error)
    assert is_blaxel_error(error, "future-code")
    assert is_blaxel_error(error, ["INVALID_IMAGE", "future-code"])
    assert not is_blaxel_error(error, "INVALID_IMAGE")
    assert not is_blaxel_error(error, [])
    assert is_blaxel_error(BlaxelError("x", body=GENERIC), 404)
    assert not is_blaxel_error(BlaxelError("x", body=GENERIC), "404")
    for other in (None, "x", ValueError("x"), {"code": "future-code"}):
        assert not is_blaxel_error(other)


@pytest.mark.parametrize(
    "cls", [SandboxAPIError, DriveAPIError, VolumeAPIError, SnapshotAPIError, ApplicationAPIError]
)
def test_resource_error_legacy_constructor_and_fields(cls):
    error = cls("old message", 404, "old error text")
    assert error.status == error.status_code == 404
    assert error.code == "old error text"
    assert error.message == str(error) == "old message"
    assert error.args == ("old message",)
    assert isinstance(error, BlaxelError)


@pytest.mark.parametrize(
    "cls", [SandboxAPIError, DriveAPIError, VolumeAPIError, SnapshotAPIError, ApplicationAPIError]
)
def test_resource_error_keeps_raw_body_headers_and_legacy_code(cls):
    response = httpx.Response(404, json=GENERIC, headers={"X-Amz-Cf-Id": "req-2"})
    parsed = Error.from_dict(GENERIC)
    assert parsed is not None
    errors.retain_response(parsed, response)
    error = cls("old message", 404, parsed.error, error=parsed)
    assert error.code == "Sandbox not found"  # compatibility, not numeric 404
    assert error.body == GENERIC
    assert error.response is response
    assert error.request_id == "req-2"
    assert parsed.to_dict() == GENERIC
    assert "_response" not in repr(parsed)
    assert parsed == Error.from_dict(GENERIC)


def test_missing_legacy_status_code_is_not_replaced_by_http_status():
    response = httpx.Response(404, json={"error": "missing"})
    parsed = Error.from_dict({"error": "missing"})
    assert parsed is not None
    errors.retain_response(parsed, response)
    error = SandboxAPIError("missing", error=parsed)
    assert error.status_code is None
    assert error.status == 404


def test_legacy_wrapper_keeps_unvalidated_generic_model_fields():
    # The old generated generic model does not validate the error field. Keep
    # its legacy wrapper fields/args intact rather than normalize them here.
    parsed = Error.from_dict(PLATFORM)
    assert parsed is not None
    response = httpx.Response(404, json=PLATFORM)
    errors.retain_response(parsed, response)
    error = SandboxAPIError(parsed.error, code=parsed.error, error=parsed)
    assert error.code is parsed.error
    assert error.args == (parsed.error,)
    assert error.message == str(error)
    assert error.body == PLATFORM
    assert error.status == 404


def test_response_error_preserves_data_message_and_unmodified_body():
    response = httpx.Response(404, json=PLATFORM, headers={"CF-Ray": "ray"})
    error = ResponseError(response)
    assert isinstance(error, BlaxelError)
    assert is_blaxel_error(error, "WORKLOAD_UNAVAILABLE")
    assert error.retryable is True
    assert error.request_id == "ray"
    assert error.body == PLATFORM
    assert "statusText" not in error.body
    assert error.data == {**PLATFORM, "status": 404, "statusText": "Not Found"}
    assert str(error) == str(error.data)
    assert error.message == str(error)
    assert error.error is None
    assert error.response is response


@pytest.mark.parametrize(
    "content,expected_body",
    [
        (b"upstream connect error", "upstream connect error"),
        (b"", ""),
    ],
)
def test_response_error_non_object_body(content, expected_body):
    error = ResponseError(httpx.Response(502, content=content))
    assert error.body == expected_body
    assert error.status == 502
    assert error.code is None


@pytest.mark.parametrize("module", [errors, sandbox_errors])
@pytest.mark.parametrize(
    "status,cls_name", [(409, "ConflictError"), (429, "RateLimitError"), (418, "UnexpectedStatus")]
)
def test_generated_status_errors_keep_safe_messages_and_gain_metadata(module, status, cls_name):
    response = httpx.Response(status, json=PLATFORM, headers={"X-Cf-Request-Id": "safe-id"})
    error = module.from_response(status, response.content, response.headers, response=response)
    assert isinstance(error, getattr(module, cls_name))
    assert isinstance(error, module.UnexpectedStatus)
    assert is_blaxel_error(error, "WORKLOAD_UNAVAILABLE")
    assert error.status == error.status_code == status
    assert error.content == response.content
    assert error.body == PLATFORM
    assert error.response is response
    assert error.request_id == "safe-id"
    assert "workload" not in str(error)
    assert error.message == str(error)


def test_creation_timeout_keeps_fields_and_gains_response_metadata():
    body = {"code": "CREATION_TIMEOUT", "message": "too slow"}
    response = httpx.Response(408, json=body, headers={"X-Cf-Request-Id": "timeout-id"})
    error = SandboxCreationTimeoutError("sbx", 10, body, response=response)
    assert is_blaxel_error(error, "CREATION_TIMEOUT")
    assert error.status == error.status_code == 408
    assert error.data is body
    assert error.body is body
    assert error.sandbox_name == "sbx"
    assert error.timeout == 10
    assert error.request_id == "timeout-id"
    assert (
        str(error) == "Sandbox sbx was not ready within 10s; the creation was cancelled. too slow"
    )


@pytest.mark.parametrize("sync", [True, False])
@pytest.mark.asyncio
async def test_high_level_creation_metadata_sync_and_async(sync):
    response = httpx.Response(409, json=ACTION, headers={"X-Cf-Request-Id": "creation-id"})
    transport = httpx.MockTransport(lambda _: response)
    client = Client(base_url="https://api.test", httpx_args={"transport": transport})
    target = "blaxel.core.sandbox.sync.sandbox" if sync else "blaxel.core.sandbox.default.sandbox"
    with patch(f"{target}.client", client):
        with pytest.raises(SandboxAPIError) as caught:
            if sync:
                SyncSandboxInstance.create(CONFIG)
            else:
                await SandboxInstance.create(CONFIG)
    error = caught.value
    assert is_blaxel_error(error, "SANDBOX_ALREADY_EXISTS")
    assert error.status == 409
    assert error.body == ACTION
    assert error.request_id == "creation-id"
    assert error.response is response
    assert error.message == ACTION["message"]
    if sync:
        client.get_httpx_client().close()
    else:
        await client.get_async_httpx_client().aclose()


@pytest.mark.parametrize("sync", [True, False])
@pytest.mark.asyncio
async def test_modeled_error_return_values_are_unchanged(sync):
    transport = httpx.MockTransport(lambda _: httpx.Response(404, json=GENERIC))
    client = Client(base_url="https://api.test", httpx_args={"transport": transport})
    result = (
        get_sandbox.sync("missing", client=client)
        if sync
        else await get_sandbox.asyncio("missing", client=client)
    )
    assert isinstance(result, Error)
    assert not is_blaxel_error(result)
    assert result.code == 404
    assert result.to_dict() == GENERIC
    if sync:
        client.get_httpx_client().close()
    else:
        await client.get_async_httpx_client().aclose()


def test_modeled_creation_and_sandbox_error_values_are_unchanged():
    result = create_sandbox._parse_response(
        client=Client(base_url="https://api.test"), response=httpx.Response(409, json=ACTION)
    )
    assert isinstance(result, SandboxError)
    assert result.to_dict() == ACTION
    result2 = get_process_identifier._parse_response(
        client=SandboxClient(base_url="https://sandbox.test"),
        response=httpx.Response(404, json={"error": "missing"}),
    )
    assert isinstance(result2, ErrorResponse)
    assert result2.to_dict() == {"error": "missing"}


def test_generated_schema_mismatch_behavior_is_unchanged():
    # Intercepting this parse failure would introduce a different error policy.
    with pytest.raises(KeyError):
        create_sandbox._parse_response(
            client=Client(base_url="https://api.test"),
            response=httpx.Response(401, json=PLATFORM),
        )


@pytest.mark.parametrize("sync", [True, False])
@pytest.mark.asyncio
async def test_network_errors_are_not_wrapped(sync):
    def fail(request):
        raise httpx.ConnectError("offline", request=request)

    client = Client(
        base_url="https://api.test", httpx_args={"transport": httpx.MockTransport(fail)}
    )
    with pytest.raises(httpx.ConnectError):
        if sync:
            get_sandbox.sync("missing", client=client)
        else:
            await get_sandbox.asyncio("missing", client=client)
    if sync:
        client.get_httpx_client().close()
    else:
        await client.get_async_httpx_client().aclose()


@pytest.mark.parametrize("module", [errors, sandbox_errors])
def test_status_header_metadata_keeps_legacy_retry_fields(module):
    error = module.from_response(
        429,
        b"unavailable",
        {"X-Blaxel-Error-Code": "TOKEN_REVOKED", "Retry-After": "7", "CF-Ray": "ray"},
    )
    assert is_blaxel_error(error, "TOKEN_REVOKED")
    assert error.error_code is None  # existing body-only, stable-code attribute
    assert error.retryable is True
    assert error.retry_after_seconds == 7
    assert error.request_id == "ray"
    assert error.body == "unavailable"
    assert str(error) == "HTTP 429 Too Many Requests"


@pytest.mark.parametrize("module", [errors, sandbox_errors])
def test_legacy_retry_metadata_inspection_stays_bounded(module):
    content = b'{"retryable":true,"padding":"' + b"x" * (64 * 1024) + b'"}'
    error = module.from_response(429, content)
    assert error.retryable is None
    assert error.body["retryable"] is True


@pytest.mark.parametrize("content", [b"[1, 2]", b"null"])
def test_response_error_unsupported_json_body_behavior_is_unchanged(content):
    with pytest.raises(TypeError):
        ResponseError(httpx.Response(502, content=content))


@pytest.mark.parametrize("sync", [True, False])
@pytest.mark.asyncio
async def test_creation_timeout_keeps_response_headers_sync_and_async(sync):
    body = {"code": "CREATION_TIMEOUT", "message": "too slow"}
    response = httpx.Response(408, json=body, headers={"X-Cf-Request-Id": "deadline-id"})
    client = Client(
        base_url="https://api.test",
        httpx_args={"transport": httpx.MockTransport(lambda _: response)},
    )
    target = "blaxel.core.sandbox.sync.sandbox" if sync else "blaxel.core.sandbox.default.sandbox"
    with patch(f"{target}.client", client):
        with pytest.raises(SandboxCreationTimeoutError) as caught:
            if sync:
                SyncSandboxInstance.create(CONFIG)
            else:
                await SandboxInstance.create(CONFIG)
    error = caught.value
    assert error.request_id == "deadline-id"
    assert error.body == error.data == body
    assert error.response is response
    assert error.__cause__ is not None
    if sync:
        client.get_httpx_client().close()
    else:
        await client.get_async_httpx_client().aclose()


def test_known_code_literal_matches_typescript_contract():
    # Exact union from TypeScript c057cff, including forward-compatibility gaps
    # deliberately excluded (generic sandbox/process error messages are not codes).
    expected = """
    ROUTE_NOT_FOUND WORKLOAD_NOT_FOUND WORKSPACE_NOT_FOUND WORKLOAD_UNAVAILABLE
    WORKLOAD_FAILED ROUTING_UNAVAILABLE AUTHENTICATION_REQUIRED AUTHENTICATION_FAILED
    TOKEN_REVOKED FORBIDDEN BAD_REQUEST USAGE_LIMIT_EXCEEDED POLICY_VIOLATION
    UPSTREAM_CONNECT_FAILED UPSTREAM_CONNECT_TIMEOUT UPSTREAM_ERROR UPSTREAM_TIMEOUT
    GATEWAY_INTERNAL_ERROR UNAUTHORIZED UNAUTHORIZED_WORKSPACE AUTHENTICATION_UNAVAILABLE
    WORKSPACE_REQUIRED READ_FAILED PARSE_FAILED VALIDATION_FAILED VALIDATION_ERROR
    INVALID_INPUT INVALID_IMAGE IMAGE_NOT_FOUND UPLOAD_NOT_SUPPORTED UNSUPPORTED_GENERATION
    KERNEL_GENERATION_MISMATCH INVALID_PORTS INVALID_REGION REGION_MISMATCH INVALID_VOLUME
    INVALID_VOLUME_COUNT INVALID_VOLUME_REGION VOLUME_ALREADY_ATTACHED VOLUME_PROVIDER_MISMATCH
    VOLUME_NOT_FOUND ACCOUNT_NOT_FOUND SANDBOX_ALREADY_EXISTS SANDBOX_DELETION_IN_PROGRESS
    SANDBOX_DELETED VOLUME_DELETED CREATION_TIMEOUT QUOTA_EXCEEDED RATE_LIMIT_EXCEEDED
    WORKSPACE_RATE_LIMIT_EXCEEDED SERVICE_UNAVAILABLE DATABASE_ERROR LOCK_ACQUISITION_FAILED
    VOLUME_LOOKUP_FAILED BUILD_TRIGGER_ERROR PRESIGNED_URL_ERROR UPLOAD_UNAVAILABLE
    DEPLOYMENT_FAILED CLUSTER_GATEWAY_ERROR LOCKDOWN_ERROR PROXY_CONFIG_ERROR
    VALIDATED_DATA_ERROR WORKSPACE_DATA_MISSING CALLBACK_SEND_FAILED FORK_FAILED
    HANDLER_ERROR INTERNAL_ERROR UNKNOWN_ERROR
    """.split()
    assert set(get_args(BlaxelErrorCode)) == set(expected)
