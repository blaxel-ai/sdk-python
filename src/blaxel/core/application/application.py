import asyncio
import time
import uuid
import warnings
from typing import Callable, Dict, List, Union

from ..client.api.applications.create_application import asyncio as create_application
from ..client.api.applications.create_application import sync as create_application_sync
from ..client.api.applications.delete_application import asyncio as delete_application
from ..client.api.applications.delete_application import sync as delete_application_sync
from ..client.api.applications.get_application import asyncio as get_application
from ..client.api.applications.get_application import sync as get_application_sync
from ..client.api.applications.list_applications import asyncio as list_applications
from ..client.api.applications.list_applications import sync as list_applications_sync
from ..client.api.applications.update_application import asyncio as update_application
from ..client.api.applications.update_application import sync as update_application_sync
from ..client.client import client
from ..client.errors import UnexpectedStatus
from ..client.models import Application, ApplicationSpec, Env, Metadata
from ..client.models.error import Error
from ..client.types import UNSET
from ..common.settings import settings

# Spec-level fields that default to UNSET on the generated model, so "is set"
# is a reliable signal of whether the caller provided them. Booleans like
# `enabled`/`proxy` default to concrete values (True/False), not UNSET, so they
# cannot be merged this way and are resolved explicitly by the caller instead.
_SPEC_MERGEABLE_FIELDS = (
    "region",
    "image",
    "memory",
    "port",
    "envs",
    "urls",
    "revision",
    "extensions",
)


def _is_set(value) -> bool:
    return value is not None and value is not UNSET


def _merge_application_spec(new_spec, current_spec, *, enabled, proxy) -> ApplicationSpec:
    """Merge a new spec over the current one, preserving fields the caller did
    not explicitly set (so an update never silently drops image/memory/envs/...).
    `enabled`/`proxy` are passed in already resolved because their generated
    defaults are indistinguishable from an explicit value."""
    merged = {"enabled": enabled}
    if proxy is not None:
        merged["proxy"] = proxy
    for attr in _SPEC_MERGEABLE_FIELDS:
        new_val = getattr(new_spec, attr, UNSET) if new_spec is not None else UNSET
        if _is_set(new_val):
            merged[attr] = new_val
            continue
        cur_val = getattr(current_spec, attr, UNSET) if current_spec is not None else UNSET
        if _is_set(cur_val):
            merged[attr] = cur_val
    return ApplicationSpec(**merged)


