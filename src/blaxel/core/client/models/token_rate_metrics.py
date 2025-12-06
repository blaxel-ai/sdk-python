from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.token_rate_metric import TokenRateMetric


T = TypeVar("T", bound="TokenRateMetrics")


@_attrs_define
class TokenRateMetrics:
    """Token rate metrics

    Attributes:
        token_rate (Union[Unset, list['TokenRateMetric']]): Token rate
        token_rate_input (Union[Unset, list['TokenRateMetric']]): Token rate input
        token_rate_output (Union[Unset, list['TokenRateMetric']]): Token rate output
    """

    token_rate: Union[Unset, list["TokenRateMetric"]] = UNSET
    token_rate_input: Union[Unset, list["TokenRateMetric"]] = UNSET
    token_rate_output: Union[Unset, list["TokenRateMetric"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        token_rate: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.token_rate, Unset):
            token_rate = []
            for token_rate_item_data in self.token_rate:
                if type(token_rate_item_data) is dict:
                    token_rate_item = token_rate_item_data
                else:
                    token_rate_item = token_rate_item_data.to_dict()
                token_rate.append(token_rate_item)

        token_rate_input: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.token_rate_input, Unset):
            token_rate_input = []
            for token_rate_input_item_data in self.token_rate_input:
                if type(token_rate_input_item_data) is dict:
                    token_rate_input_item = token_rate_input_item_data
                else:
                    token_rate_input_item = token_rate_input_item_data.to_dict()
                token_rate_input.append(token_rate_input_item)

        token_rate_output: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.token_rate_output, Unset):
            token_rate_output = []
            for token_rate_output_item_data in self.token_rate_output:
                if type(token_rate_output_item_data) is dict:
                    token_rate_output_item = token_rate_output_item_data
                else:
                    token_rate_output_item = token_rate_output_item_data.to_dict()
                token_rate_output.append(token_rate_output_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if token_rate is not UNSET:
            field_dict["tokenRate"] = token_rate
        if token_rate_input is not UNSET:
            field_dict["tokenRateInput"] = token_rate_input
        if token_rate_output is not UNSET:
            field_dict["tokenRateOutput"] = token_rate_output

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.token_rate_metric import TokenRateMetric

        if not src_dict:
            return None
        d = src_dict.copy()
        token_rate = []
        _token_rate = d.pop("tokenRate", UNSET)
        for token_rate_item_data in _token_rate or []:
            token_rate_item = TokenRateMetric.from_dict(token_rate_item_data)

            token_rate.append(token_rate_item)

        token_rate_input = []
        _token_rate_input = d.pop("tokenRateInput", UNSET)
        for token_rate_input_item_data in _token_rate_input or []:
            token_rate_input_item = TokenRateMetric.from_dict(token_rate_input_item_data)

            token_rate_input.append(token_rate_input_item)

        token_rate_output = []
        _token_rate_output = d.pop("tokenRateOutput", UNSET)
        for token_rate_output_item_data in _token_rate_output or []:
            token_rate_output_item = TokenRateMetric.from_dict(token_rate_output_item_data)

            token_rate_output.append(token_rate_output_item)

        token_rate_metrics = cls(
            token_rate=token_rate,
            token_rate_input=token_rate_input,
            token_rate_output=token_rate_output,
        )

        token_rate_metrics.additional_properties = d
        return token_rate_metrics

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
