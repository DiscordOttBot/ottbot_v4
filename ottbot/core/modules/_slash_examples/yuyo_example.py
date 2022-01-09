import typing as t

import hikari
import tanjun
import yuyo

from ottbot.core.utils.funcs import build_loaders

component, load_component, unload_component = build_loaders()


@component.with_slash_command
@tanjun.as_slash_command("yuyo", "An example yuyo component paginator")
async def cmd_yuyo(
    ctx: tanjun.abc.SlashContext, component_client: yuyo.ComponentClient = tanjun.injected(type=yuyo.ComponentClient)
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
    ctx: tanjun.abc.SlashContext, reaction_client: yuyo.ReactionClient = tanjun.injected(type=yuyo.ReactionClient)
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

