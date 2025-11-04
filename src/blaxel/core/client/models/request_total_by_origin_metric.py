from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.request_total_by_origin_metric_request_total_by_origin import (
        RequestTotalByOriginMetricRequestTotalByOrigin,
    )
    from ..models.request_total_by_origin_metric_request_total_by_origin_and_code import (
        RequestTotalByOriginMetricRequestTotalByOriginAndCode,
    )


T = TypeVar("T", bound="RequestTotalByOriginMetric")


@_attrs_define
class RequestTotalByOriginMetric:
    """Request total by origin metric

    Attributes:
        request_total_by_origin (Union[Unset, RequestTotalByOriginMetricRequestTotalByOrigin]): Request total by origin
        request_total_by_origin_and_code (Union[Unset, RequestTotalByOriginMetricRequestTotalByOriginAndCode]): Request
            total by origin and code
    """

    request_total_by_origin: Union[Unset, "RequestTotalByOriginMetricRequestTotalByOrigin"] = UNSET
    request_total_by_origin_and_code: Union[Unset, "RequestTotalByOriginMetricRequestTotalByOriginAndCode"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        request_total_by_origin: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.request_total_by_origin
            and not isinstance(self.request_total_by_origin, Unset)
            and not isinstance(self.request_total_by_origin, dict)
        ):
            request_total_by_origin = self.request_total_by_origin.to_dict()
        elif self.request_total_by_origin and isinstance(self.request_total_by_origin, dict):
            request_total_by_origin = self.request_total_by_origin

        request_total_by_origin_and_code: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.request_total_by_origin_and_code
            and not isinstance(self.request_total_by_origin_and_code, Unset)
            and not isinstance(self.request_total_by_origin_and_code, dict)
        ):
            request_total_by_origin_and_code = self.request_total_by_origin_and_code.to_dict()
        elif self.request_total_by_origin_and_code and isinstance(self.request_total_by_origin_and_code, dict):
            request_total_by_origin_and_code = self.request_total_by_origin_and_code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if request_total_by_origin is not UNSET:
            field_dict["requestTotalByOrigin"] = request_total_by_origin
        if request_total_by_origin_and_code is not UNSET:
            field_dict["requestTotalByOriginAndCode"] = request_total_by_origin_and_code

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.request_total_by_origin_metric_request_total_by_origin import (
            RequestTotalByOriginMetricRequestTotalByOrigin,
        )
        from ..models.request_total_by_origin_metric_request_total_by_origin_and_code import (
            RequestTotalByOriginMetricRequestTotalByOriginAndCode,
        )

        if not src_dict:
            return None
        d = src_dict.copy()
        _request_total_by_origin = d.pop("requestTotalByOrigin", UNSET)
        request_total_by_origin: Union[Unset, RequestTotalByOriginMetricRequestTotalByOrigin]
        if isinstance(_request_total_by_origin, Unset):
            request_total_by_origin = UNSET
        else:
            request_total_by_origin = RequestTotalByOriginMetricRequestTotalByOrigin.from_dict(_request_total_by_origin)

        _request_total_by_origin_and_code = d.pop("requestTotalByOriginAndCode", UNSET)
        request_total_by_origin_and_code: Union[Unset, RequestTotalByOriginMetricRequestTotalByOriginAndCode]
        if isinstance(_request_total_by_origin_and_code, Unset):
            request_total_by_origin_and_code = UNSET
        else:
            request_total_by_origin_and_code = RequestTotalByOriginMetricRequestTotalByOriginAndCode.from_dict(
                _request_total_by_origin_and_code
            )

        request_total_by_origin_metric = cls(
            request_total_by_origin=request_total_by_origin,
            request_total_by_origin_and_code=request_total_by_origin_and_code,
        )

        request_total_by_origin_metric.additional_properties = d
        return request_total_by_origin_metric

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
