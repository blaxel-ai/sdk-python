from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.image_tag import ImageTag


T = TypeVar("T", bound="ImageSpec")


@_attrs_define
class ImageSpec:
    """
    Attributes:
        size (Union[Unset, int]): The size of the image in bytes.
        tags (Union[Unset, list['ImageTag']]): List of tags available for this image.
    """

    size: Union[Unset, int] = UNSET
    tags: Union[Unset, list["ImageTag"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        size = self.size

        tags: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = []
            for tags_item_data in self.tags:
                if type(tags_item_data) is dict:
                    tags_item = tags_item_data
                else:
                    tags_item = tags_item_data.to_dict()
                tags.append(tags_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if size is not UNSET:
            field_dict["size"] = size
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.image_tag import ImageTag

        if not src_dict:
            return None
        d = src_dict.copy()
        size = d.pop("size", UNSET)

        tags = []
        _tags = d.pop("tags", UNSET)
        for tags_item_data in _tags or []:
            tags_item = ImageTag.from_dict(tags_item_data)

            tags.append(tags_item)

        image_spec = cls(
            size=size,
            tags=tags,
        )

        image_spec.additional_properties = d
        return image_spec

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
