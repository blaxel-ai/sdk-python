from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SandboxForkRequest")


@_attrs_define
class SandboxForkRequest:
    """Request body for forking a sandbox into an application. Creates a new application or adds a canary revision to an
    existing one.

        Attributes:
            target_name (str): Name of the target application to create or update Example: my-app.
            target_type (str): Target resource type to fork into Example: application.
            custom_domain (Union[Unset, str]): Custom domain for the application
            port (Union[Unset, int]): Port to expose from the sandbox Example: 8080.
            prefix (Union[Unset, str]): URL prefix for the application
            snapshot_id (Union[Unset, str]): Snapshot ID to fork from. When set, the application revision references this
                snapshot.
            traffic (Union[Unset, int]): Traffic percentage for canary deployment (0-100). When set on an existing target,
                creates a new revision with this traffic percentage. Example: 10.
    """

    target_name: str
    target_type: str
    custom_domain: Union[Unset, str] = UNSET
    port: Union[Unset, int] = UNSET
    prefix: Union[Unset, str] = UNSET
    snapshot_id: Union[Unset, str] = UNSET
    traffic: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        target_name = self.target_name

        target_type = self.target_type

        custom_domain = self.custom_domain

        port = self.port

        prefix = self.prefix

        snapshot_id = self.snapshot_id

        traffic = self.traffic

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "targetName": target_name,
                "targetType": target_type,
            }
        )
        if custom_domain is not UNSET:
            field_dict["customDomain"] = custom_domain
        if port is not UNSET:
            field_dict["port"] = port
        if prefix is not UNSET:
            field_dict["prefix"] = prefix
        if snapshot_id is not UNSET:
            field_dict["snapshotId"] = snapshot_id
        if traffic is not UNSET:
            field_dict["traffic"] = traffic

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        target_name = d.pop("targetName") if "targetName" in d else d.pop("target_name")

        target_type = d.pop("targetType") if "targetType" in d else d.pop("target_type")

        custom_domain = d.pop("customDomain", d.pop("custom_domain", UNSET))

        port = d.pop("port", UNSET)

        prefix = d.pop("prefix", UNSET)

        snapshot_id = d.pop("snapshotId", d.pop("snapshot_id", UNSET))

        traffic = d.pop("traffic", UNSET)

        sandbox_fork_request = cls(
            target_name=target_name,
            target_type=target_type,
            custom_domain=custom_domain,
            port=port,
            prefix=prefix,
            snapshot_id=snapshot_id,
            traffic=traffic,
        )

        sandbox_fork_request.additional_properties = d
        return sandbox_fork_request

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
