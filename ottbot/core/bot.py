import logging
import typing as t
from abc import ABC, abstractmethod
from pathlib import Path

import hikari
import sake

from ottbot import __version__
from ottbot.abc.ibot import IBot
from ottbot.config import Config
from ottbot.core.client import OttClient

_BotT = t.TypeVar("_BotT", bound="OttBot")
SERVER_ID = 545984256640286730


class OttBot(hikari.GatewayBot):
    """Main Bot Class"""

    # __slots__ = hikari.GatewayBot.__slots__ + ("client",)

    def __init__(self: _BotT) -> None:
        super().__init__(token=Config["TOKEN"], intents=hikari.Intents.ALL)
        self.guilds = []

    def create_client(self: _BotT) -> None:
        """Creates a client and adds it to the `client` attribute"""
        self.client: OttClient = OttClient.from_gateway_bot(
            self, set_global_commands=SERVER_ID
        )
        self.client.load_modules_()

    def run(self: _BotT) -> None:
        """Create the client, subscribe to important events, and run the bot"""
        self.create_client()
        subscriptions: dict[hikari.Event, t.Callable[..., t.Any]] = {
            hikari.StartingEvent: self.on_starting,
            hikari.StartedEvent: self.on_started,
            hikari.StoppingEvent: self.on_stopping,
        }
        [self.event_manager.subscribe(key, subscriptions[key]) for key in subscriptions]

        super().run(
            activity=hikari.Activity(
                name=f"/help | {__version__}", type=hikari.ActivityType.WATCHING
            )
        )

    async def on_starting(self: _BotT, event: hikari.StartingEvent) -> None:
        """Runs before bot is connected. Blocks on_started until complete."""
        # cache = sake.redis.RedisCache(self, self, address="redis://127.0.0.1")
        # await cache.open()
        logging.info("Connecting to redis server")

    async def on_started(self: _BotT, event: hikari.StartedEvent) -> None:
        """Runs once bot is fully connected"""
        self.client.scheduler.start()

        async for guild in self.rest.fetch_my_guilds():
            self.guilds.append(guild)

        for guild in self.guilds:
            for member in await self.rest.fetch_members(guild.id):
                print(member)

        # self.stdout_channel = await self.rest.fetch_channel(883885654319190016)
        # await self.stdout_channel.send(f"Testing v{__version__} now online!")

        logging.info("Bot ready")

    async def on_stopping(self: _BotT, event: hikari.StoppingEvent) -> None:
        """Runs at the beginning of shutdown sequence"""
        # await self.stdout_channel.send(f"Testing v{__version__} is shutting down.")
        self.client.scheduler.shutdown()
