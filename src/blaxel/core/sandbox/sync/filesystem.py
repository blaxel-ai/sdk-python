import io
import json
import logging
import threading
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
from .action import SyncSandboxAction

logger = logging.getLogger(__name__)

# Multipart upload constants
MULTIPART_THRESHOLD = 5 * 1024 * 1024  # 5MB
CHUNK_SIZE = 5 * 1024 * 1024  # 5MB per part
MAX_PARALLEL_UPLOADS = 3  # Number of parallel part uploads


class SyncSandboxFileSystem(SyncSandboxAction):
    def __init__(self, sandbox_config: SandboxConfiguration, process=None):
        super().__init__(sandbox_config)
        self.process = process

    def mkdir(self, path: str, permissions: str = "0755") -> SuccessResponse:
        path = self.format_path(path)
        body = FileRequest(is_directory=True, permissions=permissions)
        with self.get_client() as client_instance:
            response = client_instance.put(f"/filesystem/{path}", json=body.to_dict())
            self.handle_response_error(response)
            return SuccessResponse.from_dict(response.json())

    def write(self, path: str, content: str) -> SuccessResponse:
        path = self.format_path(path)
        content_size = len(content.encode("utf-8"))
        if content_size > MULTIPART_THRESHOLD:
            content_bytes = content.encode("utf-8")
            return self._upload_with_multipart(path, content_bytes, "0644")
        body = FileRequest(content=content)
        with self.get_client() as client_instance:
            response = client_instance.put(f"/filesystem/{path}", json=body.to_dict())
            self.handle_response_error(response)
            return SuccessResponse.from_dict(response.json())

    def write_binary(self, path: str, content: Union[bytes, bytearray, str]) -> SuccessResponse:
        path = self.format_path(path)
        if isinstance(content, str):
            local_path = Path(content)
            content = local_path.read_bytes()
        elif isinstance(content, bytearray):
            content = bytes(content)
        if len(content) > MULTIPART_THRESHOLD:
            return self._upload_with_multipart(path, content, "0644")
        binary_file = io.BytesIO(content)
        files = {
            "file": (
                "binary-file.bin",
                binary_file,
                "application/octet-stream",
            ),
        }
        data = {"permissions": "0644", "path": path}
        url = f"{self.url}/filesystem/{path}"
        headers = {**settings.headers, **self.sandbox_config.headers}
        with self.get_client() as client_instance:
            response = client_instance.put(url, files=files, data=data, headers=headers)
            if not response.is_success:
                raise Exception(f"Failed to write binary: {response.status_code} {response.text}")
            return SuccessResponse.from_dict(response.json())

    def write_tree(
        self,
        files: List[Union[SandboxFilesystemFile, Dict[str, Any]]],
        destination_path: str | None = None,
    ) -> Directory:
        files_dict = {}
        for file in files:
            if isinstance(file, dict):
                file = SandboxFilesystemFile.from_dict(file)
            files_dict[file.path] = file.content
        path = destination_path or ""
        with self.get_client() as client_instance:
            response = client_instance.put(
                f"/filesystem/tree/{path}",
                json={"files": files_dict},
                headers={"Content-Type": "application/json"},
            )
            self.handle_response_error(response)
            return Directory.from_dict(response.json())

    def read(self, path: str) -> str:
        path = self.format_path(path)
        with self.get_client() as client_instance:
            response = client_instance.get(f"/filesystem/{path}")
            self.handle_response_error(response)
            data = response.json()
            if "content" in data:
                return data["content"]
            raise Exception("Unsupported file type")

    def read_binary(self, path: str) -> bytes:
        path = self.format_path(path)
        url = f"{self.url}/filesystem/{path}"
        headers = {
            **settings.headers,
            **self.sandbox_config.headers,
            "Accept": "application/octet-stream",
        }
        with self.get_client() as client_instance:
            response = client_instance.get(url, headers=headers)
            self.handle_response_error(response)
            return response.content

    def download(self, src: str, destination_path: str, mode: int = 0o644) -> None:
        content = self.read_binary(src)
        local_path = Path(destination_path)
        local_path.write_bytes(content)
        local_path.chmod(mode)

    def rm(self, path: str, recursive: bool = False) -> SuccessResponse:
        path = self.format_path(path)
        with self.get_client() as client_instance:
            params = {"recursive": "true"} if recursive else {}
            response = client_instance.delete(f"/filesystem/{path}", params=params)
            self.handle_response_error(response)
            return SuccessResponse.from_dict(response.json())

    def ls(self, path: str) -> Directory:
        path = self.format_path(path)
        with self.get_client() as client_instance:
            response = client_instance.get(f"/filesystem/{path}")
            self.handle_response_error(response)
            data = response.json()
            if not ("files" in data or "subdirectories" in data):
                raise Exception('{"error": "Directory not found"}')
            return Directory.from_dict(data)

    def cp(self, source: str, destination: str, max_wait: int = 180000) -> CopyResponse:
        if not self.process:
            raise Exception("Process instance not available. Cannot execute cp command.")
        process = self.process.exec({"command": f"cp -r {source} {destination}"})
        process = self.process.wait(process.pid, max_wait=max_wait, interval=100)
        if process.status == "failed":
            logs = process.logs if hasattr(process, "logs") else "Unknown error"
            raise Exception(f"Could not copy {source} to {destination} cause: {logs}")
        return CopyResponse(
            message="Files copied",
            source=source,
            destination=destination,
        )

    def watch(
        self,
        path: str,
        callback: Callable[[WatchEvent], None],
        options: Dict[str, Any] | None = None,
    ) -> Dict[str, Callable]:
        path = self.format_path(path)
        closed = threading.Event()
        if options is None:
            options = {}

        def run():
            params = {}
            if options.get("ignore"):
                params["ignore"] = ",".join(options["ignore"])
            url = f"{self.url}/watch/filesystem/{path}"
            headers = {**settings.headers, **self.sandbox_config.headers}
            with httpx.Client() as client_instance:
                with client_instance.stream("GET", url, params=params, headers=headers) as response:
                    if not response.is_success:
                        raise Exception(f"Failed to start watching: {response.status_code}")
                    buffer = ""
                    for chunk in response.iter_text():
                        if closed.is_set():
                            break
                        buffer += chunk
                        lines = buffer.split("\n")
                        buffer = lines.pop()  # Keep incomplete line in buffer
                        for line in lines:
                            line = line.strip()
                            if not line:
                                continue
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
                                        content = self.read(file_path)
                                        file_event.content = content
                                    except Exception:
                                        file_event.content = None
                                callback(file_event)
                            except json.JSONDecodeError:
                                continue
                            except Exception as e:
                                if options.get("on_error"):
                                    options["on_error"](e)

        thread = threading.Thread(target=run, daemon=True)
        thread.start()

        def close():
            closed.set()

        return {"close": close}

    def format_path(self, path: str) -> str:
        return path

    def _initiate_multipart_upload(self, path: str, permissions: str = "0644") -> Dict[str, Any]:
        path = self.format_path(path)
        url = f"{self.url}/filesystem-multipart/initiate/{path}"
        headers = {**settings.headers, **self.sandbox_config.headers}
        body = {"permissions": permissions}
        with self.get_client() as client_instance:
            response = client_instance.post(url, json=body, headers=headers)
            self.handle_response_error(response)
            return response.json()

    def _upload_part(self, upload_id: str, part_number: int, data: bytes) -> Dict[str, Any]:
        url = f"{self.url}/filesystem-multipart/{upload_id}/part"
        headers = {**settings.headers, **self.sandbox_config.headers}
        params = {"partNumber": part_number}
        files = {"file": ("part", io.BytesIO(data), "application/octet-stream")}
        with self.get_client() as client_instance:
            response = client_instance.put(url, files=files, params=params, headers=headers)
            self.handle_response_error(response)
            return response.json()

    def _complete_multipart_upload(
        self, upload_id: str, parts: List[Dict[str, Any]]
    ) -> SuccessResponse:
        url = f"{self.url}/filesystem-multipart/{upload_id}/complete"
        headers = {**settings.headers, **self.sandbox_config.headers}
        body = {"parts": parts}
        with self.get_client() as client_instance:
            response = client_instance.post(url, json=body, headers=headers)
            self.handle_response_error(response)
            return SuccessResponse.from_dict(response.json())

    def _abort_multipart_upload(self, upload_id: str) -> None:
        url = f"{self.url}/filesystem-multipart/{upload_id}/abort"
        headers = {**settings.headers, **self.sandbox_config.headers}
        with self.get_client() as client_instance:
            response = client_instance.delete(url, headers=headers)
            if not response.is_success:
                logger.warning(f"Failed to abort multipart upload: {response.status_code}")

    def _upload_with_multipart(
        self, path: str, data: bytes, permissions: str = "0644"
    ) -> SuccessResponse:
        init_response = self._initiate_multipart_upload(path, permissions)
        upload_id = init_response.get("uploadId")
        if not upload_id:
            raise Exception("Failed to get upload ID from initiate response")
        try:
            size = len(data)
            num_parts = (size + CHUNK_SIZE - 1) // CHUNK_SIZE
            parts: List[Dict[str, Any]] = []
            # Upload parts sequentially but in groups using threads for parallelism
            for i in range(0, num_parts, MAX_PARALLEL_UPLOADS):
                threads = []
                results: Dict[int, Dict[str, Any]] = {}

                def make_upload(part_number: int, chunk: bytes):
                    results[part_number] = self._upload_part(upload_id, part_number, chunk)

                for j in range(MAX_PARALLEL_UPLOADS):
                    if i + j >= num_parts:
                        break
                    part_number = i + j + 1
                    start = (part_number - 1) * CHUNK_SIZE
                    end = min(start + CHUNK_SIZE, size)
                    chunk = data[start:end]
                    t = threading.Thread(target=make_upload, args=(part_number, chunk))
                    threads.append(t)
                    t.start()
                for t in threads:
                    t.join()
                for part_number, r in results.items():
                    parts.append({"partNumber": part_number, "etag": r.get("etag")})
            parts.sort(key=lambda p: p.get("partNumber", 0))
            return self._complete_multipart_upload(upload_id, parts)
        except Exception as error:
            try:
                self._abort_multipart_upload(upload_id)
            except Exception as abort_error:
                logger.warning(f"Failed to abort multipart upload: {abort_error}")
            raise error
