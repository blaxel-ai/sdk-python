from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.mcp_definition_entrypoint import MCPDefinitionEntrypoint
    from ..models.mcp_definition_form import MCPDefinitionForm


T = TypeVar("T", bound="MCPDefinition")


@_attrs_define
class MCPDefinition:
    """Definition of an MCP from the MCP Hub

    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        categories (Union[Unset, list[Any]]): Categories of the artifact
        coming_soon (Union[Unset, bool]): If the artifact is coming soon
        description (Union[Unset, str]): Description of the artifact
        display_name (Union[Unset, str]): Display name of the artifact
        enterprise (Union[Unset, bool]): If the artifact is enterprise
        entrypoint (Union[Unset, MCPDefinitionEntrypoint]): Entrypoint of the artifact
        form (Union[Unset, MCPDefinitionForm]): Form of the artifact
        hidden_secrets (Union[Unset, list[str]]): Hidden secrets of the artifact
        icon (Union[Unset, str]): Icon of the artifact
        image (Union[Unset, str]): Image of the artifact
        integration (Union[Unset, str]): Integration of the artifact
        long_description (Union[Unset, str]): Long description of the artifact
        name (Union[Unset, str]): Name of the artifact
        url (Union[Unset, str]): URL of the artifact
    """

    created_at: Union[Unset, str] = UNSET
    updated_at: Union[Unset, str] = UNSET
    categories: Union[Unset, list[Any]] = UNSET
    coming_soon: Union[Unset, bool] = UNSET
    description: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    enterprise: Union[Unset, bool] = UNSET
    entrypoint: Union[Unset, "MCPDefinitionEntrypoint"] = UNSET
    form: Union[Unset, "MCPDefinitionForm"] = UNSET
    hidden_secrets: Union[Unset, list[str]] = UNSET
    icon: Union[Unset, str] = UNSET
    image: Union[Unset, str] = UNSET
    integration: Union[Unset, str] = UNSET
    long_description: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        updated_at = self.updated_at

        categories: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.categories, Unset):
            categories = self.categories

        coming_soon = self.coming_soon

        description = self.description

        display_name = self.display_name

        enterprise = self.enterprise

        entrypoint: Union[Unset, dict[str, Any]] = UNSET
        if self.entrypoint and not isinstance(self.entrypoint, Unset) and not isinstance(self.entrypoint, dict):
            entrypoint = self.entrypoint.to_dict()
        elif self.entrypoint and isinstance(self.entrypoint, dict):
            entrypoint = self.entrypoint

        form: Union[Unset, dict[str, Any]] = UNSET
        if self.form and not isinstance(self.form, Unset) and not isinstance(self.form, dict):
            form = self.form.to_dict()
        elif self.form and isinstance(self.form, dict):
            form = self.form

        hidden_secrets: Union[Unset, list[str]] = UNSET
        if not isinstance(self.hidden_secrets, Unset):
            hidden_secrets = self.hidden_secrets

        icon = self.icon

        image = self.image

        integration = self.integration

        long_description = self.long_description

        name = self.name

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
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.mcp_definition_entrypoint import MCPDefinitionEntrypoint
        from ..models.mcp_definition_form import MCPDefinitionForm

        if not src_dict:
            return None
        d = src_dict.copy()
        created_at = d.pop("createdAt", UNSET)

        updated_at = d.pop("updatedAt", UNSET)

        categories = cast(list[Any], d.pop("categories", UNSET))

        coming_soon = d.pop("coming_soon", UNSET)

        description = d.pop("description", UNSET)

        display_name = d.pop("displayName", UNSET)

        enterprise = d.pop("enterprise", UNSET)

        _entrypoint = d.pop("entrypoint", UNSET)
        entrypoint: Union[Unset, MCPDefinitionEntrypoint]
        if isinstance(_entrypoint, Unset):
            entrypoint = UNSET
        else:
            entrypoint = MCPDefinitionEntrypoint.from_dict(_entrypoint)

        _form = d.pop("form", UNSET)
        form: Union[Unset, MCPDefinitionForm]
        if isinstance(_form, Unset):
            form = UNSET
        else:
            form = MCPDefinitionForm.from_dict(_form)

        hidden_secrets = cast(list[str], d.pop("hiddenSecrets", UNSET))

        icon = d.pop("icon", UNSET)

        image = d.pop("image", UNSET)

        integration = d.pop("integration", UNSET)

        long_description = d.pop("longDescription", UNSET)

        name = d.pop("name", UNSET)

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
            hidden_secrets=hidden_secrets,
            icon=icon,
            image=image,
            integration=integration,
            long_description=long_description,
            name=name,
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
