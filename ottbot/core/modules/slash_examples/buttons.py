import tanjun

from ottbot.core.utils.funcs import build_loaders

component, load_component, unload_component = build_loaders()


@component.with_slash_command
@tanjun.as_slash_command("button", "An example command with a button")
async def cmd_example(ctx: tanjun.abc.SlashContext) -> None:
    await ctx.respond("test")
