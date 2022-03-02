import functools
import typing as t

import hikari
import tanjun
import yuyo

from ottbot.core.bot import OttBot
from ottbot.core.utils.funcs import build_loaders

component, load_component, unload_component = build_loaders()


@component.with_slash_command
@tanjun.as_slash_command("yuyo", "An example yuyo component paginator")
async def cmd_yuyo(
    ctx: tanjun.abc.SlashContext, component_client: yuyo.ComponentClient = tanjun.inject(type=yuyo.ComponentClient)
) -> None:
    fields: t.Iterator[tuple[str | hikari.UndefinedType, hikari.Embed | hikari.UndefinedType]] = iter(
        [
            ("page 1\nok", hikari.UNDEFINED),
            (hikari.UNDEFINED, hikari.Embed(description="page 2")),
            ("page3\nok", hikari.Embed(description="page3")),
        ]
    )

    # Authors is provided here to whitelist the message's author for paginator access.
    # Alternatively `None` may be passed for authors to leave the paginator public.
    paginator = yuyo.ComponentPaginator(fields, authors=(ctx.author,))
    # Here we use "get_next_entry" to get the first entry to use in the target message for
    # this paginator while also incrementing the paginator's internal index.

    if first_entry := await paginator.get_next_entry():
        content, embed = first_entry
        message = await ctx.respond(content=content, embed=embed, component=paginator, ensure_result=True)
        component_client.set_executor(message, paginator)


@component.with_slash_command
@tanjun.as_slash_command("yuyoreaction", "An example reaction client command")
async def cmd_yuyoreaction(
    ctx: tanjun.abc.SlashContext, reaction_client: yuyo.ReactionClient = tanjun.inject(type=yuyo.ReactionClient)
) -> None:
    async def on_emoji_a(event: hikari.ReactionAddEvent | hikari.ReactionDeleteEvent) -> None:
        if event.emoji_id is not None and event.emoji_name is not None:
            print(event.emoji_name + "\n\n\n\na")
            if event.emoji_name == "⭐":
                print("[A]: star")

    handler = yuyo.ReactionHandler(authors=(ctx.author,))
    handler.add_callback("🗿", on_emoji_a)

    @handler.with_callback("🗿")
    async def on_emoji_b(event: hikari.ReactionAddEvent | hikari.ReactionDeleteEvent) -> None:
        if event.emoji_name is not None:
            print(event.emoji_name + "\n\n\n\nb callback")

    message = await ctx.respond("content", ensure_result=True)
    await message.add_reaction("🗿")
    await handler.open(message)
    reaction_client.add_handler(message, handler)


@component.with_slash_command
@tanjun.as_slash_command("yuyoid", "Test yuyo custom ids")
async def cmd_yuyoid(
    ctx: tanjun.abc.SlashContext,
    component_client: yuyo.ComponentClient = tanjun.inject(type=yuyo.ComponentClient),
    bot: OttBot = tanjun.inject(type=OttBot),
) -> None:
    if ctx.guild_id is None:
        return

    embed = hikari.Embed(title="", description="desc", color=8454399)
    self_bot = await bot.rest.fetch_my_user()
    embed.set_author(name=self_bot.username, icon=self_bot.avatar_url)
    row = (
        ctx.interaction.app.rest.build_action_row()
        .add_button(hikari.ButtonStyle.SECONDARY, "TEST_ID")
        .set_emoji("📩")
        .set_label("Add Member to Ticket")
        .add_to_container()
        .add_button(hikari.ButtonStyle.SECONDARY, "TEST_ID1")
        .set_emoji("🏴")
        .set_label("Remove Member from Ticket")
        .add_to_container()
        .add_button(hikari.ButtonStyle.SECONDARY, "TEST_ID2")
        .set_emoji("🔒")
        .set_label("Timeout Mode")
        .add_to_container()
        .add_button(hikari.ButtonStyle.DANGER, "TEST_ID3")
        .set_emoji("🛑")
        .set_label("Close Ticket")
        .add_to_container()
    )

    await ctx.respond(embed=embed, component=row)


@component.with_slash_command
@tanjun.with_str_slash_option("message", "The message to send", default="callback")
@tanjun.with_str_slash_option("id", "The id to add")
@tanjun.as_slash_command("yuyo_addid", "Add a constant id to yuyo")
async def cmd_yuyo_addid(
    ctx: tanjun.abc.SlashContext,
    message: str,
    id: str,
    component_client: yuyo.ComponentClient = tanjun.inject(type=yuyo.ComponentClient),
) -> None:
    if ctx.guild_id is None:
        return

    component_client.set_constant_id(id, functools.partial(reply_to_custom_id, message))


@component.with_slash_command
@tanjun.as_slash_command("name", "desc")
async def cmd_name(ctx: tanjun.abc.SlashContext) -> None:
    if ctx.guild_id is None:
        return


@component.with_listener(hikari.StartedEvent)
async def on_started(
    event: hikari.StartedEvent, component_client: yuyo.ComponentClient = tanjun.inject(type=yuyo.ComponentClient)
) -> None:
    async def yuyo_callback(ctx: yuyo.ComponentContext) -> None:
        print("yuyo_callback")
        await ctx.create_initial_response(hikari.ResponseType.MESSAGE_CREATE, "yuyo callback: TEST_ID")
        return

    component_client.set_constant_id("TEST_ID", yuyo_callback)


async def reply_to_custom_id(ctx, message) -> None:
    await ctx.create_initial_response(hikari.ResponseType.MESSAGE_CREATE, message)
