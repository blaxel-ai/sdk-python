from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.custom_domain_spec_status import CustomDomainSpecStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.custom_domain_spec_subject_alternative_names_item import (
        CustomDomainSpecSubjectAlternativeNamesItem,
    )
    from ..models.custom_domain_spec_txt_records import CustomDomainSpecTxtRecords


T = TypeVar("T", bound="CustomDomainSpec")


@_attrs_define
class CustomDomainSpec:
    """Custom domain specification

    Attributes:
        cname_records (Union[Unset, str]): CNAME target for the domain
        fallback_preview_id (Union[Unset, str]): Preview ID to route to when a preview lookup fails on this custom
            domain Example: my-fallback-preview.
        last_verified_at (Union[Unset, str]): Last verification attempt timestamp
        region (Union[Unset, str]): Region that the custom domain is associated with Example: us-pdx-1.
        status (Union[Unset, CustomDomainSpecStatus]): Current status of the domain (pending, verified, failed) Example:
            verified.
        subject_alternative_names (Union[Unset, list['CustomDomainSpecSubjectAlternativeNamesItem']]): Subject
            Alternative Names (SANs) for the ACM certificate. Only applicable for application domains.
        txt_records (Union[Unset, CustomDomainSpecTxtRecords]): Map of TXT record names to values for domain
            verification
        verification_error (Union[Unset, str]): Error message if verification failed
    """

    cname_records: Union[Unset, str] = UNSET
    fallback_preview_id: Union[Unset, str] = UNSET
    last_verified_at: Union[Unset, str] = UNSET
    region: Union[Unset, str] = UNSET
    status: Union[Unset, CustomDomainSpecStatus] = UNSET
    subject_alternative_names: Union[Unset, list["CustomDomainSpecSubjectAlternativeNamesItem"]] = (
        UNSET
    )
    txt_records: Union[Unset, "CustomDomainSpecTxtRecords"] = UNSET
    verification_error: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        cname_records = self.cname_records

        fallback_preview_id = self.fallback_preview_id

        last_verified_at = self.last_verified_at

        region = self.region

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        subject_alternative_names: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.subject_alternative_names, Unset):
            subject_alternative_names = []
            for subject_alternative_names_item_data in self.subject_alternative_names:
                if type(subject_alternative_names_item_data) is dict:
                    subject_alternative_names_item = subject_alternative_names_item_data
                else:
                    subject_alternative_names_item = subject_alternative_names_item_data.to_dict()
                subject_alternative_names.append(subject_alternative_names_item)

        txt_records: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.txt_records
            and not isinstance(self.txt_records, Unset)
            and not isinstance(self.txt_records, dict)
        ):
            txt_records = self.txt_records.to_dict()
        elif self.txt_records and isinstance(self.txt_records, dict):
            txt_records = self.txt_records

        verification_error = self.verification_error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cname_records is not UNSET:
            field_dict["cnameRecords"] = cname_records
        if fallback_preview_id is not UNSET:
            field_dict["fallbackPreviewId"] = fallback_preview_id
        if last_verified_at is not UNSET:
            field_dict["lastVerifiedAt"] = last_verified_at
        if region is not UNSET:
            field_dict["region"] = region
        if status is not UNSET:
            field_dict["status"] = status
        if subject_alternative_names is not UNSET:
            field_dict["subjectAlternativeNames"] = subject_alternative_names
        if txt_records is not UNSET:
            field_dict["txtRecords"] = txt_records
        if verification_error is not UNSET:
            field_dict["verificationError"] = verification_error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.custom_domain_spec_subject_alternative_names_item import (
            CustomDomainSpecSubjectAlternativeNamesItem,
        )
        from ..models.custom_domain_spec_txt_records import CustomDomainSpecTxtRecords

        if not src_dict:
            return None
        d = src_dict.copy()
        cname_records = d.pop("cnameRecords", d.pop("cname_records", UNSET))

        fallback_preview_id = d.pop("fallbackPreviewId", d.pop("fallback_preview_id", UNSET))

        last_verified_at = d.pop("lastVerifiedAt", d.pop("last_verified_at", UNSET))

        region = d.pop("region", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, CustomDomainSpecStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = CustomDomainSpecStatus(_status)

        subject_alternative_names = []
        _subject_alternative_names = d.pop(
            "subjectAlternativeNames", d.pop("subject_alternative_names", UNSET)
        )
        for subject_alternative_names_item_data in _subject_alternative_names or []:
            subject_alternative_names_item = CustomDomainSpecSubjectAlternativeNamesItem.from_dict(
                subject_alternative_names_item_data
            )

            subject_alternative_names.append(subject_alternative_names_item)

        _txt_records = d.pop("txtRecords", d.pop("txt_records", UNSET))
        txt_records: Union[Unset, CustomDomainSpecTxtRecords]
        if isinstance(_txt_records, Unset):
            txt_records = UNSET
        else:
            txt_records = CustomDomainSpecTxtRecords.from_dict(_txt_records)

        verification_error = d.pop("verificationError", d.pop("verification_error", UNSET))

        custom_domain_spec = cls(
            cname_records=cname_records,
            fallback_preview_id=fallback_preview_id,
            last_verified_at=last_verified_at,
            region=region,
            status=status,
            subject_alternative_names=subject_alternative_names,
            txt_records=txt_records,
            verification_error=verification_error,
        )

        custom_domain_spec.additional_properties = d
        return custom_domain_spec

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
