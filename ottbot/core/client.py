import typing as t
from pathlib import Path

import tanjun
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc
from hikari import traits
import hikari

from ottbot.abc.iclient import IClient
from ottbot.abc.ibot import _IBotT


_ClientT = t.TypeVar("_ClientT", bound="OttClient")


class OttClient(tanjun.Client, IClient):
    """Attachable Client for slash commands"""

    __slots__: t.Iterable[str] = tanjun.Client.__slots__ + ("scheduler", "bot")

    def __init__(self: _ClientT, *args: t.Any, **kwards: t.Any) -> None:
        tanjun.Client.__init__(*args, **kwards)
        self.scheduler: AsyncIOScheduler = AsyncIOScheduler()
        self.scheduler.configure(timezone=utc)
        self.bot: t.Optional[_IBotT] = None # type: ignore

    def load_modules_(self: _ClientT):
        """Loads slash command modules"""

        return tanjun.Client.load_modules(
            *[
                f"ottbot.core.modules.{m.stem}"
                for m in Path(__file__).parent.glob("modules/*.py")
            ]
        )

        # Fixed in #55, need to wait until @task/components is merged.
        # return super().load_modules(*Path(__file__).parent.glob("modules/*.py"))

    def from_gateway_bot(
        cls,
        bot: hikari.GatewayBotAware,
        /,
        *,
        event_managed: bool = False,
        mention_prefix: bool = False,
        set_global_commands: t.Union[
            hikari.guilds.PartialGuild, hikari.Snowflake, bool
        ] = False,
    ) -> _ClientT:
        constructor: _ClientT = (
            cls(
                rest=bot.rest,
                cache=bot.cache,
                events=bot.event_manager,
                shards=bot,
                event_managed=event_managed,
                mention_prefix=mention_prefix,
                set_global_commands=set_global_commands,
            )
            .set_human_only()
            .set_hikari_trait_injectors(bot)
        )

        return constructor

    def from_rest_bot(
        cls,
        bot: traits.RESTBotAware,
        /,
        set_global_commands: t.Union[
            hikari.SnowflakeishOr[hikari.PartialGuild], bool
        ] = False,
    ) -> _ClientT:
        constructor: _ClientT = cls(
            rest=bot.rest,
            server=bot.interaction_server,
            set_global_commands=set_global_commands,
        ).set_hikari_trait_injectors(bot)

        return constructor
