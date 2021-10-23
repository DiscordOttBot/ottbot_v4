import typing as t
from pathlib import Path

import tanjun
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc
from hikari import traits
import hikari

from ottbot.abc.iclient import IClient
from ottbot.abc.ibot import IBot
from ottbot.abc.ibot import _IBotT
from ottbot.core import utils


_ClientT = t.TypeVar("_ClientT", bound="OttClient")


class OttClient(tanjun.Client, IClient):
    """Attachable Client for slash commands"""

    __slots__: t.Iterable[str] = tanjun.Client.__slots__ + ("scheduler", "bot")

    def __init__(self: _ClientT, *args: t.Any, **kwargs: t.Any) -> None:

        self.errors = utils.Errors()
        self.embeds = utils.Embeds()
        self.bot: t.Optional[t.Any] = kwargs["shards"]

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
    def from_gateway_bot(
        cls,
        bot,
        /,
        *,
        event_managed=False,
        mention_prefix=False,
        set_global_commands=False,
    ):
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

    @classmethod
    def from_rest_bot(
        cls,
        bot,
        /,
        set_global_commands=False,
    ):
        constructor = cls(
            rest=bot.rest,
            server=bot.interaction_server,
            set_global_commands=set_global_commands,
        ).set_hikari_trait_injectors(bot)

        return constructor
