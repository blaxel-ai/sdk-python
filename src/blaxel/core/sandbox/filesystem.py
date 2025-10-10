import asyncio
import io
import json
from typing import Any, Callable, Dict, List, Union

import httpx

from ..common.settings import settings
from .action import SandboxAction
from .client.models import Directory, FileRequest, SuccessResponse
from .types import CopyResponse, SandboxConfiguration, SandboxFilesystemFile, WatchEvent


class SandboxFileSystem(SandboxAction):
    def __init__(self, sandbox_config: SandboxConfiguration, process=None):
        super().__init__(sandbox_config)
        self.process = process

    async def mkdir(self, path: str, permissions: str = "0755") -> SuccessResponse:
        path = self.format_path(path)
        body = FileRequest(is_directory=True, permissions=permissions)

        async with self.get_client() as client_instance:
            response = await client_instance.put(f"/filesystem/{path}", json=body.to_dict())
            self.handle_response_error(response)
            return SuccessResponse.from_dict(response.json())

    async def write(self, path: str, content: str) -> SuccessResponse:
        path = self.format_path(path)
        body = FileRequest(content=content)

        async with self.get_client() as client_instance:
            response = await client_instance.put(f"/filesystem/{path}", json=body.to_dict())
            self.handle_response_error(response)
            return SuccessResponse.from_dict(response.json())

    async def write_binary(self, path: str, content: Union[bytes, bytearray]) -> SuccessResponse:
        """Write binary content to a file."""
        path = self.format_path(path)

        # Convert bytearray to bytes if necessary
        if isinstance(content, bytearray):
            content = bytes(content)

        # Wrap binary content in BytesIO to provide file-like interface
        binary_file = io.BytesIO(content)

        # Prepare multipart form data
        files = {
            "file": ("binary-file.bin", binary_file, "application/octet-stream"),
        }
        data = {"permissions": "0644", "path": path}

        # Use the fixed get_client method
        url = f"{self.url}/filesystem/{path}"
        headers = {**settings.headers, **self.sandbox_config.headers}

        async with self.get_client() as client_instance:
            response = await client_instance.put(url, files=files, data=data, headers=headers)

            if not response.is_success:
                raise Exception(f"Failed to write binary: {response.status_code} {response.text}")

            return SuccessResponse.from_dict(response.json())

    async def write_tree(
        self,
        files: List[Union[SandboxFilesystemFile, Dict[str, Any]]],
        destination_path: str | None = None,
    ) -> Directory:
        """Write multiple files in a tree structure."""
        files_dict = {}
        for file in files:
            if isinstance(file, dict):
                file = SandboxFilesystemFile.from_dict(file)
            files_dict[file.path] = file.content

        path = destination_path or ""

        async with self.get_client() as client_instance:
            response = await client_instance.put(
                f"/filesystem/tree/{path}",
                json={"files": files_dict},
                headers={"Content-Type": "application/json"},
            )
            self.handle_response_error(response)
            return Directory.from_dict(response.json())

    async def read(self, path: str) -> str:
        path = self.format_path(path)

        async with self.get_client() as client_instance:
            response = await client_instance.get(f"/filesystem/{path}")
            self.handle_response_error(response)

            data = response.json()
            if "content" in data:
                return data["content"]
            raise Exception("Unsupported file type")

    async def rm(self, path: str, recursive: bool = False) -> SuccessResponse:
        path = self.format_path(path)

        async with self.get_client() as client_instance:
            params = {"recursive": "true"} if recursive else {}
            response = await client_instance.delete(f"/filesystem/{path}", params=params)
            self.handle_response_error(response)
            return SuccessResponse.from_dict(response.json())

    async def ls(self, path: str) -> Directory:
        path = self.format_path(path)

        async with self.get_client() as client_instance:
            response = await client_instance.get(f"/filesystem/{path}")
            self.handle_response_error(response)

            data = response.json()
            if not ("files" in data or "subdirectories" in data):
                raise Exception('{"error": "Directory not found"}')
            return Directory.from_dict(data)

    async def cp(self, source: str, destination: str, max_wait: int = 180000) -> CopyResponse:
        """Copy files or directories using the cp command.

        Args:
            source: Source path
            destination: Destination path
            max_wait: Maximum time to wait for the copy operation in milliseconds (default: 180000)
        """
        if not self.process:
            raise Exception("Process instance not available. Cannot execute cp command.")

        # Execute cp -r command
        process = await self.process.exec({
            "command": f"cp -r {source} {destination}"
        })

        # Wait for process to complete
        process = await self.process.wait(process.pid, max_wait=max_wait, interval=100)

        # Check if process failed
        if process.status == "failed":
            logs = process.logs if hasattr(process, "logs") else "Unknown error"
            raise Exception(f"Could not copy {source} to {destination} cause: {logs}")

        return CopyResponse(
            message="Files copied",
            source=source,
            destination=destination
        )

    def watch(
        self,
        path: str,
        callback: Callable[[WatchEvent], None],
        options: Dict[str, Any] | None = None,
    ) -> Dict[str, Callable]:
        """Watch for file system changes."""
        path = self.format_path(path)
        closed = False

        if options is None:
            options = {}

        async def start_watching():
            nonlocal closed
            params = {}
            if options.get("ignore"):
                params["ignore"] = ",".join(options["ignore"])

            url = f"{self.url}/watch/filesystem/{path}"
            headers = {**settings.headers, **self.sandbox_config.headers}
            async with httpx.AsyncClient() as client_instance:
                async with client_instance.stream(
                    "GET", url, params=params, headers=headers
                ) as response:
                    if not response.is_success:
                        raise Exception(f"Failed to start watching: {response.status_code}")
                    buffer = ""
                    async for chunk in response.aiter_text():
                        if closed:
                            break

                        buffer += chunk
                        lines = buffer.split("\n")
                        buffer = lines.pop()  # Keep incomplete line in buffer

                        for line in lines:
                            line = line.strip()
                            if not line:
                                continue

                            # Skip keepalive messages
                            if line.startswith("[keepalive]"):
                                continue

                            try:
                                file_event_data = json.loads(line)
                                file_event = WatchEvent(
                                    op=file_event_data.get("op", ""),
                                    path=file_event_data.get("path", ""),
                                    name=file_event_data.get("name", ""),
                                    content=file_event_data.get("content"),
                                )

                                if options.get("with_content") and file_event.op in [
                                    "CREATE",
                                    "WRITE",
                                ]:
                                    try:
                                        file_path = file_event.path
                                        if file_path.endswith("/"):
                                            file_path = file_path + file_event.name
                                        else:
                                            file_path = file_path + "/" + file_event.name

                                        content = await self.read(file_path)
                                        file_event.content = content
                                    except:
                                        file_event.content = None

                                await callback(file_event)
                            except json.JSONDecodeError:
                                continue
                            except Exception as e:
                                if options.get("on_error"):
                                    options["on_error"](e)

        # Start watching in the background
        task = asyncio.create_task(start_watching())

        def close():
            nonlocal closed
            closed = True
            task.cancel()

        return {"close": close}

    def format_path(self, path: str) -> str:
        """Format path for filesystem operations.

        Simplified to match TypeScript behavior - returns path as-is.
        """
        return path
