from collections.abc import AsyncIterator, Awaitable, Callable, Iterator
from typing import Any, Generic, TypeVar

from .types import UNSET, Unset

T = TypeVar("T")
RawPage = TypeVar("RawPage")

DEFAULT_PAGE_LIMIT = 50


def split_list_response(src: Any) -> tuple[list[Any], Any, dict[str, Any]]:
    if not src:
        return [], UNSET, {}
    if isinstance(src, list):
        return src, UNSET, {}

    data = src.copy()
    items = data.pop("data", UNSET)
    meta = data.pop("meta", UNSET)
    return list(items or []), meta, data


def get_page_data(page: Any) -> list[Any]:
    if page is None:
        return []
    if isinstance(page, list):
        return page

    data = getattr(page, "data", UNSET)
    if data is UNSET or data is None:
        return []
    return list(data)


def get_page_meta(page: Any) -> Any:
    if page is None or isinstance(page, list):
        return UNSET
    return getattr(page, "meta", UNSET)


def _has_more(meta: Any) -> bool:
    return meta is not UNSET and meta is not None and bool(getattr(meta, "has_more", False))


def _next_cursor(meta: Any) -> str | None:
    if not _has_more(meta):
        return None

    next_cursor = getattr(meta, "next_cursor", None)
    if next_cursor is UNSET or next_cursor == "":
        return None
    return next_cursor


class PaginatedList(list[T], Generic[T]):
    """A single cursor-paginated page returned by a list endpoint."""

    def __init__(
        self,
        data: list[T] | None = None,
        *,
        meta: Any = UNSET,
        fetch_next: Callable[[str], "PaginatedList[T]"] | None = None,
    ):
        super().__init__(data or [])
        self.meta = meta
        self._fetch_next = fetch_next

    @property
    def data(self) -> list[T]:
        return self

    @property
    def has_more(self) -> bool:
        return _has_more(self.meta)

    @property
    def next_cursor(self) -> str | None:
        return _next_cursor(self.meta)

    @property
    def is_empty(self) -> bool:
        return len(self) == 0

    def next_page(self) -> "PaginatedList[T]":
        if not self.next_cursor or self._fetch_next is None:
            return PaginatedList([])
        return self._fetch_next(self.next_cursor)

    def auto_paging_iter(self) -> Iterator[T]:
        page: PaginatedList[T] = self
        while True:
            yield from page
            if not page.has_more:
                break
            page = page.next_page()
            if page.is_empty:
                break


class AsyncPaginatedList(list[T], Generic[T]):
    """A single cursor-paginated page returned by an async list endpoint."""

    def __init__(
        self,
        data: list[T] | None = None,
        *,
        meta: Any = UNSET,
        fetch_next: Callable[[str], Awaitable["AsyncPaginatedList[T]"]] | None = None,
    ):
        super().__init__(data or [])
        self.meta = meta
        self._fetch_next = fetch_next

    @property
    def data(self) -> list[T]:
        return self

    @property
    def has_more(self) -> bool:
        return _has_more(self.meta)

    @property
    def next_cursor(self) -> str | None:
        return _next_cursor(self.meta)

    @property
    def is_empty(self) -> bool:
        return len(self) == 0

    async def next_page(self) -> "AsyncPaginatedList[T]":
        if not self.next_cursor or self._fetch_next is None:
            return AsyncPaginatedList([])
        return await self._fetch_next(self.next_cursor)

    async def auto_paging_iter(self) -> AsyncIterator[T]:
        page: AsyncPaginatedList[T] = self
        while True:
            for item in page:
                yield item
            if not page.has_more:
                break
            page = await page.next_page()
            if page.is_empty:
                break


def make_paginated_list(
    page: RawPage,
    *,
    mapper: Callable[[Any], T],
    fetch_next: Callable[[str], PaginatedList[T]] | None = None,
) -> PaginatedList[T]:
    return PaginatedList(
        [mapper(item) for item in get_page_data(page)],
        meta=get_page_meta(page),
        fetch_next=fetch_next,
    )


def make_async_paginated_list(
    page: RawPage,
    *,
    mapper: Callable[[Any], T],
    fetch_next: Callable[[str], Awaitable[AsyncPaginatedList[T]]] | None = None,
) -> AsyncPaginatedList[T]:
    return AsyncPaginatedList(
        [mapper(item) for item in get_page_data(page)],
        meta=get_page_meta(page),
        fetch_next=fetch_next,
    )


def normalize_cursor(cursor: str | None) -> str | Unset:
    return cursor if cursor is not None else UNSET
