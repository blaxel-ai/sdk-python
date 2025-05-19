from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.jobs_chart_value import JobsChartValue


T = TypeVar("T", bound="JobsNetworkChart")


@_attrs_define
class JobsNetworkChart:
    """Jobs chart

    Attributes:
        received (Union[Unset, JobsChartValue]): Jobs CPU usage
        sent (Union[Unset, JobsChartValue]): Jobs CPU usage
    """

    received: Union[Unset, "JobsChartValue"] = UNSET
    sent: Union[Unset, "JobsChartValue"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        received: Union[Unset, dict[str, Any]] = UNSET
        if self.received and not isinstance(self.received, Unset) and not isinstance(self.received, dict):
            received = self.received.to_dict()
        elif self.received and isinstance(self.received, dict):
            received = self.received

        sent: Union[Unset, dict[str, Any]] = UNSET
        if self.sent and not isinstance(self.sent, Unset) and not isinstance(self.sent, dict):
            sent = self.sent.to_dict()
        elif self.sent and isinstance(self.sent, dict):
            sent = self.sent

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if received is not UNSET:
            field_dict["received"] = received
        if sent is not UNSET:
            field_dict["sent"] = sent

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.jobs_chart_value import JobsChartValue

        if not src_dict:
            return None
        d = src_dict.copy()
        _received = d.pop("received", UNSET)
        received: Union[Unset, JobsChartValue]
        if isinstance(_received, Unset):
            received = UNSET
        else:
            received = JobsChartValue.from_dict(_received)

        _sent = d.pop("sent", UNSET)
        sent: Union[Unset, JobsChartValue]
        if isinstance(_sent, Unset):
            sent = UNSET
        else:
            sent = JobsChartValue.from_dict(_sent)

        jobs_network_chart = cls(
            received=received,
            sent=sent,
        )

        jobs_network_chart.additional_properties = d
        return jobs_network_chart

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
