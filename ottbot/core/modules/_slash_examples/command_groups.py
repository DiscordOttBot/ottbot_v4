import asyncio
import typing as t

import hikari
import tanjun

from ottbot.core.utils.funcs import build_loaders

component, load_component, unload_component = build_loaders()


cmd_group = component.with_slash_command(tanjun.slash_command_group("places", "get info about places"))

nested_group = cmd_group.with_command(tanjun.slash_command_group("interaction", "say hello or something!"))


@cmd_group.with_command
# Here we add a required string option which'll be convertered to an emoji object.
@tanjun.with_str_slash_option("emoji", "Option description")
@tanjun.as_slash_command("japan", "command description")
async def japan_command(ctx: tanjun.abc.Context, emoji: hikari.Emoji) -> None:
    await ctx.respond(f"Nihongo ga dekimasu ka? {emoji}")


@cmd_group.with_command
@tanjun.as_slash_command("europe", "command description")
async def europe_command(ctx: tanjun.abc.Context) -> None:
    await ctx.respond("I don't know how to describe Europe... small?")


@nested_group.with_command
# This adds a required member option to the command which'll be passed to the
# "member" argument as type hikari.Member.
@tanjun.with_member_slash_option("member", "Option description")
# This adds an optional string option to the command which'll be passed
# to the "name" argument as type str if it was provided else None.
@tanjun.with_str_slash_option("name", "Option description", default=None)
@tanjun.as_slash_command("hi", "command description")
async def hi_command(ctx: tanjun.abc.Context, name: t.Optional[str], member: hikari.Member) -> None:
    if name:
        await ctx.respond(f"Hi, {name} and {member.username}")

    else:
        await ctx.respond(f"Hi {member.username}")


@component.with_command
@tanjun.as_slash_command("defer", "Lower level command which explicitly defers")
async def defer_command(ctx: tanjun.abc.SlashContext) -> None:

    # Note that if we want the response that's later edited in to be ephemeral
    # then we can pass `flags=hikari.MessageFlags.EPHEMERAL` to `SlashContext.defer`.
    await ctx.defer(flags=hikari.MessageFlag.EPHEMERAL)
    await asyncio.sleep(5)  # Do some work which may take a while
    # Either edit_initial_response or respond may be used here.
    await ctx.edit_initial_response("Done 👍")
