"""
Response interceptor that enhances authentication error messages (401/403)
with a link to the authentication documentation.
"""

import json
import logging

import httpx

logger = logging.getLogger(__name__)

DOCUMENTATION_URL = "For more information on authentication, visit: https://docs.blaxel.ai/sdk-reference/introduction#how-authentication-works"


def authentication_error_interceptor_sync(response: httpx.Response) -> None:
    """
    Intercepts HTTP responses and adds authentication documentation
    to 401/403 error responses (synchronous version)
    """
    # Only process authentication errors (401/403)
    if response.status_code not in (401, 403):
        return

    try:
        # Read the response body if not already read
        response.read()
        body_text = response.text

        # Try to parse as JSON
        try:
            original_error = json.loads(body_text)

            # Create enhanced error with authentication documentation
            auth_error = {
                **original_error,
                "documentation": DOCUMENTATION_URL,
            }

            enhanced_body = json.dumps(auth_error)
        except json.JSONDecodeError:
            # If not JSON, just append the documentation as text
            enhanced_body = f"{body_text}\n{DOCUMENTATION_URL}"

        # Update the response with the enhanced body
        response._content = enhanced_body.encode("utf-8")

    except Exception as error:
        # If anything fails, log the error and leave the response unchanged
        logger.error("Error processing authentication error response: %s", error)


async def authentication_error_interceptor_async(
    response: httpx.Response,
) -> None:
    """
    Intercepts HTTP responses and adds authentication documentation
    to 401/403 error responses (asynchronous version)
    """
    # Only process authentication errors (401/403)
    if response.status_code not in (401, 403):
        return

    try:
        # Read the response body if not already read
        await response.aread()
        body_text = response.text

        # Try to parse as JSON
        try:
            original_error = json.loads(body_text)

            # Create enhanced error with authentication documentation
            auth_error = {
                **original_error,
                "documentation": DOCUMENTATION_URL,
            }

            enhanced_body = json.dumps(auth_error)
        except json.JSONDecodeError:
            # If not JSON, just append the documentation as text
            enhanced_body = f"{body_text}\n{DOCUMENTATION_URL}"

        # Update the response with the enhanced body
        response._content = enhanced_body.encode("utf-8")

    except Exception as error:
        # If anything fails, log the error and leave the response unchanged
        logger.error("Error processing authentication error response: %s", error)


response_interceptors_sync = [
    authentication_error_interceptor_sync,
]

response_interceptors_async = [
    authentication_error_interceptor_async,
]
