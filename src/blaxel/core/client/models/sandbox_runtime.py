from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.port import Port
    from ..models.sandbox_runtime_envs_item import SandboxRuntimeEnvsItem


T = TypeVar("T", bound="SandboxRuntime")


@_attrs_define
class SandboxRuntime:
    """Runtime configuration for Sandbox

    Attributes:
        envs (Union[Unset, list['SandboxRuntimeEnvsItem']]): The env variables to set in the sandbox. Should be a list
            of Kubernetes EnvVar types
        expires (Union[Unset, str]): The expiration date for the sandbox in ISO 8601 format - 2024-12-31T23:59:59Z
        image (Union[Unset, str]): The Docker image for the sandbox
        memory (Union[Unset, int]): The memory for the sandbox in MB
        ports (Union[Unset, list['Port']]): Set of ports for a resource
        ttl (Union[Unset, str]): The TTL for the sandbox in seconds - 30m, 24h, 7d
    """

    envs: Union[Unset, list["SandboxRuntimeEnvsItem"]] = UNSET
    expires: Union[Unset, str] = UNSET
    image: Union[Unset, str] = UNSET
    memory: Union[Unset, int] = UNSET
    ports: Union[Unset, list["Port"]] = UNSET
    ttl: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        envs: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.envs, Unset):
            envs = []
            for envs_item_data in self.envs:
                if type(envs_item_data) is dict:
                    envs_item = envs_item_data
                else:
                    envs_item = envs_item_data.to_dict()
                envs.append(envs_item)

        expires = self.expires

        image = self.image

        memory = self.memory

        ports: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.ports, Unset):
            ports = []
            for componentsschemas_ports_item_data in self.ports:
                if type(componentsschemas_ports_item_data) is dict:
                    componentsschemas_ports_item = componentsschemas_ports_item_data
                else:
                    componentsschemas_ports_item = componentsschemas_ports_item_data.to_dict()
                ports.append(componentsschemas_ports_item)

        ttl = self.ttl

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if envs is not UNSET:
            field_dict["envs"] = envs
        if expires is not UNSET:
            field_dict["expires"] = expires
        if image is not UNSET:
            field_dict["image"] = image
        if memory is not UNSET:
            field_dict["memory"] = memory
        if ports is not UNSET:
            field_dict["ports"] = ports
        if ttl is not UNSET:
            field_dict["ttl"] = ttl

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.port import Port
        from ..models.sandbox_runtime_envs_item import SandboxRuntimeEnvsItem

        if not src_dict:
            return None
        d = src_dict.copy()
        envs = []
        _envs = d.pop("envs", UNSET)
        for envs_item_data in _envs or []:
            envs_item = SandboxRuntimeEnvsItem.from_dict(envs_item_data)

            envs.append(envs_item)

        expires = d.pop("expires", UNSET)

        image = d.pop("image", UNSET)

        memory = d.pop("memory", UNSET)

        ports = []
        _ports = d.pop("ports", UNSET)
        for componentsschemas_ports_item_data in _ports or []:
            componentsschemas_ports_item = Port.from_dict(componentsschemas_ports_item_data)

            ports.append(componentsschemas_ports_item)

        ttl = d.pop("ttl", UNSET)

        sandbox_runtime = cls(
            envs=envs,
            expires=expires,
            image=image,
            memory=memory,
            ports=ports,
            ttl=ttl,
        )

        sandbox_runtime.additional_properties = d
        return sandbox_runtime

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
