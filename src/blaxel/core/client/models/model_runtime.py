from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.model_runtime_type import ModelRuntimeType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelRuntime")


@_attrs_define
class ModelRuntime:
    """Configuration identifying which external LLM provider and model this gateway endpoint proxies to

    Attributes:
        endpoint_name (Union[Unset, str]): Provider-specific endpoint name (e.g., HuggingFace Inference Endpoints name)
        model (Union[Unset, str]): Model identifier at the provider (e.g., gpt-4.1, claude-sonnet-4-20250514, mistral-
            large-latest) Example: gpt-4.1.
        organization (Union[Unset, str]): Organization or account identifier at the provider (required for some
            providers like OpenAI) Example: org-abc123.
        type_ (Union[Unset, ModelRuntimeType]): LLM provider type determining the API protocol and authentication method
            Example: openai.
    """

    endpoint_name: Union[Unset, str] = UNSET
    model: Union[Unset, str] = UNSET
    organization: Union[Unset, str] = UNSET
    type_: Union[Unset, ModelRuntimeType] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        endpoint_name = self.endpoint_name

        model = self.model

        organization = self.organization

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if endpoint_name is not UNSET:
            field_dict["endpointName"] = endpoint_name
        if model is not UNSET:
            field_dict["model"] = model
        if organization is not UNSET:
            field_dict["organization"] = organization
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        endpoint_name = d.pop("endpointName", d.pop("endpoint_name", UNSET))

        model = d.pop("model", UNSET)

        organization = d.pop("organization", UNSET)

        _type_ = d.pop("type", d.pop("type_", UNSET))
        type_: Union[Unset, ModelRuntimeType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = ModelRuntimeType(_type_)

        model_runtime = cls(
            endpoint_name=endpoint_name,
            model=model,
            organization=organization,
            type_=type_,
        )

        model_runtime.additional_properties = d
        return model_runtime

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
