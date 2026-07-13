from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.changelog_entry import ChangelogEntry


T = TypeVar("T", bound="ChangelogResponse")


@_attrs_define
class ChangelogResponse:
    """Latest changelog entries shown in the controlplane UI.

    Attributes:
        entries (Union[Unset, list['ChangelogEntry']]): Latest changelog entries, newest first.
    """

    entries: Union[Unset, list["ChangelogEntry"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        entries: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.entries, Unset):
            entries = []
            for entries_item_data in self.entries:
                if type(entries_item_data) is dict:
                    entries_item = entries_item_data
                else:
                    entries_item = entries_item_data.to_dict()
                entries.append(entries_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if entries is not UNSET:
            field_dict["entries"] = entries

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.changelog_entry import ChangelogEntry

        if not src_dict:
            return None
        d = src_dict.copy()
        entries = []
        _entries = d.pop("entries", UNSET)
        for entries_item_data in _entries or []:
            entries_item = ChangelogEntry.from_dict(entries_item_data)

            entries.append(entries_item)

        changelog_response = cls(
            entries=entries,
        )

        changelog_response.additional_properties = d
        return changelog_response

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
