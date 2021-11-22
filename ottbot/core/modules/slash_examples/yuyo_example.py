import asyncio
import tanjun
import yuyo
import hikari

from ottbot.core.utils.funcs import build_loaders


component, load_component, unload_component = build_loaders()


@component.with_slash_command
@tanjun.as_slash_command("yuyo", "An example yuyo component paginator")
async def cmd_yuyo(
    ctx: tanjun.abc.SlashContext, component_client: yuyo.ComponentClient = tanjun.injected(type=yuyo.ComponentClient)
) -> None:
    fields = iter(
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
@tanjun.as_slash_command("yuyoreaction", "An example reaction command")
async def cmd_yuyoreaction(
    ctx: tanjun.abc.SlashContext, reaction_client: yuyo.ReactionClient = tanjun.injected(type=yuyo.ReactionClient)
) -> None:

    await ctx.respond("work in progess")

    # fields = iter(
    #     [
    #         ("page 1\nok", hikari.UNDEFINED),
    #         (hikari.UNDEFINED, hikari.Embed(description="page 2")),
    #         ("page3\nok", hikari.Embed(description="page3")),
    #     ]
    # )

    # paginator = yuyo.ComponentPaginator(fields, authors=(ctx.author,))

    # if first_entry := await paginator.get_next_entry():
    #     content, embed = first_entry
    #     message = await ctx.respond(content=content, embed=embed, ensure_result=True)
    #     reaction_client.add_handler(message, paginator)
