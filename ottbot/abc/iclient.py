import typing as t
from abc import ABC, abstractmethod, abstractclassmethod

import hikari
from hikari import traits
import tanjun

_IClientT = t.TypeVar("_IClientT", bound="IClient")


class IClient(ABC):
    """Interface for the Tanjun Command Handler Client"""

    @abstractmethod
    def __init__(self: _IClientT, *args: t.Any, **kwargs: t.Any) -> None:
        self.errors: t.Optional[t.Any]
        self.embeds: t.Optional[t.Any]

    @abstractmethod
    def load_modules_(self: _IClientT) -> _IClientT:
        """Load slash command"""

    @abstractclassmethod
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
    ) -> tanjun.Client:
        """Class gateway factory method to be overwritten in child class"""

    @abstractclassmethod
    def from_rest_bot(
        cls,
        bot: traits.RESTBotAware,
        /,
        set_global_commands: t.Union[
            hikari.SnowflakeishOr[hikari.PartialGuild], bool
        ] = False,
    ) -> tanjun.Client:
        """Class rest factory method to be overwritten in child class"""
