from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.apply_edit_request import ApplyEditRequest
from ...models.apply_edit_response import ApplyEditResponse
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    path: str,
    *,
    body: ApplyEditRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/codegen/fastapply/{path}",
    }

    if type(body) is dict:
        _body = body
    else:
        _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union[ApplyEditResponse, ErrorResponse] | None:
    if response.status_code == 200:
        response_200 = ApplyEditResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422
    if response.status_code == 503:
        response_503 = ErrorResponse.from_dict(response.json())

        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[ApplyEditResponse, ErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    path: str,
    *,
    client: Client,
    body: ApplyEditRequest,
) -> Response[Union[ApplyEditResponse, ErrorResponse]]:
    r"""Apply code edit

     Uses the configured LLM provider (Relace or Morph) to apply a code edit to the original content.

    To use this endpoint as an agent tool, follow these guidelines:

    Use this tool to make an edit to an existing file. This will be read by a less intelligent model,
    which will quickly apply the edit. You should make it clear what the edit is, while also minimizing
    the unchanged code you write.

    When writing the edit, you should specify each edit in sequence, with the special comment \"// ...
    existing code ...\" to represent unchanged code in between edited lines.

    Example format:
    // ... existing code ...
    FIRST_EDIT
    // ... existing code ...
    SECOND_EDIT
    // ... existing code ...
    THIRD_EDIT
    // ... existing code ...

    You should still bias towards repeating as few lines of the original file as possible to convey the
    change. But, each edit should contain minimally sufficient context of unchanged lines around the
    code you're editing to resolve ambiguity.

    DO NOT omit spans of pre-existing code (or comments) without using the \"// ... existing code ...\"
    comment to indicate its absence. If you omit the existing code comment, the model may inadvertently
    delete these lines.

    If you plan on deleting a section, you must provide context before and after to delete it. If the
    initial code is \"Block 1\nBlock 2\nBlock 3\", and you want to remove Block 2, you would output \"//
    ... existing code ...\nBlock 1\nBlock 3\n// ... existing code ...\".

    Make sure it is clear what the edit should be, and where it should be applied. Make edits to a file
    in a single edit_file call instead of multiple edit_file calls to the same file. The apply model can
    handle many distinct edits at once.

    Args:
        path (str):
        body (ApplyEditRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApplyEditResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        path=path,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    path: str,
    *,
    client: Client,
    body: ApplyEditRequest,
) -> Union[ApplyEditResponse, ErrorResponse] | None:
    r"""Apply code edit

     Uses the configured LLM provider (Relace or Morph) to apply a code edit to the original content.

    To use this endpoint as an agent tool, follow these guidelines:

    Use this tool to make an edit to an existing file. This will be read by a less intelligent model,
    which will quickly apply the edit. You should make it clear what the edit is, while also minimizing
    the unchanged code you write.

    When writing the edit, you should specify each edit in sequence, with the special comment \"// ...
    existing code ...\" to represent unchanged code in between edited lines.

    Example format:
    // ... existing code ...
    FIRST_EDIT
    // ... existing code ...
    SECOND_EDIT
    // ... existing code ...
    THIRD_EDIT
    // ... existing code ...

    You should still bias towards repeating as few lines of the original file as possible to convey the
    change. But, each edit should contain minimally sufficient context of unchanged lines around the
    code you're editing to resolve ambiguity.

    DO NOT omit spans of pre-existing code (or comments) without using the \"// ... existing code ...\"
    comment to indicate its absence. If you omit the existing code comment, the model may inadvertently
    delete these lines.

    If you plan on deleting a section, you must provide context before and after to delete it. If the
    initial code is \"Block 1\nBlock 2\nBlock 3\", and you want to remove Block 2, you would output \"//
    ... existing code ...\nBlock 1\nBlock 3\n// ... existing code ...\".

    Make sure it is clear what the edit should be, and where it should be applied. Make edits to a file
    in a single edit_file call instead of multiple edit_file calls to the same file. The apply model can
    handle many distinct edits at once.

    Args:
        path (str):
        body (ApplyEditRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApplyEditResponse, ErrorResponse]
    """

    return sync_detailed(
        path=path,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    path: str,
    *,
    client: Client,
    body: ApplyEditRequest,
) -> Response[Union[ApplyEditResponse, ErrorResponse]]:
    r"""Apply code edit

     Uses the configured LLM provider (Relace or Morph) to apply a code edit to the original content.

    To use this endpoint as an agent tool, follow these guidelines:

    Use this tool to make an edit to an existing file. This will be read by a less intelligent model,
    which will quickly apply the edit. You should make it clear what the edit is, while also minimizing
    the unchanged code you write.

    When writing the edit, you should specify each edit in sequence, with the special comment \"// ...
    existing code ...\" to represent unchanged code in between edited lines.

    Example format:
    // ... existing code ...
    FIRST_EDIT
    // ... existing code ...
    SECOND_EDIT
    // ... existing code ...
    THIRD_EDIT
    // ... existing code ...

    You should still bias towards repeating as few lines of the original file as possible to convey the
    change. But, each edit should contain minimally sufficient context of unchanged lines around the
    code you're editing to resolve ambiguity.

    DO NOT omit spans of pre-existing code (or comments) without using the \"// ... existing code ...\"
    comment to indicate its absence. If you omit the existing code comment, the model may inadvertently
    delete these lines.

    If you plan on deleting a section, you must provide context before and after to delete it. If the
    initial code is \"Block 1\nBlock 2\nBlock 3\", and you want to remove Block 2, you would output \"//
    ... existing code ...\nBlock 1\nBlock 3\n// ... existing code ...\".

    Make sure it is clear what the edit should be, and where it should be applied. Make edits to a file
    in a single edit_file call instead of multiple edit_file calls to the same file. The apply model can
    handle many distinct edits at once.

    Args:
        path (str):
        body (ApplyEditRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApplyEditResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        path=path,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    path: str,
    *,
    client: Client,
    body: ApplyEditRequest,
) -> Union[ApplyEditResponse, ErrorResponse] | None:
    r"""Apply code edit

     Uses the configured LLM provider (Relace or Morph) to apply a code edit to the original content.

    To use this endpoint as an agent tool, follow these guidelines:

    Use this tool to make an edit to an existing file. This will be read by a less intelligent model,
    which will quickly apply the edit. You should make it clear what the edit is, while also minimizing
    the unchanged code you write.

    When writing the edit, you should specify each edit in sequence, with the special comment \"// ...
    existing code ...\" to represent unchanged code in between edited lines.

    Example format:
    // ... existing code ...
    FIRST_EDIT
    // ... existing code ...
    SECOND_EDIT
    // ... existing code ...
    THIRD_EDIT
    // ... existing code ...

    You should still bias towards repeating as few lines of the original file as possible to convey the
    change. But, each edit should contain minimally sufficient context of unchanged lines around the
    code you're editing to resolve ambiguity.

    DO NOT omit spans of pre-existing code (or comments) without using the \"// ... existing code ...\"
    comment to indicate its absence. If you omit the existing code comment, the model may inadvertently
    delete these lines.

    If you plan on deleting a section, you must provide context before and after to delete it. If the
    initial code is \"Block 1\nBlock 2\nBlock 3\", and you want to remove Block 2, you would output \"//
    ... existing code ...\nBlock 1\nBlock 3\n// ... existing code ...\".

    Make sure it is clear what the edit should be, and where it should be applied. Make edits to a file
    in a single edit_file call instead of multiple edit_file calls to the same file. The apply model can
    handle many distinct edits at once.

    Args:
        path (str):
        body (ApplyEditRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApplyEditResponse, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            path=path,
            client=client,
            body=body,
        )
    ).parsed
