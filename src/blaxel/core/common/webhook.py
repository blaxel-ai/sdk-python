"""Webhook signature verification for async-sidecar callbacks."""

import hashlib
import hmac
import time
from typing import Protocol


class RequestLike(Protocol):
    """Protocol for request-like objects with body and headers."""

    @property
    def body(self) -> bytes:
        """Raw request body as bytes."""
        ...

    @property
    def headers(self) -> dict[str, str]:
        """Request headers as dictionary."""
        ...


class AsyncSidecarCallback:
    """Callback payload from async-sidecar."""

    def __init__(
        self,
        status_code: int,
        response_body: str,
        response_length: int,
        timestamp: int,
    ):
        self.status_code = status_code
        self.response_body = response_body
        self.response_length = response_length
        self.timestamp = timestamp


def verify_webhook_signature(
    body: bytes | str,
    signature: str,
    secret: str,
    timestamp: str | None = None,
    max_age: int = 300,
) -> bool:
    """
    Verify the HMAC-SHA256 signature of a webhook callback from async-sidecar.

    Args:
        body: The raw request body (bytes or string)
        signature: The X-Blaxel-Signature header value (format: "sha256=<hex_digest>")
        secret: The secret key used to sign the webhook (same as CALLBACK_SECRET in async-sidecar)
        timestamp: Optional X-Blaxel-Timestamp header value for replay attack prevention
        max_age: Maximum age of the webhook in seconds (default: 300 = 5 minutes)

    Returns:
        True if the signature is valid, False otherwise

    Example:
        ```python
        from blaxel.core import verify_webhook_signature
        from flask import Flask, request

        app = Flask(__name__)

        @app.route('/webhook', methods=['POST'])
        def webhook():
            is_valid = verify_webhook_signature(
                body=request.get_data(),
                signature=request.headers.get('X-Blaxel-Signature', ''),
                secret='your-callback-secret'
            )

            if not is_valid:
                return {'error': 'Invalid signature'}, 401

            data = request.json
            # Process callback...
            return {'received': True}
        ```
    """
    if not body or not signature or not secret:
        return False

    try:
        # Verify timestamp if provided (prevents replay attacks)
        if timestamp:
            request_time = int(timestamp)
            current_time = int(time.time())
            age = abs(current_time - request_time)

            if age > max_age:
                return False

        # Convert body to bytes if string
        body_bytes = body.encode("utf-8") if isinstance(body, str) else body

        # Extract hex signature from "sha256=<hex>" format
        expected_signature = signature.replace("sha256=", "")

        # Compute HMAC-SHA256 signature
        computed_signature = hmac.new(
            secret.encode("utf-8"), body_bytes, hashlib.sha256
        ).hexdigest()

        # Timing-safe comparison to prevent timing attacks
        return hmac.compare_digest(expected_signature, computed_signature)

    except (ValueError, TypeError):
        # Invalid signature format or other error
        return False


def verify_webhook_from_request(
    request: RequestLike,
    secret: str,
    max_age: int = 300,
) -> bool:
    """
    Helper to verify webhook from a request object (Flask, FastAPI, etc.).

    Args:
        request: Request object with `body` and `headers` attributes
        secret: The callback secret
        max_age: Optional maximum age in seconds (default: 300)

    Returns:
        True if the signature is valid, False otherwise

    Example with Flask:
        ```python
        from blaxel.core import verify_webhook_from_request
        from flask import Flask, request

        app = Flask(__name__)

        @app.route('/webhook', methods=['POST'])
        def webhook():
            if not verify_webhook_from_request(request, 'your-callback-secret'):
                return {'error': 'Invalid signature'}, 401

            data = request.json
            print(f"Received callback: {data}")
            return {'received': True}
        ```

    Example with FastAPI:
        ```python
        from blaxel.core import verify_webhook_signature
        from fastapi import FastAPI, Request, HTTPException

        app = FastAPI()

        @app.post('/webhook')
        async def webhook(request: Request):
            body = await request.body()
            signature = request.headers.get('x-blaxel-signature', '')

            if not verify_webhook_signature(body, signature, 'your-callback-secret'):
                raise HTTPException(status_code=401, detail='Invalid signature')

            data = await request.json()
            return {'received': True}
        ```
    """
    signature = request.headers.get("x-blaxel-signature", "")
    timestamp = request.headers.get("x-blaxel-timestamp")

    if not signature:
        return False

    return verify_webhook_signature(
        body=request.body,
        signature=signature,
        secret=secret,
        timestamp=timestamp,
        max_age=max_age,
    )


__all__ = [
    "verify_webhook_signature",
    "verify_webhook_from_request",
    "AsyncSidecarCallback",
    "RequestLike",
]
