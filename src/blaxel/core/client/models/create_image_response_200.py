from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateImageResponse200")


@_attrs_define
class CreateImageResponse200:
    """
    Attributes:
        image (Union[Unset, str]): The registered image reference (only present when image was provided in request)
        message (Union[Unset, str]): Status message
        name (Union[Unset, str]): Name of the image
        resource_type (Union[Unset, str]): Resource type
    """

    image: Union[Unset, str] = UNSET
    message: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    resource_type: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        image = self.image

        message = self.message

        name = self.name

        resource_type = self.resource_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if image is not UNSET:
            field_dict["image"] = image
        if message is not UNSET:
            field_dict["message"] = message
        if name is not UNSET:
            field_dict["name"] = name
        if resource_type is not UNSET:
            field_dict["resourceType"] = resource_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        image = d.pop("image", UNSET)

        message = d.pop("message", UNSET)

        name = d.pop("name", UNSET)

        resource_type = d.pop("resourceType", d.pop("resource_type", UNSET))

        create_image_response_200 = cls(
            image=image,
            message=message,
            name=name,
            resource_type=resource_type,
        )

        create_image_response_200.additional_properties = d
        return create_image_response_200

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
