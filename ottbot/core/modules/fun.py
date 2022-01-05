import random

import tanjun
from ottbot.core.utils.funcs import build_loaders
from ottbot.core.bot import OttBot
from ottbot.constants import ZWJ

component, load_component, unload_component = build_loaders()


@component.with_slash_command
@tanjun.with_str_slash_option("question", "The question to ask")
@tanjun.as_slash_command("8ball", "Ask the magic 8ball a question")
async def cmd_8ball(ctx: tanjun.abc.SlashContext, question: str, bot: OttBot = tanjun.injected(type=OttBot)) -> None:
    """Ask the magic 8ball a question"""
    member = await bot.rest.fetch_member(ctx.guild_id, ctx.author)
    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful.",
    ]
    embed = bot.embeds.build(
        ctx,
        title=f"{member.display_name}: {question}{'' if question[-1] == '?' else '?'}",
        description=random.choice(responses),
    )
    await ctx.respond(ZWJ, embed=embed)


@component.with_slash_command
@tanjun.with_int_slash_option("count", "The number of dice to roll")
@tanjun.with_int_slash_option("sides", "The number of sides on the dice", default=6)
@tanjun.as_slash_command("dice", "Roll some dice")
async def cmd_dice(ctx: tanjun.abc.SlashContext, count: int, sides: int) -> None:
    if count > 100:
        await ctx.respond("No more than 100 dice can be rolled at once.")
    elif sides > 100:
        await ctx.respond("The dice cannot have more than 100 sides.")

    await ctx.respond(
        f"{' + '.join((l := [f'{random.randint(1, sides)}' for _ in range(count)]))} = {sum([int(n) for n in l])}"
    )


@component.with_slash_command
@tanjun.as_slash_command("cf", "Flip a coin")
async def cmd_cf(ctx: tanjun.abc.SlashContext) -> None:
    await ctx.respond("Heads" if random.randint(0, 1) == 0 else "Tails")


@component.with_slash_command
@tanjun.with_int_slash_option("min", "The minimum number", default=1)
@tanjun.with_int_slash_option("max", "The maximum number", default=100)
@tanjun.as_slash_command("rand", "Get a random number")
async def cmd_rand(ctx: tanjun.abc.SlashContext, min: int, max: int) -> None:
    await ctx.respond(random.randint(min, max))
    
@component.with_slash_command
@tanjun.as_slash_command("float", "Get a decimal between 0 and 1")
async def cmd_float(ctx: tanjun.abc.SlashContext) -> None:
    await ctx.respond(random.random())


