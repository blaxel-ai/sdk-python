from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.process_upgrade_state import ProcessUpgradeState
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpgradeStatus")


@_attrs_define
class UpgradeStatus:
    """
    Attributes:
        status (ProcessUpgradeState):
        step (str): Current/last step (none, starting, download, validate, replace, completed, skipped) Example:
            download.
        version (str): Version being upgraded to Example: latest.
        binary_path (Union[Unset, str]): Path to downloaded binary Example: /tmp/sandbox-api-new.
        bytes_downloaded (Union[Unset, int]): Bytes downloaded Example: 25034936.
        download_url (Union[Unset, str]): URL used for download Example: https://github.com/....
        error (Union[Unset, str]): Error message if failed Example: Failed to download binary.
        last_attempt (Union[Unset, str]): When the upgrade was attempted
    """

    status: ProcessUpgradeState
    step: str
    version: str
    binary_path: Union[Unset, str] = UNSET
    bytes_downloaded: Union[Unset, int] = UNSET
    download_url: Union[Unset, str] = UNSET
    error: Union[Unset, str] = UNSET
    last_attempt: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        step = self.step

        version = self.version

        binary_path = self.binary_path

        bytes_downloaded = self.bytes_downloaded

        download_url = self.download_url

        error = self.error

        last_attempt = self.last_attempt

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "step": step,
                "version": version,
            }
        )
        if binary_path is not UNSET:
            field_dict["binaryPath"] = binary_path
        if bytes_downloaded is not UNSET:
            field_dict["bytesDownloaded"] = bytes_downloaded
        if download_url is not UNSET:
            field_dict["downloadUrl"] = download_url
        if error is not UNSET:
            field_dict["error"] = error
        if last_attempt is not UNSET:
            field_dict["lastAttempt"] = last_attempt

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        status = ProcessUpgradeState(d.pop("status"))

        step = d.pop("step")

        version = d.pop("version")

        binary_path = d.pop("binaryPath", d.pop("binary_path", UNSET))

        bytes_downloaded = d.pop("bytesDownloaded", d.pop("bytes_downloaded", UNSET))

        download_url = d.pop("downloadUrl", d.pop("download_url", UNSET))

        error = d.pop("error", UNSET)

        last_attempt = d.pop("lastAttempt", d.pop("last_attempt", UNSET))

        upgrade_status = cls(
            status=status,
            step=step,
            version=version,
            binary_path=binary_path,
            bytes_downloaded=bytes_downloaded,
            download_url=download_url,
            error=error,
            last_attempt=last_attempt,
        )

        upgrade_status.additional_properties = d
        return upgrade_status

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
