import asyncio
import typing as t

import aiofiles
import asyncpg

from ottbot import Config


class AsyncPGDatabase:
    """Wrapper class for AsyncPG Database access."""

    def __init__(self) -> None:
        self.calls: int = 0
        self.db: str = Config["DB_NAME"]
        self.host: str = "127.0.0.1"
        self.user: str = Config["PG_USERNAME"]
        self.password: str = Config["PG_PASSWORD"]
        self.port: int = 5432
        self.schema: str = "./ottbot/data/static/schema.sql"

    async def connect(self) -> None:
        """Opens a connection pool."""

        self.pool = await asyncpg.create_pool(
            user=self.user,
            host=self.host,
            port=self.port,
            database=self.db,
            password=self.password,
            loop=asyncio.get_running_loop(),
        )

        await self.scriptexec(self.schema)

    async def close(self) -> None:
        """Closes the connection pool"""
        if self.pool:
            await self.pool.close()
        else:
            raise ValueError("Pool is not defined")

    @staticmethod
    def with_connection(func: t.Callable[..., t.Any]) -> t.Callable[..., t.Any]:  # type: ignore
        """A decorator used to acquire a connection from the pool"""

        async def wrapper(self: "AsyncPGDatabase", *args: t.Any) -> t.Any:
            if self.pool is None:
                return
            async with self.pool.acquire() as conn:
                self.calls += 1
                return await func(self, *args, conn=conn)

        return wrapper

    @with_connection
    async def fetch(self, q: str, *values: t.Any, conn: asyncpg.Connection) -> t.Optional[t.Any]:
        """Read 1 field of applicable data"""

        query = await conn.prepare(q)
        return await query.fetchval(*values)

    @with_connection
    async def row(self, q: str, *values: t.Any, conn: asyncpg.Connection) -> t.Optional[t.List[t.Any]]:
        """Read 1 row of applicable data"""

        query = await conn.prepare(q)
        if data := await query.fetchrow(*values):
            return [r for r in data]

        return None

    @with_connection
    async def rows(self, q: str, *values: t.Any, conn: asyncpg.Connection) -> t.Optional[t.List[t.Iterable[t.Any]]]:
        """Read all rows of applicable data"""

        query = await conn.prepare(q)
        if data := await query.fetch(*values):
            return [*map(lambda r: tuple(r.values())[0], data)]

        return None

    @with_connection
    async def column(self, q: str, *values: t.Any, conn: asyncpg.Connection) -> t.List[t.Any]:
        """Read a single column of applicable data."""
        query = await conn.prepare(q)
        return [r[0] for r in await query.fetch(*values)]

    @with_connection
    async def execute(self, q: str, *values: t.Any, conn: asyncpg.Connection) -> None:
        """Execute a write operation on the database"""
        query = await conn.prepare(q)
        await query.fetch(*values)

    @with_connection
    async def executemany(self, q: str, values: t.List[t.Iterable[t.Any]], conn: asyncpg.Connection) -> None:
        """Execute a write operation for each set of values"""
        query = await conn.prepare(q)
        await query.executemany(values)

    @with_connection
    async def scriptexec(self, path: str, conn: asyncpg.Connection) -> None:
        """Execute an sql script at a given path."""
        async with aiofiles.open(path, "r", encoding="utf-8") as script:
            await conn.execute((await script.read()))
