from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.request_total_metric_request_total_per_code import (
        RequestTotalMetricRequestTotalPerCode,
    )
    from ..models.request_total_metric_rps_per_code import RequestTotalMetricRpsPerCode


T = TypeVar("T", bound="RequestTotalMetric")


@_attrs_define
class RequestTotalMetric:
    """Metrics for request total

    Attributes:
        request_total (Union[Unset, float]): Number of requests for all resources globally
        request_total_per_code (Union[Unset, RequestTotalMetricRequestTotalPerCode]): Number of requests for all
            resources globally per code
        rps (Union[Unset, float]): Number of requests per second for all resources globally
        rps_per_code (Union[Unset, RequestTotalMetricRpsPerCode]): Number of requests for all resources globally
    """

    request_total: Union[Unset, float] = UNSET
    request_total_per_code: Union[Unset, "RequestTotalMetricRequestTotalPerCode"] = UNSET
    rps: Union[Unset, float] = UNSET
    rps_per_code: Union[Unset, "RequestTotalMetricRpsPerCode"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        request_total = self.request_total

        request_total_per_code: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.request_total_per_code
            and not isinstance(self.request_total_per_code, Unset)
            and not isinstance(self.request_total_per_code, dict)
        ):
            request_total_per_code = self.request_total_per_code.to_dict()
        elif self.request_total_per_code and isinstance(self.request_total_per_code, dict):
            request_total_per_code = self.request_total_per_code

        rps = self.rps

        rps_per_code: Union[Unset, dict[str, Any]] = UNSET
        if self.rps_per_code and not isinstance(self.rps_per_code, Unset) and not isinstance(self.rps_per_code, dict):
            rps_per_code = self.rps_per_code.to_dict()
        elif self.rps_per_code and isinstance(self.rps_per_code, dict):
            rps_per_code = self.rps_per_code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if request_total is not UNSET:
            field_dict["requestTotal"] = request_total
        if request_total_per_code is not UNSET:
            field_dict["requestTotalPerCode"] = request_total_per_code
        if rps is not UNSET:
            field_dict["rps"] = rps
        if rps_per_code is not UNSET:
            field_dict["rpsPerCode"] = rps_per_code

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.request_total_metric_request_total_per_code import (
            RequestTotalMetricRequestTotalPerCode,
        )
        from ..models.request_total_metric_rps_per_code import RequestTotalMetricRpsPerCode

        if not src_dict:
            return None
        d = src_dict.copy()
        request_total = d.pop("requestTotal", UNSET)

        _request_total_per_code = d.pop("requestTotalPerCode", UNSET)
        request_total_per_code: Union[Unset, RequestTotalMetricRequestTotalPerCode]
        if isinstance(_request_total_per_code, Unset):
            request_total_per_code = UNSET
        else:
            request_total_per_code = RequestTotalMetricRequestTotalPerCode.from_dict(_request_total_per_code)

        rps = d.pop("rps", UNSET)

        _rps_per_code = d.pop("rpsPerCode", UNSET)
        rps_per_code: Union[Unset, RequestTotalMetricRpsPerCode]
        if isinstance(_rps_per_code, Unset):
            rps_per_code = UNSET
        else:
            rps_per_code = RequestTotalMetricRpsPerCode.from_dict(_rps_per_code)

        request_total_metric = cls(
            request_total=request_total,
            request_total_per_code=request_total_per_code,
            rps=rps,
            rps_per_code=rps_per_code,
        )

        request_total_metric.additional_properties = d
        return request_total_metric

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
