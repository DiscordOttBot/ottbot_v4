import tanjun

from ottbot.core.utils.funcs import build_loaders


component, load_component, unload_component = build_loaders()


cmd_group = component.with_slash_command(tanjun.slash_command_group("places", "get info about places"))

@component.with_slash_command
@tanjun.as_slash_command("example", "An example slash command")
async def cmd_example(ctx: tanjun.abc.SlashContext) -> None:
    await ctx.respond("test")

