import hikari
import tanjun

from ottbot.core.utils.funcs import build_loaders


component, load_component, unload_component = build_loaders()


@component.with_slash_command
@tanjun.with_str_slash_option(
    "err",
    "an error",
    choices=[
        "NotEnoughArgumentsError",
        "TooManyArgumentsError",
        "MissingDependencyError",
        "ConversionError",
        "Exception",
    ],
)
@tanjun.as_slash_command("error", "Command that triggers a bot error")
async def cmd_example(ctx: tanjun.abc.SlashContext, err: str) -> None:

    error_dict: dict[str, BaseException] = {
        "NotEnoughArgumentsError": tanjun.NotEnoughArgumentsError("Test Error", "asdf"),
        "TooManyArgumentsError": tanjun.TooManyArgumentsError("Test Error", "asdf"),
        "MissingDependencyError": tanjun.MissingDependencyError("Test Error"),
        "ConversionError": tanjun.ConversionError("Test Error", "asdf"),
        "Exception": Exception,
    }
    raise error_dict[err] from BaseException
    await ctx.respond("well, no errors!")
