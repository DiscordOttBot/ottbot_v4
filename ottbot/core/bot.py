import logging
import typing as t
from pathlib import Path
from abc import ABC, abstractmethod

import hikari

# import sake

from ottbot import __version__
from ottbot.config import Config

from ottbot.core.client import OttClient

# from ottbot.interfaces.ibot import IBot

_BotT = t.TypeVar("_BotT", bound="OttBot")


class OttBot(hikari.GatewayBot):
    """Placeholder"""

    # __slots__ = hikari.GatewayBot.__slots__ + ("client",)

    def __init__(self: _BotT) -> None:
        super().__init__(token=Config["TOKEN"], intents=hikari.Intents.ALL)

    def create_client(self: _BotT) -> None:
        self.client: OttClient = OttClient.from_gateway_bot(
            self, set_global_commands=545984256640286730
        )  # test server id
        self.client.load_modules_()

    def run(self: _BotT) -> None:
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
        # cache = sake.redis.RedisCache(self, self, address="redis://127.0.0.1")
        # await cache.open()
        logging.info("Connecting to redis server")

    async def on_started(self: _BotT, event: hikari.StartedEvent) -> None:
        self.client.scheduler.start()

        # self.stdout_channel = await self.rest.fetch_channel(883885654319190016)
        # await self.stdout_channel.send(f"Testing v{__version__} now online!")

        logging.info("Bot ready")

    async def on_stopping(self: _BotT, event: hikari.StoppingEvent) -> None:
        # await self.stdout_channel.send(f"Testing v{__version__} is shutting down.")
        self.client.scheduler.shutdown()
