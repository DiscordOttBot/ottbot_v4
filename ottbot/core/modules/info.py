import hikari
import tanjun

from ottbot.constants import ZWJ
from ottbot.core.bot import OttBot
from ottbot.core.utils.funcs import build_loaders

component, load_component, unload_component = build_loaders()


@component.with_slash_command
@tanjun.with_member_slash_option("user", "The user to spotlight", default=None)
@tanjun.as_slash_command("spotlight", "Displays previous messages from a user")
async def cmd_spotlight(
    ctx: tanjun.abc.SlashContext, user: hikari.Member | None, bot: OttBot = tanjun.inject(type=OttBot)
) -> None:
    if ctx.guild_id is None:
        return
    if user is None:
        user = await bot.rest.fetch_member(ctx.guild_id, ctx.author)
    messages: list[hikari.Message] = []
    cached_messages = bot.cache.get_messages_view()

    async for m in cached_messages.iterator():
        if m.author.id == user.id and m.guild_id == ctx.guild_id:
            messages.append(m)
        if len(messages) >= 10:
            break

    link = "[Jump](https://discord.com/channels/{}/{}/{})"
    fields = [
        (
            "Messages",
            "\n".join(
                [
                    f"{link.format(ctx.guild_id, m.channel_id, m.id)} <t:{m.created_at.timestamp():.0f}:T>: {m.content}"
                    for m in messages
                ]
            ),
            False,
        )
    ]

    embed = bot.embeds.build(
        ctx=ctx,
        title=f"{user.display_name}'s Messages",
        description=f"The recient messages of {user.mention}",
        thumbnail=user.avatar_url,
        color=user.accent_color,
        fields=fields if messages else [("Messages", "No messages found", False)],
    )
    await ctx.respond(ZWJ, embed=embed)
