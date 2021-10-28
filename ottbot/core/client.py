import typing as t
from pathlib import Path

import tanjun
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc
from hikari import traits as hikari_traits
import hikari

from ottbot.abc.iclient import IClient
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
        bot: hikari_traits.GatewayBotAware,
        /,
        *,
        event_managed: bool = True,
        mention_prefix: bool = False,
        set_global_commands: t.Union[
            hikari.SnowflakeishOr[hikari.PartialGuild], bool
        ] = False,
    ):
        """Build a `Client` from a `hikari.traits.GatewayBotAware` instance.

        Notes
        -----
        * This implicitly defaults the client to human only mode.
        * This sets type dependency injectors for the hikari traits present in
        `bot` (including `hikari.traits.GatewayBotaWARE`).
        * The endpoint used by `set_global_commands` has a strict ratelimit
        which, as of writing, only allows for 2 requests per minute (with that
        ratelimit either being per-guild if targeting a specific guild
        otherwise globally).

        Parameters
        ----------
        bot : hikari.traits.GatewayBotAware
            The bot client to build from.

            This will be used to infer the relevant Hikari clients to use.

        Other Parameters
        ----------------
        event_managed : bool
            Whether or not this client is managed by the event manager.

            An event managed client will be automatically started and closed
            based on Hikari's lifetime events.

            Defaults to `True`.
        mention_prefix : bool
            Whether or not mention prefixes should be automatically set when this
            client is first started.

            Defaults to `False` and it should be noted that this only applies to
            message commands.
        set_global_commands : typing.Union[hikari.SnowflakeishOr[hikari.PartialGuild], bool]
        Whether or not to automatically set global slash commands when this
        client is first started. Defaults to `False`.

        If a guild object or ID is passed here then the global commands will be
        set on this specific guild at startup rather than globally. This
        can be useful for testing/debug purposes as slash commands may take
        up to an hour to propagate globally but will immediately propagate
        when set on a specific guild.
        """
        constructor = (
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
        """Build a `Client` from a `hikari.traits.RESTBotAware` instance.

        Notes
        -----
        * This sets type dependency injectors for the hikari traits present in
        `bot` (including `hikari.traits.RESTBotAware`).
        * The endpoint used by `set_global_commands` has a strict ratelimit
        which, as of writing, only allows for 2 requests per minute (with that
        ratelimit either being per-guild if targeting a specific guild
        otherwise globally).

        Parameters
        ----------
        bot : hikari.traits.RESTBotAware
            The bot client to build from.

        Other Parameters
        ----------------
        set_global_commands : typing.Union[hikari.SnowflakeishOr[hikari.PartialGuild], bool]
            Whether or not to automatically set global slash commands when this
            client is first started. Defaults to `False`.

            If a guild object or ID is passed here then the global commands will be
            set on this specific guild at startup rather than globally. This
            can be useful for testing/debug purposes as slash commands may take
            up to an hour to propagate globally but will immediately propagate
            when set on a specific guild.
        """
        constructor = cls(
            rest=bot.rest,
            server=bot.interaction_server,
            set_global_commands=set_global_commands,
        ).set_hikari_trait_injectors(bot)

        return constructor
