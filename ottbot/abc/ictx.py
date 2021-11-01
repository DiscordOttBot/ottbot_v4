from abc import ABC, abstractmethod
from ottbot.core.bot import OttBot
from ottbot.core.client import OttClient

import typing as t
import tanjun


class ICtx(ABC):
    @abstractmethod
    def __init__(self, bot: OttBot, client: OttClient) -> None:
        ...

    @abstractmethod
    @property
    def bot(self) -> OttBot:
        ...

    @abstractmethod
    @bot.setter
    def bot(self, client: OttClient) -> None:
        ...

    @abstractmethod
    @property
    def client(self) -> OttClient:
        ...

    @abstractmethod
    @client.setter
    def client(self, client: OttClient) -> None:
        ...


class ICtxWrapper(ABC):
    @abstractmethod
    def __init__(
        self, ctx: tanjun.SlashContext, bot: OttBot, client: OttClient
    ) -> None:
        ...

    @abstractmethod
    @property
    def ctx(self) -> tanjun.SlashContext:
        ...

    @abstractmethod
    @ctx.setter
    def ctx(self, ctx: tanjun.SlashContext) -> None:
        ...

    @abstractmethod
    @property
    def bot(self) -> OttBot:
        ...

    @abstractmethod
    @bot.setter
    def bot(self, client: OttClient) -> None:
        ...

    @abstractmethod
    @property
    def client(self) -> OttClient:
        ...

    @abstractmethod
    @client.setter
    def client(self, client: OttClient) -> None:
        ...


class ISlashFactory(ABC):
    @abstractmethod
    @staticmethod
    def build(
        name: tuple[str, str], args: tuple[tuple[t.Any, t.Any]]
    ) -> t.Callable[..., t.Awaitalbe[t.Any, None]]:
        ...


class IContextDecorator(ABC):
    @abstractmethod
    @staticmethod
    def decorator():
        ...


# ctx wrapper
#     hold more data: bot, client
# SlashContext child
#     easier to pass and get hold of
# slash factory / decorator
#     automatically get bot and client as args
