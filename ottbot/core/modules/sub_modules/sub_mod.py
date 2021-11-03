import tanjun

from ottbot.core.utils.funcs import build_loaders

component, load_component, unload_component = build_loaders()


@component.with_slash_command
@tanjun.as_slash_command("subcmd", "An example sub module command")
async def cmd_sub(ctx: tanjun.abc.SlashContext) -> None:
    await ctx.respond("subcmd")
