from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sso_domain_spec_status import SSODomainSpecStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="SSODomainSpec")


@_attrs_define
class SSODomainSpec:
    """SSO domain specification

    Attributes:
        allowed_auth_methods (Union[Unset, list[str]]): List of allowed login methods for this domain. When set, users
            with this email domain can only use the specified methods. Possible values are google, saml, email. Empty list
            means no restriction.
        auto_join_workspaces (Union[Unset, list[str]]): List of workspace names where users with this domain auto-join
            on login
        last_used_auth_method (Union[Unset, str]): The authentication method last used by a user with this domain
            (google, saml, email)
        last_used_auth_method_at (Union[Unset, str]): Timestamp of when the last authentication method was used
        last_verified_at (Union[Unset, str]): Last verification attempt timestamp
        status (Union[Unset, SSODomainSpecStatus]): Current verification status of the domain (pending, verified,
            failed) Example: verified.
        txt_record_name (Union[Unset, str]): DNS TXT record name that must be created for verification
        txt_record_value (Union[Unset, str]): DNS TXT record value that must be set for verification
        verification_error (Union[Unset, str]): Error message if verification failed
    """

    allowed_auth_methods: Union[Unset, list[str]] = UNSET
    auto_join_workspaces: Union[Unset, list[str]] = UNSET
    last_used_auth_method: Union[Unset, str] = UNSET
    last_used_auth_method_at: Union[Unset, str] = UNSET
    last_verified_at: Union[Unset, str] = UNSET
    status: Union[Unset, SSODomainSpecStatus] = UNSET
    txt_record_name: Union[Unset, str] = UNSET
    txt_record_value: Union[Unset, str] = UNSET
    verification_error: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        allowed_auth_methods: Union[Unset, list[str]] = UNSET
        if not isinstance(self.allowed_auth_methods, Unset):
            allowed_auth_methods = self.allowed_auth_methods

        auto_join_workspaces: Union[Unset, list[str]] = UNSET
        if not isinstance(self.auto_join_workspaces, Unset):
            auto_join_workspaces = self.auto_join_workspaces

        last_used_auth_method = self.last_used_auth_method

        last_used_auth_method_at = self.last_used_auth_method_at

        last_verified_at = self.last_verified_at

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        txt_record_name = self.txt_record_name

        txt_record_value = self.txt_record_value

        verification_error = self.verification_error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if allowed_auth_methods is not UNSET:
            field_dict["allowedAuthMethods"] = allowed_auth_methods
        if auto_join_workspaces is not UNSET:
            field_dict["autoJoinWorkspaces"] = auto_join_workspaces
        if last_used_auth_method is not UNSET:
            field_dict["lastUsedAuthMethod"] = last_used_auth_method
        if last_used_auth_method_at is not UNSET:
            field_dict["lastUsedAuthMethodAt"] = last_used_auth_method_at
        if last_verified_at is not UNSET:
            field_dict["lastVerifiedAt"] = last_verified_at
        if status is not UNSET:
            field_dict["status"] = status
        if txt_record_name is not UNSET:
            field_dict["txtRecordName"] = txt_record_name
        if txt_record_value is not UNSET:
            field_dict["txtRecordValue"] = txt_record_value
        if verification_error is not UNSET:
            field_dict["verificationError"] = verification_error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        allowed_auth_methods = cast(
            list[str], d.pop("allowedAuthMethods", d.pop("allowed_auth_methods", UNSET))
        )

        auto_join_workspaces = cast(
            list[str], d.pop("autoJoinWorkspaces", d.pop("auto_join_workspaces", UNSET))
        )

        last_used_auth_method = d.pop("lastUsedAuthMethod", d.pop("last_used_auth_method", UNSET))

        last_used_auth_method_at = d.pop(
            "lastUsedAuthMethodAt", d.pop("last_used_auth_method_at", UNSET)
        )

        last_verified_at = d.pop("lastVerifiedAt", d.pop("last_verified_at", UNSET))

        _status = d.pop("status", UNSET)
        status: Union[Unset, SSODomainSpecStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = SSODomainSpecStatus(_status)

        txt_record_name = d.pop("txtRecordName", d.pop("txt_record_name", UNSET))

        txt_record_value = d.pop("txtRecordValue", d.pop("txt_record_value", UNSET))

        verification_error = d.pop("verificationError", d.pop("verification_error", UNSET))

        sso_domain_spec = cls(
            allowed_auth_methods=allowed_auth_methods,
            auto_join_workspaces=auto_join_workspaces,
            last_used_auth_method=last_used_auth_method,
            last_used_auth_method_at=last_used_auth_method_at,
            last_verified_at=last_verified_at,
            status=status,
            txt_record_name=txt_record_name,
            txt_record_value=txt_record_value,
            verification_error=verification_error,
        )

        sso_domain_spec.additional_properties = d
        return sso_domain_spec

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
