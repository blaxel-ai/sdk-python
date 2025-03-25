from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.function_schema_not import FunctionSchemaNot
    from ..models.function_schema_properties import FunctionSchemaProperties


T = TypeVar("T", bound="FunctionSchema")


@_attrs_define
class FunctionSchema:
    """Function schema

    Attributes:
        all_of (Union[Unset, list[Any]]): List of schemas that this schema extends
        any_of (Union[Unset, list[Any]]): List of possible schemas, any of which this schema could be
        description (Union[Unset, str]): Description of the schema
        enum (Union[Unset, list[str]]): Enum values
        format_ (Union[Unset, str]): Format of the schema
        items (Union[Unset, FunctionSchema]): Function schema
        max_length (Union[Unset, float]): Maximum length for string types
        maximum (Union[Unset, float]): Maximum value for number types
        min_length (Union[Unset, float]): Minimum length for string types
        minimum (Union[Unset, float]): Minimum value for number types
        not_ (Union[Unset, FunctionSchemaNot]): Schema that this schema must not be
        one_of (Union[Unset, list[Any]]): List of schemas, one of which this schema must be
        pattern (Union[Unset, str]): Pattern for string types
        properties (Union[Unset, FunctionSchemaProperties]): Properties of the schema
        required (Union[Unset, list[str]]): Required properties of the schema
        title (Union[Unset, str]): Title of the schema
        type_ (Union[Unset, str]): Type of the schema
    """

    all_of: Union[Unset, list[Any]] = UNSET
    any_of: Union[Unset, list[Any]] = UNSET
    description: Union[Unset, str] = UNSET
    enum: Union[Unset, list[str]] = UNSET
    format_: Union[Unset, str] = UNSET
    items: Union[Unset, "FunctionSchema"] = UNSET
    max_length: Union[Unset, float] = UNSET
    maximum: Union[Unset, float] = UNSET
    min_length: Union[Unset, float] = UNSET
    minimum: Union[Unset, float] = UNSET
    not_: Union[Unset, "FunctionSchemaNot"] = UNSET
    one_of: Union[Unset, list[Any]] = UNSET
    pattern: Union[Unset, str] = UNSET
    properties: Union[Unset, "FunctionSchemaProperties"] = UNSET
    required: Union[Unset, list[str]] = UNSET
    title: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        all_of: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.all_of, Unset):
            all_of = self.all_of

        any_of: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.any_of, Unset):
            any_of = self.any_of

        description = self.description

        enum: Union[Unset, list[str]] = UNSET
        if not isinstance(self.enum, Unset):
            enum = self.enum

        format_ = self.format_

        items: Union[Unset, dict[str, Any]] = UNSET
        if self.items and not isinstance(self.items, Unset) and not isinstance(self.items, dict):
            items = self.items.to_dict()
        elif self.items and isinstance(self.items, dict):
            items = self.items

        max_length = self.max_length

        maximum = self.maximum

        min_length = self.min_length

        minimum = self.minimum

        not_: Union[Unset, dict[str, Any]] = UNSET
        if self.not_ and not isinstance(self.not_, Unset) and not isinstance(self.not_, dict):
            not_ = self.not_.to_dict()
        elif self.not_ and isinstance(self.not_, dict):
            not_ = self.not_

        one_of: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.one_of, Unset):
            one_of = self.one_of

        pattern = self.pattern

        properties: Union[Unset, dict[str, Any]] = UNSET
        if self.properties and not isinstance(self.properties, Unset) and not isinstance(self.properties, dict):
            properties = self.properties.to_dict()
        elif self.properties and isinstance(self.properties, dict):
            properties = self.properties

        required: Union[Unset, list[str]] = UNSET
        if not isinstance(self.required, Unset):
            required = self.required

        title = self.title

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if all_of is not UNSET:
            field_dict["allOf"] = all_of
        if any_of is not UNSET:
            field_dict["anyOf"] = any_of
        if description is not UNSET:
            field_dict["description"] = description
        if enum is not UNSET:
            field_dict["enum"] = enum
        if format_ is not UNSET:
            field_dict["format"] = format_
        if items is not UNSET:
            field_dict["items"] = items
        if max_length is not UNSET:
            field_dict["maxLength"] = max_length
        if maximum is not UNSET:
            field_dict["maximum"] = maximum
        if min_length is not UNSET:
            field_dict["minLength"] = min_length
        if minimum is not UNSET:
            field_dict["minimum"] = minimum
        if not_ is not UNSET:
            field_dict["not"] = not_
        if one_of is not UNSET:
            field_dict["oneOf"] = one_of
        if pattern is not UNSET:
            field_dict["pattern"] = pattern
        if properties is not UNSET:
            field_dict["properties"] = properties
        if required is not UNSET:
            field_dict["required"] = required
        if title is not UNSET:
            field_dict["title"] = title
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.function_schema_not import FunctionSchemaNot
        from ..models.function_schema_properties import FunctionSchemaProperties

        if not src_dict:
            return None
        d = src_dict.copy()
        all_of = cast(list[Any], d.pop("allOf", UNSET))

        any_of = cast(list[Any], d.pop("anyOf", UNSET))

        description = d.pop("description", UNSET)

        enum = cast(list[str], d.pop("enum", UNSET))

        format_ = d.pop("format", UNSET)

        _items = d.pop("items", UNSET)
        items: Union[Unset, FunctionSchema]
        if isinstance(_items, Unset):
            items = UNSET
        else:
            items = FunctionSchema.from_dict(_items)

        max_length = d.pop("maxLength", UNSET)

        maximum = d.pop("maximum", UNSET)

        min_length = d.pop("minLength", UNSET)

        minimum = d.pop("minimum", UNSET)

        _not_ = d.pop("not", UNSET)
        not_: Union[Unset, FunctionSchemaNot]
        if isinstance(_not_, Unset):
            not_ = UNSET
        else:
            not_ = FunctionSchemaNot.from_dict(_not_)

        one_of = cast(list[Any], d.pop("oneOf", UNSET))

        pattern = d.pop("pattern", UNSET)

        _properties = d.pop("properties", UNSET)
        properties: Union[Unset, FunctionSchemaProperties]
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = FunctionSchemaProperties.from_dict(_properties)

        required = cast(list[str], d.pop("required", UNSET))

        title = d.pop("title", UNSET)

        type_ = d.pop("type", UNSET)

        function_schema = cls(
            all_of=all_of,
            any_of=any_of,
            description=description,
            enum=enum,
            format_=format_,
            items=items,
            max_length=max_length,
            maximum=maximum,
            min_length=min_length,
            minimum=minimum,
            not_=not_,
            one_of=one_of,
            pattern=pattern,
            properties=properties,
            required=required,
            title=title,
            type_=type_,
        )

        function_schema.additional_properties = d
        return function_schema

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
