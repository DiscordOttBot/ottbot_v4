import asyncio

import hikari
import tanjun
from hikari.impl.special_endpoints import ActionRowBuilder
from hikari.interactions.base_interactions import ResponseType
from hikari.messages import ButtonStyle
from ottbot.core.bot import OttBot

from ottbot.core.utils.funcs import build_loaders

component, load_component, unload_component = build_loaders()


@component.with_slash_command
@tanjun.as_slash_command("paginate", "Paginate through a list of options!")
async def command_paginate(ctx: tanjun.abc.Context) -> None:
    values: tuple[str, str, str, str, str, str] = (
        "Page 1",
        "Page 2",
        "Page 3",
        "Page 4",
        "Page 5",
        "Page 6",
    )
    index: int = 0

    button_menu: ActionRowBuilder = (
        ctx.rest.build_action_row()
        .add_button(ButtonStyle.SECONDARY, "<<")
        .set_label("<<")
        .add_to_container()
        .add_button(ButtonStyle.PRIMARY, "<")
        .set_label("<")
        .add_to_container()
        .add_button(ButtonStyle.PRIMARY, ">")
        .set_label(">")
        .add_to_container()
        .add_button(ButtonStyle.SECONDARY, ">>")
        .set_label(">>")
        .add_to_container()
    )

    await ctx.respond(values[0], component=button_menu)

    while True:

        try:
            event: hikari.InteractionCreateEvent = await ctx.client.events.wait_for(
                hikari.InteractionCreateEvent, timeout=60
            )
            ctx.client.bot.logger.critical(f"\n\nEVENT: {event} | {type(event)}")
        except asyncio.TimeoutError:
            await ctx.edit_initial_response("Timed out.", components=[])
        else:
            if event.interaction.custom_id == "<<":
                index = 0
            elif event.interaction.custom_id == "<":
                index = (index - 1) % len(values)
            elif event.interaction.custom_id == ">":
                index = (index + 1) % len(values)
            elif event.interaction.custom_id == ">>":
                index = len(values) - 1

            await ctx.edit_initial_response(values[index])
            await event.interaction.create_initial_response(
                ResponseType.DEFERRED_MESSAGE_UPDATE, values[index]
            )


@component.with_slash_command
@tanjun.as_slash_command(
    "nsfw",
    "An example command that sends only to the command author",
    default_to_ephemeral=True,
)
async def cmd_nsfw(ctx: tanjun.abc.SlashContext) -> None:
    await ctx.respond("Heyy~")


@component.with_slash_command
@tanjun.with_str_slash_option(
    "c", "A very important choice", choices=["lmao", "bababooey"]
)
@tanjun.as_slash_command(
    "choice", "An example command where you have a dropdown choice menu"
)
async def cmd_choice(ctx: tanjun.abc.SlashContext, c: str) -> None:
    await ctx.respond(f"**{c}** was a good choice")


@component.with_slash_command
@tanjun.with_str_slash_option(
    "message", "The message that will be repeated", default=""
)
@tanjun.as_slash_command("echo", "Echo the message back to the user")
async def cmd_echo(
    ctx: tanjun.abc.SlashContext,
    message: str,
    bot: OttBot = tanjun.injected(type=OttBot),
) -> None:
    embed = bot.embeds.build(
        ctx=ctx,
        title=f"{ctx.author.username}'s message",
        fields=(("message", message, True),),
    )
    await ctx.respond(embed=embed)
