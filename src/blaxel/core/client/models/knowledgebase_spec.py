from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.knowledgebase_spec_options import KnowledgebaseSpecOptions
    from ..models.revision_configuration import RevisionConfiguration


T = TypeVar("T", bound="KnowledgebaseSpec")


@_attrs_define
class KnowledgebaseSpec:
    """Knowledgebase specification

    Attributes:
        collection_name (Union[Unset, str]): Collection name
        embedding_model (Union[Unset, str]): Embedding model
        embedding_model_type (Union[Unset, str]): Embedding model type
        enabled (Union[Unset, bool]): Enable or disable the agent
        integration_connections (Union[Unset, list[str]]):
        options (Union[Unset, KnowledgebaseSpecOptions]): Options specific to the knowledge base
        policies (Union[Unset, list[str]]):
        revision (Union[Unset, RevisionConfiguration]): Revision configuration
        sandbox (Union[Unset, bool]): Sandbox mode
    """

    collection_name: Union[Unset, str] = UNSET
    embedding_model: Union[Unset, str] = UNSET
    embedding_model_type: Union[Unset, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    integration_connections: Union[Unset, list[str]] = UNSET
    options: Union[Unset, "KnowledgebaseSpecOptions"] = UNSET
    policies: Union[Unset, list[str]] = UNSET
    revision: Union[Unset, "RevisionConfiguration"] = UNSET
    sandbox: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        collection_name = self.collection_name

        embedding_model = self.embedding_model

        embedding_model_type = self.embedding_model_type

        enabled = self.enabled

        integration_connections: Union[Unset, list[str]] = UNSET
        if not isinstance(self.integration_connections, Unset):
            integration_connections = self.integration_connections

        options: Union[Unset, dict[str, Any]] = UNSET
        if self.options and not isinstance(self.options, Unset) and not isinstance(self.options, dict):
            options = self.options.to_dict()
        elif self.options and isinstance(self.options, dict):
            options = self.options

        policies: Union[Unset, list[str]] = UNSET
        if not isinstance(self.policies, Unset):
            policies = self.policies

        revision: Union[Unset, dict[str, Any]] = UNSET
        if self.revision and not isinstance(self.revision, Unset) and not isinstance(self.revision, dict):
            revision = self.revision.to_dict()
        elif self.revision and isinstance(self.revision, dict):
            revision = self.revision

        sandbox = self.sandbox

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if collection_name is not UNSET:
            field_dict["collectionName"] = collection_name
        if embedding_model is not UNSET:
            field_dict["embeddingModel"] = embedding_model
        if embedding_model_type is not UNSET:
            field_dict["embeddingModelType"] = embedding_model_type
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if integration_connections is not UNSET:
            field_dict["integrationConnections"] = integration_connections
        if options is not UNSET:
            field_dict["options"] = options
        if policies is not UNSET:
            field_dict["policies"] = policies
        if revision is not UNSET:
            field_dict["revision"] = revision
        if sandbox is not UNSET:
            field_dict["sandbox"] = sandbox

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.knowledgebase_spec_options import KnowledgebaseSpecOptions
        from ..models.revision_configuration import RevisionConfiguration

        if not src_dict:
            return None
        d = src_dict.copy()
        collection_name = d.pop("collectionName", UNSET)

        embedding_model = d.pop("embeddingModel", UNSET)

        embedding_model_type = d.pop("embeddingModelType", UNSET)

        enabled = d.pop("enabled", UNSET)

        integration_connections = cast(list[str], d.pop("integrationConnections", UNSET))

        _options = d.pop("options", UNSET)
        options: Union[Unset, KnowledgebaseSpecOptions]
        if isinstance(_options, Unset):
            options = UNSET
        else:
            options = KnowledgebaseSpecOptions.from_dict(_options)

        policies = cast(list[str], d.pop("policies", UNSET))

        _revision = d.pop("revision", UNSET)
        revision: Union[Unset, RevisionConfiguration]
        if isinstance(_revision, Unset):
            revision = UNSET
        else:
            revision = RevisionConfiguration.from_dict(_revision)

        sandbox = d.pop("sandbox", UNSET)

        knowledgebase_spec = cls(
            collection_name=collection_name,
            embedding_model=embedding_model,
            embedding_model_type=embedding_model_type,
            enabled=enabled,
            integration_connections=integration_connections,
            options=options,
            policies=policies,
            revision=revision,
            sandbox=sandbox,
        )

        knowledgebase_spec.additional_properties = d
        return knowledgebase_spec

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
