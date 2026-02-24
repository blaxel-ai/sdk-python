from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.image_metadata import ImageMetadata
    from ..models.image_spec import ImageSpec


T = TypeVar("T", bound="Image")


@_attrs_define
class Image:
    """
    Attributes:
        metadata (ImageMetadata):
        spec (ImageSpec):
    """

    metadata: "ImageMetadata"
    spec: "ImageSpec"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        if type(self.metadata) is dict:
            metadata = self.metadata
        else:
            metadata = self.metadata.to_dict()

        if type(self.spec) is dict:
            spec = self.spec
        else:
            spec = self.spec.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metadata": metadata,
                "spec": spec,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.image_metadata import ImageMetadata
        from ..models.image_spec import ImageSpec

        if not src_dict:
            return None
        d = src_dict.copy()
        metadata = ImageMetadata.from_dict(d.pop("metadata"))

        spec = ImageSpec.from_dict(d.pop("spec"))

        image = cls(
            metadata=metadata,
            spec=spec,
        )

        image.additional_properties = d
        return image

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
