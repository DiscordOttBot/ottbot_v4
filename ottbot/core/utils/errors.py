import typing as t

import hikari
import tanjun

import ottbot


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
    def embed(self, ctx: tanjun.abc.Context, message: str) -> hikari.Embed:
        assert isinstance(ctx.client, ottbot.OttClient)
        desc: str = f"❌ {message}"

        embed: hikari.Embed = ctx.client.embeds.build(
            ctx=ctx, description=desc, footer="None"
        )

        return embed

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
