import pytest

from blaxel.core.sandbox.sync.filesystem import SyncSandboxFileSystem


def test_sync_multipart_upload_aborts_when_part_thread_fails():
    filesystem = object.__new__(SyncSandboxFileSystem)
    uploaded_parts = []
    aborted_uploads = []
    completed_parts = []

    filesystem._initiate_multipart_upload = lambda path, permissions="0644": {
        "uploadId": "upload-1"
    }

    def upload_part(upload_id, part_number, data):
        uploaded_parts.append(part_number)
        if part_number == 2:
            raise RuntimeError("part 2 failed")
        return {"partNumber": part_number, "etag": f"etag-{part_number}"}

    filesystem._upload_part = upload_part
    filesystem._abort_multipart_upload = lambda upload_id: aborted_uploads.append(upload_id)
    filesystem._complete_multipart_upload = lambda upload_id, parts: completed_parts.append(parts)

    with pytest.raises(RuntimeError, match="part 2 failed"):
        filesystem._upload_with_multipart("/tmp/large.bin", b"0" * (11 * 1024 * 1024))

    assert 2 in uploaded_parts
    assert aborted_uploads == ["upload-1"]
    assert completed_parts == []
