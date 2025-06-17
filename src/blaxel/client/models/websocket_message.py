from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="WebsocketMessage")


@_attrs_define
class WebsocketMessage:
    """WebSocket connection details

    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        id (Union[Unset, str]): Unique message ID
        message (Union[Unset, str]): Message
        ttl (Union[Unset, int]): TTL timestamp for automatic deletion
        workspace (Union[Unset, str]): Workspace the connection belongs to
    """

    created_at: Union[Unset, str] = UNSET
    updated_at: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    message: Union[Unset, str] = UNSET
    ttl: Union[Unset, int] = UNSET
    workspace: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        updated_at = self.updated_at

        id = self.id

        message = self.message

        ttl = self.ttl

        workspace = self.workspace

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if id is not UNSET:
            field_dict["id"] = id
        if message is not UNSET:
            field_dict["message"] = message
        if ttl is not UNSET:
            field_dict["ttl"] = ttl
        if workspace is not UNSET:
            field_dict["workspace"] = workspace

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        created_at = d.pop("createdAt", UNSET)

        updated_at = d.pop("updatedAt", UNSET)

        id = d.pop("id", UNSET)

        message = d.pop("message", UNSET)

        ttl = d.pop("ttl", UNSET)

        workspace = d.pop("workspace", UNSET)

        websocket_message = cls(
            created_at=created_at,
            updated_at=updated_at,
            id=id,
            message=message,
            ttl=ttl,
            workspace=workspace,
        )

        websocket_message.additional_properties = d
        return websocket_message

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
