import hikari
import tanjun
from emoji import emoji_count
from hikari.events.reaction_events import GuildReactionAddEvent

from ottbot.core.bot import OttBot
from ottbot.core.utils.funcs import build_loaders

component, load_component, unload_component = build_loaders()


@component.with_slash_command
@tanjun.as_slash_command("reaction_test", "A command to test reactions")
async def cmd_reaction_test(ctx: tanjun.abc.SlashContext, bot: OttBot = tanjun.injected(type=OttBot)) -> None:
    message = await ctx.respond("React to this message", ensure_result=True)
    event = await bot.wait_for(GuildReactionAddEvent, timeout=60, predicate=lambda e: e.message_id == message.id)
    emoji = (await bot.rest.fetch_emoji(event.guild_id, event.emoji_id)).name if event.emoji_id else event.emoji_name

    bot.logger.info(emoji)
    bot.logger.info(repr(emoji))

    await message.edit(content=f"Reaction added: {emoji}")
    # match (event.emoji_name):
    #     case "":
    #         ...
    #     case _:
    #         ...


@component.with_slash_command
@tanjun.as_slash_command("emoji_db_test", "A command to test emojies in the database")
async def test_db_emoji(ctx: tanjun.abc.SlashContext, bot: OttBot = tanjun.injected(type=OttBot)) -> None:
    message = await ctx.respond("React to this message", ensure_result=True)
    event = await bot.wait_for(GuildReactionAddEvent, timeout=60, predicate=lambda e: e.message_id == message.id)
    emoji = (await bot.rest.fetch_emoji(event.guild_id, event.emoji_id)).name if event.emoji_id else event.emoji_name

    if emoji is None:
        return
    elif isinstance(emoji, hikari.UnicodeEmoji):
        await message.edit(content=f"Unicode emoji {emoji}")
    elif isinstance(emoji, str) and event.emoji_id is not None:
        await message.edit(content=f"Custom emoji {emoji} (ID: {event.emoji_id})")

    # await bot.pool.execute("INSERT INTO test_table (emoji) VALUES ($1)", emoji)


async def _is_unicode_or_custom_emoji(ctx: tanjun.abc.Context, to_check: str) -> bool:
    """Helper function to check if a string is an unicode emoji or a custom emoji."""
    if not emoji_count(to_check):
        try:
            custom_emoji_id = to_check.split(":")[-1][:-1]
            custom_emote = await tanjun.to_emoji(custom_emoji_id, ctx)
            if not custom_emote:
                return False
        except ValueError:
            return False
    return True


# TODO: https://gitlab.com/aster.codes/vegas2/-/blob/main/vegas2/plugins/roles.py
# TODO: https://gitlab.com/aster.codes/vegas2/-/blob/main/vegas2/models/autoroles/autoroles.py
