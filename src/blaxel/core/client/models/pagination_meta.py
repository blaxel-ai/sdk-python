from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PaginationMeta")


@_attrs_define
class PaginationMeta:
    """Pagination metadata returned alongside a page of listing results. Always present on listing endpoints starting with
    API version 2026-04-28.

        Attributes:
            has_more (Union[Unset, bool]): True when more pages are available beyond the current one.
            next_cursor (Union[Unset, str]): Opaque cursor to pass back as the `cursor` query param for the next page. Empty
                when there are no more pages.
            total (Union[Unset, int]): Total number of items in the workspace, ignoring the current page's filters. Lets the
                UI render "page X of Y" without walking the cursor chain. Computed from the hash-only metadata.workspace GSI
                count, so search (`q`) does not narrow it.
    """

    has_more: Union[Unset, bool] = UNSET
    next_cursor: Union[Unset, str] = UNSET
    total: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        has_more = self.has_more

        next_cursor = self.next_cursor

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if has_more is not UNSET:
            field_dict["hasMore"] = has_more
        if next_cursor is not UNSET:
            field_dict["nextCursor"] = next_cursor
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        has_more = d.pop("hasMore", d.pop("has_more", UNSET))

        next_cursor = d.pop("nextCursor", d.pop("next_cursor", UNSET))

        total = d.pop("total", UNSET)

        pagination_meta = cls(
            has_more=has_more,
            next_cursor=next_cursor,
            total=total,
        )

        pagination_meta.additional_properties = d
        return pagination_meta

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
