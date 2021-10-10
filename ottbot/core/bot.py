import asyncio
import logging
import os
import time
import typing as t
from pathlib import Path

import hikari
import sake
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ottbot.abc.ibot import IBot
from ottbot.config import Config
from ottbot.core.utils import BetterTimedRotatingFileHandler, Embeds, Errors
from ottbot.core.client import OttClient

_BotT = t.TypeVar("_BotT", bound="OttBot")
EventT = t.Union[
    hikari.StartingEvent,
    hikari.StartedEvent,
    hikari.StoppingEvent,
    hikari.StoppedEvent,
]

SERVER_ID: int = 545984256640286730


class OttBot(hikari.GatewayBot, IBot):
    """Main Bot Class"""

    __slots__: tuple = (*hikari.GatewayBot.__slots__, "client", "guilds")

    def __init__(self: _BotT, version: str = "") -> None:
        self._dynamic = os.path.join(".", "ottbot", "data", "dynamic")
        self._static = os.path.join(".", "ottbot", "data", "static")
        self._log = os.path.join(".", "ottbot", "data", "logs")

        self.version = version

        self.scheduler = AsyncIOScheduler()
        self.errors = Errors()
        self.embeds = Embeds()

        super().__init__(token=self._get_token(), intents=hikari.Intents.ALL)
        self.guilds: list[hikari.OwnGuild] = []

    def _get_token(self) -> str:
        if isinstance(token := Config["TOKEN"], str):
            return token
        raise ValueError("Invalid token in .env file")

    def create_client(self: _BotT) -> None:
        """Creates a client and adds it to the `client` attribute"""
        self.client: OttClient = OttClient.from_gateway_bot(
            self, set_global_commands=SERVER_ID
        )
        self.client.bot = self
        self.client.load_modules_()

    async def init_cache(self):
        cache: sake.redis.RedisCache = sake.redis.RedisCache(
            self, None, address="redis://127.0.0.1"
        )
        try:
            await cache.open()
        except ConnectionRefusedError as e:
            logging.warning(f"Redis Error: {e}")
        except Exception as e:
            logging.critical(e)

    def run(self):
        """Create the client, subscribe to important events, and run the bot"""
        self.create_client()
        subscriptions: dict[t.Any, t.Callable[..., t.Coroutine[t.Any, t.Any, None]]] = {
            hikari.StartingEvent: self.on_starting,
            hikari.StartedEvent: self.on_started,
            hikari.StoppingEvent: self.on_stopping,
        }
        [self.event_manager.subscribe(key, subscriptions[key]) for key in subscriptions]

        super().run(
            activity=hikari.Activity(
                name=f"/help | {self.version}", type=hikari.ActivityType.WATCHING
            )
        )

    def logging_config(self) -> None:
        """Logging configuration for the bot"""

        btrfh = BetterTimedRotatingFileHandler(path=self._log)
        ff = logging.Formatter(
            f"[%(asctime)s] %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        btrfh.setFormatter(ff)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(btrfh)

    async def on_starting(self: _BotT, event: hikari.StartingEvent) -> None:
        """Runs before bot is connected. Blocks on_started until complete."""

        logging.info("Connecting to redis server")
        await self.init_cache()

    async def on_started(self: _BotT, event: hikari.StartedEvent) -> None:
        """Runs once bot is fully connected"""
        self.client.scheduler.start()

        async for guild in self.rest.fetch_my_guilds():
            self.guilds.append(guild)

        logging.info("Bot ready")

    async def on_stopping(self: _BotT, event: hikari.StoppingEvent) -> None:
        """Runs at the beginning of shutdown sequence"""
        self.client.scheduler.shutdown()
        self.dispatch

    async def on_guild_available(
        self: _BotT, event: hikari.GuildAvailableEvent
    ) -> None:
        ...
