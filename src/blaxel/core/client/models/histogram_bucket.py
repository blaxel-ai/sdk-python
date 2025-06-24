from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="HistogramBucket")


@_attrs_define
class HistogramBucket:
    """Histogram bucket

    Attributes:
        count (Union[Unset, int]): Count
        end (Union[Unset, float]): End
        start (Union[Unset, float]): Start
    """

    count: Union[Unset, int] = UNSET
    end: Union[Unset, float] = UNSET
    start: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        end = self.end

        start = self.start

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if count is not UNSET:
            field_dict["count"] = count
        if end is not UNSET:
            field_dict["end"] = end
        if start is not UNSET:
            field_dict["start"] = start

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        count = d.pop("count", UNSET)

        end = d.pop("end", UNSET)

        start = d.pop("start", UNSET)

        histogram_bucket = cls(
            count=count,
            end=end,
            start=start,
        )

        histogram_bucket.additional_properties = d
        return histogram_bucket

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
