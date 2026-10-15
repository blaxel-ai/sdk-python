from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ChangelogEntry")


@_attrs_define
class ChangelogEntry:
    """Changelog entry shown in the controlplane UI.

    Attributes:
        content (Union[Unset, str]): Markdown body for the changelog entry.
        date (Union[Unset, str]): Release date for the changelog entry in YYYY-MM-DD format. Example: 2026-07-07.
        title (Union[Unset, str]): Changelog entry title. Example: New sandbox scheduling controls.
    """

    content: Union[Unset, str] = UNSET
    date: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content = self.content

        date = self.date

        title = self.title

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if content is not UNSET:
            field_dict["content"] = content
        if date is not UNSET:
            field_dict["date"] = date
        if title is not UNSET:
            field_dict["title"] = title

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        content = d.pop("content", UNSET)

        date = d.pop("date", UNSET)

        title = d.pop("title", UNSET)

        changelog_entry = cls(
            content=content,
            date=date,
            title=title,
        )

        changelog_entry.additional_properties = d
        return changelog_entry

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
