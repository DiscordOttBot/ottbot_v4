import asyncio
import logging
import os
import time
import typing as t
from pathlib import Path

import hikari
import sake
import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from ottbot.abc.ibot import IBot
from ottbot.config import Config
from ottbot.core.client import OttClient
from ottbot.core.utils import (
    BetterTimedRotatingFileHandler,
    Embeds,
    Errors,
    HikariFormatter,
)

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

    __slots__: tuple = (
        *hikari.GatewayBot.__slots__,
        "client",
        "embeds",
        "errors",
        "guilds",
        "version",
        "_dynamic",
        "_static",
        "_log",
    )

    def __init__(self: _BotT, version: str = "") -> None:
        self._dynamic = os.path.join(".", "ottbot", "data", "dynamic")
        self._static = os.path.join(".", "ottbot", "data", "static")
        self._log = os.path.join(".", "ottbot", "data", "logs")

        self.version: str = version

        self.scheduler: AsyncIOScheduler = AsyncIOScheduler()
        self.errors: Errors = Errors()
        self.embeds: Embeds = Embeds()

        self.guilds: list[hikari.OwnGuild] = []
        self.init_logger()

        super().__init__(
            token=self._get_token(), intents=hikari.Intents.ALL, logs="DEBUG"
        )

    def _get_token(self: _BotT) -> str:
        if isinstance(token := Config["TOKEN"], str):
            return token
        raise ValueError("Invalid token in .env file")

    def create_client(self: _BotT) -> None:
        """Creates a tanjun client and dynamically links the bot and the client"""
        self.client: OttClient = OttClient.from_gateway_bot(
            self, set_global_commands=SERVER_ID
        )
        self.client.bot = self
        self.client.load_modules_()

    async def init_cache(self: _BotT):
        cache: sake.redis.RedisCache = sake.redis.RedisCache(
            self, None, address="redis://127.0.0.1"
        )
        try:
            await cache.open()
        except ConnectionRefusedError as e:
            logging.warning(f"Redis Error: {e}")
        except Exception as e:
            logging.critical(e)

    def run(self: _BotT):
        """Create the client, subscribe to important events, and run the bot.

        When running an API along side the bot, use `await bot.start()` and `await bot.close()` on api events instead."""

        self.create_client()
        subscriptions: dict[t.Any, t.Callable[..., t.Coroutine[t.Any, t.Any, None]]] = {
            hikari.StartingEvent: self.on_starting,
            hikari.StartedEvent: self.on_started,
            hikari.StoppingEvent: self.on_stopping,
        }
        [self.event_manager.subscribe(key, subscriptions[key]) for key in subscriptions]

        self.logger.info("Bot started")

        super().run(
            activity=hikari.Activity(
                name=f"/help | {self.version}", type=hikari.ActivityType.WATCHING
            )
        )

    async def start(self: _BotT) -> None:

        self.logger.info("Starting Bot")

        self.create_client()

        subscriptions: dict[t.Any, t.Callable[..., t.Coroutine[t.Any, t.Any, None]]] = {
            hikari.StartingEvent: self.on_starting,
            hikari.StartedEvent: self.on_started,
            hikari.StoppingEvent: self.on_stopping,
        }
        [self.event_manager.subscribe(key, subscriptions[key]) for key in subscriptions]

        await super().start(
            activity=hikari.Activity(
                name=f"/help | {self.version}", type=hikari.ActivityType.WATCHING
            )
        )

    def init_logger(self: _BotT, log_level: int = logging.DEBUG) -> None:
        """Initializes the logger for the bot"""

        file_fmt = logging.Formatter(
            f"[%(asctime)s.%(msecs)03d] %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        btrfh = BetterTimedRotatingFileHandler(path=self._log)
        btrfh.setFormatter(file_fmt)

        sh = logging.StreamHandler()
        sh.setFormatter(HikariFormatter())
        sh.setLevel(log_level)

        logger = logging.getLogger(__name__)
        logger.setLevel(log_level)
        logger.addHandler(btrfh)
        logger.addHandler(sh)

        self.logger = logger

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