class ApplicationAPIError(Exception):
    """Exception raised when application API returns an error."""

    def __init__(self, message: str, status_code: int | None = None, code: str | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.code = code


class _AsyncDeleteDescriptor:
    """Descriptor that provides both class-level and instance-level delete functionality."""

    def __init__(self, delete_func: Callable):
        self._delete_func = delete_func

    def __get__(self, instance, owner):
        if instance is None:
            return self._delete_func
        else:

            async def instance_delete() -> Application:
                return await self._delete_func(instance.metadata.name or "")

            return instance_delete


class _SyncDeleteDescriptor:
    """Descriptor that provides both class-level and instance-level delete functionality (sync)."""

    def __init__(self, delete_func: Callable):
        self._delete_func = delete_func

    def __get__(self, instance, owner):
        if instance is None:
            return self._delete_func
        else:

            def instance_delete() -> Application:
                return self._delete_func(instance.metadata.name or "")

            return instance_delete


class _AsyncUpdateDescriptor:
    """Descriptor that provides both class-level and instance-level update functionality."""

    def __init__(self, update_func: Callable):
        self._update_func = update_func

    def __get__(self, instance, owner):
        if instance is None:
            return self._update_func
        else:

            async def instance_update(
                updates: Union["ApplicationCreateConfiguration", Application, Dict[str, any]],
            ) -> "ApplicationInstance":
                return await self._update_func(instance.metadata.name or "", updates)

            return instance_update


class _SyncUpdateDescriptor:
    """Descriptor that provides both class-level and instance-level update functionality (sync)."""

    def __init__(self, update_func: Callable):
        self._update_func = update_func

    def __get__(self, instance, owner):
        if instance is None:
            return self._update_func
        else:

            def instance_update(
                updates: Union["ApplicationCreateConfiguration", Application, Dict[str, any]],
            ) -> "SyncApplicationInstance":
                return self._update_func(instance.metadata.name or "", updates)

            return instance_update


class ApplicationCreateConfiguration:
    """Simplified configuration for creating applications with default values."""

    def __init__(
        self,
        name: str | None = None,
        display_name: str | None = None,
        labels: Dict[str, str] | None = None,
        image: str | None = None,
        region: str | None = None,
        enabled: bool | None = None,
        memory: int | None = None,
        port: int | None = None,
        envs: List["Env"] | None = None,
    ):
        self.name = name
        self.display_name = display_name
        self.labels = labels
        self.image = image
        self.region = region
        self.enabled = enabled
        self.memory = memory
        self.port = port
        self.envs = envs

    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> "ApplicationCreateConfiguration":
        raw_envs = data.get("envs")
        envs = (
            [e if isinstance(e, Env) else Env.from_dict(e) for e in raw_envs]
            if raw_envs is not None
            else None
        )
        return cls(
            name=data.get("name"),
            display_name=data.get("display_name"),
            labels=data.get("labels"),
            image=data.get("image"),
            region=data.get("region"),
            enabled=data.get("enabled"),
            memory=data.get("memory"),
            port=data.get("port"),
            envs=envs,
        )

    def to_spec(self) -> ApplicationSpec:
        """Build an ApplicationSpec from this configuration, setting only the
        fields the caller actually provided (so unset fields stay UNSET)."""
        spec_kwargs = {
            "region": self.region or settings.region or UNSET,
            "enabled": self.enabled if self.enabled is not None else True,
        }
        if self.image is not None:
            spec_kwargs["image"] = self.image
        if self.memory is not None:
            spec_kwargs["memory"] = self.memory
        if self.port is not None:
            spec_kwargs["port"] = self.port
        if self.envs is not None:
            spec_kwargs["envs"] = self.envs
        return ApplicationSpec(**spec_kwargs)

    def to_update_spec(self) -> ApplicationSpec:
        """Build a spec carrying only the compute fields explicitly provided,
        for use with `_merge_application_spec` (no create-time defaults so unset
        fields fall back to the current application on update)."""
        spec_kwargs = {}
        if self.region is not None:
            spec_kwargs["region"] = self.region
        if self.image is not None:
            spec_kwargs["image"] = self.image
        if self.memory is not None:
            spec_kwargs["memory"] = self.memory
        if self.port is not None:
            spec_kwargs["port"] = self.port
        if self.envs is not None:
            spec_kwargs["envs"] = self.envs
        return ApplicationSpec(**spec_kwargs)


class ApplicationInstance:
    delete: "_AsyncDeleteDescriptor"

    def __init__(self, application: Application):
        self.application = application

    @property
    def metadata(self):
        return self.application.metadata

    @property
    def spec(self):
        return self.application.spec

    @property
    def status(self):
        return self.application.status

    @property
    def events(self):
        return self.application.events

    @property
    def name(self):
        return self.application.metadata.name if self.application.metadata else None

    @property
    def display_name(self):
        return self.application.metadata.display_name if self.application.metadata else None

    @classmethod
    async def create(
        cls, config: Union[ApplicationCreateConfiguration, Application, Dict[str, any]]
    ) -> "ApplicationInstance":
        default_name = f"app-{uuid.uuid4().hex[:8]}"

        if isinstance(config, Application):
            application = config
        elif isinstance(config, ApplicationCreateConfiguration):
            application = Application(
                metadata=Metadata(
                    name=config.name or default_name,
                    display_name=config.display_name or config.name or default_name,
                    labels=config.labels,
                ),
                spec=config.to_spec(),
            )
        elif isinstance(config, dict):
            app_config = ApplicationCreateConfiguration.from_dict(config)
            application = Application(
                metadata=Metadata(
                    name=app_config.name or default_name,
                    display_name=app_config.display_name or app_config.name or default_name,
                    labels=app_config.labels,
                ),
                spec=app_config.to_spec(),
            )
        else:
            raise ValueError(
                f"Invalid config type: {type(config)}. Expected ApplicationCreateConfiguration, Application, or dict."
            )

        if not application.metadata:
            application.metadata = Metadata(name=default_name)
        if not application.metadata.name:
            application.metadata.name = default_name
        if not application.spec:
            application.spec = ApplicationSpec()

        if not application.spec.region or application.spec.region is UNSET:
            warnings.warn(
                "ApplicationInstance.create: 'region' is not set. In a future version, 'region' will be a required parameter. "
                "Please specify a region (e.g. 'us-pdx-1', 'eu-lon-1', 'us-was-1') in the application configuration or set the BL_REGION environment variable.",
                FutureWarning,
                stacklevel=2,
            )

        response = await create_application(client=client, body=application)
        if isinstance(response, Error):
            status_code = int(response.code) if response.code is not UNSET else None
            message = response.message if response.message is not UNSET else response.error
            raise ApplicationAPIError(message, status_code=status_code, code=response.error)
        return cls(response)

    @classmethod
    async def get(cls, application_name: str) -> "ApplicationInstance":
        response = await get_application(application_name=application_name, client=client)
        if response is None:
            raise ApplicationAPIError(
                f"Application '{application_name}' not found", status_code=404, code="NOT_FOUND"
            )
        if isinstance(response, Error):
            status_code = int(response.code) if response.code is not UNSET else None
            message = response.message if response.message is not UNSET else response.error
            raise ApplicationAPIError(message, status_code=status_code, code=response.error)
        return cls(response)

    @classmethod
    async def list(cls) -> list["ApplicationInstance"]:
        response = await list_applications(client=client)
        if isinstance(response, Error):
            return []
        if response is None:
            return []
        data = response.data if not isinstance(response.data, type(UNSET)) else []
        return [cls(app) for app in data or []]

    @classmethod
    async def create_if_not_exists(
        cls, config: Union[ApplicationCreateConfiguration, Application, Dict[str, any]]
    ) -> "ApplicationInstance":
        """Create an application if it doesn't exist, otherwise return existing."""
        try:
            return await cls.create(config)
        except (ApplicationAPIError, UnexpectedStatus) as e:
            is_conflict = False
            if isinstance(e, ApplicationAPIError):
                is_conflict = e.status_code == 409 or e.code in [
                    "409",
                    "APPLICATION_ALREADY_EXISTS",
                ]
            elif isinstance(e, UnexpectedStatus):
                is_conflict = e.status_code == 409

            if is_conflict:
                if isinstance(config, ApplicationCreateConfiguration):
                    name = config.name
                elif isinstance(config, dict):
                    name = config.get("name")
                elif isinstance(config, Application):
                    name = config.metadata.name if config.metadata else None
                else:
                    name = None

                if not name:
                    raise ValueError("Application name is required")

                return await cls.get(name)
            raise


class SyncApplicationInstance:
    delete: "_SyncDeleteDescriptor"

    """Synchronous application instance for managing application deployments."""

    def __init__(self, application: Application):
        self.application = application

    @property
    def metadata(self):
        return self.application.metadata

    @property
    def spec(self):
        return self.application.spec

    @property
    def status(self):
        return self.application.status

    @property
    def events(self):
        return self.application.events

    @property
    def name(self):
        return self.application.metadata.name if self.application.metadata else None

    @property
    def display_name(self):
        return self.application.metadata.display_name if self.application.metadata else None

    @classmethod
    def create(
        cls, config: Union[ApplicationCreateConfiguration, Application, Dict[str, any]]
    ) -> "SyncApplicationInstance":
        """Create a new application synchronously."""
        default_name = f"app-{uuid.uuid4().hex[:8]}"

        if isinstance(config, Application):
            application = config
        elif isinstance(config, ApplicationCreateConfiguration):
            application = Application(
                metadata=Metadata(
                    name=config.name or default_name,
                    display_name=config.display_name or config.name or default_name,
                    labels=config.labels,
                ),
                spec=config.to_spec(),
            )
        elif isinstance(config, dict):
            app_config = ApplicationCreateConfiguration.from_dict(config)
            application = Application(
                metadata=Metadata(
                    name=app_config.name or default_name,
                    display_name=app_config.display_name or app_config.name or default_name,
                    labels=app_config.labels,
                ),
                spec=app_config.to_spec(),
            )
        else:
            raise ValueError(
                f"Invalid config type: {type(config)}. Expected ApplicationCreateConfiguration, Application, or dict."
            )

        if not application.metadata:
            application.metadata = Metadata(name=default_name)
        if not application.metadata.name:
            application.metadata.name = default_name
        if not application.spec:
            application.spec = ApplicationSpec()

        if not application.spec.region or application.spec.region is UNSET:
            warnings.warn(
                "SyncApplicationInstance.create: 'region' is not set. In a future version, 'region' will be a required parameter. "
                "Please specify a region (e.g. 'us-pdx-1', 'eu-lon-1', 'us-was-1') in the application configuration or set the BL_REGION environment variable.",
                FutureWarning,
                stacklevel=2,
            )

        response = create_application_sync(client=client, body=application)
        if isinstance(response, Error):
            status_code = int(response.code) if response.code is not UNSET else None
            message = response.message if response.message is not UNSET else response.error
            raise ApplicationAPIError(message, status_code=status_code, code=response.error)
        return cls(response)

    @classmethod
    def get(cls, application_name: str) -> "SyncApplicationInstance":
        """Get an application by name synchronously."""
        response = get_application_sync(application_name=application_name, client=client)
        if response is None:
            raise ApplicationAPIError(
                f"Application '{application_name}' not found", status_code=404, code="NOT_FOUND"
            )
        if isinstance(response, Error):
            status_code = int(response.code) if response.code is not UNSET else None
            message = response.message if response.message is not UNSET else response.error
            raise ApplicationAPIError(message, status_code=status_code, code=response.error)
        return cls(response)

    @classmethod
    def list(cls) -> List["SyncApplicationInstance"]:
        """List all applications synchronously."""
        response = list_applications_sync(client=client)
        if isinstance(response, Error):
            return []
        if response is None:
            return []
        data = response.data if not isinstance(response.data, type(UNSET)) else []
        return [cls(app) for app in data or []]

    @classmethod
    def create_if_not_exists(
        cls, config: Union[ApplicationCreateConfiguration, Application, Dict[str, any]]
    ) -> "SyncApplicationInstance":
        """Create an application if it doesn't exist, otherwise return existing."""
        try:
            return cls.create(config)
        except (ApplicationAPIError, UnexpectedStatus) as e:
            is_conflict = False
            if isinstance(e, ApplicationAPIError):
                is_conflict = e.status_code == 409 or e.code in [
                    "409",
                    "APPLICATION_ALREADY_EXISTS",
                ]
            elif isinstance(e, UnexpectedStatus):
                is_conflict = e.status_code == 409

            if is_conflict:
                if isinstance(config, ApplicationCreateConfiguration):
                    name = config.name
                elif isinstance(config, dict):
                    name = config.get("name")
                elif isinstance(config, Application):
                    name = config.metadata.name if config.metadata else None
                else:
                    name = None

                if not name:
                    raise ValueError("Application name is required")

                return cls.get(name)
            raise


async def _delete_application_by_name(application_name: str) -> Application:
    """Delete an application by name (async)."""
    response = await delete_application(application_name=application_name, client=client)
    if isinstance(response, Error):
        status_code = int(response.code) if response.code is not UNSET else None
        message = response.message if response.message is not UNSET else response.error
        raise ApplicationAPIError(message, status_code=status_code, code=response.error)
    return response


def _delete_application_by_name_sync(application_name: str) -> Application:
    """Delete an application by name (sync)."""
    response = delete_application_sync(application_name=application_name, client=client)
    if isinstance(response, Error):
        status_code = int(response.code) if response.code is not UNSET else None
        message = response.message if response.message is not UNSET else response.error
        raise ApplicationAPIError(message, status_code=status_code, code=response.error)
    return response


async def _update_application_by_name(
    application_name: str,
    updates: Union[ApplicationCreateConfiguration, Application, Dict[str, any]],
) -> "ApplicationInstance":
    """Update an application by name (async)."""
    app_instance = await ApplicationInstance.get(application_name)
    current_app = app_instance.application

    if isinstance(updates, Application):
        new_metadata = updates.metadata
        new_spec = updates.spec
        resolved_enabled = (
            new_spec.enabled
            if new_spec is not None and new_spec.enabled is not None
            else (current_app.spec.enabled if current_app.spec else True)
        )
        resolved_proxy = (
            new_spec.proxy
            if new_spec is not None
            else (current_app.spec.proxy if current_app.spec else None)
        )
    elif isinstance(updates, ApplicationCreateConfiguration):
        new_metadata = Metadata(
            name=current_app.metadata.name if current_app.metadata else application_name,
            display_name=updates.display_name,
            labels=updates.labels,
        )
        new_spec = updates.to_update_spec()
        resolved_enabled = (
            updates.enabled
            if updates.enabled is not None
            else (current_app.spec.enabled if current_app.spec else True)
        )
        resolved_proxy = current_app.spec.proxy if current_app.spec else None
    elif isinstance(updates, dict):
        config = ApplicationCreateConfiguration.from_dict(updates)
        new_metadata = Metadata(
            name=current_app.metadata.name if current_app.metadata else application_name,
            display_name=config.display_name,
            labels=config.labels,
        )
        new_spec = config.to_update_spec()
        resolved_enabled = (
            config.enabled
            if config.enabled is not None
            else (current_app.spec.enabled if current_app.spec else True)
        )
        resolved_proxy = current_app.spec.proxy if current_app.spec else None
    else:
        raise ValueError(
            f"Invalid updates type: {type(updates)}. Expected ApplicationCreateConfiguration, Application, or dict."
        )

    merged_metadata = Metadata(
        name=current_app.metadata.name if current_app.metadata else application_name,
        display_name=new_metadata.display_name
        if new_metadata and new_metadata.display_name
        else (current_app.metadata.display_name if current_app.metadata else None),
        labels=new_metadata.labels
        if new_metadata and new_metadata.labels
        else (current_app.metadata.labels if current_app.metadata else None),
    )

    merged_spec = _merge_application_spec(
        new_spec,
        current_app.spec,
        enabled=resolved_enabled,
        proxy=resolved_proxy,
    )

    body = Application(
        metadata=merged_metadata,
        spec=merged_spec,
    )

    response = await update_application(application_name=application_name, client=client, body=body)
    if isinstance(response, Error):
        status_code = int(response.code) if response.code is not UNSET else None
        message = response.message if response.message is not UNSET else response.error
        raise ApplicationAPIError(message, status_code=status_code, code=response.error)
    await asyncio.sleep(0.5)
    return ApplicationInstance(response)


def _update_application_by_name_sync(
    application_name: str,
    updates: Union[ApplicationCreateConfiguration, Application, Dict[str, any]],
) -> "SyncApplicationInstance":
    """Update an application by name (sync)."""
    app_instance = SyncApplicationInstance.get(application_name)
    current_app = app_instance.application

    if isinstance(updates, Application):
        new_metadata = updates.metadata
        new_spec = updates.spec
        resolved_enabled = (
            new_spec.enabled
            if new_spec is not None and new_spec.enabled is not None
            else (current_app.spec.enabled if current_app.spec else True)
        )
        resolved_proxy = (
            new_spec.proxy
            if new_spec is not None
            else (current_app.spec.proxy if current_app.spec else None)
        )
    elif isinstance(updates, ApplicationCreateConfiguration):
        new_metadata = Metadata(
            name=current_app.metadata.name if current_app.metadata else application_name,
            display_name=updates.display_name,
            labels=updates.labels,
        )
        new_spec = updates.to_update_spec()
        resolved_enabled = (
            updates.enabled
            if updates.enabled is not None
            else (current_app.spec.enabled if current_app.spec else True)
        )
        resolved_proxy = current_app.spec.proxy if current_app.spec else None
    elif isinstance(updates, dict):
        config = ApplicationCreateConfiguration.from_dict(updates)
        new_metadata = Metadata(
            name=current_app.metadata.name if current_app.metadata else application_name,
            display_name=config.display_name,
            labels=config.labels,
        )
        new_spec = config.to_update_spec()
        resolved_enabled = (
            config.enabled
            if config.enabled is not None
            else (current_app.spec.enabled if current_app.spec else True)
        )
        resolved_proxy = current_app.spec.proxy if current_app.spec else None
    else:
        raise ValueError(
            f"Invalid updates type: {type(updates)}. Expected ApplicationCreateConfiguration, Application, or dict."
        )

    merged_metadata = Metadata(
        name=current_app.metadata.name if current_app.metadata else application_name,
        display_name=new_metadata.display_name
        if new_metadata and new_metadata.display_name
        else (current_app.metadata.display_name if current_app.metadata else None),
        labels=new_metadata.labels
        if new_metadata and new_metadata.labels
        else (current_app.metadata.labels if current_app.metadata else None),
    )

    merged_spec = _merge_application_spec(
        new_spec,
        current_app.spec,
        enabled=resolved_enabled,
        proxy=resolved_proxy,
    )

    body = Application(
        metadata=merged_metadata,
        spec=merged_spec,
    )

    response = update_application_sync(application_name=application_name, client=client, body=body)
    if isinstance(response, Error):
        status_code = int(response.code) if response.code is not UNSET else None
        message = response.message if response.message is not UNSET else response.error
        raise ApplicationAPIError(message, status_code=status_code, code=response.error)
    time.sleep(0.5)
    return SyncApplicationInstance(response)


ApplicationInstance.delete = _AsyncDeleteDescriptor(_delete_application_by_name)
SyncApplicationInstance.delete = _SyncDeleteDescriptor(_delete_application_by_name_sync)

ApplicationInstance.update = _AsyncUpdateDescriptor(_update_application_by_name)
SyncApplicationInstance.update = _SyncUpdateDescriptor(_update_application_by_name_sync)
