from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DriveSpec")


@_attrs_define
class DriveSpec:
    """Immutable drive configuration set at creation time

    Attributes:
        infrastructure_id (Union[Unset, str]): The internal infrastructure resource identifier for this drive (bucket
            name)
        region (Union[Unset, str]): Deployment region for the drive (e.g., us-pdx-1, eu-lon-1). Must match the region of
            resources it attaches to. Example: us-pdx-1.
        size (Union[Unset, int]): Optional size limit for the drive in GB. If not specified, drive has no size limit.
            Example: 100.
    """

    infrastructure_id: Union[Unset, str] = UNSET
    region: Union[Unset, str] = UNSET
    size: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        infrastructure_id = self.infrastructure_id

        region = self.region

        size = self.size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if infrastructure_id is not UNSET:
            field_dict["infrastructureId"] = infrastructure_id
        if region is not UNSET:
            field_dict["region"] = region
        if size is not UNSET:
            field_dict["size"] = size

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        infrastructure_id = d.pop("infrastructureId", d.pop("infrastructure_id", UNSET))

        region = d.pop("region", UNSET)

        size = d.pop("size", UNSET)

        drive_spec = cls(
            infrastructure_id=infrastructure_id,
            region=region,
            size=size,
        )

        drive_spec.additional_properties = d
        return drive_spec

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
