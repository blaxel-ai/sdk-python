from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.custom_domain_spec_domain_type import CustomDomainSpecDomainType
from ..models.custom_domain_spec_status import CustomDomainSpecStatus
from ..models.custom_domain_spec_validation_method import CustomDomainSpecValidationMethod
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
        cname_records (str | Unset): CNAME target for the domain
        domain_type (CustomDomainSpecDomainType | Unset): Type of custom domain (previews or applications) Example:
            applications.
        fallback_preview_id (str | Unset): Preview ID to route to when a preview lookup fails on this custom domain
            Example: my-fallback-preview.
        last_verified_at (str | Unset): Last verification attempt timestamp
        region (str | Unset): Region that the custom domain is associated with Example: us-pdx-1.
        status (CustomDomainSpecStatus | Unset): Current status of the domain (pending, verified, failed) Example:
            verified.
        subject_alternative_names (list[CustomDomainSpecSubjectAlternativeNamesItem] | Unset): Subject Alternative Names
            (SANs) for the ACM certificate. Only applicable for application domains.
        txt_records (CustomDomainSpecTxtRecords | Unset): Map of TXT record names to values for domain verification
        validation_method (CustomDomainSpecValidationMethod | Unset): How the TLS certificate is validated. "dns"
            (default) requires the certificate validation CNAME records to be published; "http" validates over HTTP once the
            domain points to Blaxel and requires no validation record. HTTP validation is not available for wildcard domains
            (previews or "*." names) and cannot be changed after creation. Default: CustomDomainSpecValidationMethod.DNS.
            Example: dns.
        verification_error (str | Unset): Error message if verification failed
    """

    cname_records: str | Unset = UNSET
    domain_type: CustomDomainSpecDomainType | Unset = UNSET
    fallback_preview_id: str | Unset = UNSET
    last_verified_at: str | Unset = UNSET
    region: str | Unset = UNSET
    status: CustomDomainSpecStatus | Unset = UNSET
    subject_alternative_names: list[CustomDomainSpecSubjectAlternativeNamesItem] | Unset = UNSET
    txt_records: CustomDomainSpecTxtRecords | Unset = UNSET
    validation_method: CustomDomainSpecValidationMethod | Unset = (
        CustomDomainSpecValidationMethod.DNS
    )
    verification_error: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cname_records = self.cname_records

        domain_type: str | Unset = UNSET
        if not isinstance(self.domain_type, Unset):
            domain_type = self.domain_type.value

        fallback_preview_id = self.fallback_preview_id

        last_verified_at = self.last_verified_at

        region = self.region

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        subject_alternative_names: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.subject_alternative_names, Unset):
            subject_alternative_names = []
            for subject_alternative_names_item_data in self.subject_alternative_names:
                if type(subject_alternative_names_item_data) is dict:
                    subject_alternative_names_item = subject_alternative_names_item_data
                else:
                    subject_alternative_names_item = subject_alternative_names_item_data.to_dict()
                subject_alternative_names.append(subject_alternative_names_item)

        txt_records: dict[str, Any] | Unset = UNSET
        if (
            self.txt_records
            and not isinstance(self.txt_records, Unset)
            and not isinstance(self.txt_records, dict)
        ):
            txt_records = self.txt_records.to_dict()
        elif self.txt_records and isinstance(self.txt_records, dict):
            txt_records = self.txt_records

        validation_method: str | Unset = UNSET
        if not isinstance(self.validation_method, Unset):
            validation_method = self.validation_method.value

        verification_error = self.verification_error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cname_records is not UNSET:
            field_dict["cnameRecords"] = cname_records
        if domain_type is not UNSET:
            field_dict["domainType"] = domain_type
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
        if validation_method is not UNSET:
            field_dict["validationMethod"] = validation_method
        if verification_error is not UNSET:
            field_dict["verificationError"] = verification_error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        from ..models.custom_domain_spec_subject_alternative_names_item import (
            CustomDomainSpecSubjectAlternativeNamesItem,
        )  # noqa: PLC0415
        from ..models.custom_domain_spec_txt_records import (
            CustomDomainSpecTxtRecords,  # noqa: PLC0415
        )

        if not src_dict:
            return None
        d = dict(src_dict)
        cname_records = d.pop("cnameRecords", d.pop("cname_records", UNSET))

        _domain_type = d.pop("domainType", d.pop("domain_type", UNSET))
        domain_type: CustomDomainSpecDomainType | Unset
        if isinstance(_domain_type, Unset) or _domain_type == "":
            domain_type = UNSET
        else:
            domain_type = CustomDomainSpecDomainType(_domain_type)

        fallback_preview_id = d.pop("fallbackPreviewId", d.pop("fallback_preview_id", UNSET))

        last_verified_at = d.pop("lastVerifiedAt", d.pop("last_verified_at", UNSET))

        region = d.pop("region", UNSET)

        _status = d.pop("status", UNSET)
        status: CustomDomainSpecStatus | Unset
        if isinstance(_status, Unset) or _status == "":
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
        txt_records: CustomDomainSpecTxtRecords | Unset
        if isinstance(_txt_records, Unset):
            txt_records = UNSET
        else:
            txt_records = CustomDomainSpecTxtRecords.from_dict(_txt_records)

        _validation_method = d.pop("validationMethod", d.pop("validation_method", UNSET))
        validation_method: CustomDomainSpecValidationMethod | Unset
        if isinstance(_validation_method, Unset) or _validation_method == "":
            validation_method = UNSET
        else:
            validation_method = CustomDomainSpecValidationMethod(_validation_method)

        verification_error = d.pop("verificationError", d.pop("verification_error", UNSET))

        custom_domain_spec = cls(
            cname_records=cname_records,
            domain_type=domain_type,
            fallback_preview_id=fallback_preview_id,
            last_verified_at=last_verified_at,
            region=region,
            status=status,
            subject_alternative_names=subject_alternative_names,
            txt_records=txt_records,
            validation_method=validation_method,
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
