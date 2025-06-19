from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestTotalResponseData")


@_attrs_define
class RequestTotalResponseData:
    """Request total response data

    Attributes:
        request_total (Union[Unset, float]): Request total
        status_code (Union[Unset, str]): Status code
        workload_id (Union[Unset, str]): Workload ID
        workload_type (Union[Unset, str]): Workload type
        workspace (Union[Unset, str]): Workspace
    """

    request_total: Union[Unset, float] = UNSET
    status_code: Union[Unset, str] = UNSET
    workload_id: Union[Unset, str] = UNSET
    workload_type: Union[Unset, str] = UNSET
    workspace: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        request_total = self.request_total

        status_code = self.status_code

        workload_id = self.workload_id

        workload_type = self.workload_type

        workspace = self.workspace

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if request_total is not UNSET:
            field_dict["requestTotal"] = request_total
        if status_code is not UNSET:
            field_dict["statusCode"] = status_code
        if workload_id is not UNSET:
            field_dict["workloadId"] = workload_id
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
        request_total = d.pop("requestTotal", UNSET)

        status_code = d.pop("statusCode", UNSET)

        workload_id = d.pop("workloadId", UNSET)

        workload_type = d.pop("workloadType", UNSET)

        workspace = d.pop("workspace", UNSET)

        request_total_response_data = cls(
            request_total=request_total,
            status_code=status_code,
            workload_id=workload_id,
            workload_type=workload_type,
            workspace=workspace,
        )

        request_total_response_data.additional_properties = d
        return request_total_response_data

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
