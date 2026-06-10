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
from ..client.models import Application, ApplicationSpec, Metadata
from ..client.models.error import Error
from ..client.types import UNSET
from ..common.settings import settings


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
    ):
        self.name = name
        self.display_name = display_name
        self.labels = labels
        self.image = image
        self.region = region
        self.enabled = enabled

    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> "ApplicationCreateConfiguration":
        return cls(
            name=data.get("name"),
            display_name=data.get("display_name"),
            labels=data.get("labels"),
            image=data.get("image"),
            region=data.get("region"),
            enabled=data.get("enabled"),
        )


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
                spec=ApplicationSpec(
                    region=config.region or settings.region or UNSET,
                    enabled=config.enabled if config.enabled is not None else True,
                ),
            )
        elif isinstance(config, dict):
            app_config = ApplicationCreateConfiguration.from_dict(config)
            application = Application(
                metadata=Metadata(
                    name=app_config.name or default_name,
                    display_name=app_config.display_name or app_config.name or default_name,
                    labels=app_config.labels,
                ),
                spec=ApplicationSpec(
                    region=app_config.region or settings.region or UNSET,
                    enabled=app_config.enabled if app_config.enabled is not None else True,
                ),
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
                spec=ApplicationSpec(
                    region=config.region or settings.region or UNSET,
                    enabled=config.enabled if config.enabled is not None else True,
                ),
            )
        elif isinstance(config, dict):
            app_config = ApplicationCreateConfiguration.from_dict(config)
            application = Application(
                metadata=Metadata(
                    name=app_config.name or default_name,
                    display_name=app_config.display_name or app_config.name or default_name,
                    labels=app_config.labels,
                ),
                spec=ApplicationSpec(
                    region=app_config.region or settings.region or UNSET,
                    enabled=app_config.enabled if app_config.enabled is not None else True,
                ),
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
    return response


def _delete_application_by_name_sync(application_name: str) -> Application:
    """Delete an application by name (sync)."""
    response = delete_application_sync(application_name=application_name, client=client)
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
    elif isinstance(updates, ApplicationCreateConfiguration):
        new_metadata = Metadata(
            name=current_app.metadata.name if current_app.metadata else application_name,
            display_name=updates.display_name,
            labels=updates.labels,
        )
        new_spec = ApplicationSpec(
            region=updates.region,
            enabled=updates.enabled,
        )
    elif isinstance(updates, dict):
        config = ApplicationCreateConfiguration.from_dict(updates)
        new_metadata = Metadata(
            name=current_app.metadata.name if current_app.metadata else application_name,
            display_name=config.display_name,
            labels=config.labels,
        )
        new_spec = ApplicationSpec(
            region=config.region,
            enabled=config.enabled,
        )
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

    merged_spec = ApplicationSpec(
        region=new_spec.region
        if new_spec and new_spec.region
        else (current_app.spec.region if current_app.spec else None),
        enabled=new_spec.enabled
        if new_spec and new_spec.enabled is not None
        else (current_app.spec.enabled if current_app.spec else True),
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
    elif isinstance(updates, ApplicationCreateConfiguration):
        new_metadata = Metadata(
            name=current_app.metadata.name if current_app.metadata else application_name,
            display_name=updates.display_name,
            labels=updates.labels,
        )
        new_spec = ApplicationSpec(
            region=updates.region,
            enabled=updates.enabled,
        )
    elif isinstance(updates, dict):
        config = ApplicationCreateConfiguration.from_dict(updates)
        new_metadata = Metadata(
            name=current_app.metadata.name if current_app.metadata else application_name,
            display_name=config.display_name,
            labels=config.labels,
        )
        new_spec = ApplicationSpec(
            region=config.region,
            enabled=config.enabled,
        )
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

    merged_spec = ApplicationSpec(
        region=new_spec.region
        if new_spec and new_spec.region
        else (current_app.spec.region if current_app.spec else None),
        enabled=new_spec.enabled
        if new_spec and new_spec.enabled is not None
        else (current_app.spec.enabled if current_app.spec else True),
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
