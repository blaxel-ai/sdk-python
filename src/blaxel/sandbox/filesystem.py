import asyncio
from typing import Dict

from ..common.settings import settings
from .base import SandboxHandleBase
from .client.api.filesystem.delete_filesystem_path import (
    asyncio_detailed as delete_filesystem_by_path,
)
from .client.api.filesystem.get_filesystem_path import asyncio_detailed as get_filesystem_by_path
from .client.api.filesystem.put_filesystem_path import asyncio_detailed as put_filesystem_by_path
from .client.client import client
from .client.models import Directory, FileRequest, SuccessResponse


class SandboxFileSystem(SandboxHandleBase):
    def __init__(self, sandbox):
        super().__init__(sandbox)
        self.client = client.with_base_url(self.url).with_headers(settings.headers)

    async def mkdir(self, path: str, permissions: str = "0755") -> SuccessResponse:
        path = self.format_path(path)
        body = FileRequest(is_directory=True, permissions=permissions)
        response = await put_filesystem_by_path(path=path, client=self.client, body=body)
        self.handle_response(response)
        return response.parsed

    async def write(self, path: str, content: str) -> SuccessResponse:
        path = self.format_path(path)
        body = FileRequest(content=content)
        response = await put_filesystem_by_path(path=path, client=self.client, body=body)
        self.handle_response(response)
        return response.parsed

    async def read(self, path: str) -> str:
        path = self.format_path(path)
        response = await get_filesystem_by_path(path=path, client=self.client)
        self.handle_response(response)
        if "content" not in response.parsed.additional_properties:
            raise Exception('{"error": "File not found"}')
        return response.parsed.additional_properties["content"]

    async def rm(self, path: str, recursive: bool = False) -> SuccessResponse:
        path = self.format_path(path)
        response = await delete_filesystem_by_path(path=path, client=self.client, recursive=recursive)
        self.handle_response(response)
        return response.parsed

    async def ls(self, path: str) -> Directory:
        path = self.format_path(path)
        response = await get_filesystem_by_path(path=path, client=self.client)
        self.handle_response(response)
        if not hasattr(response.parsed, "files") and not hasattr(response.parsed, "subdirectories"):
            raise Exception('{"error": "Directory not found"}')
        return response.parsed

    async def cp(self, source: str, destination: str) -> Dict[str, str]:
        source = self.format_path(source)
        destination = self.format_path(destination)
        response = await get_filesystem_by_path(path=source, client=self.client)
        self.handle_response(response)
        data = response.parsed
        if "content" in data.additional_properties:
            await self.write(destination, data.additional_properties["content"])
            return {
                "message": "File copied successfully",
                "source": source,
                "destination": destination,
            }
        elif hasattr(data, "subdirectories") or hasattr(data, "files"):
            # Create destination directory
            await self.mkdir(destination)
            # Process subdirectories in batches of 5
            subdirectories = getattr(data, "subdirectories", []) or []
            for i in range(0, len(subdirectories), 5):
                batch = subdirectories[i:i+5]
                await asyncio.gather(*[
                    self.cp(
                        getattr(subdir, "path", f"{source}/{getattr(subdir, 'path', '')}"),
                        f"{destination}/{getattr(subdir, 'path', '')}"
                    ) for subdir in batch
                ])
            # Process files in batches of 10
            files = getattr(data, "files", []) or []
            for i in range(0, len(files), 10):
                batch = files[i:i+10]
                await asyncio.gather(*[
                    self.write(
                        f"{destination}/{getattr(file, 'path', '')}",
                        await self.read(getattr(file, "path", f"{source}/{getattr(file, 'path', '')}"))
                    ) for file in batch
                ])
            return {
                "message": "Directory copied successfully",
                "source": source,
                "destination": destination,
            }
        raise Exception("Unsupported file type")

    def format_path(self, path: str) -> str:
        if path == "/":
            return "%2F"
        if path.startswith("/"):
            path = path[1:]
        return path