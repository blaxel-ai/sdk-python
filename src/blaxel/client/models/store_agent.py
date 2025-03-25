from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.store_agent_labels import StoreAgentLabels
    from ..models.store_configuration import StoreConfiguration


T = TypeVar("T", bound="StoreAgent")


@_attrs_define
class StoreAgent:
    """Store agent

    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        created_by (Union[Unset, str]): The user or service account who created the resource
        updated_by (Union[Unset, str]): The user or service account who updated the resource
        configuration (Union[Unset, list['StoreConfiguration']]): Store agent configuration
        description (Union[Unset, str]): Store agent description
        display_name (Union[Unset, str]): Store agent display name
        image (Union[Unset, str]): Store agent image
        labels (Union[Unset, StoreAgentLabels]): Store agent labels
        name (Union[Unset, str]): Store agent name
        prompt (Union[Unset, str]): Store agent prompt, this is to define what the agent does
    """

    created_at: Union[Unset, str] = UNSET
    updated_at: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    updated_by: Union[Unset, str] = UNSET
    configuration: Union[Unset, list["StoreConfiguration"]] = UNSET
    description: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    image: Union[Unset, str] = UNSET
    labels: Union[Unset, "StoreAgentLabels"] = UNSET
    name: Union[Unset, str] = UNSET
    prompt: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        updated_at = self.updated_at

        created_by = self.created_by

        updated_by = self.updated_by

        configuration: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.configuration, Unset):
            configuration = []
            for configuration_item_data in self.configuration:
                if type(configuration_item_data) == dict:
                    configuration_item = configuration_item_data
                else:
                    configuration_item = configuration_item_data.to_dict()
                configuration.append(configuration_item)

        description = self.description

        display_name = self.display_name

        image = self.image

        labels: Union[Unset, dict[str, Any]] = UNSET
        if self.labels and not isinstance(self.labels, Unset) and not isinstance(self.labels, dict):
            labels = self.labels.to_dict()
        elif self.labels and isinstance(self.labels, dict):
            labels = self.labels

        name = self.name

        prompt = self.prompt

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if updated_by is not UNSET:
            field_dict["updatedBy"] = updated_by
        if configuration is not UNSET:
            field_dict["configuration"] = configuration
        if description is not UNSET:
            field_dict["description"] = description
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if image is not UNSET:
            field_dict["image"] = image
        if labels is not UNSET:
            field_dict["labels"] = labels
        if name is not UNSET:
            field_dict["name"] = name
        if prompt is not UNSET:
            field_dict["prompt"] = prompt

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.store_agent_labels import StoreAgentLabels
        from ..models.store_configuration import StoreConfiguration

        if not src_dict:
            return None
        d = src_dict.copy()
        created_at = d.pop("createdAt", UNSET)

        updated_at = d.pop("updatedAt", UNSET)

        created_by = d.pop("createdBy", UNSET)

        updated_by = d.pop("updatedBy", UNSET)

        configuration = []
        _configuration = d.pop("configuration", UNSET)
        for configuration_item_data in _configuration or []:
            configuration_item = StoreConfiguration.from_dict(configuration_item_data)

            configuration.append(configuration_item)

        description = d.pop("description", UNSET)

        display_name = d.pop("displayName", UNSET)

        image = d.pop("image", UNSET)

        _labels = d.pop("labels", UNSET)
        labels: Union[Unset, StoreAgentLabels]
        if isinstance(_labels, Unset):
            labels = UNSET
        else:
            labels = StoreAgentLabels.from_dict(_labels)

        name = d.pop("name", UNSET)

        prompt = d.pop("prompt", UNSET)

        store_agent = cls(
            created_at=created_at,
            updated_at=updated_at,
            created_by=created_by,
            updated_by=updated_by,
            configuration=configuration,
            description=description,
            display_name=display_name,
            image=image,
            labels=labels,
            name=name,
            prompt=prompt,
        )

        store_agent.additional_properties = d
        return store_agent

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
