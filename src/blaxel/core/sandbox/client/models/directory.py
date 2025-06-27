from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.file import File
    from ..models.subdirectory import Subdirectory


T = TypeVar("T", bound="Directory")


@_attrs_define
class Directory:
    """
    Attributes:
        files (list['File']):
        name (str):
        path (str):
        subdirectories (list['Subdirectory']): @name Subdirectories
    """

    files: list["File"]
    name: str
    path: str
    subdirectories: list["Subdirectory"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        files = []
        for files_item_data in self.files:
            if type(files_item_data) is dict:
                files_item = files_item_data
            else:
                files_item = files_item_data.to_dict()
            files.append(files_item)

        name = self.name

        path = self.path

        subdirectories = []
        for subdirectories_item_data in self.subdirectories:
            if type(subdirectories_item_data) is dict:
                subdirectories_item = subdirectories_item_data
            else:
                subdirectories_item = subdirectories_item_data.to_dict()
            subdirectories.append(subdirectories_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "files": files,
                "name": name,
                "path": path,
                "subdirectories": subdirectories,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.file import File
        from ..models.subdirectory import Subdirectory

        if not src_dict:
            return None
        d = src_dict.copy()
        files = []
        _files = d.pop("files")
        for files_item_data in _files:
            files_item = File.from_dict(files_item_data)

            files.append(files_item)

        name = d.pop("name")

        path = d.pop("path")

        subdirectories = []
        _subdirectories = d.pop("subdirectories")
        for subdirectories_item_data in _subdirectories:
            subdirectories_item = Subdirectory.from_dict(subdirectories_item_data)

            subdirectories.append(subdirectories_item)

        directory = cls(
            files=files,
            name=name,
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
