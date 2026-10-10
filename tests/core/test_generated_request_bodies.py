from io import BytesIO

from blaxel.core.sandbox.client.api.filesystem.put_filesystem_path import _get_kwargs
from blaxel.core.sandbox.client.models import FileRequest, PutFilesystemPathFilesBody
from blaxel.core.sandbox.client.types import File


def test_multi_body_endpoint_accepts_plain_dict_as_json():
    kwargs = _get_kwargs("tmp/a", body={"content": "hello"})

    assert kwargs["json"] == {"content": "hello"}
    assert kwargs["headers"]["Content-Type"] == "application/json"


def test_multi_body_endpoint_sends_model_as_json():
    kwargs = _get_kwargs("tmp/a", body=FileRequest(content="hello"))

    assert kwargs["json"] == {"content": "hello"}


def test_multi_body_endpoint_lets_httpx_set_multipart_boundary():
    body = PutFilesystemPathFilesBody(file=File(payload=BytesIO(b"hi")))

    kwargs = _get_kwargs("tmp/a", body=body)

    assert "files" in kwargs
    assert "Content-Type" not in kwargs["headers"]
