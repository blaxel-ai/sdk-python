from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.export_options_headers import ExportOptionsHeaders
    from ..models.multipart_upload import MultipartUpload


T = TypeVar("T", bound="ExportOptions")


@_attrs_define
class ExportOptions:
    """
    Attributes:
        async_ (Union[Unset, bool]): Async starts the export and answers immediately, leaving it to run: an
            archive of a large filesystem takes longer than a request may be held
            open. Its progress is reported by /archive/status.
        dry_run (Union[Unset, bool]): DryRun reports what would be archived, and its exact size, without
            stopping anything and without uploading.
        excludes (Union[Unset, list[str]]): Excludes are added to the paths excluded by default.
        headers (Union[Unset, ExportOptionsHeaders]): Headers are sent with the upload request as given. A presigned URL
            only
            accepts the headers it was signed for, so these have to match what the
            caller signed: sending one that was not signed, or signing one that is not
            sent, is rejected as a signature mismatch. Typical use is a storage class,
            x-amz-storage-class: GLACIER_IR.
        image_device (Union[Unset, str]): ImageDevice is the device holding the pristine image. It is found on its
            own, wherever the sandbox booted from attached it, and naming one here
            only overrides that. Example: /dev/vda.
        image_mount_point (Union[Unset, str]): ImageMountPoint is a directory where the pristine image is already
            mounted.
            When set the image device is neither mounted nor unmounted. Example: /mnt/lower.
        multipart (Union[Unset, MultipartUpload]):
        save_processes (Union[Unset, bool]): SaveProcesses stores the process list in the archive so restore can
            relaunch the workload. Defaults to true; set it to false to archive
            storage only. Example: True.
        stop_timeout_seconds (Union[Unset, int]): StopTimeoutSeconds bounds the graceful stop of each process. Example:
            30.
        url (Union[Unset, str]): URL is a presigned S3 PUT URL the archive is streamed to. Empty is only
            valid with DryRun, or with Multipart. Example: https://bucket.s3.amazonaws.com/key?....
    """

    async_: Union[Unset, bool] = UNSET
    dry_run: Union[Unset, bool] = UNSET
    excludes: Union[Unset, list[str]] = UNSET
    headers: Union[Unset, "ExportOptionsHeaders"] = UNSET
    image_device: Union[Unset, str] = UNSET
    image_mount_point: Union[Unset, str] = UNSET
    multipart: Union[Unset, "MultipartUpload"] = UNSET
    save_processes: Union[Unset, bool] = UNSET
    stop_timeout_seconds: Union[Unset, int] = UNSET
    url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        async_ = self.async_

        dry_run = self.dry_run

        excludes: Union[Unset, list[str]] = UNSET
        if not isinstance(self.excludes, Unset):
            excludes = self.excludes

        headers: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.headers
            and not isinstance(self.headers, Unset)
            and not isinstance(self.headers, dict)
        ):
            headers = self.headers.to_dict()
        elif self.headers and isinstance(self.headers, dict):
            headers = self.headers

        image_device = self.image_device

        image_mount_point = self.image_mount_point

        multipart: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.multipart
            and not isinstance(self.multipart, Unset)
            and not isinstance(self.multipart, dict)
        ):
            multipart = self.multipart.to_dict()
        elif self.multipart and isinstance(self.multipart, dict):
            multipart = self.multipart

        save_processes = self.save_processes

        stop_timeout_seconds = self.stop_timeout_seconds

        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if async_ is not UNSET:
            field_dict["async"] = async_
        if dry_run is not UNSET:
            field_dict["dryRun"] = dry_run
        if excludes is not UNSET:
            field_dict["excludes"] = excludes
        if headers is not UNSET:
            field_dict["headers"] = headers
        if image_device is not UNSET:
            field_dict["imageDevice"] = image_device
        if image_mount_point is not UNSET:
            field_dict["imageMountPoint"] = image_mount_point
        if multipart is not UNSET:
            field_dict["multipart"] = multipart
        if save_processes is not UNSET:
            field_dict["saveProcesses"] = save_processes
        if stop_timeout_seconds is not UNSET:
            field_dict["stopTimeoutSeconds"] = stop_timeout_seconds
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.export_options_headers import ExportOptionsHeaders
        from ..models.multipart_upload import MultipartUpload

        if not src_dict:
            return None
        d = src_dict.copy()
        async_ = d.pop("async", d.pop("async_", UNSET))

        dry_run = d.pop("dryRun", d.pop("dry_run", UNSET))

        excludes = cast(list[str], d.pop("excludes", UNSET))

        _headers = d.pop("headers", UNSET)
        headers: Union[Unset, ExportOptionsHeaders]
        if isinstance(_headers, Unset):
            headers = UNSET
        else:
            headers = ExportOptionsHeaders.from_dict(_headers)

        image_device = d.pop("imageDevice", d.pop("image_device", UNSET))

        image_mount_point = d.pop("imageMountPoint", d.pop("image_mount_point", UNSET))

        _multipart = d.pop("multipart", UNSET)
        multipart: Union[Unset, MultipartUpload]
        if isinstance(_multipart, Unset):
            multipart = UNSET
        else:
            multipart = MultipartUpload.from_dict(_multipart)

        save_processes = d.pop("saveProcesses", d.pop("save_processes", UNSET))

        stop_timeout_seconds = d.pop("stopTimeoutSeconds", d.pop("stop_timeout_seconds", UNSET))

        url = d.pop("url", UNSET)

        export_options = cls(
            async_=async_,
            dry_run=dry_run,
            excludes=excludes,
            headers=headers,
            image_device=image_device,
            image_mount_point=image_mount_point,
            multipart=multipart,
            save_processes=save_processes,
            stop_timeout_seconds=stop_timeout_seconds,
            url=url,
        )

        export_options.additional_properties = d
        return export_options

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
