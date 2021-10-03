# type: ignore
import asyncio
import typing as t

import asyncpg


_AsyncPGDatabaseT = t.TypeVar("_AsyncPGDatabaseT", bound="AsyncPGDatabase")


class AsyncPGDatabase(object):
    """A database wrapper for postgresql"""

    def __init__(self: _AsyncPGDatabaseT) -> None:
        raise NotImplemented
