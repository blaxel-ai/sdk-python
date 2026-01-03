from __future__ import annotations

import asyncio
import hashlib
import io
import json
import shutil
import tempfile
import time
import zipfile
from dataclasses import dataclass, field
from http import HTTPStatus
from pathlib import Path
from typing import Callable, List, Optional

import httpx
from dockerfile_parse import DockerfileParser  # type: ignore[import-untyped]

from ..client.client import client
from ..client.models.metadata import Metadata
from ..client.models.metadata_labels import MetadataLabels
from ..client.models.runtime import Runtime
from ..client.models.sandbox import Sandbox
from ..client.models.sandbox_spec import SandboxSpec
from ..client.types import Response

SANDBOX_API_IMAGE = "ghcr.io/blaxel-ai/sandbox"
SANDBOX_API_PATH = "/usr/local/bin/sandbox-api"


@dataclass
class LocalFile:
    """Represents a local file to be copied into the build context."""

    source_path: Path
    destination_path: str
    context_name: str  # Name in the build context


@dataclass
class ImageBuildContext:
    """Contains all information needed to generate a deployable folder."""

    base_image: str
    instructions: List[str] = field(default_factory=list)
    local_files: List[LocalFile] = field(default_factory=list)
    has_entrypoint: bool = False

    def generate_dockerfile(self) -> str:
        """Generate the Dockerfile content using dockerfile-parse."""
        # Use BytesIO to prevent writing to disk
        # Note: type hint says IO[str] but runtime actually requires bytes
        dfp = DockerfileParser(fileobj=io.BytesIO())  # type: ignore[arg-type]
        dfp.content = f"FROM {self.base_image}\n"

        if self.instructions:
            # add_lines expects a string with newline-separated instructions
            dfp.add_lines("\n".join(self.instructions))

        return dfp.content

    def compute_hash(self) -> str:
        """Compute a hash of the image configuration for caching purposes."""
        content = self.generate_dockerfile()
        for local_file in self.local_files:
            if local_file.source_path.exists():
                content += f"\n{local_file.context_name}:{local_file.source_path.stat().st_mtime}"
        return hashlib.sha256(content.encode()).hexdigest()[:12]


