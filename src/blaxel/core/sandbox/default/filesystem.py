import asyncio
import io
import json
import logging
from pathlib import Path
from typing import Any, Callable, Dict, List, Union

import httpx

from ...common.settings import settings
from ..client.models import Directory, FileRequest, SuccessResponse
from ..types import (
    CopyResponse,
    SandboxConfiguration,
    SandboxFilesystemFile,
    WatchEvent,
)
from .action import SandboxAction

# Multipart upload constants
MULTIPART_THRESHOLD = 5 * 1024 * 1024  # 5MB
CHUNK_SIZE = 5 * 1024 * 1024  # 5MB per part
MAX_PARALLEL_UPLOADS = 3  # Number of parallel part uploads

logger = logging.getLogger(__name__)


class SandboxFileSystem(SandboxAction):
    def __init__(self, sandbox_config: SandboxConfiguration, process=None):
        super().__init__(sandbox_config)
        self.process = process

    async def mkdir(self, path: str, permissions: str = "0755") -> SuccessResponse:
        path = self.format_path(path)
        body = FileRequest(is_directory=True, permissions=permissions)

        client = self.get_client()
        response = await client.put(f"/filesystem/{path}", json=body.to_dict())
        try:
            data = json.loads(await response.aread())
            self.handle_response_error(response)
            return SuccessResponse.from_dict(data)
        finally:
            await response.aclose()

    async def write(self, path: str, content: str) -> SuccessResponse:
        path = self.format_path(path)

        # Calculate content size in bytes
        content_size = len(content.encode("utf-8"))

        # Use multipart upload for large files
        if content_size > MULTIPART_THRESHOLD:
            content_bytes = content.encode("utf-8")
            return await self._upload_with_multipart(path, content_bytes, "0644")

        # Use regular upload for small files
        body = FileRequest(content=content)

        client = self.get_client()
        response = await client.put(f"/filesystem/{path}", json=body.to_dict())
        try:
            data = json.loads(await response.aread())
            self.handle_response_error(response)
            return SuccessResponse.from_dict(data)
        finally:
            await response.aclose()

    async def write_binary(
        self, path: str, content: Union[bytes, bytearray, str]
    ) -> SuccessResponse:
        """Write binary content to a file.

        Args:
            path: The path in the sandbox to write to
            content: Binary content as bytes, bytearray, or string path to a local file

        Returns:
            SuccessResponse indicating success
        """
        path = self.format_path(path)

        # If content is a string, treat it as a file path and read it
        if isinstance(content, str):
            local_path = Path(content)
            content = local_path.read_bytes()
        # Convert bytearray to bytes if necessary
        elif isinstance(content, bytearray):
            content = bytes(content)

        # Use multipart upload for large files
        if len(content) > MULTIPART_THRESHOLD:
            return await self._upload_with_multipart(path, content, "0644")

        # Use regular upload for small files
        # Wrap binary content in BytesIO to provide file-like interface
        binary_file = io.BytesIO(content)

        # Prepare multipart form data
        files = {
            "file": (
                "binary-file.bin",
                binary_file,
                "application/octet-stream",
            ),
        }
        data = {"permissions": "0644", "path": path}

        # Use the fixed get_client method
        url = f"{self.url}/filesystem/{path}"
        headers = {**settings.headers, **self.sandbox_config.headers}

        client = self.get_client()
        response = await client.put(url, files=files, data=data, headers=headers)
        try:
            content_bytes = await response.aread()
            if not response.is_success:
                error_text = content_bytes.decode("utf-8", errors="ignore")
                raise Exception(f"Failed to write binary: {response.status_code} {error_text}")
            return SuccessResponse.from_dict(json.loads(content_bytes))
        finally:
            await response.aclose()

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

        client = self.get_client()
        response = await client.put(
            f"/filesystem/tree/{path}",
            json={"files": files_dict},
            headers={"Content-Type": "application/json"},
        )
        try:
            data = json.loads(await response.aread())
            self.handle_response_error(response)
            return Directory.from_dict(data)
        finally:
            await response.aclose()

    async def read(self, path: str) -> str:
        path = self.format_path(path)

        client = self.get_client()
        response = await client.get(f"/filesystem/{path}")
        try:
            data = json.loads(await response.aread())
            self.handle_response_error(response)
            if "content" in data:
                return data["content"]
            raise Exception("Unsupported file type")
        finally:
            await response.aclose()

    async def read_binary(self, path: str) -> bytes:
        """Read binary content from a file.

        Args:
            path: The path in the sandbox to read from

        Returns:
            Binary content as bytes
        """
        path = self.format_path(path)

        url = f"{self.url}/filesystem/{path}"
        headers = {
            **settings.headers,
            **self.sandbox_config.headers,
            "Accept": "application/octet-stream",
        }

        client = self.get_client()
        response = await client.get(url, headers=headers)
        try:
            content = await response.aread()
            self.handle_response_error(response)
            return content
        finally:
            await response.aclose()

    async def download(self, src: str, destination_path: str, mode: int = 0o644) -> None:
        """Download a file from the sandbox to the local filesystem.

        Args:
            src: The path in the sandbox to download from
            destination_path: The local path to save to
            mode: File permissions mode (default: 0o644)
        """
        content = await self.read_binary(src)
        local_path = Path(destination_path)
        local_path.write_bytes(content)
        local_path.chmod(mode)

    async def rm(self, path: str, recursive: bool = False) -> SuccessResponse:
        path = self.format_path(path)

        client = self.get_client()
        params = {"recursive": "true"} if recursive else {}
        response = await client.delete(f"/filesystem/{path}", params=params)
        try:
            data = json.loads(await response.aread())
            self.handle_response_error(response)
            return SuccessResponse.from_dict(data)
        finally:
            await response.aclose()

    async def ls(self, path: str) -> Directory:
        path = self.format_path(path)

        client = self.get_client()
        response = await client.get(f"/filesystem/{path}")
        try:
            data = json.loads(await response.aread())
            self.handle_response_error(response)
            if not ("files" in data or "subdirectories" in data):
                raise Exception('{"error": "Directory not found"}')
            return Directory.from_dict(data)
        finally:
            await response.aclose()

    async def find(
        self,
        path: str,
        type: str | None = None,
        patterns: List[str] | None = None,
        max_results: int | None = None,
        exclude_dirs: List[str] | None = None,
        exclude_hidden: bool | None = None,
    ):
        """Find files and directories.

        Args:
            path: Path to search in
            type: Type of search ('file' or 'directory')
            patterns: File patterns to include (e.g., ['*.py', '*.json'])
            max_results: Maximum number of results to return
            exclude_dirs: Directory names to skip
            exclude_hidden: Exclude hidden files and directories

        Returns:
            FindResponse with matching files/directories
        """
        path = self.format_path(path)

        params = {}
        if type is not None:
            params["type"] = type
        if patterns is not None and len(patterns) > 0:
            params["patterns"] = ",".join(patterns)
        if max_results is not None:
            params["maxResults"] = max_results
        if exclude_dirs is not None and len(exclude_dirs) > 0:
            params["excludeDirs"] = ",".join(exclude_dirs)
        if exclude_hidden is not None:
            params["excludeHidden"] = exclude_hidden

        url = f"{self.url}/filesystem-find/{path}"
        headers = {**settings.headers, **self.sandbox_config.headers}

        client = self.get_client()
        response = await client.get(url, params=params, headers=headers)
        try:
            data = json.loads(await response.aread())
            self.handle_response_error(response)

            from ..client.models.find_response import FindResponse

            return FindResponse.from_dict(data)
        finally:
            await response.aclose()

    async def grep(
        self,
        query: str,
        path: str = "/",
        case_sensitive: bool | None = None,
        context_lines: int | None = None,
        max_results: int | None = None,
        file_pattern: str | None = None,
        exclude_dirs: List[str] | None = None,
    ):
        """Search for text content inside files using ripgrep.

        Args:
            query: Text to search for
            path: Directory path to search in
            case_sensitive: Case sensitive search (default: false)
            context_lines: Number of context lines to include (default: 0)
            max_results: Maximum number of results to return (default: 100)
            file_pattern: File pattern to include (e.g., '*.py')
            exclude_dirs: Directory names to skip

        Returns:
            ContentSearchResponse with matching lines
        """
        path = self.format_path(path)

        params = {"query": query}
        if case_sensitive is not None:
            params["caseSensitive"] = case_sensitive
        if context_lines is not None:
            params["contextLines"] = context_lines
        if max_results is not None:
            params["maxResults"] = max_results
        if file_pattern is not None:
            params["filePattern"] = file_pattern
        if exclude_dirs is not None and len(exclude_dirs) > 0:
            params["excludeDirs"] = ",".join(exclude_dirs)

        url = f"{self.url}/filesystem-content-search/{path}"
        headers = {**settings.headers, **self.sandbox_config.headers}

        client = self.get_client()
        response = await client.get(url, params=params, headers=headers)
        try:
            data = json.loads(await response.aread())
            self.handle_response_error(response)

            from ..client.models.content_search_response import (
                ContentSearchResponse,
            )

            return ContentSearchResponse.from_dict(data)
        finally:
            await response.aclose()

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
        process = await self.process.exec({"command": f"cp -r {source} {destination}"})

        # Wait for process to complete
        process = await self.process.wait(process.pid, max_wait=max_wait, interval=100)

        # Check if process failed
        if process.status == "failed":
            logs = process.logs if hasattr(process, "logs") else "Unknown error"
            raise Exception(f"Could not copy {source} to {destination} cause: {logs}")

        return CopyResponse(message="Files copied", source=source, destination=destination)

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

    # Multipart upload helper methods
    async def _initiate_multipart_upload(
        self, path: str, permissions: str = "0644"
    ) -> Dict[str, Any]:
        """Initiate a multipart upload session."""
        path = self.format_path(path)
        url = f"{self.url}/filesystem-multipart/initiate/{path}"
        headers = {**settings.headers, **self.sandbox_config.headers}
        body = {"permissions": permissions}

        client = self.get_client()
        response = await client.post(url, json=body, headers=headers)
        try:
            data = json.loads(await response.aread())
            self.handle_response_error(response)
            return data
        finally:
            await response.aclose()

    async def _upload_part(self, upload_id: str, part_number: int, data: bytes) -> Dict[str, Any]:
        """Upload a single part of a multipart upload."""
        url = f"{self.url}/filesystem-multipart/{upload_id}/part"
        headers = {**settings.headers, **self.sandbox_config.headers}
        params = {"partNumber": part_number}

        # Prepare multipart form data with the file chunk
        files = {"file": ("part", io.BytesIO(data), "application/octet-stream")}

        client = self.get_client()
        response = await client.put(url, files=files, params=params, headers=headers)
        try:
            data = json.loads(await response.aread())
            self.handle_response_error(response)
            return data
        finally:
            await response.aclose()

    async def _complete_multipart_upload(
        self, upload_id: str, parts: List[Dict[str, Any]]
    ) -> SuccessResponse:
        """Complete a multipart upload by assembling all parts."""
        url = f"{self.url}/filesystem-multipart/{upload_id}/complete"
        headers = {**settings.headers, **self.sandbox_config.headers}
        body = {"parts": parts}

        client = self.get_client()
        response = await client.post(url, json=body, headers=headers)
        try:
            data = json.loads(await response.aread())
            self.handle_response_error(response)
            return SuccessResponse.from_dict(data)
        finally:
            await response.aclose()

    async def _abort_multipart_upload(self, upload_id: str) -> None:
        """Abort a multipart upload and clean up all parts."""
        url = f"{self.url}/filesystem-multipart/{upload_id}/abort"
        headers = {**settings.headers, **self.sandbox_config.headers}

        client = self.get_client()
        response = await client.delete(url, headers=headers)
        try:
            # Don't raise error if abort fails - we want to throw the original error
            if not response.is_success:
                print(f"Warning: Failed to abort multipart upload: {response.status_code}")
        finally:
            await response.aclose()

    async def _upload_with_multipart(
        self, path: str, data: bytes, permissions: str = "0644"
    ) -> SuccessResponse:
        """Upload a file using multipart upload for large files."""
        # Initiate multipart upload
        init_response = await self._initiate_multipart_upload(path, permissions)
        upload_id = init_response.get("uploadId")

        if not upload_id:
            raise Exception("Failed to get upload ID from initiate response")

        try:
            size = len(data)
            num_parts = (size + CHUNK_SIZE - 1) // CHUNK_SIZE  # Ceiling division
            parts: List[Dict[str, Any]] = []

            # Upload parts in batches for parallel processing
            for i in range(0, num_parts, MAX_PARALLEL_UPLOADS):
                batch_tasks = []

                for j in range(MAX_PARALLEL_UPLOADS):
                    if i + j >= num_parts:
                        break

                    part_number = i + j + 1
                    start = (part_number - 1) * CHUNK_SIZE
                    end = min(start + CHUNK_SIZE, size)
                    chunk = data[start:end]

                    batch_tasks.append(self._upload_part(upload_id, part_number, chunk))

                # Wait for batch to complete
                batch_results = await asyncio.gather(*batch_tasks)
                parts.extend(
                    [
                        {
                            "partNumber": r.get("partNumber"),
                            "etag": r.get("etag"),
                        }
                        for r in batch_results
                    ]
                )

            # Sort parts by partNumber to ensure correct order
            parts.sort(key=lambda p: p.get("partNumber", 0))

            # Complete the upload
            return await self._complete_multipart_upload(upload_id, parts)
        except Exception as error:
            # Abort the upload on failure
            try:
                await self._abort_multipart_upload(upload_id)
            except Exception as abort_error:
                # Log but don't throw - we want to throw the original error
                logger.warning(f"Failed to abort multipart upload: {abort_error}")
            raise error
