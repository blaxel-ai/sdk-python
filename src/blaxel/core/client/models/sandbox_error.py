from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sandbox_error_details import SandboxErrorDetails


T = TypeVar("T", bound="SandboxError")


@_attrs_define
class SandboxError:
    """Error response returned by the CreateSandbox endpoint with extended details about the failure

    Attributes:
        code (str): Error code identifying the kind of error (e.g., INVALID_IMAGE, QUOTA_EXCEEDED) Example:
            INVALID_IMAGE.
        message (str): Human-readable error message describing what went wrong Example: Sandbox image blaxel/dev-ts-
            app:latest is not supported.
        details (Union[Unset, SandboxErrorDetails]): Additional error details. For INVALID_IMAGE errors, includes
            requested_image and supported_images array.
        sandbox_name (Union[Unset, str]): Name of the sandbox that failed to create Example: mysandbox.
        status_code (Union[Unset, int]): HTTP status code Example: 400.
        step (Union[Unset, str]): Processing step where the error occurred Example: validate_and_prepare.
        timestamp (Union[Unset, str]): ISO 8601 timestamp of when the error occurred Example:
            2025-12-19T22:36:29.336304095Z.
        workspace (Union[Unset, str]): Workspace name where the sandbox creation was attempted Example: main.
    """

    code: str
    message: str
    details: Union[Unset, "SandboxErrorDetails"] = UNSET
    sandbox_name: Union[Unset, str] = UNSET
    status_code: Union[Unset, int] = UNSET
    step: Union[Unset, str] = UNSET
    timestamp: Union[Unset, str] = UNSET
    workspace: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        message = self.message

        details: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.details
            and not isinstance(self.details, Unset)
            and not isinstance(self.details, dict)
        ):
            details = self.details.to_dict()
        elif self.details and isinstance(self.details, dict):
            details = self.details

        sandbox_name = self.sandbox_name

        status_code = self.status_code

        step = self.step

        timestamp = self.timestamp

        workspace = self.workspace

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
            }
        )
        if details is not UNSET:
            field_dict["details"] = details
        if sandbox_name is not UNSET:
            field_dict["sandbox_name"] = sandbox_name
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if step is not UNSET:
            field_dict["step"] = step
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if workspace is not UNSET:
            field_dict["workspace"] = workspace

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.sandbox_error_details import SandboxErrorDetails

        if not src_dict:
            return None
        d = src_dict.copy()
        code = d.pop("code")

        message = d.pop("message")

        _details = d.pop("details", UNSET)
        details: Union[Unset, SandboxErrorDetails]
        if isinstance(_details, Unset):
            details = UNSET
        else:
            details = SandboxErrorDetails.from_dict(_details)

        sandbox_name = d.pop("sandbox_name", UNSET)

        status_code = d.pop("status_code", UNSET)

        step = d.pop("step", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        workspace = d.pop("workspace", UNSET)

        sandbox_error = cls(
            code=code,
            message=message,
            details=details,
            sandbox_name=sandbox_name,
            status_code=status_code,
            step=step,
            timestamp=timestamp,
            workspace=workspace,
        )

        sandbox_error.additional_properties = d
        return sandbox_error

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
