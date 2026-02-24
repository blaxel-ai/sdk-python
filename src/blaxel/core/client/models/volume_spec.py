from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="VolumeSpec")


@_attrs_define
class VolumeSpec:
    """Immutable volume configuration set at creation time (size and region cannot be changed after creation)

    Attributes:
        infrastructure_id (Union[Unset, str]): The internal infrastructure resource identifier for this volume
        region (Union[Unset, str]): Deployment region for the volume (e.g., us-pdx-1, eu-lon-1). Must match the region
            of sandboxes it attaches to. Example: us-pdx-1.
        size (Union[Unset, int]): Storage capacity in megabytes. Can be increased after creation but not decreased.
            Example: 1024.
        template (Union[Unset, str]): Volume template to initialize from, with optional revision (e.g., "mytemplate:1"
            or "mytemplate:latest") Example: mytemplate:latest.
    """

    infrastructure_id: Union[Unset, str] = UNSET
    region: Union[Unset, str] = UNSET
    size: Union[Unset, int] = UNSET
    template: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        infrastructure_id = self.infrastructure_id

        region = self.region

        size = self.size

        template = self.template

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if infrastructure_id is not UNSET:
            field_dict["infrastructureId"] = infrastructure_id
        if region is not UNSET:
            field_dict["region"] = region
        if size is not UNSET:
            field_dict["size"] = size
        if template is not UNSET:
            field_dict["template"] = template

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        infrastructure_id = d.pop("infrastructureId", d.pop("infrastructure_id", UNSET))

        region = d.pop("region", UNSET)

        size = d.pop("size", UNSET)

        template = d.pop("template", UNSET)

        volume_spec = cls(
            infrastructure_id=infrastructure_id,
            region=region,
            size=size,
            template=template,
        )

        volume_spec.additional_properties = d
        return volume_spec

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
