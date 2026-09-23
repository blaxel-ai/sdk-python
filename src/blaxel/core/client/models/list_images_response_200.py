from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.image_summary import ImageSummary
    from ..models.pagination_meta import PaginationMeta


T = TypeVar("T", bound="ListImagesResponse200")


@_attrs_define
class ListImagesResponse200:
    """
    Attributes:
        data (list['ImageSummary']):
        meta (PaginationMeta): Pagination metadata returned alongside a page of listing results. Always present on
            listing endpoints starting with API version 2026-04-28.
    """

    data: list["ImageSummary"]
    meta: "PaginationMeta"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        data = []
        for data_item_data in self.data:
            if type(data_item_data) is dict:
                data_item = data_item_data
            else:
                data_item = data_item_data.to_dict()
            data.append(data_item)

        if type(self.meta) is dict:
            meta = self.meta
        else:
            meta = self.meta.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "meta": meta,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.image_summary import ImageSummary
        from ..models.pagination_meta import PaginationMeta

        if not src_dict:
            return None
        d = src_dict.copy()
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = ImageSummary.from_dict(data_item_data)

            data.append(data_item)

        meta = PaginationMeta.from_dict(d.pop("meta"))

        list_images_response_200 = cls(
            data=data,
            meta=meta,
        )

        list_images_response_200.additional_properties = d
        return list_images_response_200

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
