import datetime
import logging
import os
import typing as t
from glob import glob

import hikari
from pytz import utc
import sake
import tanjun
import yuyo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from hikari import presences

from ottbot import constants
from ottbot.abc.ibot import IBot
from ottbot.config import Config
from ottbot.core.client import OttClient
from ottbot.core.db import AsyncPGDatabase
from ottbot.core.utils.embeds import Embeds
from ottbot.core.utils.errors import Errors
from ottbot.core.utils.funcs import delete_button_callback, parse_log_level
from ottbot.core.utils.hooks import (
    build_on_error,
    build_on_parser_error,
    on_general_error,
)
from ottbot.core.utils.lines import Lines
from ottbot.core.utils.rotating_logs import (
    BetterTimedRotatingFileHandler,
    HikariFormatter,
)
from ottbot.core.utils.session_manager import SessionManager
from ottbot.core.utils.tasks import clean_invite_table

_BotT = t.TypeVar("_BotT", bound="OttBot")
EventT = t.Union[
    hikari.StartingEvent,
    hikari.StartedEvent,
    hikari.StoppingEvent,
    hikari.StoppedEvent,
]


class OttBot(hikari.GatewayBot, IBot):
    """Main Bot Class"""

    __slots__: t.Iterable[str] = (
        *hikari.GatewayBot.__slots__,
        "client",
        "embeds",
        "errors",
        "guilds",
        "log_level",
        "version",
        "_dynamic",
        "_static",
        "_log",
    )

    def __init__(self: _BotT, version: str = "", log_level: str = "info") -> None:
        self._dynamic: str = os.path.join(".", "ottbot", "data", "dynamic")
        self._static: str = os.path.join(".", "ottbot", "data", "static")
        self._log: str = os.path.join(".", "ottbot", "data", "logs")

        self.version: str = version
        self.log_level: str = log_level

        self.scheduler: AsyncIOScheduler = AsyncIOScheduler(timezone=utc)
        self.errors: Errors = Errors(self)
        self.embeds: Embeds = Embeds()
        self.lines: Lines = Lines()
        self.pool: AsyncPGDatabase = AsyncPGDatabase()

        self.guilds: list[hikari.OwnGuild] = []
        self.init_logger()

        super().__init__(
            token=self._get_token(),
            intents=hikari.Intents.ALL,
            logs=parse_log_level(self.log_level),
        )

    def _get_token(self: _BotT) -> str:
        if isinstance(token := Config["TOKEN"], str):
            return token
        raise ValueError("Invalid token in .env file")

    def create_client(self: _BotT) -> None:
        """Creates a tanjun client and dynamically links the bot and the client"""
        # self.logger.info("Creating client")

        # create yuyo clients
        component_client = yuyo.ComponentClient.from_gateway_bot(
            self, event_managed=False
        ).set_constant_id(  # if `event_managed=False` you need to manually start and stop the client
            constants.DELETE_CUSTOM_ID, delete_button_callback
        )
        reaction_client = yuyo.ReactionClient.from_gateway_bot(self, event_managed=True)

        # Passing `event_managed=True` will link the clients lifetime to the hikari bot's.
        # Using `.add_client_callback()` will link the lifetime to the tanjun command client's lifetime.
        # Pretty much the same thing.

        cache = sake.redis.RedisCache(app=self, event_manager=self.event_manager, address="redis://127.0.0.1")

        # create tanjun client
        self.client: OttClient = OttClient.from_gateway_bot_(
            self, declare_global_commands=constants.SERVER_ID, event_managed=True
        ).load_modules_()
        self.client = (
            self.client.set_hooks(
                tanjun.AnyHooks()
                .set_on_error(build_on_error(self.logger))
                .set_on_parser_error(build_on_parser_error(self.logger))
            )
            .set_type_dependency(OttClient, self.client)  # bot type dependency is automatically set
            .set_type_dependency(yuyo.ReactionClient, reaction_client)  #
            .set_type_dependency(yuyo.ComponentClient, component_client)
            .set_type_dependency(AsyncPGDatabase, self.pool)
            .set_type_dependency(AsyncIOScheduler, self.scheduler)
            .set_type_dependency(sake.redis.RedisCache, cache)
            .add_client_callback(tanjun.ClientCallbackNames.STARTING, component_client.open)
            .add_client_callback(tanjun.ClientCallbackNames.CLOSING, component_client.close)
            .add_client_callback(tanjun.ClientCallbackNames.STARTING, self.scheduler.start)
            .add_client_callback(tanjun.ClientCallbackNames.CLOSING, self.scheduler.shutdown)
        )
        SessionManager(self.client.rest.http_settings, self.client.rest.proxy_settings, "Discord Bot").load_into_client(
            self.client
        )

    async def init_cache(self: _BotT):
        # cache = sake.redis.RedisCache(app=self, event_manager=self.event_manager, address="redis://127.0.0.1")
        # try:
        #     await cache.open()
        # except ConnectionRefusedError as e:
        #     logging.warning(f"Redis Error: {e}")
        # except Exception as e:
        #     logging.critical(e)
        ...

    def run_(
        self,
        *,
        activity: t.Optional[presences.Activity] = None,
        afk: bool = False,
        asyncio_debug: t.Optional[bool] = None,
        check_for_updates: bool = True,
        close_passed_executor: bool = False,
        close_loop: bool = True,
        coroutine_tracking_depth: t.Optional[int] = None,
        enable_signal_handlers: bool = True,
        idle_since: t.Optional[datetime.datetime] = None,
        ignore_session_start_limit: bool = False,
        large_threshold: int = 250,
        propagate_interrupts: bool = False,
        status: presences.Status = presences.Status.ONLINE,
        shard_ids: t.Optional[t.AbstractSet[int]] = None,
        shard_count: t.Optional[int] = None,
    ) -> None:
        """Create the client, subscribe to important events, and run the bot.

        When running an API along side the bot, use `await bot.start_()`
        and `await bot.close()` on api events instead."""
        self.create_client()
        self.subscribe_to_events()

        super().run(
            activity=activity,
            afk=afk,
            asyncio_debug=asyncio_debug,
            check_for_updates=check_for_updates,
            close_passed_executor=close_passed_executor,
            close_loop=close_loop,
            coroutine_tracking_depth=coroutine_tracking_depth,
            enable_signal_handlers=enable_signal_handlers,
            idle_since=idle_since,
            ignore_session_start_limit=ignore_session_start_limit,
            large_threshold=large_threshold,
            propagate_interrupts=propagate_interrupts,
            status=status,
            shard_ids=shard_ids,
            shard_count=shard_count,
        )

    async def start_(
        self: _BotT,
        *,
        activity: t.Optional[presences.Activity] = None,
        afk: bool = False,
        check_for_updates: bool = True,
        idle_since: t.Optional[datetime.datetime] = None,
        ignore_session_start_limit: bool = False,
        large_threshold: int = 250,
        shard_ids: t.Optional[t.AbstractSet[int]] = None,
        shard_count: t.Optional[int] = None,
        status: presences.Status = presences.Status.ONLINE,
    ) -> None:
        """Bot's startup loop"""

        self.create_client()
        self.subscribe_to_events()

        await super().start(
            activity=activity,
            afk=afk,
            check_for_updates=check_for_updates,
            idle_since=idle_since,
            ignore_session_start_limit=ignore_session_start_limit,
            large_threshold=large_threshold,
            shard_ids=shard_ids,
            shard_count=shard_count,
            status=status,
        )

    def init_logger(self: _BotT) -> None:
        """Initializes the logger for the bot"""

        log_level = parse_log_level(self.log_level)

        file_fmt = logging.Formatter(
            "[%(asctime)s.%(msecs)03d] %(levelname)s | %(message)s",
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

    def subscribe_to_events(self: _BotT) -> None:
        # self.logger.info("Subscribing to events")
        subscriptions: dict[t.Any, t.Callable[..., t.Coroutine[t.Any, t.Any, None]]] = {
            hikari.StartingEvent: self.on_starting,
            hikari.StartedEvent: self.on_started,
            hikari.StoppingEvent: self.on_stopping,
            hikari.StoppedEvent: self.on_stopped,
            hikari.GuildAvailableEvent: self.on_guild_available,
            hikari.ExceptionEvent: on_general_error,
        }
        [self.event_manager.subscribe(key, subscriptions[key]) for key in subscriptions]

    async def on_starting(self: _BotT, event: hikari.StartingEvent) -> None:
        """Runs before bot is connected. Blocks on_started until complete."""
        # try:
        #     await self.cache.open()
        # except ConnectionRefusedError as e:
        #     logging.warning(f"Redis Error: {e}")
        # except Exception as e:
        #     logging.critical(e)

        # self.logger.info("Connecting to database")
        try:
            await self.pool.connect()
        except ConnectionRefusedError as e:
            self.logger.error(f"Cannot connect to Database: {e}")
            ...

    async def on_started(self: _BotT, event: hikari.StartedEvent) -> None:
        """Runs once bot is fully connected"""

        # self.logger.info("Connecting to redis server")
        await self.init_cache()

        self.client.scheduler.start()
        await self.schedule_tasks()

        logging.info("Bot ready")

    async def on_stopping(self: _BotT, event: hikari.StoppingEvent) -> None:
        """Runs at the beginning of shutdown sequence"""
        self.client.scheduler.shutdown()
        # self.dispatch
        # await self.cache

    async def on_stopped(self: _BotT, event: hikari.StoppingEvent) -> None:
        """Runs after the bot has been shutdown"""
        ...

    async def on_guild_available(self: _BotT, event: hikari.GuildAvailableEvent) -> None:
        # self.guilds.append(event.guild)
        ...

    async def schedule_tasks(self) -> None:
        self.scheduler.add_job(clean_invite_table, trigger=CronTrigger(second=0, minute=0, hour=0), args=[self.pool])

    def clean_dynamic_dir(self: _BotT) -> None:
        filelist = glob(os.path.join(self._dynamic, "*"))
        for f in filelist:
            os.remove(f)
