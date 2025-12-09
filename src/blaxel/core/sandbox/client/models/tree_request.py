from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tree_request_files import TreeRequestFiles


T = TypeVar("T", bound="TreeRequest")


@_attrs_define
class TreeRequest:
    """
    Attributes:
        files (Union[Unset, TreeRequestFiles]):  Example: {'"dir/file2.txt"': '"content2"}', '{"file1.txt"':
            '"content1"'}.
    """

    files: Union[Unset, "TreeRequestFiles"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        files: Union[Unset, dict[str, Any]] = UNSET
        if self.files and not isinstance(self.files, Unset) and not isinstance(self.files, dict):
            files = self.files.to_dict()
        elif self.files and isinstance(self.files, dict):
            files = self.files

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if files is not UNSET:
            field_dict["files"] = files

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.tree_request_files import TreeRequestFiles

        if not src_dict:
            return None
        d = src_dict.copy()
        _files = d.pop("files", UNSET)
        files: Union[Unset, TreeRequestFiles]
        if isinstance(_files, Unset):
            files = UNSET
        else:
            files = TreeRequestFiles.from_dict(_files)

        tree_request = cls(
            files=files,
        )

        tree_request.additional_properties = d
        return tree_request

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
