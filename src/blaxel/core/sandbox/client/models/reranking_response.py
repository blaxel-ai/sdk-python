from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ranked_file import RankedFile


T = TypeVar("T", bound="RerankingResponse")


@_attrs_define
class RerankingResponse:
    """
    Attributes:
        files (Union[Unset, list['RankedFile']]):
        message (Union[Unset, str]):  Example: Found 5 relevant files.
        success (Union[Unset, bool]):  Example: True.
    """

    files: Union[Unset, list["RankedFile"]] = UNSET
    message: Union[Unset, str] = UNSET
    success: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        files: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.files, Unset):
            files = []
            for files_item_data in self.files:
                if type(files_item_data) is dict:
                    files_item = files_item_data
                else:
                    files_item = files_item_data.to_dict()
                files.append(files_item)

        message = self.message

        success = self.success

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if files is not UNSET:
            field_dict["files"] = files
        if message is not UNSET:
            field_dict["message"] = message
        if success is not UNSET:
            field_dict["success"] = success

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.ranked_file import RankedFile

        if not src_dict:
            return None
        d = src_dict.copy()
        files = []
        _files = d.pop("files", UNSET)
        for files_item_data in _files or []:
            files_item = RankedFile.from_dict(files_item_data)

            files.append(files_item)

        message = d.pop("message", UNSET)

        success = d.pop("success", UNSET)

        reranking_response = cls(
            files=files,
            message=message,
            success=success,
        )

        reranking_response.additional_properties = d
        return reranking_response

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