class ImageInstance:
    """
    A fluent builder for creating sandbox images programmatically.

    Similar to Modal's Image class, allows chaining operations to build
    a custom image from a base image.

    Example:
        image = (
            ImageInstance.from_registry("python:3.11-slim")
            .apt_install("git", "curl")
            .workdir("/app")
            .run_commands("pip install --upgrade pip")
            .env(PYTHONUNBUFFERED="1")
        )
        image.build(
            name="my-sandbox",
            memory=4096,
            timeout=900.0,
            on_status_change=print_status,
            sandbox_version="latest",
        )
    """

    def __init__(self, context: ImageBuildContext):
        self._context = context

    def _clone_context(self) -> ImageBuildContext:
        """Create a copy of the current context."""
        return ImageBuildContext(
            base_image=self._context.base_image,
            instructions=self._context.instructions.copy(),
            local_files=self._context.local_files.copy(),
            has_entrypoint=self._context.has_entrypoint,
        )

    @classmethod
    def from_registry(cls, tag: str) -> "ImageInstance":
        """
        Create an image from a Docker registry image.

        Args:
            tag: The image tag (e.g., "python:3.11-slim", "ubuntu:22.04")

        Returns:
            A new Image instance
        """
        context = ImageBuildContext(base_image=tag)
        return cls(context)

    def workdir(self, path: str) -> "ImageInstance":
        """
        Set the working directory for subsequent instructions.

        Args:
            path: The working directory path inside the container

        Returns:
            A new Image instance with the working directory set
        """
        new_context = self._clone_context()
        new_context.instructions.append(f"WORKDIR {path}")
        return ImageInstance(new_context)

    def run_commands(self, *commands: str) -> "ImageInstance":
        """
        Run shell commands in the image.

        Args:
            *commands: One or more shell commands to run

        Returns:
            A new Image instance with the commands added
        """
        new_context = self._clone_context()
        for cmd in commands:
            new_context.instructions.append(f"RUN {cmd}")
        return ImageInstance(new_context)

    def env(self, **variables: str) -> "ImageInstance":
        """
        Set environment variables.

        Args:
            **variables: Environment variables as keyword arguments

        Returns:
            A new Image instance with the environment variables set
        """
        if not variables:
            return self

        new_context = self._clone_context()
        for key, value in variables.items():
            new_context.instructions.append(f'ENV {key}="{value}"')
        return ImageInstance(new_context)

    def copy(self, source: str, destination: str) -> "ImageInstance":
        """
        Copy files or directories from the build context to the image.

        Args:
            source: Source path (relative to build context)
            destination: Destination path in the image

        Returns:
            A new Image instance with the copy instruction
        """
        new_context = self._clone_context()
        new_context.instructions.append(f"COPY {source} {destination}")
        return ImageInstance(new_context)

    def add_local_file(
        self, source_path: str, destination: str, context_name: Optional[str] = None
    ) -> "ImageInstance":
        """
        Add a local file to the build context and copy it to the image.

        Args:
            source_path: Path to the local file
            destination: Destination path in the image
            context_name: Optional name for the file in the build context

        Returns:
            A new Image instance with the file added
        """
        source = Path(source_path).resolve()
        if context_name is None:
            context_name = source.name

        new_context = self._clone_context()
        new_context.local_files.append(LocalFile(source, destination, context_name))
        new_context.instructions.append(f"COPY {context_name} {destination}")
        return ImageInstance(new_context)

    def add_local_dir(
        self, source_path: str, destination: str, context_name: Optional[str] = None
    ) -> "ImageInstance":
        """
        Add a local directory to the build context and copy it to the image.

        Args:
            source_path: Path to the local directory
            destination: Destination path in the image
            context_name: Optional name for the directory in the build context

        Returns:
            A new Image instance with the directory added
        """
        source = Path(source_path).resolve()
        if context_name is None:
            context_name = source.name

        new_context = self._clone_context()
        new_context.local_files.append(LocalFile(source, destination, context_name))
        new_context.instructions.append(f"COPY {context_name} {destination}")
        return ImageInstance(new_context)

    def expose(self, *ports: int) -> "ImageInstance":
        """
        Expose ports.

        Args:
            *ports: Port numbers to expose

        Returns:
            A new Image instance with the ports exposed
        """
        if not ports:
            return self

        new_context = self._clone_context()
        for port in ports:
            new_context.instructions.append(f"EXPOSE {port}")
        return ImageInstance(new_context)

    def entrypoint(self, *args: str) -> "ImageInstance":
        """
        Set the entrypoint for the image.

        Args:
            *args: Entrypoint command and arguments

        Returns:
            A new Image instance with the entrypoint set
        """
        if not args:
            return self

        # Format as JSON array for exec form
        args_json = ", ".join(f'"{arg}"' for arg in args)
        new_context = self._clone_context()
        new_context.instructions.append(f"ENTRYPOINT [{args_json}]")
        new_context.has_entrypoint = True
        return ImageInstance(new_context)

    def user(self, user: str) -> "ImageInstance":
        """
        Set the user for subsequent instructions.

        Args:
            user: Username or UID

        Returns:
            A new Image instance with the user set
        """
        new_context = self._clone_context()
        new_context.instructions.append(f"USER {user}")
        return ImageInstance(new_context)

    def label(self, **labels: str) -> "ImageInstance":
        """
        Add labels to the image.

        Args:
            **labels: Labels as keyword arguments

        Returns:
            A new Image instance with the labels added
        """
        if not labels:
            return self

        new_context = self._clone_context()
        for key, value in labels.items():
            new_context.instructions.append(f'LABEL {key}="{value}"')
        return ImageInstance(new_context)

    def arg(self, name: str, default: Optional[str] = None) -> "ImageInstance":
        """
        Define a build argument.

        Args:
            name: Argument name
            default: Optional default value

        Returns:
            A new Image instance with the argument defined
        """
        new_context = self._clone_context()
        if default is not None:
            new_context.instructions.append(f"ARG {name}={default}")
        else:
            new_context.instructions.append(f"ARG {name}")
        return ImageInstance(new_context)

    @property
    def dockerfile(self) -> str:
        """Get the generated Dockerfile content."""
        return self._context.generate_dockerfile()

    @property
    def hash(self) -> str:
        """Get a hash of the image configuration."""
        return self._context.compute_hash()

    @property
    def base_image(self) -> str:
        """Get the base image tag."""
        return self._context.base_image

    def _has_sandbox_api(self) -> bool:
        """Check if sandbox-api is already included in the image."""
        dockerfile = self._context.generate_dockerfile()
        return "sandbox-api" in dockerfile or "blaxel-ai/sandbox" in dockerfile

    def _prepare_for_sandbox(self, sandbox_version: str = "latest") -> "ImageInstance":
        """
        Prepare the image for sandbox deployment by adding sandbox-api.

        This method adds the sandbox-api binary from the Blaxel sandbox image
        and sets the default entrypoint if not already specified.

        Args:
            sandbox_version: Version of the sandbox image to use (default "latest")

        Returns:
            A new Image instance prepared for sandbox deployment
        """
        new_context = self._clone_context()

        # Add sandbox-api if not already present
        if not self._has_sandbox_api():
            sandbox_image = f"{SANDBOX_API_IMAGE}:{sandbox_version}"
            copy_instruction = f"COPY --from={sandbox_image} /sandbox-api {SANDBOX_API_PATH}"
            new_context.instructions.append(copy_instruction)

        # Add default entrypoint if not set by user
        if not new_context.has_entrypoint:
            new_context.instructions.append(f'ENTRYPOINT ["{SANDBOX_API_PATH}"]')
            new_context.has_entrypoint = True

        return ImageInstance(new_context)

    def write(self, output_path: str, name: Optional[str] = None) -> Path:
        """
        Write the image to a deployable folder structure.

        Args:
            output_path: Path to the output directory
            name: Optional name for the generated folder (defaults to hash-based name)

        Returns:
            Path to the generated folder
        """
        output_dir = Path(output_path).resolve()

        # Create folder name based on hash if not provided
        if name is None:
            name = f"image-{self.hash}"

        build_dir = output_dir / name
        build_dir.mkdir(parents=True, exist_ok=True)

        # Generate Dockerfile
        dockerfile_path = build_dir / "Dockerfile"
        dockerfile_path.write_text(self._context.generate_dockerfile())

        # Copy local files to build context
        for local_file in self._context.local_files:
            if not local_file.source_path.exists():
                raise FileNotFoundError(f"Local file not found: {local_file.source_path}")

            dest = build_dir / local_file.context_name
            if local_file.source_path.is_dir():
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(local_file.source_path, dest)
            else:
                shutil.copy2(local_file.source_path, dest)

        # Generate a manifest file with metadata
        manifest = {
            "base_image": self._context.base_image,
            "hash": self.hash,
            "instructions_count": len(self._context.instructions),
            "local_files_count": len(self._context.local_files),
        }
        manifest_path = build_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2))

        return build_dir

    def write_temp(self) -> Path:
        """
        Write the image to a deployable folder in a temporary directory.

        Returns:
            Path to the generated folder
        """
        temp_dir = tempfile.mkdtemp(prefix="blaxel-image-")
        return self.write(temp_dir)

    def _create_zip(self, build_dir: Path) -> bytes:
        """
        Create a zip file from the build directory.

        Args:
            build_dir: Path to the build directory

        Returns:
            Zip file content as bytes
        """
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for file_path in build_dir.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(build_dir)
                    zf.write(file_path, arcname)
        zip_buffer.seek(0)
        return zip_buffer.getvalue()

    def _create_sandbox_payload(self, name: str, memory: int = 4096) -> Sandbox:
        """
        Create the sandbox payload for deployment.

        Args:
            name: Name for the sandbox
            memory: Memory in MB (default 4096)

        Returns:
            Sandbox object
        """
        labels = MetadataLabels()
        labels["x-blaxel-auto-generated"] = "true"

        metadata = Metadata(
            name=name,
            labels=labels,
        )

        runtime = Runtime(memory=memory)
        spec = SandboxSpec(runtime=runtime)

        return Sandbox(metadata=metadata, spec=spec)

    def _create_sandbox_with_upload_sync(
        self, sandbox: Sandbox
    ) -> tuple[Response[Sandbox], str | None]:
        """
        Create or update a sandbox with the upload query parameter.

        Args:
            sandbox: Sandbox payload

        Returns:
            Tuple of (Response, upload_url)
        """
        name = sandbox.metadata.name if sandbox.metadata else ""
        body = sandbox.to_dict()

        # Try PUT first (update), fall back to POST (create)
        http_client = client.get_httpx_client()

        # Try update first
        response = http_client.request(
            method="put",
            url=f"/sandboxes/{name}",
            json=body,
            params={"upload": "true"},
            headers={"Content-Type": "application/json"},
        )

        # If 404, try create
        if response.status_code == 404:
            response = http_client.request(
                method="post",
                url="/sandboxes",
                json=body,
                params={"upload": "true"},
                headers={"Content-Type": "application/json"},
            )

        upload_url = response.headers.get("x-blaxel-upload-url")

        result = Response(
            status_code=HTTPStatus(response.status_code),
            content=response.content,
            headers=response.headers,
            parsed=Sandbox.from_dict(response.json()) if response.status_code == 200 else None,
        )

        return result, upload_url

    async def _create_sandbox_with_upload(
        self, sandbox: Sandbox
    ) -> tuple[Response[Sandbox], str | None]:
        """
        Create or update a sandbox with the upload query parameter (async).

        Args:
            sandbox: Sandbox payload

        Returns:
            Tuple of (Response, upload_url)
        """
        name = sandbox.metadata.name if sandbox.metadata else ""
        body = sandbox.to_dict()

        # Try PUT first (update), fall back to POST (create)
        http_client = client.get_async_httpx_client()

        # Try update first
        response = await http_client.request(
            method="put",
            url=f"/sandboxes/{name}",
            json=body,
            params={"upload": "true"},
            headers={"Content-Type": "application/json"},
        )

        # If 404, try create
        if response.status_code == 404:
            response = await http_client.request(
                method="post",
                url="/sandboxes",
                json=body,
                params={"upload": "true"},
                headers={"Content-Type": "application/json"},
            )

        upload_url = response.headers.get("x-blaxel-upload-url")

        result = Response(
            status_code=HTTPStatus(response.status_code),
            content=response.content,
            headers=response.headers,
            parsed=Sandbox.from_dict(response.json()) if response.status_code == 200 else None,
        )

        return result, upload_url

    def _upload_zip_sync(self, upload_url: str, zip_content: bytes) -> None:
        """
        Upload the zip file to the given URL.

        Args:
            upload_url: URL to upload to
            zip_content: Zip file content
        """
        # Use a standalone client for upload (not the Blaxel client)
        with httpx.Client() as http_client:
            response = http_client.put(
                upload_url,
                content=zip_content,
                headers={"Content-Type": "application/zip"},
                timeout=300.0,  # 5 minute timeout for uploads
            )
            if response.status_code >= 400:
                raise RuntimeError(f"Upload failed with status {response.status_code}: {response.text}")

    async def _upload_zip(self, upload_url: str, zip_content: bytes) -> None:
        """
        Upload the zip file to the given URL (async).

        Args:
            upload_url: URL to upload to
            zip_content: Zip file content
        """
        async with httpx.AsyncClient() as http_client:
            response = await http_client.put(
                upload_url,
                content=zip_content,
                headers={"Content-Type": "application/zip"},
                timeout=300.0,  # 5 minute timeout for uploads
            )
            if response.status_code >= 400:
                raise RuntimeError(f"Upload failed with status {response.status_code}: {response.text}")

    def _get_sandbox_status_sync(self, name: str) -> str | None:
        """
        Get the current status of a sandbox.

        Args:
            name: Sandbox name

        Returns:
            Status string or None
        """
        http_client = client.get_httpx_client()
        response = http_client.get(f"/sandboxes/{name}")
        if response.status_code == 200:
            data = response.json()
            return data.get("status")
        return None

    async def _get_sandbox_status(self, name: str) -> str | None:
        """
        Get the current status of a sandbox (async).

        Args:
            name: Sandbox name

        Returns:
            Status string or None
        """
        http_client = client.get_async_httpx_client()
        response = await http_client.get(f"/sandboxes/{name}")
        if response.status_code == 200:
            data = response.json()
            return data.get("status")
        return None

    def _wait_for_deployment_sync(
        self,
        name: str,
        timeout: float = 900.0,
        poll_interval: float = 3.0,
        on_status_change: Optional[Callable[[str], None]] = None,
    ) -> str:
        """
        Wait for a sandbox deployment to complete.

        Args:
            name: Sandbox name
            timeout: Maximum time to wait in seconds (default 15 minutes)
            poll_interval: Time between status checks in seconds
            on_status_change: Optional callback for status changes

        Returns:
            Final status string

        Raises:
            TimeoutError: If deployment times out
            RuntimeError: If deployment fails
        """
        start_time = time.time()
        last_status = None
        terminal_states = {"DEPLOYED", "FAILED", "TERMINATED"}
        build_started = False

        while time.time() - start_time < timeout:
            status = self._get_sandbox_status_sync(name)

            if status and status != last_status:
                last_status = status
                if on_status_change:
                    on_status_change(status)

            # Track if the build has started (status changed from DEPLOYED)
            if status and status != "DEPLOYED":
                build_started = True

            # Only consider DEPLOYED as terminal if the build has started
            # This handles re-builds where status starts as DEPLOYED
            if status in terminal_states:
                if status == "FAILED":
                    raise RuntimeError(f"Deployment failed for sandbox '{name}'")
                if status == "TERMINATED":
                    raise RuntimeError(f"Sandbox '{name}' was terminated")
                if status == "DEPLOYED" and build_started:
                    return status

            time.sleep(poll_interval)

        raise TimeoutError(f"Deployment timed out after {timeout} seconds")

    async def _wait_for_deployment(
        self,
        name: str,
        timeout: float = 900.0,
        poll_interval: float = 3.0,
        on_status_change: Optional[Callable[[str], None]] = None,
    ) -> str:
        """
        Wait for a sandbox deployment to complete (async).

        Args:
            name: Sandbox name
            timeout: Maximum time to wait in seconds (default 15 minutes)
            poll_interval: Time between status checks in seconds
            on_status_change: Optional callback for status changes

        Returns:
            Final status string

        Raises:
            TimeoutError: If deployment times out
            RuntimeError: If deployment fails
        """
        start_time = time.time()
        last_status = None
        terminal_states = {"DEPLOYED", "FAILED", "TERMINATED"}
        build_started = False

        while time.time() - start_time < timeout:
            status = await self._get_sandbox_status(name)

            if status and status != last_status:
                last_status = status
                if on_status_change:
                    on_status_change(status)

            # Track if the build has started (status changed from DEPLOYED)
            if status and status != "DEPLOYED":
                build_started = True

            # Only consider DEPLOYED as terminal if the build has started
            # This handles re-builds where status starts as DEPLOYED
            if status in terminal_states:
                if status == "FAILED":
                    raise RuntimeError(f"Deployment failed for sandbox '{name}'")
                if status == "TERMINATED":
                    raise RuntimeError(f"Sandbox '{name}' was terminated")
                if status == "DEPLOYED" and build_started:
                    return status

            await asyncio.sleep(poll_interval)

        raise TimeoutError(f"Deployment timed out after {timeout} seconds")

    def build_sync(
        self,
        name: str,
        memory: int = 4096,
        timeout: float = 900.0,
        on_status_change: Optional[Callable[[str], None]] = None,
        sandbox_version: str = "latest",
    ) -> Sandbox:
        """
        Build and deploy the image as a sandbox.

        This method:
        1. Prepares the image for sandbox deployment (adds sandbox-api)
        2. Builds the image folder
        3. Creates a zip of the folder
        4. Creates/updates the sandbox resource
        5. Uploads the zip to Blaxel
        6. Waits for deployment to complete

        Args:
            name: Name for the sandbox
            memory: Memory in MB (default 4096)
            timeout: Maximum time to wait for deployment in seconds (default 15 minutes)
            on_status_change: Optional callback called when status changes
            sandbox_version: Version of sandbox-api to use (default "latest")

        Returns:
            The deployed Sandbox object

        Raises:
            RuntimeError: If deployment fails
            TimeoutError: If deployment times out
        """
        # Prepare image for sandbox deployment (add sandbox-api and entrypoint)
        prepared_image = self._prepare_for_sandbox(sandbox_version)

        # Write the image folder
        build_dir = prepared_image.write_temp()

        try:
            # Create zip
            zip_content = self._create_zip(build_dir)

            # Create sandbox payload
            sandbox_payload = self._create_sandbox_payload(name, memory)

            # Create/update sandbox and get upload URL
            response, upload_url = self._create_sandbox_with_upload_sync(sandbox_payload)

            if response.status_code.value >= 400:
                raise RuntimeError(
                    f"Failed to create sandbox: {response.status_code.value} - {response.content.decode()}"
                )

            if not upload_url:
                raise RuntimeError("No upload URL returned from API")

            # Upload the zip
            self._upload_zip_sync(upload_url, zip_content)

            # Wait for deployment to complete
            self._wait_for_deployment_sync(
                name, timeout=timeout, on_status_change=on_status_change
            )

            # Get the final sandbox state
            http_client = client.get_httpx_client()
            final_response = http_client.get(f"/sandboxes/{name}")
            if final_response.status_code == 200:
                sandbox = Sandbox.from_dict(final_response.json())
                if sandbox:
                    return sandbox

            if response.parsed:
                return response.parsed

            raise RuntimeError(f"Failed to get sandbox '{name}' after deployment")

        finally:
            # Cleanup temp directory
            shutil.rmtree(build_dir.parent, ignore_errors=True)

    async def build(
        self,
        name: str,
        memory: int = 4096,
        timeout: float = 900.0,
        on_status_change: Optional[Callable[[str], None]] = None,
        sandbox_version: str = "latest",
    ) -> Sandbox:
        """
        Build and deploy the image as a sandbox (async).

        This method:
        1. Prepares the image for sandbox deployment (adds sandbox-api)
        2. Builds the image folder
        3. Creates a zip of the folder
        4. Creates/updates the sandbox resource
        5. Uploads the zip to Blaxel
        6. Waits for deployment to complete

        Args:
            name: Name for the sandbox
            memory: Memory in MB (default 4096)
            timeout: Maximum time to wait for deployment in seconds (default 15 minutes)
            on_status_change: Optional callback called when status changes
            sandbox_version: Version of sandbox-api to use (default "latest")

        Returns:
            The deployed Sandbox object

        Raises:
            RuntimeError: If deployment fails
            TimeoutError: If deployment times out
        """
        # Prepare image for sandbox deployment (add sandbox-api and entrypoint)
        prepared_image = self._prepare_for_sandbox(sandbox_version)

        # Write the image folder (sync, as it's file I/O)
        build_dir = prepared_image.write_temp()

        try:
            # Create zip (sync, as it's file I/O)
            zip_content = self._create_zip(build_dir)

            # Create sandbox payload
            sandbox_payload = self._create_sandbox_payload(name, memory)

            # Create/update sandbox and get upload URL
            response, upload_url = await self._create_sandbox_with_upload(
                sandbox_payload
            )

            if response.status_code.value >= 400:
                raise RuntimeError(
                    f"Failed to create sandbox: {response.status_code.value} - {response.content.decode()}"
                )

            if not upload_url:
                raise RuntimeError("No upload URL returned from API")

            # Upload the zip
            await self._upload_zip(upload_url, zip_content)

            # Wait for deployment to complete
            await self._wait_for_deployment(
                name, timeout=timeout, on_status_change=on_status_change
            )

            # Get the final sandbox state
            http_client = client.get_async_httpx_client()
            final_response = await http_client.get(f"/sandboxes/{name}")
            if final_response.status_code == 200:
                sandbox = Sandbox.from_dict(final_response.json())
                if sandbox:
                    return sandbox

            if response.parsed:
                return response.parsed

            raise RuntimeError(f"Failed to get sandbox '{name}' after deployment")

        finally:
            # Cleanup temp directory
            shutil.rmtree(build_dir.parent, ignore_errors=True)
