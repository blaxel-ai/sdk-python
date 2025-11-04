from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TokenTotalMetric")


@_attrs_define
class TokenTotalMetric:
    """Token total metric

    Attributes:
        average_token_input_per_request (Union[Unset, float]): Average input token per request
        average_token_output_per_request (Union[Unset, float]): Average output token per request
        average_token_per_request (Union[Unset, float]): Average token per request
        token_input (Union[Unset, float]): Total input tokens
        token_output (Union[Unset, float]): Total output tokens
        token_total (Union[Unset, float]): Total tokens
    """

    average_token_input_per_request: Union[Unset, float] = UNSET
    average_token_output_per_request: Union[Unset, float] = UNSET
    average_token_per_request: Union[Unset, float] = UNSET
    token_input: Union[Unset, float] = UNSET
    token_output: Union[Unset, float] = UNSET
    token_total: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        average_token_input_per_request = self.average_token_input_per_request

        average_token_output_per_request = self.average_token_output_per_request

        average_token_per_request = self.average_token_per_request

        token_input = self.token_input

        token_output = self.token_output

        token_total = self.token_total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if average_token_input_per_request is not UNSET:
            field_dict["averageTokenInputPerRequest"] = average_token_input_per_request
        if average_token_output_per_request is not UNSET:
            field_dict["averageTokenOutputPerRequest"] = average_token_output_per_request
        if average_token_per_request is not UNSET:
            field_dict["averageTokenPerRequest"] = average_token_per_request
        if token_input is not UNSET:
            field_dict["tokenInput"] = token_input
        if token_output is not UNSET:
            field_dict["tokenOutput"] = token_output
        if token_total is not UNSET:
            field_dict["tokenTotal"] = token_total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        average_token_input_per_request = d.pop("averageTokenInputPerRequest", UNSET)

        average_token_output_per_request = d.pop("averageTokenOutputPerRequest", UNSET)

        average_token_per_request = d.pop("averageTokenPerRequest", UNSET)

        token_input = d.pop("tokenInput", UNSET)

        token_output = d.pop("tokenOutput", UNSET)

        token_total = d.pop("tokenTotal", UNSET)

        token_total_metric = cls(
            average_token_input_per_request=average_token_input_per_request,
            average_token_output_per_request=average_token_output_per_request,
            average_token_per_request=average_token_per_request,
            token_input=token_input,
            token_output=token_output,
            token_total=token_total,
        )

        token_total_metric.additional_properties = d
        return token_total_metric

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
