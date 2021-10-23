import typing as t

import hikari
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
    def embed(self, ctx: tanjun.abc.Context, message: str) -> t.Optional[hikari.Embed]:
        assert isinstance(ctx.client, IClient)
        desc: str = f"❌ {message}"

        if ctx.client.embeds is not None:
            embed: hikari.Embed = ctx.client.embeds.build(
                ctx=ctx, description=desc, footer="None"
            )

            return embed
        else:
            return None

    @staticmethod
    def ngon(message: str) -> NGonError:
        """Create an extreemly important error"""
        return NGonError(message)

    @staticmethod
    def parse(exc: Exception):
        print(exc)
        raise exc

    async def parse_tanjun(
        self, exc: t.Union[tanjun.CommandError, Exception], ctx: tanjun.abc.Context
    ) -> None:
        """Parse tanjun errors"""
        if isinstance(
            exc, (tanjun.NotEnoughArgumentsError, tanjun.TooManyArgumentsError)
        ):
            await ctx.respond(self.embed(ctx, f"**ERROR**```{exc.message}```"))
            raise exc

        elif isinstance(exc, tanjun.MissingDependencyError):
            await ctx.respond(self.embed(ctx, f"**ERROR**```{exc.message}```"))
            raise exc

        else:
            print(exc)
            raise exc
