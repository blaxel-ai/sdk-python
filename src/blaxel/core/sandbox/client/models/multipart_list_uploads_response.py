from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filesystem_multipart_upload import FilesystemMultipartUpload


T = TypeVar("T", bound="MultipartListUploadsResponse")


@_attrs_define
class MultipartListUploadsResponse:
    """
    Attributes:
        uploads (Union[Unset, list['FilesystemMultipartUpload']]):
    """

    uploads: Union[Unset, list["FilesystemMultipartUpload"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uploads: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.uploads, Unset):
            uploads = []
            for uploads_item_data in self.uploads:
                if type(uploads_item_data) is dict:
                    uploads_item = uploads_item_data
                else:
                    uploads_item = uploads_item_data.to_dict()
                uploads.append(uploads_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uploads is not UNSET:
            field_dict["uploads"] = uploads

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.filesystem_multipart_upload import FilesystemMultipartUpload

        if not src_dict:
            return None
        d = src_dict.copy()
        uploads = []
        _uploads = d.pop("uploads", UNSET)
        for uploads_item_data in _uploads or []:
            uploads_item = FilesystemMultipartUpload.from_dict(uploads_item_data)

            uploads.append(uploads_item)

        multipart_list_uploads_response = cls(
            uploads=uploads,
        )

        multipart_list_uploads_response.additional_properties = d
        return multipart_list_uploads_response

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
