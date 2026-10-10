from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateImageBody")


@_attrs_define
class CreateImageBody:
    """
    Attributes:
        name (str): Name of the image to build
        resource_type (str): Resource type (agent, function, sandbox, job)
        generation (Union[Unset, str]): Runtime generation (e.g., mk3). Defaults to mk3 if not specified.
        image (Union[Unset, str]): A pre-built Docker image reference (e.g., docker.io/myorg/myimage:latest). When
            provided, the build step is skipped and the image is used directly as the source for the resource runtime.
    """

    name: str
    resource_type: str
    generation: Union[Unset, str] = UNSET
    image: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        resource_type = self.resource_type

        generation = self.generation

        image = self.image

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "resourceType": resource_type,
            }
        )
        if generation is not UNSET:
            field_dict["generation"] = generation
        if image is not UNSET:
            field_dict["image"] = image

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        name = d.pop("name")

        resource_type = d.pop("resourceType") if "resourceType" in d else d.pop("resource_type")

        generation = d.pop("generation", UNSET)

        image = d.pop("image", UNSET)

        create_image_body = cls(
            name=name,
            resource_type=resource_type,
            generation=generation,
            image=image,
        )

        create_image_body.additional_properties = d
        return create_image_body

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
