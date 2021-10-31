import typing as t
from collections import abc as collections
from pathlib import Path

import hikari
import tanjun
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from hikari import traits as hikari_traits
from pytz import utc

from ottbot.abc.iclient import IClient

_ClientT = t.TypeVar("_ClientT", bound="OttClient")


class OttClient(tanjun.Client, IClient):
    """Attachable Client for slash commands"""

    __slots__: t.Iterable[str] = tanjun.Client.__slots__ + ("scheduler", "bot", "errors", "embeds")

    def __init__(self: _ClientT, bot=None, *args: t.Any, **kwargs: t.Any) -> None:

        self.bot = kwargs["shards"] 

        super().__init__(*args, **kwargs)
        self.scheduler: AsyncIOScheduler = AsyncIOScheduler()
        self.scheduler.configure(timezone=utc)

    def load_modules_(self):
        """Loads slash command modules"""

        return super().load_modules(
            *[
                f"ottbot.core.modules.{m.stem}"
                for m in Path(__file__).parent.glob("modules/*.py")
            ]
        )

        # Fixed in #55, need to wait until @task/components is merged.
        # return super().load_modules(*Path(__file__).parent.glob("modules/*.py"))

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
        set_global_commands: t.Union[
            hikari.SnowflakeishOr[hikari.PartialGuild], bool
        ] = False,
        command_ids: t.Optional[
            collections.Mapping[str, hikari.SnowflakeishOr[hikari.Command]]
        ] = None,
    ) -> "OttClient":
        return (
            cls(
                bot=bot,
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
        set_global_commands: t.Union[
            hikari.SnowflakeishOr[hikari.PartialGuild], bool
        ] = False,
        command_ids: t.Optional[
            collections.Mapping[str, hikari.SnowflakeishOr[hikari.Command]]
        ] = None,
    ) -> "OttClient":
        return cls(
            rest=bot.rest,
            server=bot.interaction_server,
            declare_global_commands=declare_global_commands,
            set_global_commands=set_global_commands,
            command_ids=command_ids,
            _stack_level=1,
        ).set_hikari_trait_injectors(bot)
