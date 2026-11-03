from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.entrypoint import Entrypoint
    from ..models.form import Form
    from ..models.mcp_definition_categories_item import MCPDefinitionCategoriesItem


T = TypeVar("T", bound="MCPDefinition")


@_attrs_define
class MCPDefinition:
    """Definition of an MCP from the MCP Hub

    Attributes:
        created_at (str | Unset): The date and time when the resource was created
        updated_at (str | Unset): The date and time when the resource was updated
        categories (list[MCPDefinitionCategoriesItem] | Unset): Categories of the artifact
        coming_soon (bool | Unset): If the artifact is coming soon
        description (str | Unset): Description of the artifact
        display_name (str | Unset): Display name of the artifact
        enterprise (bool | Unset): If the artifact is enterprise
        entrypoint (Entrypoint | Unset): Entrypoint of the artifact
        form (Form | Unset): Form of the artifact
        hidden (bool | Unset): If the artifact is hidden
        hidden_secrets (list[str] | Unset): Hidden secrets of the artifact
        icon (str | Unset): Icon of the artifact
        image (str | Unset): Image of the artifact
        integration (str | Unset): Integration of the artifact
        long_description (str | Unset): Long description of the artifact
        name (str | Unset): Name of the artifact
        transport (str | Unset): Transport compatibility for the MCP, can be "websocket" or "http-stream"
        url (str | Unset): URL of the artifact
    """

    created_at: str | Unset = UNSET
    updated_at: str | Unset = UNSET
    categories: list[MCPDefinitionCategoriesItem] | Unset = UNSET
    coming_soon: bool | Unset = UNSET
    description: str | Unset = UNSET
    display_name: str | Unset = UNSET
    enterprise: bool | Unset = UNSET
    entrypoint: Entrypoint | Unset = UNSET
    form: Form | Unset = UNSET
    hidden: bool | Unset = UNSET
    hidden_secrets: list[str] | Unset = UNSET
    icon: str | Unset = UNSET
    image: str | Unset = UNSET
    integration: str | Unset = UNSET
    long_description: str | Unset = UNSET
    name: str | Unset = UNSET
    transport: str | Unset = UNSET
    url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        updated_at = self.updated_at

        categories: list[dict[str, Any]] | Unset = UNSET
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

        entrypoint: dict[str, Any] | Unset = UNSET
        if (
            self.entrypoint
            and not isinstance(self.entrypoint, Unset)
            and not isinstance(self.entrypoint, dict)
        ):
            entrypoint = self.entrypoint.to_dict()
        elif self.entrypoint and isinstance(self.entrypoint, dict):
            entrypoint = self.entrypoint

        form: dict[str, Any] | Unset = UNSET
        if self.form and not isinstance(self.form, Unset) and not isinstance(self.form, dict):
            form = self.form.to_dict()
        elif self.form and isinstance(self.form, dict):
            form = self.form

        hidden = self.hidden

        hidden_secrets: list[str] | Unset = UNSET
        if not isinstance(self.hidden_secrets, Unset):
            hidden_secrets = self.hidden_secrets

        icon = self.icon

        image = self.image

        integration = self.integration

        long_description = self.long_description

        name = self.name

        transport = self.transport

        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
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
        if entrypoint is not UNSET:
            field_dict["entrypoint"] = entrypoint
        if form is not UNSET:
            field_dict["form"] = form
        if hidden is not UNSET:
            field_dict["hidden"] = hidden
        if hidden_secrets is not UNSET:
            field_dict["hiddenSecrets"] = hidden_secrets
        if icon is not UNSET:
            field_dict["icon"] = icon
        if image is not UNSET:
            field_dict["image"] = image
        if integration is not UNSET:
            field_dict["integration"] = integration
        if long_description is not UNSET:
            field_dict["longDescription"] = long_description
        if name is not UNSET:
            field_dict["name"] = name
        if transport is not UNSET:
            field_dict["transport"] = transport
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        from ..models.entrypoint import Entrypoint  # noqa: PLC0415
        from ..models.form import Form  # noqa: PLC0415
        from ..models.mcp_definition_categories_item import (
            MCPDefinitionCategoriesItem,  # noqa: PLC0415
        )

        if not src_dict:
            return None
        d = dict(src_dict)
        created_at = d.pop("createdAt", d.pop("created_at", UNSET))

        updated_at = d.pop("updatedAt", d.pop("updated_at", UNSET))

        categories = []
        _categories = d.pop("categories", UNSET)
        for categories_item_data in _categories or []:
            categories_item = MCPDefinitionCategoriesItem.from_dict(categories_item_data)

            categories.append(categories_item)

        coming_soon = d.pop("coming_soon", UNSET)

        description = d.pop("description", UNSET)

        display_name = d.pop("displayName", d.pop("display_name", UNSET))

        enterprise = d.pop("enterprise", UNSET)

        _entrypoint = d.pop("entrypoint", UNSET)
        entrypoint: Entrypoint | Unset
        if isinstance(_entrypoint, Unset):
            entrypoint = UNSET
        else:
            entrypoint = Entrypoint.from_dict(_entrypoint)

        _form = d.pop("form", UNSET)
        form: Form | Unset
        if isinstance(_form, Unset):
            form = UNSET
        else:
            form = Form.from_dict(_form)

        hidden = d.pop("hidden", UNSET)

        hidden_secrets = cast(list[str], d.pop("hiddenSecrets", d.pop("hidden_secrets", UNSET)))

        icon = d.pop("icon", UNSET)

        image = d.pop("image", UNSET)

        integration = d.pop("integration", UNSET)

        long_description = d.pop("longDescription", d.pop("long_description", UNSET))

        name = d.pop("name", UNSET)

        transport = d.pop("transport", UNSET)

        url = d.pop("url", UNSET)

        mcp_definition = cls(
            created_at=created_at,
            updated_at=updated_at,
            categories=categories,
            coming_soon=coming_soon,
            description=description,
            display_name=display_name,
            enterprise=enterprise,
            entrypoint=entrypoint,
            form=form,
            hidden=hidden,
            hidden_secrets=hidden_secrets,
            icon=icon,
            image=image,
            integration=integration,
            long_description=long_description,
            name=name,
            transport=transport,
            url=url,
        )

        mcp_definition.additional_properties = d
        return mcp_definition

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
