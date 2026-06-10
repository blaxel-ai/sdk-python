from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.volume_template import VolumeTemplate


T = TypeVar("T", bound="DeleteVolumeTemplateVersionResponse200")


@_attrs_define
class DeleteVolumeTemplateVersionResponse200:
    """
    Attributes:
        message (Union[Unset, str]):
        template (Union[Unset, VolumeTemplate]): Volume template for creating pre-configured volumes
    """

    message: Union[Unset, str] = UNSET
    template: Union[Unset, "VolumeTemplate"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        template: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.template
            and not isinstance(self.template, Unset)
            and not isinstance(self.template, dict)
        ):
            template = self.template.to_dict()
        elif self.template and isinstance(self.template, dict):
            template = self.template

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if message is not UNSET:
            field_dict["message"] = message
        if template is not UNSET:
            field_dict["template"] = template

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.volume_template import VolumeTemplate

        if not src_dict:
            return None
        d = src_dict.copy()
        message = d.pop("message", UNSET)

        _template = d.pop("template", UNSET)
        template: Union[Unset, VolumeTemplate]
        if isinstance(_template, Unset):
            template = UNSET
        else:
            template = VolumeTemplate.from_dict(_template)

        delete_volume_template_version_response_200 = cls(
            message=message,
            template=template,
        )

        delete_volume_template_version_response_200.additional_properties = d
        return delete_volume_template_version_response_200

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
