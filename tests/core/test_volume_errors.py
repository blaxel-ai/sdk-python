"""Control-plane errors must not be returned as if they were volumes.

``delete_volume`` returns ``Union[Error, Volume] | None``. The delete helpers used
to return that untouched, so a failed delete looked like a success to any caller
that did not inspect the return value.
"""

from unittest.mock import AsyncMock, patch

import pytest

from blaxel.core.client.models import Metadata, Volume, VolumeSpec
from blaxel.core.client.models.error import Error
from blaxel.core.volume.volume import SyncVolumeInstance, VolumeAPIError, VolumeInstance


def api_error(code=403, message="insufficient permissions"):
    return Error(error="FORBIDDEN", code=code, message=message)


@pytest.mark.asyncio
async def test_delete_raises_on_error_response():
    with patch("blaxel.core.volume.volume.delete_volume", new_callable=AsyncMock) as mock_delete:
        mock_delete.return_value = api_error(code=500, message="control plane exploded")

        with pytest.raises(VolumeAPIError, match="control plane exploded") as excinfo:
            await VolumeInstance.delete("my-volume")

    assert excinfo.value.status_code == 500


@pytest.mark.asyncio
async def test_delete_returns_payload_on_success():
    with patch("blaxel.core.volume.volume.delete_volume", new_callable=AsyncMock) as mock_delete:
        mock_delete.return_value = Volume(
            metadata=Metadata(name="my-volume"), spec=VolumeSpec(size=1024)
        )

        result = await VolumeInstance.delete("my-volume")

        assert result.metadata.name == "my-volume"


def test_sync_delete_raises_on_error_response():
    with patch("blaxel.core.volume.volume.delete_volume_sync") as mock_delete:
        mock_delete.return_value = api_error(code=404, message="volume not found")

        with pytest.raises(VolumeAPIError, match="volume not found"):
            SyncVolumeInstance.delete("my-volume")
