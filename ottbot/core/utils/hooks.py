import traceback
import typing as t
from logging import Logger

import hikari
import tanjun

from ottbot import constants
from ottbot.core.utils.funcs import to_dict


def _embed(ctx: tanjun.abc.Context, message: str) -> hikari.Embed:
    embed = hikari.Embed(
        title=f"Command Error: /{ctx.triggering_name}", description=message, color=constants.FAILED_COLOUR
    )

    return embed


def build_on_error(
    logger: Logger,
) -> t.Callable[[tanjun.abc.Context, Exception], t.Coroutine[t.Any, t.Any, t.Optional[bool]]]:
    async def on_error(ctx: tanjun.abc.Context, exc: Exception) -> None:
        log_exc(ctx, exc, logger)

        if isinstance(exc, hikari.BadRequestError):
            logger.error(f"Hikari Error\n{exc!r}\n{ctx!r}")
            await ctx.respond(_embed(ctx, f"**Hikari Error** ```{exc.args[0]}```"))
            raise exc

        elif isinstance(exc, hikari.ExceptionEvent):
            await ctx.respond(
                _embed(ctx, f"**HIKARI ERROR**```{exc.args[0] if len(exc.args) > 0  else 'No error message'}```")
            )
            print(exc.args)
            raise exc

        elif isinstance(exc, Exception):
            await ctx.respond(_embed(ctx, f"**ERROR**```{exc.args[0] if len(exc.args) > 0 else 'No error message'}```"))

            print(exc.args)
            raise exc
        else:
            raise exc

    return on_error


# "CommandError",
# "ConversionError",
# "HaltExecution",
# "FailedCheck",
# "MissingDependencyError",
# "NotEnoughArgumentsError",
# "TooManyArgumentsError",
# "ParserError",
# "TanjunError",
# "TanjunWarning",
# "StateWarning",


def build_on_parser_error(logger: Logger):
    async def on_parser_error(ctx: tanjun.abc.Context, exc: tanjun.ParserError) -> None:
        log_exc(ctx, exc, logger)

        if isinstance(exc, (tanjun.NotEnoughArgumentsError, tanjun.TooManyArgumentsError)):
            logger.error(f"Argument Error\n{exc!r}\n{ctx!r}")
            await ctx.respond(_embed(ctx, f"**Argument Error**```{exc.message}```"))
            raise exc

        elif isinstance(exc, tanjun.MissingDependencyError):
            logger.error(f"Missing Dependency Error\n{exc!r}\n{ctx!r}")
            await ctx.respond(_embed(ctx, f"**Dependency Error**```{exc.message}```"))
            raise exc

        elif isinstance(exc, tanjun.ConversionError):
            logger.error(f"Conversion Error\n{exc!r}\n{ctx!r}")
            await ctx.respond(_embed(ctx, f"**Conversion Error**```{exc.message}```"))
            raise exc

        # TODO: Add CooldownError once it exists
        else:
            logger.error(f"Uncaught Error\n{exc!r}\n{ctx!r}")

            raise exc

    return on_parser_error


def log_exc(ctx: tanjun.abc.Context, exc: BaseException, logger: Logger) -> None:
    # ctx
    d = to_dict(ctx, ignore_underscores=False)
    error_msg = f"Error: {exc!r}" + "\nCtx = {\n"
    for key in d.keys():
        error_msg += f"{key}: {d[key]}," + "\n"
    error_msg += "}\n"

    # traceback
    error_msg += "Traceback:\n"
    error_msg += "".join(traceback.format_tb(exc.__traceback__))

    logger.error(error_msg)


# @bot.listen(hikari.ExceptionEvent[hikari.BadRequestError])
async def on_general_error(event: hikari.ExceptionEvent):
    if isinstance(event.exception, hikari.BadRequestError):
        ...
