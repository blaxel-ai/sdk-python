"""Shared by the async and sync ``read_tree``: the error type and the bounded reads."""

import asyncio
from collections.abc import Awaitable, Callable, Iterator
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
from typing import Any, Literal
from urllib.parse import quote


class FilesystemReadTreeError(Exception):
    """Raised by ``read_tree`` on any failure. No partial contents are returned.

    ``code`` is ``MAX_FILES``, ``DISCOVERY`` or ``READ``, ``root`` is the directory passed
    to ``read_tree`` and ``path`` is the relative path that could not be read (``READ``
    only). The underlying error, if any, is ``__cause__``.
    """

    def __init__(
        self,
        message: str,
        code: Literal["MAX_FILES", "DISCOVERY", "READ"],
        root: str,
        path: str | None = None,
    ):
        super().__init__(message)
        self.code = code
        self.root = root
        self.path = path


@contextmanager
def _wrap(code: Literal["DISCOVERY", "READ"], root: str, path: str | None = None) -> Iterator[None]:
    try:
        yield
    except Exception as cause:
        where = f" {path}" if path else ""
        raise FilesystemReadTreeError(
            f"read_tree {code}{where}: {cause}", code, root, path
        ) from cause


def _check(max_files: int, concurrency: int) -> None:
    # find returns at most 1000 matches, so a higher cap could not detect overflow.
    if max_files > 999:
        raise ValueError("max_files must be at most 999")
    if concurrency < 1:
        raise ValueError("concurrency must be at least 1")


def _paths(found: Any, root: str, max_files: int) -> list[str]:
    paths = sorted(match.path for match in found.matches)
    if len(paths) > max_files:
        raise FilesystemReadTreeError(
            f"read_tree MAX_FILES: more than {max_files} files match", "MAX_FILES", root
        )
    return paths


def _read_path(root: str, member: str) -> str:
    # ``read`` does not encode its path, so encode the root and the names ``find`` returned.
    return quote(f"{root.rstrip('/')}/{member}")


async def _read_tree_async(
    root: str,
    max_files: int,
    concurrency: int,
    find: Callable[[int], Awaitable[Any]],
    read: Callable[[str], Awaitable[str]],
) -> dict[str, str]:
    _check(max_files, concurrency)
    with _wrap("DISCOVERY", root):
        found = await find(max_files + 1)
    paths = _paths(found, root, max_files)
    gate = asyncio.Semaphore(concurrency)

    async def read_one(member: str) -> str:
        async with gate:
            with _wrap("READ", root, member):
                return await read(_read_path(root, member))

    tasks = [asyncio.ensure_future(read_one(member)) for member in paths]
    try:
        return dict(zip(paths, await asyncio.gather(*tasks)))
    finally:
        # After a failure, stop the reads that have not finished.
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)


def _read_tree_sync(
    root: str,
    max_files: int,
    concurrency: int,
    find: Callable[[int], Any],
    read: Callable[[str], str],
) -> dict[str, str]:
    _check(max_files, concurrency)
    with _wrap("DISCOVERY", root):
        found = find(max_files + 1)
    paths = _paths(found, root, max_files)

    def read_one(member: str) -> str:
        with _wrap("READ", root, member):
            return read(_read_path(root, member))

    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = {pool.submit(read_one, member): member for member in paths}
        try:
            contents = {futures[future]: future.result() for future in as_completed(futures)}
        finally:
            # After a failure, start no more reads; the ones running finish first.
            pool.shutdown(cancel_futures=True)
    return {member: contents[member] for member in paths}
