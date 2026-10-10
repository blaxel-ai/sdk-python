"""Shared by the async and sync ``read_tree``: the request and the response mapping."""

from typing import Any
from urllib.parse import quote


def _tree_request(
    path: str,
    patterns: list[str] | None,
    exclude_dirs: list[str] | None,
    exclude_hidden: bool | None,
    max_files: int | None,
    max_bytes: int | None,
) -> tuple[str, dict[str, Any]]:
    params: dict[str, Any] = {"recursive": "true", "content": "true"}
    if patterns:
        params["patterns"] = ",".join(patterns)
    if exclude_dirs:
        params["excludeDirs"] = ",".join(exclude_dirs)
    if exclude_hidden is not None:
        params["excludeHidden"] = "true" if exclude_hidden else "false"
    if max_files is not None:
        params["maxFiles"] = max_files
    if max_bytes is not None:
        params["maxBytes"] = max_bytes
    return f"/filesystem/tree/{quote(path)}", params


def _tree_files(data: dict[str, Any]) -> dict[str, str]:
    # An older sandbox API ignores the query and lists only direct children,
    # without ``recursive``. Fail instead of returning that as the whole tree.
    if data.get("recursive") is not True:
        raise RuntimeError(
            "read_tree needs a newer sandbox API: this sandbox does not support "
            "recursive tree reads; update its image"
        )
    root = data.get("path") or "/"
    prefix = root if root.endswith("/") else f"{root}/"
    files = {}
    for file in data.get("files") or []:
        content = file.get("content")
        path = file.get("path") or ""
        if isinstance(content, str) and path.startswith(prefix):
            files[path[len(prefix) :]] = content
    return dict(sorted(files.items()))
