# TODO: Update error handler

import typing as t

import hikari
from ottbot.abc.ibot import IBot
import tanjun

from ottbot.abc.iclient import IClient


class Doneions(Exception):
    """Error Level that will personally email me if this ever triggers"""

    def __init__(self, message: str = "") -> None:
        self._email()
        super().__init__(message)

    def _email(self) -> None:
        ...


class NGonError(Exception):
    """Error level above critical"""

    ...


class Errors:
    def embed(
        self, ctx: tanjun.abc.Context, message: str, bot: IBot = tanjun.injected(type=IBot)
    ) -> t.Optional[hikari.Embed]:
        assert isinstance(ctx.client, IClient)
        desc: str = f"❌ {message}"

        embed: hikari.Embed = bot.embeds.build(ctx=ctx, description=desc, footer="None")

        return embed

    @staticmethod
    def ngon(message: str) -> NGonError:
        """Create an extreemly important error"""
        return NGonError(message)
