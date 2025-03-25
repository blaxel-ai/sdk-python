from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.store_configuration_option import StoreConfigurationOption


T = TypeVar("T", bound="StoreConfiguration")


@_attrs_define
class StoreConfiguration:
    """Store configuration for resources (eg: agent, function, etc)

    Attributes:
        available_models (Union[Unset, list[str]]): Available models for the configuration
        description (Union[Unset, str]): Store configuration description
        display_name (Union[Unset, str]): Store configuration display name
        if_ (Union[Unset, str]): Conditional rendering for the configuration, example: provider === 'openai'
        name (Union[Unset, str]): Store configuration name
        options (Union[Unset, list['StoreConfigurationOption']]):
        required (Union[Unset, bool]): Store configuration required
        secret (Union[Unset, bool]): Store configuration secret
        type_ (Union[Unset, str]): Store configuration type
    """

    available_models: Union[Unset, list[str]] = UNSET
    description: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    if_: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    options: Union[Unset, list["StoreConfigurationOption"]] = UNSET
    required: Union[Unset, bool] = UNSET
    secret: Union[Unset, bool] = UNSET
    type_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        available_models: Union[Unset, list[str]] = UNSET
        if not isinstance(self.available_models, Unset):
            available_models = self.available_models

        description = self.description

        display_name = self.display_name

        if_ = self.if_

        name = self.name

        options: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.options, Unset):
            options = []
            for options_item_data in self.options:
                if type(options_item_data) == dict:
                    options_item = options_item_data
                else:
                    options_item = options_item_data.to_dict()
                options.append(options_item)

        required = self.required

        secret = self.secret

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if available_models is not UNSET:
            field_dict["availableModels"] = available_models
        if description is not UNSET:
            field_dict["description"] = description
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if if_ is not UNSET:
            field_dict["if"] = if_
        if name is not UNSET:
            field_dict["name"] = name
        if options is not UNSET:
            field_dict["options"] = options
        if required is not UNSET:
            field_dict["required"] = required
        if secret is not UNSET:
            field_dict["secret"] = secret
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.store_configuration_option import StoreConfigurationOption

        if not src_dict:
            return None
        d = src_dict.copy()
        available_models = cast(list[str], d.pop("availableModels", UNSET))

        description = d.pop("description", UNSET)

        display_name = d.pop("displayName", UNSET)

        if_ = d.pop("if", UNSET)

        name = d.pop("name", UNSET)

        options = []
        _options = d.pop("options", UNSET)
        for options_item_data in _options or []:
            options_item = StoreConfigurationOption.from_dict(options_item_data)

            options.append(options_item)

        required = d.pop("required", UNSET)

        secret = d.pop("secret", UNSET)

        type_ = d.pop("type", UNSET)

        store_configuration = cls(
            available_models=available_models,
            description=description,
            display_name=display_name,
            if_=if_,
            name=name,
            options=options,
            required=required,
            secret=secret,
            type_=type_,
        )

        store_configuration.additional_properties = d
        return store_configuration

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
