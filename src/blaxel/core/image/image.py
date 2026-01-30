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

    def compute_hash(self, max_file_size: int = 100 * 1024 * 1024) -> str:
        """
        Compute a hash of the image configuration for caching purposes.

        Args:
            max_file_size: Maximum file size to include in hash computation (default 100MB).
                          Files larger than this will only use mtime for hashing.

        Returns:
            A 12-character hash string
        """
        content = self.generate_dockerfile()
        for local_file in self.local_files:
            if local_file.source_path.exists():
                stat = local_file.source_path.stat()
                # Use mtime for all files, but skip size check for very large files
                # to prevent resource exhaustion
                if stat.st_size <= max_file_size:
                    content += f"\n{local_file.context_name}:{stat.st_mtime}:{stat.st_size}"
                else:
                    # For very large files, just use mtime (already fast)
                    content += f"\n{local_file.context_name}:{stat.st_mtime}:large"
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

    def pip_install(
        self,
        *packages: str,
        find_links: Optional[str] = None,
        index_url: Optional[str] = None,
        extra_index_url: Optional[str] = None,
        pre: bool = False,
        extra_options: str = "",
    ) -> "ImageInstance":
        """
        Install Python packages using pip.

        Args:
            *packages: Package names to install (e.g., "requests", "numpy>=1.20")
            find_links: URL to look for packages (--find-links)
            index_url: Base URL of the Python Package Index (--index-url)
            extra_index_url: Extra URLs of package indexes (--extra-index-url)
            pre: Include pre-release versions (--pre)
            extra_options: Additional pip options as a string

        Returns:
            A new Image instance with the packages installed

        Example:
            image.pip_install("requests", "numpy>=1.20", pre=True)
        """
        if not packages:
            return self

        options = []
        if find_links:
            options.append(f"--find-links {find_links}")
        if index_url:
            options.append(f"--index-url {index_url}")
        if extra_index_url:
            options.append(f"--extra-index-url {extra_index_url}")
        if pre:
            options.append("--pre")
        if extra_options:
            options.append(extra_options)

        options_str = " ".join(options)
        packages_str = " ".join(packages)

        cmd = f"pip install {options_str} {packages_str}".strip()
        # Clean up multiple spaces
        cmd = " ".join(cmd.split())

        return self.run_commands(cmd)

    def apt_install(
        self,
        *packages: str,
        update: bool = True,
        clean: bool = True,
    ) -> "ImageInstance":
        """
        Install packages using apt-get (Debian/Ubuntu).

        Args:
            *packages: Package names to install
            update: Run apt-get update before installing (default True)
            clean: Clean up apt cache after installing (default True)

        Returns:
            A new Image instance with the packages installed

        Example:
            image.apt_install("git", "curl", "build-essential")
        """
        if not packages:
            return self

        packages_str = " ".join(packages)
        commands = []

        if update:
            commands.append("apt-get update")

        commands.append(f"apt-get install -y --no-install-recommends {packages_str}")

        if clean:
            commands.append("rm -rf /var/lib/apt/lists/*")

        # Combine into a single RUN command for smaller image layers
        cmd = " && ".join(commands)
        return self.run_commands(cmd)

    def apk_add(
        self,
        *packages: str,
        update: bool = True,
        no_cache: bool = True,
        clean: bool = True,
    ) -> "ImageInstance":
        """
        Install packages using apk (Alpine Linux).

        Args:
            *packages: Package names to install
            update: Run apk update before installing (default True)
            no_cache: Use --no-cache flag (default True, implies no cache cleanup needed)
            clean: Clean up apk cache after installing (default True, ignored if no_cache=True)

        Returns:
            A new Image instance with the packages installed

        Example:
            image.apk_add("git", "curl", "build-base")
        """
        if not packages:
            return self

        packages_str = " ".join(packages)
        commands = []

        if no_cache:
            commands.append(f"apk add --no-cache {packages_str}")
        else:
            if update:
                commands.append("apk update")
            commands.append(f"apk add {packages_str}")
            if clean:
                commands.append("rm -rf /var/cache/apk/*")

        cmd = " && ".join(commands)
        return self.run_commands(cmd)

    def npm_install(
        self,
        *packages: str,
        package_manager: str = "npm",
        global_install: bool = False,
        save_dev: bool = False,
    ) -> "ImageInstance":
        """
        Install Node.js packages using npm, yarn, pnpm, or bun.

        Args:
            *packages: Package names to install. If empty, installs from package.json
            package_manager: Package manager to use ("npm", "yarn", "pnpm", "bun")
            global_install: Install packages globally (default False)
            save_dev: Save as dev dependencies (default False)

        Returns:
            A new Image instance with the packages installed

        Example:
            # Install specific packages with npm
            image.npm_install("express", "lodash")

            # Install from package.json with yarn
            image.npm_install(package_manager="yarn")

            # Install global packages with pnpm
            image.npm_install("typescript", package_manager="pnpm", global_install=True)

            # Install with bun
            image.npm_install("elysia", package_manager="bun")
        """
        pm = package_manager.lower()
        pkgs = " ".join(packages)
        g, d = global_install, save_dev

        # Command builders: (install_cmd, add_cmd_with_packages)
        builders = {
            "npm": lambda: ("npm install", f"npm install {'-g ' if g else ''}{('--save-dev ' if d else '')}{pkgs}"),
            "yarn": lambda: ("yarn install", f"yarn {'global add' if g else 'add'} {('--dev ' if d and not g else '')}{pkgs}"),
            "pnpm": lambda: ("pnpm install", f"pnpm add {'-g ' if g else ''}{('-D ' if d else '')}{pkgs}"),
            "bun": lambda: ("bun install", f"bun add {'-g ' if g else ''}{('-d ' if d else '')}{pkgs}"),
        }

        if pm not in builders:
            raise ValueError(f"Invalid package manager: {pm}. Must be one of {set(builders.keys())}")

        install_cmd, add_cmd = builders[pm]()
        cmd = " ".join((add_cmd if packages else install_cmd).split())
        return self.run_commands(cmd)

    def gem_install(self, *packages: str, no_document: bool = True) -> "ImageInstance":
        """
        Install Ruby gems.

        Args:
            *packages: Gem names to install
            no_document: Skip documentation generation (default True)

        Returns:
            A new Image instance with the gems installed

        Example:
            image.gem_install("rails", "bundler")
        """
        if not packages:
            return self

        flags = "--no-document " if no_document else ""
        cmd = f"gem install {flags}{' '.join(packages)}"
        return self.run_commands(" ".join(cmd.split()))

    def cargo_install(self, *packages: str, locked: bool = False) -> "ImageInstance":
        """
        Install Rust packages using cargo.

        Args:
            *packages: Crate names to install
            locked: Use locked dependencies (default False)

        Returns:
            A new Image instance with the packages installed

        Example:
            image.cargo_install("ripgrep", "fd-find")
        """
        if not packages:
            return self

        flags = "--locked " if locked else ""
        cmd = f"cargo install {flags}{' '.join(packages)}"
        return self.run_commands(" ".join(cmd.split()))

    def go_install(self, *packages: str) -> "ImageInstance":
        """
        Install Go packages.

        Args:
            *packages: Package paths to install (e.g., "github.com/user/repo@latest")

        Returns:
            A new Image instance with the packages installed

        Example:
            image.go_install("github.com/golangci/golangci-lint/cmd/golangci-lint@latest")
        """
        if not packages:
            return self

        commands = [f"go install {pkg}" for pkg in packages]
        return self.run_commands(" && ".join(commands))

    def composer_install(
        self,
        *packages: str,
        no_dev: bool = False,
        optimize_autoloader: bool = False,
    ) -> "ImageInstance":
        """
        Install PHP packages using Composer.

        Args:
            *packages: Package names to install. If empty, installs from composer.json
            no_dev: Skip dev dependencies (default False)
            optimize_autoloader: Optimize autoloader (default False)

        Returns:
            A new Image instance with the packages installed

        Example:
            image.composer_install("laravel/framework", "guzzlehttp/guzzle")
        """
        flags = f"{'--no-dev ' if no_dev else ''}{'--optimize-autoloader ' if optimize_autoloader else ''}"
        if packages:
            cmd = f"composer require {flags}{' '.join(packages)}"
        else:
            cmd = f"composer install {flags}"
        return self.run_commands(" ".join(cmd.split()))

    def uv_install(
        self,
        *packages: str,
        system: bool = True,
        upgrade: bool = False,
    ) -> "ImageInstance":
        """
        Install Python packages using uv (fast Python package installer).

        Args:
            *packages: Package names to install
            system: Install to system Python (default True)
            upgrade: Upgrade packages if already installed (default False)

        Returns:
            A new Image instance with the packages installed

        Example:
            image.uv_install("requests", "pandas", "numpy")
        """
        if not packages:
            return self

        flags = f"{'--system ' if system else ''}{'--upgrade ' if upgrade else ''}"
        cmd = f"uv pip install {flags}{' '.join(packages)}"
        return self.run_commands(" ".join(cmd.split()))

    def pipx_install(self, *packages: str) -> "ImageInstance":
        """
        Install Python CLI applications using pipx.

        Args:
            *packages: Package names to install

        Returns:
            A new Image instance with the packages installed

        Example:
            image.pipx_install("black", "ruff", "poetry")
        """
        if not packages:
            return self

        commands = [f"pipx install {pkg}" for pkg in packages]
        return self.run_commands(" && ".join(commands))

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

        Note: The caller is responsible for cleaning up the temporary directory
        when finished. Use `shutil.rmtree(path.parent, ignore_errors=True)` to clean up.

        For automatic cleanup, consider using this pattern:
            build_dir = image.write_temp()
            try:
                # ... use build_dir ...
            finally:
                shutil.rmtree(build_dir.parent, ignore_errors=True)

        Returns:
            Path to the generated folder (parent is the temp directory to clean up)
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

        Raises:
            ValueError: If a file path escapes the build directory (Zip Slip protection)
        """
        build_dir = build_dir.resolve()
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for file_path in build_dir.rglob("*"):
                if file_path.is_file():
                    # Resolve to handle symlinks and get the real path
                    resolved_path = file_path.resolve()

                    # Zip Slip protection: ensure the resolved path is within build_dir
                    try:
                        resolved_path.relative_to(build_dir)
                    except ValueError:
                        raise ValueError(
                            f"Path traversal detected: {file_path} resolves outside build directory"
                        )

                    arcname = file_path.relative_to(build_dir)
                    zf.write(resolved_path, arcname)
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

        # Parse JSON response safely
        parsed_sandbox = None
        if response.status_code == 200:
            try:
                json_data = response.json()
                parsed_sandbox = Sandbox.from_dict(json_data)
            except (json.JSONDecodeError, ValueError):
                # Response is not valid JSON or cannot be parsed as Sandbox
                pass

        result = Response(
            status_code=HTTPStatus(response.status_code),
            content=response.content,
            headers=response.headers,
            parsed=parsed_sandbox,
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

        # Parse JSON response safely
        parsed_sandbox = None
        if response.status_code == 200:
            try:
                json_data = response.json()
                parsed_sandbox = Sandbox.from_dict(json_data)
            except (json.JSONDecodeError, ValueError):
                # Response is not valid JSON or cannot be parsed as Sandbox
                pass

        result = Response(
            status_code=HTTPStatus(response.status_code),
            content=response.content,
            headers=response.headers,
            parsed=parsed_sandbox,
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
            try:
                data = response.json()
                return data.get("status")
            except (json.JSONDecodeError, ValueError):
                return None
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
            try:
                data = response.json()
                return data.get("status")
            except (json.JSONDecodeError, ValueError):
                return None
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
                try:
                    sandbox = Sandbox.from_dict(final_response.json())
                    if sandbox:
                        return sandbox
                except (json.JSONDecodeError, ValueError):
                    pass

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
                try:
                    sandbox = Sandbox.from_dict(final_response.json())
                    if sandbox:
                        return sandbox
                except (json.JSONDecodeError, ValueError):
                    pass

            if response.parsed:
                return response.parsed

            raise RuntimeError(f"Failed to get sandbox '{name}' after deployment")

        finally:
            # Cleanup temp directory
            shutil.rmtree(build_dir.parent, ignore_errors=True)
