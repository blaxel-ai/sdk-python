from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LastNRequestsMetric")


@_attrs_define
class LastNRequestsMetric:
    """Last N requests

    Attributes:
        date (Union[Unset, str]): Timestamp
        workload_type (Union[Unset, str]): Workload type
        workspace (Union[Unset, str]): Workspace
    """

    date: Union[Unset, str] = UNSET
    workload_type: Union[Unset, str] = UNSET
    workspace: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date = self.date

        workload_type = self.workload_type

        workspace = self.workspace

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if date is not UNSET:
            field_dict["date"] = date
        if workload_type is not UNSET:
            field_dict["workloadType"] = workload_type
        if workspace is not UNSET:
            field_dict["workspace"] = workspace

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        date = d.pop("date", UNSET)

        workload_type = d.pop("workloadType", UNSET)

        workspace = d.pop("workspace", UNSET)

        last_n_requests_metric = cls(
            date=date,
            workload_type=workload_type,
            workspace=workspace,
        )

        last_n_requests_metric.additional_properties = d
        return last_n_requests_metric

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
