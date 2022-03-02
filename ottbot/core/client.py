import typing as t
from collections import abc as collections

import hikari
import tanjun
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from hikari import traits as hikari_traits
from pytz import utc

from ottbot.abc.iclient import IClient
from ottbot.core.utils.funcs import get_list_of_files

_ClientT = t.TypeVar("_ClientT", bound="OttClient")


class OttClient(tanjun.Client, IClient):
    """Attachable Client for slash commands"""

    __slots__: t.Iterable[str] = (
        *tanjun.Client.__slots__,
        "scheduler",
        "bot",
    )

    def __init__(self: _ClientT, *args: t.Any, **kwargs: t.Any) -> None:

        self.bot = kwargs["shards"]
        self.version = self.bot.version

        super().__init__(*args, **kwargs)
        self.scheduler: AsyncIOScheduler = AsyncIOScheduler(timezone=utc)
        self.scheduler.configure(timezone=utc)

    def load_modules_(self, module: str = ""):
        """Loads slash command modules"""

        return super().load_modules(*get_list_of_files("ottbot/core/modules/" + module, ignore_underscores=False))

    @classmethod
    def from_gateway_bot_(
        cls,
        bot: hikari_traits.GatewayBotAware,
        /,
        *,
        event_managed: bool = True,
        mention_prefix: bool = False,
        declare_global_commands: t.Union[
            hikari.SnowflakeishSequence[hikari.PartialGuild],
            hikari.SnowflakeishOr[hikari.PartialGuild],
            bool,
        ] = False,
        set_global_commands: t.Union[hikari.SnowflakeishOr[hikari.PartialGuild], bool] = False,
        command_ids: t.Optional[collections.Mapping[str, hikari.SnowflakeishOr[hikari.Command]]] = None,
    ) -> "OttClient":
        return (
            cls(
                rest=bot.rest,
                cache=bot.cache,
                events=bot.event_manager,
                shards=bot,
                event_managed=event_managed,
                mention_prefix=mention_prefix,
                declare_global_commands=declare_global_commands,
                set_global_commands=set_global_commands,
                command_ids=command_ids,
                _stack_level=1,
            )
            .set_human_only()
            .set_hikari_trait_injectors(bot)
        )

    @classmethod
    def from_rest_bot_(
        cls,
        bot: hikari_traits.RESTBotAware,
        /,
        declare_global_commands: t.Union[
            hikari.SnowflakeishSequence[hikari.PartialGuild],
            hikari.SnowflakeishOr[hikari.PartialGuild],
            bool,
        ] = False,
        set_global_commands: t.Union[hikari.SnowflakeishOr[hikari.PartialGuild], bool] = False,
        command_ids: t.Optional[collections.Mapping[str, hikari.SnowflakeishOr[hikari.Command]]] = None,
    ) -> "OttClient":
        return cls(
            rest=bot.rest,
            server=bot.interaction_server,
            declare_global_commands=declare_global_commands,
            set_global_commands=set_global_commands,
            command_ids=command_ids,
            _stack_level=1,
        ).set_hikari_trait_injectors(bot)
