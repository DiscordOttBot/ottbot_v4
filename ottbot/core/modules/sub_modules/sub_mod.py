import typing as t

import tanjun

from ottbot.core.utils.funcs import build_load_component

component = tanjun.Component()


@component.with_slash_command
@tanjun.as_slash_command("subcmd", "An example sub module command")
async def cmd_sub(ctx: tanjun.abc.SlashContext) -> None:
    await ctx.respond("subcmd")


load_component: t.Callable[[tanjun.Client], None] = build_load_component(component)
