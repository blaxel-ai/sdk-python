from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.volume_template_state_status import VolumeTemplateStateStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="VolumeTemplateState")


@_attrs_define
class VolumeTemplateState:
    """Volume template state

    Attributes:
        last_version_uploaded_at (Union[Unset, str]): Timestamp of last version upload
        latest_version (Union[Unset, str]): Current/latest S3 version ID
        status (Union[Unset, VolumeTemplateStateStatus]): Status of the volume template (created, ready, error)
        version_count (Union[Unset, int]): Total number of versions for this template
    """

    last_version_uploaded_at: Union[Unset, str] = UNSET
    latest_version: Union[Unset, str] = UNSET
    status: Union[Unset, VolumeTemplateStateStatus] = UNSET
    version_count: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        last_version_uploaded_at = self.last_version_uploaded_at

        latest_version = self.latest_version

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        version_count = self.version_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if last_version_uploaded_at is not UNSET:
            field_dict["lastVersionUploadedAt"] = last_version_uploaded_at
        if latest_version is not UNSET:
            field_dict["latestVersion"] = latest_version
        if status is not UNSET:
            field_dict["status"] = status
        if version_count is not UNSET:
            field_dict["versionCount"] = version_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        last_version_uploaded_at = d.pop(
            "lastVersionUploadedAt", d.pop("last_version_uploaded_at", UNSET)
        )

        latest_version = d.pop("latestVersion", d.pop("latest_version", UNSET))

        _status = d.pop("status", UNSET)
        status: Union[Unset, VolumeTemplateStateStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = VolumeTemplateStateStatus(_status)

        version_count = d.pop("versionCount", d.pop("version_count", UNSET))

        volume_template_state = cls(
            last_version_uploaded_at=last_version_uploaded_at,
            latest_version=latest_version,
            status=status,
            version_count=version_count,
        )

        volume_template_state.additional_properties = d
        return volume_template_state

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
