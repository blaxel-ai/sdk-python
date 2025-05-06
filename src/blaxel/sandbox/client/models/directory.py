from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.file import File
    from ..models.subdirectory import Subdirectory


T = TypeVar("T", bound="Directory")


@_attrs_define
class Directory:
    """
    Attributes:
        files (Union[Unset, list['File']]):
        path (Union[Unset, str]):
        subdirectories (Union[Unset, list['Subdirectory']]): @name Subdirectories
    """

    files: Union[Unset, list["File"]] = UNSET
    path: Union[Unset, str] = UNSET
    subdirectories: Union[Unset, list["Subdirectory"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        files: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.files, Unset):
            files = []
            for files_item_data in self.files:
                if type(files_item_data) == dict:
                    files_item = files_item_data
                else:
                    files_item = files_item_data.to_dict()
                files.append(files_item)

        path = self.path

        subdirectories: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.subdirectories, Unset):
            subdirectories = []
            for subdirectories_item_data in self.subdirectories:
                if type(subdirectories_item_data) == dict:
                    subdirectories_item = subdirectories_item_data
                else:
                    subdirectories_item = subdirectories_item_data.to_dict()
                subdirectories.append(subdirectories_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if files is not UNSET:
            field_dict["files"] = files
        if path is not UNSET:
            field_dict["path"] = path
        if subdirectories is not UNSET:
            field_dict["subdirectories"] = subdirectories

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.file import File
        from ..models.subdirectory import Subdirectory

        if not src_dict:
            return None
        d = src_dict.copy()
        files = []
        _files = d.pop("files", UNSET)
        for files_item_data in _files or []:
            files_item = File.from_dict(files_item_data)

            files.append(files_item)

        path = d.pop("path", UNSET)

        subdirectories = []
        _subdirectories = d.pop("subdirectories", UNSET)
        for subdirectories_item_data in _subdirectories or []:
            subdirectories_item = Subdirectory.from_dict(subdirectories_item_data)

            subdirectories.append(subdirectories_item)

        directory = cls(
            files=files,
            path=path,
            subdirectories=subdirectories,
        )

        directory.additional_properties = d
        return directory

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
