from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.port import Port
    from ..models.sandbox_definition_categories_item import SandboxDefinitionCategoriesItem


T = TypeVar("T", bound="SandboxDefinition")


@_attrs_define
class SandboxDefinition:
    """Pre-configured sandbox template available in the Sandbox Hub for quick deployment with predefined tools and
    configurations

        Attributes:
            categories (Union[Unset, list['SandboxDefinitionCategoriesItem']]): Categories of the defintion
            coming_soon (Union[Unset, bool]): If the definition is coming soon
            description (Union[Unset, str]): Description of the defintion Example: Python environment with data science
                libraries pre-installed.
            display_name (Union[Unset, str]): Display name of the definition Example: Python Data Science.
            enterprise (Union[Unset, bool]): If the definition is enterprise
            hidden (Union[Unset, bool]): If the definition is hidden
            icon (Union[Unset, str]): Icon of the definition
            image (Union[Unset, str]): Image of the Sandbox definition Example: blaxel/python-data-science:latest.
            long_description (Union[Unset, str]): Long description of the defintion
            memory (Union[Unset, int]): Memory of the Sandbox definition in MB Example: 2048.
            name (Union[Unset, str]): Name of the artifact Example: python-data-science.
            ports (Union[Unset, list['Port']]): Set of ports for a resource
            tags (Union[Unset, str]): Tags of the definition
            url (Union[Unset, str]): URL of the definition
    """

    categories: Union[Unset, list["SandboxDefinitionCategoriesItem"]] = UNSET
    coming_soon: Union[Unset, bool] = UNSET
    description: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    enterprise: Union[Unset, bool] = UNSET
    hidden: Union[Unset, bool] = UNSET
    icon: Union[Unset, str] = UNSET
    image: Union[Unset, str] = UNSET
    long_description: Union[Unset, str] = UNSET
    memory: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    ports: Union[Unset, list["Port"]] = UNSET
    tags: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        categories: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.categories, Unset):
            categories = []
            for categories_item_data in self.categories:
                if type(categories_item_data) is dict:
                    categories_item = categories_item_data
                else:
                    categories_item = categories_item_data.to_dict()
                categories.append(categories_item)

        coming_soon = self.coming_soon

        description = self.description

        display_name = self.display_name

        enterprise = self.enterprise

        hidden = self.hidden

        icon = self.icon

        image = self.image

        long_description = self.long_description

        memory = self.memory

        name = self.name

        ports: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.ports, Unset):
            ports = []
            for componentsschemas_ports_item_data in self.ports:
                if type(componentsschemas_ports_item_data) is dict:
                    componentsschemas_ports_item = componentsschemas_ports_item_data
                else:
                    componentsschemas_ports_item = componentsschemas_ports_item_data.to_dict()
                ports.append(componentsschemas_ports_item)

        tags = self.tags

        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if categories is not UNSET:
            field_dict["categories"] = categories
        if coming_soon is not UNSET:
            field_dict["coming_soon"] = coming_soon
        if description is not UNSET:
            field_dict["description"] = description
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if enterprise is not UNSET:
            field_dict["enterprise"] = enterprise
        if hidden is not UNSET:
            field_dict["hidden"] = hidden
        if icon is not UNSET:
            field_dict["icon"] = icon
        if image is not UNSET:
            field_dict["image"] = image
        if long_description is not UNSET:
            field_dict["longDescription"] = long_description
        if memory is not UNSET:
            field_dict["memory"] = memory
        if name is not UNSET:
            field_dict["name"] = name
        if ports is not UNSET:
            field_dict["ports"] = ports
        if tags is not UNSET:
            field_dict["tags"] = tags
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.port import Port
        from ..models.sandbox_definition_categories_item import SandboxDefinitionCategoriesItem

        if not src_dict:
            return None
        d = src_dict.copy()
        categories = []
        _categories = d.pop("categories", UNSET)
        for categories_item_data in _categories or []:
            categories_item = SandboxDefinitionCategoriesItem.from_dict(categories_item_data)

            categories.append(categories_item)

        coming_soon = d.pop("coming_soon", UNSET)

        description = d.pop("description", UNSET)

        display_name = d.pop("displayName", d.pop("display_name", UNSET))

        enterprise = d.pop("enterprise", UNSET)

        hidden = d.pop("hidden", UNSET)

        icon = d.pop("icon", UNSET)

        image = d.pop("image", UNSET)

        long_description = d.pop("longDescription", d.pop("long_description", UNSET))

        memory = d.pop("memory", UNSET)

        name = d.pop("name", UNSET)

        ports = []
        _ports = d.pop("ports", UNSET)
        for componentsschemas_ports_item_data in _ports or []:
            componentsschemas_ports_item = Port.from_dict(componentsschemas_ports_item_data)

            ports.append(componentsschemas_ports_item)

        tags = d.pop("tags", UNSET)

        url = d.pop("url", UNSET)

        sandbox_definition = cls(
            categories=categories,
            coming_soon=coming_soon,
            description=description,
            display_name=display_name,
            enterprise=enterprise,
            hidden=hidden,
            icon=icon,
            image=image,
            long_description=long_description,
            memory=memory,
            name=name,
            ports=ports,
            tags=tags,
            url=url,
        )

        sandbox_definition.additional_properties = d
        return sandbox_definition

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
