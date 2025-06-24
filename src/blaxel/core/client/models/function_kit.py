from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.function_schema import FunctionSchema


T = TypeVar("T", bound="FunctionKit")


@_attrs_define
class FunctionKit:
    """Function kit

    Attributes:
        description (Union[Unset, str]): Description of the function kit, very important for the agent to work with your
            kit
        name (Union[Unset, str]): The kit name, very important for the agent to work with your kit
        schema (Union[Unset, FunctionSchema]): Function schema
    """

    description: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    schema: Union[Unset, "FunctionSchema"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        name = self.name

        schema: Union[Unset, dict[str, Any]] = UNSET
        if self.schema and not isinstance(self.schema, Unset) and not isinstance(self.schema, dict):
            schema = self.schema.to_dict()
        elif self.schema and isinstance(self.schema, dict):
            schema = self.schema

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if name is not UNSET:
            field_dict["name"] = name
        if schema is not UNSET:
            field_dict["schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.function_schema import FunctionSchema

        if not src_dict:
            return None
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        name = d.pop("name", UNSET)

        _schema = d.pop("schema", UNSET)
        schema: Union[Unset, FunctionSchema]
        if isinstance(_schema, Unset):
            schema = UNSET
        else:
            schema = FunctionSchema.from_dict(_schema)

        function_kit = cls(
            description=description,
            name=name,
            schema=schema,
        )

        function_kit.additional_properties = d
        return function_kit

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
